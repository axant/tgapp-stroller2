# coding=utf-8
from __future__ import unicode_literals

from tg import TGController
from tg import expose, flash, require, url, lurl, request, redirect, validate
from tg.i18n import ugettext as _, lazy_ugettext as l_

from tw2.core import Validator
from tw2.forms import ListForm, TextField, SingleSelectField, TextArea


class NewProductForm(ListForm):
    css_class = 'form-group'

    sku = TextField(validator=Validator(required=True), css_class='form_control')
    name = TextField(validator=Validator(required=True), css_class='form_control')
    category_id = SingleSelectField(validator=Validator(required=True), css_class='form_control')
    description = TextArea(validator=Validator(required=True), css_class='form_control')
    price = TextField(validator=Validator(required=True), css_class='form_control')
    vat = TextField(validator=Validator(required=True), css_class='form_control')
    qty = TextField(validator=Validator(required=True), css_class='form_control')


class RootController(TGController):
    @expose('stroller2.templates.index')
    def index(self):
        print ' lol'
        return dict()

    @expose()
    def new_product(self):
        return dict(form=NewProductForm)