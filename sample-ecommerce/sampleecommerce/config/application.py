# -*- coding: utf-8 -*-
"""WSGI application initialization for sample-ecommerce."""
from sampleecommerce.config.app_cfg import base_config
from depot.manager import DepotManager

__all__ = ['make_app']


def make_app(global_conf, **app_conf):
    """
    Set sample-ecommerce up with the settings found in the PasteDeploy configuration
    file used.

    :param dict global_conf: The global settings for sample-ecommerce
                             (those defined under the ``[DEFAULT]`` section).

    :return: The sample-ecommerce application with all the relevant middleware
        loaded.

    This is the PasteDeploy factory for the sample-ecommerce application.

    ``app_conf`` contains all the application-specific settings (those defined
    under ``[app:main]``.
    """
    app = base_config.make_wsgi_app(global_conf, app_conf, wrap_app=None)

    # Wrap your final TurboGears 2 application with custom middleware here

    # The following line is needed because during tests we create multiple apps and DEPOT can only have a single middleware.
    DepotManager._middleware = None
    app = DepotManager.make_middleware(app)

    return app
