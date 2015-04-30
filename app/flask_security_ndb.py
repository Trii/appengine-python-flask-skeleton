# -*- coding: utf-8 -*-
"""
.. module:: flask_security_ndb
   :synopsis: Google App Engine NDB support for Flask-Security

The :mod:`<flask_security_ndb>` module adds support for the Google App Engine datastore using NDB

"""
from flask.ext.security import datastore, UserMixin, RoleMixin
from google.appengine.ext import ndb
from google.appengine.api import mail

__all__ = ['Role', 'User', 'NDBUserDatastore']

class KeyPropertyProxy(list):
    """A Proxy object that lets you deal with Kinds stored in a repeated ndb.KeyProperty"""

    def __init__(self, owner=None, field=None):
        if not owner or not field:
            raise ValueError("owner/field cannot be null")
        self.target = getattr(owner, field, None)
        if self.target is None:
            raise AttributeError("{}.{}".format(owner, field))
        self._load()

    def __iter__(self):
        self._load()
        return super(KeyPropertyProxy, self).__iter__()

    def remove(self, model):
        """
        :param ndb.Model model: Item to remove
        """
        self._load()
        self.target.remove(model.key)
        super(KeyPropertyProxy, self).remove(model)

    def append(self, model):
        """
        :param ndb.Model model: Item to remove
        """
        self._load()
        self.target.append(model.key)
        super(KeyPropertyProxy, self).append(model)

    def insert(self, i, model):
        """
        :param int i:
        :param ndb.Model model: Item to remove
        """
        self._load()
        self.target.insert(i, model.key)
        super(KeyPropertyProxy, self).insert(i, model)

    def extend(self, models):
        """
        :param list of ndb.Model models:
        """
        self._load()
        self.target.extend([m.key for m in models])
        super(KeyPropertyProxy, self).extend(models)

    def __contains__(self, model):
        # just in case I didn't initialize in the right place?
        self._load()
        return super(KeyPropertyProxy, self).__contains__(model)

    def _load(self):
        if self.target and len(self.target) != len(self):
            list.extend(self, ndb.get_multi(self.target))

class NDBBase(ndb.Model):
    @property
    def id(self):
        """Override for getting the ID.

        Resolves NotImplementedError: No `id` attribute - override `get_id`

        :rtype: str
        """
        return self.key.id()

class Role(NDBBase, RoleMixin):
    name = ndb.StringProperty()
    description = ndb.StringProperty()


class User(NDBBase, UserMixin):
    email = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    active = ndb.BooleanProperty(default=True)
    confirmed_at = ndb.DateTimeProperty()
    last_login_at = ndb.DateTimeProperty()
    current_login_at = ndb.DateTimeProperty()
    last_login_ip = ndb.TextProperty()
    current_login_ip = ndb.TextProperty()
    login_count = ndb.IntegerProperty(indexed=False, default=0)
    roles_ = ndb.KeyProperty(Role, repeated=True)

    def __init__(self, *args, **kwds):
        self._roles_cache = []
        super(User, self).__init__(*args, **kwds)

    @property
    def roles(self):
        if len(self._roles_cache) != len(self.roles_):
            self._roles_cache = ndb.get_multi(self.roles_)
        return self._roles_cache

    @roles.setter
    def roles(self, role):
        self._roles_cache.append(role)
        self.roles_.append(role.key)


class NDBDatastore(datastore.Datastore):
    """Datastore adapter for NDB"""

    def __init__(self, *args, **kwargs):
        pass

    def put(self, model):
        """Saves a model to the datastore

        :param ndb.Model model: The model to save
        :return: The new entity
        :rtype: ndb.Model
        """
        model.put()
        return model

    def delete(self, model):
        """Deletes a model

        :param ndb.Model model: The ndb entity to delete
        """
        model.key.delete()


class NDBUserDatastore(NDBDatastore, datastore.UserDatastore):
    """An NDB datastore implementation for Flask-Security."""

    def __init__(self, user_model, role_model):
        """Initializes the User Datastore.

        :param ndb.Model user_model: A user model class definition
        :param ndb.Model role_model: A role model class definition
        """
        NDBDatastore.__init__(self)
        datastore.UserDatastore.__init__(self, user_model, role_model)

    def _prepare_create_user_args(self, **kwargs):
        """App Engine override to set email as the :class:`ndb.Key`'s id"""
        kwargs['id'] = kwargs.get('email', None)
        return super(NDBUserDatastore, self)._prepare_create_user_args(**kwargs)

    # def _prepare_role_modify_args(self, user, role):
    #     """Returns a User and ndb.Key(Role) suitable for ndb operations
    #
    #     :param User user:
    #     :param Role role:
    #     :return: The User and Role Key tuple
    #     :rtype: (User, ndb.Key)
    #     """
    #     user, role = super(NDBUserDatastore, self)._prepare_role_modify_args(user, role)
    #     return user, role.key

    def create_role(self, **kwargs):
        """App Engine override to set name as the :class:`ndb.Key`'s id"""
        kwargs['id'] = kwargs.get('name', None)
        return super(NDBUserDatastore, self).create_role(**kwargs)

    def get_user(self, id_or_email):
        """Returns a user matching the specified ID or email address.

        :param str id_or_email: User's ID (email address)
        :rtype: User or None
        """
        return self.user_model.get_by_id(id_or_email)

    def find_user(self, **kwargs):
        """Returns a user matching the provided parameters.

        :rtype: User or None
        """
        if 'id' in kwargs:
            return self.get_user(kwargs['id'])
        filters = [getattr(self.user_model, k) == v
                   for k, v in kwargs.iteritems() if hasattr(self.user_model, k)]
        return self.user_model.query(*filters).get()

    def find_role(self, role):
        """Returns a role matching the provided name.

        :param str role: Role name
        :rtype: Role or None
        """
        return self.role_model.get_by_id(role)

def send_email(message):
    """Sends a :class:`flask.ext.mail.Message` using the GAE infrastructure

    :param flask.ext.mail.Message message:
    """
    mail.send_mail(message.sender, message.send_to, message.subject,
                   body=message.body, html=message.html)
