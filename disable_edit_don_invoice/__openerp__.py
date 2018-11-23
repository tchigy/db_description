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
    'name': 'Disable Edit on paid invoices',
    'version': '1.0',
    'author': 'Soltani Charif',
    'website': 'https://www.linkedin.com/in/soltani-charif-b0351811a/',
    'summary': 'Hide edit button based on Purchase state',
    'description': """
This module disable Edit on Invoices in state ['paid', 'cancel']
You can improve this module by playing around with `form_view_disable_edit.js`

You can change the condition of the hidden process for example
if you just want to hide edit in confirmed state just change this:

   `if (this.model == 'account.invoice' & _.contains(['paid', 'cancel'], record.state))`

   To this:

   `if (this.model == 'account.invoice' & record.state == 'paid')`
""",
    'depends': ['web', 'account'],
    'category': 'web',
    'images': [
        'static/src/img/main_screenshot.png'
    ],
    'demo': [],
    'data': ['backend_assets.xml'],
    'auto_install': False,
    'application': True,
    'installable': True,
}
