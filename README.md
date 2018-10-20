## 2. version
Module works fine in 10.0 version but you can change it to work in other version most of the code are the same.

## 1. Installation
Adding the module to your addons-path it's not enough in order to give an application name to your first database. you need to add this configuration in your config file.

    `server_wide_modules = web,web_kanban,db_description`

This way you tell odoo to load the module when there is no database in the system.