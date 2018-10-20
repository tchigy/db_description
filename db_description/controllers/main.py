# -*- coding: utf-8 -*-
from odoo.addons import web
from odoo import http
import jinja2
import logging
import odoo
import os
import re
from odoo.http import request
import sys

_logger = logging.getLogger(__name__)

# change default file loader
if hasattr(sys, 'frozen'):
    # When running on compiled windows binary, we don't have access to package loader.
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'views'))
    description_loader = jinja2.FileSystemLoader(path)
else:
    description_loader = jinja2.PackageLoader('odoo.addons.db_description', "views")

local_env = jinja2.Environment(loader=description_loader, autoescape=True)

# using class inheritance didn't work for me TODO: find a way to use inheritance
# use monkey patching

# we need to load our manage not the one in web.
def _render_template(self, **d):
    d.setdefault('manage',True)
    d['insecure'] = odoo.tools.config['admin_passwd'] == 'admin'
    d['list_db'] = odoo.tools.config['list_db']
    d['langs'] = odoo.service.db.exp_list_lang()
    d['countries'] = odoo.service.db.exp_list_countries()
    d['pattern'] = web.controllers.main.DBNAME_PATTERN  # keep the same pattern of odoo
    # databases list
    d['databases'] = []
    try:
        d['databases'] = http.db_list()
    except odoo.exceptions.AccessDenied:
        monodb = http.db_monodb()
        if monodb:
            d['databases'] = [monodb]
    return local_env.get_template("database_manager.html").render(d)


# change Odoo method with ours
web.controllers.main.Database._render_template = _render_template


# we need to handle db_filter to deal with two types of database list
# list of db names and list of dictionaries.
def db_filter(dbs_list, httprequest=None):
    httprequest = httprequest or request.httprequest
    h = httprequest.environ.get('HTTP_HOST', '').split(':')[0]
    d, _, r = h.partition('.')
    if d == "www" and r:
        d = r.partition('.')[0]
    is_dict = False
    # handle list of dictionaries
    if dbs_list and isinstance(dbs_list[0], dict):
        dbs_names = [db_info['db'] for db_info in dbs_list]
        is_dict = True
    else:
        dbs_names = dbs_list
    if odoo.tools.config['dbfilter']:
        r = odoo.tools.config['dbfilter'].replace('%h', h).replace('%d', d)
        dbs_names = [i for i in dbs_names if re.match(r, i)]
    elif odoo.tools.config['db_name']:
        # In case --db-filter is not provided and --database is passed, Odoo will
        # use the value of --database as a comma seperated list of exposed databases.
        exposed_dbs = set(db.strip() for db in odoo.tools.config['db_name'].split(','))
        dbs_names = sorted(exposed_dbs.intersection(dbs_names))
    if is_dict:
        # Loop only one time
        dbs_list = {db_info['db']: db_info for db_info in dbs_list}
        # convert list of dict
        dbs_names = [dbs_list[db_name] for db_name in dbs_names]

    return dbs_names


# change Odoo method with ours
odoo.http.db_filter = db_filter


# add db_name parameter to request to render it in login page
original_ensure_db = web.controllers.main.ensure_db
from odoo.addons.db_description.service import db as local_db


def ensure_db(*args, **kwargs):
    """ add db_name param to request"""
    res = original_ensure_db(*args, **kwargs)
    db_name = request.params.get('db_name', False)
    if db_name:
        # set the db_name on the request and the session.
        if not hasattr(request, 'db_name') or request.db_name != db_name:
            request.db_name = db_name
            request.session.db_name = db_name
    # get the db_name from the session if there is noe
    elif hasattr(request, 'session'):
        if getattr(request.session, 'db_name'):
            request.db_name = request.session.db_name
        else:
            # the session don't have db_name attribute try to use db attribute
            # to find the description of the database.
            db = request.session.db
            if db:
                dbs = local_db.get_dbs()
                request.db_name = dbs.get(db, db)
            else:
                request.db_name = db
    else:
        request.db_name = False
    return res


web.controllers.main.ensure_db = ensure_db


# add description parameter to database_list
from odoo.addons.db_description.service import db
original_create = web.controllers.main.Database.create
@http.route('/web/database/create', type='http', auth="none", methods=['POST'], csrf=False)
def create(self, master_pwd, description, name, lang, password, **post):
    """ handle decritpion of the applications"""
    db.add_app(description, name)
    res = original_create(self, master_pwd, name, lang, password, **post)
    return res

web.controllers.main.Database.create = create



def db_monodb(httprequest=None):
    """
        Magic function to find the current database.

        Implementation details:

        * Magic
        * More magic

        Returns ``None`` if the magic is not magic enough.
    """
    httprequest = httprequest or odoo.http.request.httprequest

    dbs = odoo.http.db_list(True, httprequest)

    # try the db already in the session
    db_session = httprequest.session.db
    # db_list now returns a dictionary
    if db_session in [dbi['db'] for dbi in dbs]:
        return db_session

    # if there is only one possible db, we take that one
    if len(dbs) == 1:
        return dbs[0] if isinstance(dbs[0], (str, unicode)) else dbs[0]['db']
    return None

http.db_monodb = db_monodb
# web was imported first we change the reference of this variable ^_^
web.controllers.main.db_monodb = db_monodb