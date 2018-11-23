##############################################################################
#
#    Soltani Charif, Open Source Contributor
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Disable Edit on done and cancel PO',
    'version': '1.0',
    'author': 'Soltani Charif',
    'website': 'https://www.linkedin.com/in/soltani-charif-b0351811a/',
    'summary': 'Hide edit button based on Purchase state',
    'description': """
This module disable Edit on Purchase Order in state ['done', 'cancel']
You can improve this module by playing around with `form_view_disable_edit.js`

You can change the condition of the hidden process for example
if you just want to hide edit in confirmed state just change this:

   `if (this.model == 'purchase.order' & _.contains(['done', 'cancel'], record.state))`

   To this:

   `if (this.model == 'purchase.order' & record.state == 'done')`

If you want to have this behavior in other modules like sale.order

    `if (_.contains(['purchase.order', 'sale.order'], this.model) & _.contains(['done', 'cancel'], record.state))`

don't forget to add dependency on your addon manifest `__openerp__.py` to make sure that
your module is installed after sale module
""",
    'depends': ['web', 'purchase'],
    'category': 'web',
    'demo': [],
    'images': [
        'static/src/img/main_screenshot.png'
    ],
    'data': ['backend_assets.xml'],
    'auto_install': False,
    'application': True,
    'installable': True,
}
