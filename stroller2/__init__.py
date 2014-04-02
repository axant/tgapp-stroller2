# -*- coding: utf-8 -*-
"""The tgapp-stroller2 package"""
import tg


def plugme(app_config, options):
    tg.config['_pluggable_stroller2_config'] = options

    return dict(appid='commerce', global_helpers=False)