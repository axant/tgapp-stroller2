# -*- coding: utf-8 -*-
"""The tgapp-stroller2 package"""
import tg
import os
from tg import hooks

depot_photos_path = os.path.join(
    os.getcwd(),
    'public', 'depot'
)

product_photos_path = os.path.join(
    depot_photos_path,
    'product_images'
)


def plugme(app_config, options):
    try:
        # TG 2.3
        app_config['_pluggable_stroller2_config'] = options
        run_enable_depot = False
        if 'depot_backend_type' not in app_config.keys():
            app_config['depot_backend_type'] = 'depot.io.local.LocalFileStorage'
        if 'depot_storage_path' not in app_config.keys():
            app_config['depot_storage_path'] = depot_photos_path
        if 'depot.product_images.backend' not in app_config.keys():
            app_config['depot.product_images.backend'] = app_config['depot_backend_type']
            run_enable_depot = True
        if 'depot.product_images.backend' not in app_config.keys():
            app_config['depot.product_images.storage_path'] = product_photos_path
            run_enable_depot = True
        if run_enable_depot:
            hooks.register('after_config', enable_depot)
    except TypeError:
        # TG 2.4
        app_config.update_blueprint({
            '_pluggable_stroller2_config': options
        })
        run_enable_depot = False
        try:
            app_config.get_blueprint_value('depot_backend_type')
        except KeyError:
            app_config.update_blueprint({
                'depot_backend_type': 'depot.io.local.LocalFileStorage'
            })
        try:
            app_config.get_blueprint_value('depot_storage_path')
        except KeyError:
            app_config.update_blueprint({
                'depot_storage_path': depot_photos_path
            })
        try:
            app_config.get_blueprint_value('depot.product_images.backend')
        except KeyError:
            app_config.update_blueprint({
                'depot.product_images.backend': 'depot.io.local.LocalFileStorage'
            })
            run_enable_depot = True
        try:
            app_config.get_blueprint_value('depot.product_images.storage_path')
        except KeyError:
            app_config.update_blueprint({
                'depot.product_images.storage_path': product_photos_path
            })
            run_enable_depot = True
        if run_enable_depot:
            hooks.register('after_wsgi_middlewares', enable_depot)
    return dict(appid='commerce', global_helpers=True)


def enable_depot(app):
    import logging
    log = logging.getLogger('stroller2.depot')

    # DEPOT setup
    from depot.manager import DepotManager

    storages = {
        'product_images': 'product_image'
    }

    for storage in storages:
        prefix = 'depot.%s.' % storage
        log.info('Configuring Storage %s*', prefix)
        DepotManager.configure(storage, tg.config, prefix)
        DepotManager.alias(storages[storage], storage)
        DepotManager.make_middleware(app=app)
    return app
