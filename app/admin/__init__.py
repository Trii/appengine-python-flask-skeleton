# -*- coding: utf-8 -*-
"""
.. module:: admin
    :synopsis: Setup of Flask-Admin plugin

Use https://console.developers.google.com/project/<project_id>/permissions to add
new application administrators

"""
from flask_admin import Admin, base

# Initialize Flask-Admin
admin_app = Admin(template_mode='bootstrap3')
admin_app.name = "Josh's awesome app"


def add_default_views(admin_app_):
    from admin.views import UserAdmin, RoleAdmin
    from flask_security_ndb import User, Role
    # Add Flask-Admin views for Users and Roles
    admin_app_.add_view(UserAdmin(User, category='Entities'))
    admin_app_.add_view(RoleAdmin(Role, category='Entities'))
    admin_app_.add_link(base.MenuLink(name='Site Home', url='/'))
