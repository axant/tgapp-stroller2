# coding=utf-8
from __future__ import unicode_literals
from formencode.validators import Number
import tg

from tw2.core import Validator, IntValidator, Deferred
from tw2.forms import Form, TextField, TextArea, SubmitButton, HiddenField, ListForm, MultipleSelectField, TableForm, \
    SingleSelectField
from tg import app_globals
from tg.i18n import ugettext as _, lazy_ugettext as l_


class NewProductForm(ListForm):
    name = TextField(label=l_('Name'), validator=Validator(required=True), css_class='form-control',
                     container_attrs={'class': 'form-group'})
    description = TextArea(label=l_('Description'), validator=Validator(required=True), css_class='form-control',
                           container_attrs={'class': 'form-group'})
    sku = TextField(label=l_('SKU'), validator=Validator(required=True), css_class='form-control',
                    container_attrs={'class': 'form-group'})
    categories_ids = MultipleSelectField(label=l_('Categories'), validator=Validator(required=True),
                                         css_class="form-control", container_attrs={'class': 'form-group'},
                                         options=Deferred(lambda: [(c._id, c.name[tg.config.lang])
                                                                   for c in app_globals.shop.category.get_all()]))
    price = TextField(label=l_('Price'), validator=Number(min=0.0, not_empty=True), css_class='form-control',
                      container_attrs={'class': 'form-group'})
    rate = TextField(label=l_('Rate'), validator=IntValidator(min=0, required=True), css_class='form-control',
                     container_attrs={'class': 'form-group'})
    vat = TextField(label=l_('Vat'), validator=Number(min=0.0, not_empty=True), css_class='form-control',
                    container_attrs={'class': 'form-group'})
    qty = TextField(label=l_('Qty'), validator=IntValidator(min=0, required=True), css_class='form-control',
                    container_attrs={'class': 'form-group'})
    weight = TextField(label=l_('Weight (g)'), validator=Number(min=0.0, not_empty=True),
                       css_class='form-control')

    submit = SubmitButton(value=l_('Create'), css_class='btn btn-default')


class NewCategoryForm(ListForm):
    name = TextField(label=l_('Name'), validator=Validator(required=True), css_class='form-control',
                     container_attrs={'class': 'form-group'})
    parent_id = SingleSelectField(label=l_('Parent'),
                                  css_class="form-control", container_attrs={'class': 'form-group'},
                                  options=Deferred(lambda: [(c._id, c.name[tg.config.lang])
                                                            for c in app_globals.shop.category.get_all()]))
    submit = SubmitButton(value=l_('Create'), css_class='btn btn-default')


class EditCategoryForm(ListForm):
    category_id = HiddenField()
    name = TextField(label=l_('Name'), validator=Validator(required=True), css_class='form-control',
                     container_attrs={'class': 'form-group'})
    parent_id = SingleSelectField(label=l_('Parent'),
                                  css_class="form-control", container_attrs={'class': 'form-group'},
                                  options=Deferred(lambda: [(c._id, c.name[tg.config.lang])
                                                            for c in app_globals.shop.category.get_all()]))
    submit = SubmitButton(value=l_('Save'), css_class='btn btn-default')