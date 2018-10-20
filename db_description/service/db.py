# -*- coding: utf-8 -*-
import odoo
from odoo import service, http
import os
import io

db_list_file_name = 'db_list'

# *******************************************************************************************************************************************
def ensure_db_list_file():
    """ create the file if it's not there"""
    addons_path = http.addons_manifest['db_description']['addons_path']
    file_path = os.path.join(addons_path, 'db_description', db_list_file_name)
    if os.path.exists(file_path) and not os.path.isfile(file_path):
        import shutil
        shutil.rmtree(file_path)
    # make sure to create it if it's missing.
    io.open(file_path, 'a').close()


def get_dbs():
    """ return list of database with descriptions"""
    ensure_db_list_file()
    dbs = {}
    if not 'db_description' in http.addons_manifest.iterkeys(): return dbs
    addons_path = http.addons_manifest['db_description']['addons_path']
    with io.open(os.path.join(addons_path, 'db_description', db_list_file_name), 'r', encoding='utf-8') as f:
        for l in f:
            if l and ':' in l:
                db_info = l.split(':')
                dbs[db_info[0]] = db_info[1]
    return dbs


def exist_description(db_name, description):
    ensure_db_list_file()
    addons_path = http.addons_manifest['db_description']['addons_path']
    with io.open(os.path.join(addons_path, 'db_description', db_list_file_name), 'r', encoding='utf-8') as f:
        for line in f:
            db_info = line.split(':')
            if len(db_info) >= 2 and db_info[1].strip().lower() == description.strip().lower() and db_info[0] != db_name:
                raise Exception(u'You cannot use the same description for more than one database.')


def add_app(description, db_name):
    """ add database description to db_list file."""
    ensure_db_list_file()
    exist_description(db_name, description)

    remove_app(db_name)
    addons_path = http.addons_manifest['db_description']['addons_path']
    with io.open(os.path.join(addons_path, 'db_description', db_list_file_name), 'a', encoding='utf-8') as f:
        f.write('%s:%s\n' % (db_name.strip(), description.strip()))


def remove_app(db_name):
    ensure_db_list_file()
    addons_path = http.addons_manifest['db_description']['addons_path']
    with io.open(os.path.join(addons_path, 'db_description', db_list_file_name), 'r', encoding='utf-8') as f:
        lines = f.readlines()
    with io.open(os.path.join(addons_path, 'db_description', db_list_file_name), 'w', encoding='utf-8') as f:
        for line in lines:
            if db_name != line.split(':')[0].strip() and ':' in line:
                f.write(line)


# *******************************************************************************************************************************************
# override the list_dbs
original_db_list = service.db.list_dbs

def list_dbs(*args, **kwargs):
    """ convert original Odoo list to list of dict."""
    res = original_db_list(*args, **kwargs)
    res_dict = []
    dbs = get_dbs()
    for d in res:
        db_dict = {'name': dbs.get(d) or d, 'db': d}
        res_dict.append(db_dict)
    return res_dict


# change Odoo function
service.db.list_dbs = list_dbs



# *******************************************************************************************************************************************
# add rename function
def exp_rename_app(name, old_description, new_description):
    """ rename application or add it."""
    exist_description(name, new_description)
    addons_path = http.addons_manifest['db_description']['addons_path']
    file_path = os.path.join(addons_path, 'db_description', db_list_file_name)

    # read all descriptions
    with io.open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    descp_exist = False
    with io.open(file_path, 'w', encoding='utf-8') as f:
        for line in lines:
            db_info = line.split(':')
            if len(db_info) != 2: continue  # remove errors
            db_name, app_name = db_info[0], db_info[1]
            if old_description == app_name.strip() and db_name.strip() == name.strip():
                f.write('%s:%s\n' % (db_name, new_description))
                descp_exist = True
            else:
                f.write('%s:%s' % (db_name, app_name))

    if not descp_exist:
        # add the app
        add_app(new_description, name)

service.db.exp_rename_app = exp_rename_app


# *******************************************************************************************************************************************
# handle drop method i could not avoid rewriting the code because
# Odoo method checks the database inside the code
def exp_drop(db_name):
    """ drop database and remove it's description."""
    if db_name not in (inf['db'] for inf in list_dbs(True)):
        return False
    odoo.modules.registry.RegistryManager.delete(db_name)
    odoo.sql_db.close_db(db_name)

    db = odoo.sql_db.db_connect('postgres')
    with service.db.closing(db.cursor()) as cr:
        cr.autocommit(True) # avoid transaction block
        service.db._drop_conn(cr, db_name)
        try:
            cr.execute('DROP DATABASE "%s"' % db_name)
        except Exception, e:
            service.db._logger.info('DROP DB: %s failed:\n%s', db_name, e)
            raise Exception("Couldn't drop database %s: %s" % (db_name, e))
        else:
            service.db._logger.info('DROP DB: %s', db_name)
            remove_app(db_name)


service.db.exp_drop = exp_drop