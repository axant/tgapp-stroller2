# coding=utf-8
from __future__ import unicode_literals
from formencode.validators import Number

from tw2.core import Validator, IntValidator
from tw2.forms import ListForm, TextField, SingleSelectField, TextArea, SubmitButton
from tg.i18n import ugettext as _, lazy_ugettext as l_


class NewProductForm(ListForm):

    name = TextField(label=l_('Name'), validator=Validator(required=True), css_class='form-control',
                     container_attrs={'class': 'form-group'})
    description = TextArea(label=l_('Description'), validator=Validator(required=True), css_class='form-control',
                           container_attrs={'class': 'form-group'})
    sku = TextField(label=l_('SKU'), validator=Validator(required=True), css_class='form-control',
                        container_attrs={'class': 'form-group'})
    category_id = SingleSelectField(label=l_('Category'), validator=Validator(required=True), options=[],
                                    css_class='form-control', container_attrs={'class': 'form-group'})
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

    submit = SubmitButton(value=l_('Save'), css_class='btn btn-default')

