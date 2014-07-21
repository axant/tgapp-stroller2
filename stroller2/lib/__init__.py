# coding=utf-8
from __future__ import unicode_literals

from tg import config


def get_new_product_form():
    stroller2_config = config['_pluggable_stroller2_config']

    new_product_form = stroller2_config.get('new_product_form_instance')
    if not new_product_form:
        form_path = stroller2_config.get('new_product_form', 'stroller2.lib.forms.NewProductForm')
        module, form_name = form_path.rsplit('.', 1)
        module = __import__(module, fromlist=form_name)
        form_class = getattr(module, form_name)
        new_product_form = stroller2_config['new_product_form_instance'] = form_class()

    return new_product_form


def get_edit_product_form():
    stroller2_config = config['_pluggable_stroller2_config']

    edit_product_form = stroller2_config.get('edit_product_form_instance')
    if not edit_product_form:
        form_path = stroller2_config.get('edit_product_form', 'stroller2.lib.forms.EditProductForm')
        module, form_name = form_path.rsplit('.', 1)
        module = __import__(module, fromlist=form_name)
        form_class = getattr(module, form_name)
        edit_product_form = stroller2_config['edit_product_form_instance'] = form_class()

    return edit_product_form


def get_new_category_form():
    stroller2_config = config['_pluggable_stroller2_config']

    new_category_form = stroller2_config.get('new_category_form_instance')
    if not new_category_form:
        form_path = stroller2_config.get('new_category_form', 'stroller2.lib.forms.NewCategoryForm')
        module, form_name = form_path.rsplit('.', 1)
        module = __import__(module, fromlist=form_name)
        form_class = getattr(module, form_name)
        new_category_form = stroller2_config['new_category_form_instance'] = form_class()

    return new_category_form


def get_edit_category_form():
    stroller2_config = config['_pluggable_stroller2_config']

    edit_category_form = stroller2_config.get('edit_category_form_instance')
    if not edit_category_form:
        form_path = stroller2_config.get('edit_category_form', 'stroller2.lib.forms.EditCategoryForm')
        module, form_name = form_path.rsplit('.', 1)
        module = __import__(module, fromlist=form_name)
        form_class = getattr(module, form_name)
        edit_category_form = stroller2_config['edit_category_form_instance'] = form_class()

    return edit_category_form


def get_buy_product_form():
    stroller2_config = config['_pluggable_stroller2_config']

    buy_product_form = stroller2_config.get('buy_product_form_instance')
    if not buy_product_form:
        form_path = stroller2_config.get('buy_product_form', 'stroller2.lib.forms.BuyProductForm')
        module, form_name = form_path.rsplit('.', 1)
        module = __import__(module, fromlist=form_name)
        form_class = getattr(module, form_name)
        buy_product_form = stroller2_config['buy_product_form_instance'] = form_class()

    return buy_product_form