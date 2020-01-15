# coding=utf-8
from __future__ import unicode_literals

from tg import config

forms_types = {
    'new_product': {'name': 'new_product_form', 'klass': 'stroller2.lib.forms.NewProductForm', 'instance': 'new_product_form_instance'},
    'edit_product': {'name': 'edit_product_form', 'klass': 'stroller2.lib.forms.EditProductForm', 'instance': 'edit_product_form_instance'},
    'buy_product': {'name': 'buy_product_form', 'klass': 'stroller2.lib.forms.BuyProductForm', 'instance': 'buy_product_form_instance'},
    'new_category': {'name': 'new_category_form', 'klass': 'stroller2.lib.forms.NewCategoryForm', 'instance': 'new_category_form_instance'},
    'edit_category': {'name': 'edit_category_form', 'klass': 'stroller2.lib.forms.EditCategoryForm', 'instance': 'edit_category_form_instance'},
    'new_user_address': {'name': 'new_user_address_form', 'klass': 'stroller2.lib.forms.NewUserAddressForm', 'instance': 'new_user_address_form_instance'}
}


def get_form(form_name):
    stroller2_config = config['_pluggable_stroller2_config']
    new_form = stroller2_config.get(forms_types[form_name]['instance'])
    if not new_form:
        form_path = stroller2_config.get(
            forms_types[form_name]['name'],
            forms_types[form_name]['klass']
        )
        module, form_name = form_path.rsplit('.', 1)
        module = __import__(module, fromlist=form_name)
        form_class = getattr(module, form_name)
        new_form = form_class()
    return new_form


def get_new_product_form():
    return get_form('new_product')


def get_new_user_address_form():
    return get_form('new_user_address')


def get_edit_product_form():
    return get_form('edit_product')


def get_new_category_form():
    return get_form('new_category')


def get_edit_category_form():
    return get_form('edit_category')


def get_buy_product_form():
    return get_form('buy_product')
