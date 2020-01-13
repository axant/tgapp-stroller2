# -*- coding: utf-8 -*-
"""The tgapp-stroller2 package"""
import tg


def plugme(app_config, options):
    try:
        # TG 2.3
        app_config['_pluggable_stroller2_config'] = options
    except TypeError:
        # TG 2.4
        app_config.update_blueprint({
            '_pluggable_stroller2_config': options
        })

    return dict(appid='commerce', global_helpers=True)
