# -*- coding: utf-8 -*-
"""
Global configuration file for TG2-specific settings in sample-ecommerce.

This file complements development/deployment.ini.

"""
from tg import FullStackApplicationConfigurator
import sampleecommerce
from sampleecommerce import model

base_config = FullStackApplicationConfigurator()

# General configuration
base_config.update_blueprint({
    # True to prevent dispatcher from striping extensions
    # For example /socket.io would be served by "socket_io"
    # method instead of "socket".
    'disable_request_extensions': False,

    # Set None to disable escaping punctuation characters to "_"
    # when dispatching methods.
    # Set to a function to provide custom escaping.
    'dispatch_path_translator': True,

    'package': sampleecommerce
})

# ToscaWidgets configuration
base_config.update_blueprint({
    'tw2.enabled': True,
})

# Rendering Engines Configuration
rendering_config = {
    'renderers': ['json'],  # Enable json in expose
    'default_renderer': 'kajiki',
}
rendering_config['renderers'].append('kajiki')
# Change this in setup.py too for i18n to work.
rendering_config['templating.kajiki.strip_text'] = False
base_config.update_blueprint(rendering_config)

# Configure Sessions, store data as JSON to avoid pickle security issues
base_config.update_blueprint({
    'session.enabled': True,
    'session.data_serializer': 'json',
})

# Configure the base Ming Setup
base_config.update_blueprint({
    'use_sqlalchemy': False,
    'tm.enabled': False,

    'use_ming': True,
    'model': sampleecommerce.model,
    'DBSession': sampleecommerce.model.DBSession,
})
# This tells to TurboGears how to retrieve the data for your user
from tg.configuration.auth import TGAuthMetadata


class ApplicationAuthMetadata(TGAuthMetadata):
    def __init__(self, dbsession, user_class):
        self.user_class = user_class

    def authenticate(self, environ, identity):
        login = identity['login']
        user = self.user_class.query.get(user_name=login)

        if not user:
            login = None
        elif not user.validate_password(identity['password']):
            login = None

        if login is None:
            try:
                from urllib.parse import parse_qs, urlencode
            except ImportError:
                from urlparse import parse_qs
                from urllib import urlencode
            from tg.exceptions import HTTPFound

            params = parse_qs(environ['QUERY_STRING'])
            params.pop('password', None)  # Remove password in case it was there
            if user is None:
                params['failure'] = 'user-not-found'
            else:
                params['login'] = identity['login']
                params['failure'] = 'invalid-password'

            # When authentication fails send user to login page.
            environ['repoze.who.application'] = HTTPFound(
                location=environ['SCRIPT_NAME'] + '?'.join(('/login', urlencode(params, True)))
            )

        return login

    def get_user(self, identity, userid):
        return self.user_class.query.get(user_name=userid)

    def get_groups(self, identity, userid):
        return [g.group_name for g in identity['user'].groups]

    def get_permissions(self, identity, userid):
        return [p.permission_name for p in identity['user'].permissions]

# Configure the authentication backend
base_config.update_blueprint({
    'auth_backend': 'ming',

    # YOU MUST CHANGE THIS VALUE IN PRODUCTION TO SECURE YOUR APP
    'sa_auth.cookie_secret': "b0ff7718-b191-4daf-ac7f-d348b0771ffb",
    'sa_auth.authmetadata': ApplicationAuthMetadata(model.DBSession, model.User),

    # You may optionally define a page where you want users
    # to be redirected to on login:
    'sa_auth.post_login_url': '/post_login',

    # You may optionally define a page where you want users
    # to be redirected to on logout:
    'sa_auth.post_logout_url': '/post_logout',
    
    # In case ApplicationAuthMetadata didn't find the user discard the whole identity.
    # This might happen if logged-in users are deleted.
    'identity.allow_missing_user': False,

    # override this if you would like to provide a different who plugin for
    # managing login and logout of your application
    'sa_auth.form_plugin': None,
    
    # You can use a different repoze.who Authenticator if you want to
    # change the way users can login
    # 'sa_auth.authenticators': [('myauth', SomeAuthenticator()],
    
    # You can add more repoze.who metadata providers to fetch
    # user metadata.
    # Remember to set 'sa_auth.authmetadata' to None
    # to disable authmetadata and use only your own metadata providers
    # 'sa_auth.mdproviders': [('myprovider', SomeMDProvider()],
})
try:
    # Enable DebugBar if available, install tgext.debugbar to turn it on
    from tgext.debugbar import enable_debugbar
    enable_debugbar(base_config)
except ImportError:
    pass

from tgext.pluggable import plug
plug(
    base_config,
    'tgext.ecommerce',
    edit_order_form='sampleecommerce.config.ecommerce_hooks.EditOrderForm',
    global_models=True
)
plug(
    base_config,
    'stroller2',
    global_models=True
)
