# coding=utf-8
from __future__ import unicode_literals
from .widget import AjaxManagePhotos
from formencode.validators import Number
from stroller2.lib.utils import json_lurl
import tg

from tw2.core import Validator, IntValidator, Deferred
from tw2.forms import Form, TextField, TextArea, SubmitButton, HiddenField, ListForm,\
    MultipleSelectField, FileField, SingleSelectField, ListLayout
from tg import app_globals
from tg.i18n import lazy_ugettext as l_


class CustomListLayout(ListLayout):
    inline_engine_name = 'kajiki'
    template = '''
<div>
    <py:for each="c in w.children_hidden">
        ${c.display()}
    </py:for>
    <div py:for="i,c in enumerate(w.children_non_hidden)" class="${(i % 2 and 'even' or 'odd') + ((c.validator and getattr(c.validator, 'required', getattr(c.validator, 'not_empty', False))) and ' required' or '') + (c.error_msg and ' error' or '')}" title="${w.hover_help and c.help_text or None}" py:attrs="c.container_attrs">
        <label for="${c.id}" py:attrs="getattr(c, 'label_attrs', {})">$c.label</label>
        <div py:attrs="getattr(c, 'wrapper_attrs', {})">${c.display()}</div>
        <py:if test="not w.hover_help">$c.help_text</py:if>
        <span id="${c.compound_id}:error" class="error" py:content="c.error_msg"/>
    </div>
    <div class="error"><span id="${w.compound_id}:error" class="error" ><py:for each="error in w.rollup_errors"><p>${error}</p></py:for></span></div>
</div>
'''


class NewProductForm(ListForm):

    name = TextField(label=l_('Name'), validator=Validator(required=True), css_class='form-control',
                     container_attrs={'class': 'form-group'})
    description = TextArea(label=l_('Description'), validator=Validator(required=True), css_class='form-control',
                           container_attrs={'class': 'form-group'})
    sku = TextField(label=l_('SKU'), validator=Validator(required=True), css_class='form-control',
                    container_attrs={'class': 'form-group'})
    categories_ids = MultipleSelectField(label=l_('Categories'), validator=Validator(required=True),
                                         css_class="form-control", container_attrs={'class': 'form-group'},
                                         options=Deferred(lambda: [(c._id, c.name_with_ancestors)
                                                                   for c in app_globals.shop.category.get_all()]))
    price = TextField(label=l_('Price'), validator=Number(min=0.0, not_empty=True), css_class='form-control',
                      container_attrs={'class': 'form-group'})
    rate = TextField(label=l_('Rate'), validator=IntValidator(min=0, required=True), css_class='form-control',
                     container_attrs={'class': 'form-group'})
    vat = TextField(label=l_('Vat'), validator=Number(min=0.0, not_empty=True), css_class='form-control',
                    container_attrs={'class': 'form-group'})
    qty = TextField(label=l_('Quantity'), validator=IntValidator(min=0, required=True), css_class='form-control',
                    container_attrs={'class': 'form-group'})
    weight = TextField(label=l_('Weight (g)'), validator=Number(min=0.0, not_empty=True),
                       css_class='form-control')
    photos = AjaxManagePhotos(label=l_('Photos'),
                              css_class="ajax_manage_photos",
                              action=json_lurl('/commerce/manage/product/photos/save'),
                              delete_action=json_lurl('/commerce/manage/product/photos/remove'))

    submit = SubmitButton(value=l_('Create'), css_class='btn btn-default')


class NewUserAddressForm(ListForm):
    receiver = TextField(label=l_('Receiver'), validator=Validator(required=True), css_class='form-control',
                    container_attrs={'class': 'form-group'})
    address = TextArea(label=l_('Address'), validator=Validator(required=True), css_class='form-control',
                    container_attrs={'class': 'form-group'})
    city = TextField(label=l_('City'), validator=Validator(required=True), css_class='form-control',
                    container_attrs={'class': 'form-group'})
    province = TextField(label=l_('Province'), validator=Validator(required=True), css_class='form-control',
                    container_attrs={'class': 'form-group'})
    state = TextField(label=l_('State'), validator=Validator(required=True), css_class='form-control',
                    container_attrs={'class': 'form-group'})
    zip = TextField(label=l_('Zip Code'), validator=Validator(required=True), css_class='form-control',
                    container_attrs={'class': 'form-group'})
    country = TextField(label=l_('Country'), validator=Validator(required=True), css_class='form-control',
                    container_attrs={'class': 'form-group'})
    details = TextField(label=l_('Details'), validator=Validator(required=True), css_class='form-control',
                    container_attrs={'class': 'form-group'})
    image = FileField(label=l_('Image'),
                            css_class='form-control', container_attrs={'class': 'form-group', 'accept': 'image/*'})
    submit = SubmitButton(value=l_('Create'), css_class='btn btn-default')


class EditUserAddressForm(ListForm):
    address_id = HiddenField()
    receiver = TextField(label=l_('Receiver'), validator=Validator(required=True), css_class='form-control',
                         container_attrs={'class': 'form-group'})
    address = TextArea(label=l_('Address'), validator=Validator(required=True), css_class='form-control',
                       container_attrs={'class': 'form-group'})
    city = TextField(label=l_('City'), validator=Validator(required=True), css_class='form-control',
                     container_attrs={'class': 'form-group'})
    province = TextField(label=l_('Province'), validator=Validator(required=True), css_class='form-control',
                         container_attrs={'class': 'form-group'})
    state = TextField(label=l_('State'), validator=Validator(required=True), css_class='form-control',
                      container_attrs={'class': 'form-group'})
    zip = TextField(label=l_('Zip Code'), validator=Validator(required=True), css_class='form-control',
                        container_attrs={'class': 'form-group'})
    country = TextField(label=l_('Country'), validator=Validator(required=True), css_class='form-control',
                        container_attrs={'class': 'form-group'})
    details = TextField(label=l_('Details'), validator=Validator(required=True), css_class='form-control',
                        container_attrs={'class': 'form-group'})

    submit = SubmitButton(value=l_('Save'), css_class='btn btn-default')


class EditProductForm(ListForm):
    product_id = HiddenField()
    name = TextField(label=l_('Name'), validator=Validator(required=True), css_class='form-control',
                     container_attrs={'class': 'form-group'})
    description = TextArea(label=l_('Description'), validator=Validator(required=True), css_class='form-control',
                           container_attrs={'class': 'form-group'})
    sku = TextField(label=l_('SKU'), validator=Validator(required=True), css_class='form-control',
                    container_attrs={'class': 'form-group'})
    categories_ids = MultipleSelectField(label=l_('Categories'), validator=Validator(required=True),
                                         css_class="form-control", container_attrs={'class': 'form-group'},
                                         options=Deferred(lambda: [(c._id, c.name_with_ancestors)
                                                                   for c in app_globals.shop.category.get_all()]))
    price = TextField(label=l_('Price'), validator=Number(min=0.0, not_empty=True), css_class='form-control',
                      container_attrs={'class': 'form-group'})
    rate = TextField(label=l_('Rate'), validator=IntValidator(min=0, required=True), css_class='form-control',
                     container_attrs={'class': 'form-group'})
    vat = TextField(label=l_('Vat'), validator=Number(min=0.0, not_empty=True), css_class='form-control',
                    container_attrs={'class': 'form-group'})
    qty = TextField(label=l_('Quantity'), validator=IntValidator(min=0, required=True), css_class='form-control',
                    container_attrs={'class': 'form-group'})
    weight = TextField(label=l_('Weight (g)'), validator=Number(min=0.0, not_empty=True),
                       css_class='form-control')
    photos = AjaxManagePhotos(label=l_('Photos'),
                              css_class="ajax_manage_photos",
                              action=json_lurl('/commerce/manage/product/photos/save'),
                              delete_action=json_lurl('/commerce/manage/product/photos/remove'))

    submit = SubmitButton(value=l_('Save'), css_class='btn btn-default')


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
    parent_id = SingleSelectField(
        label=l_('Parent'),
        css_class="form-control", container_attrs={'class': 'form-group'},
        options=Deferred(lambda: [
            (c._id, c.name[tg.config.lang]) for c in app_globals.shop.category.get_all()
        ])
    )
    submit = SubmitButton(value=l_('Save'), css_class='btn btn-default')


class BuyProductForm(Form):
    child = CustomListLayout
    css_class = "form-horizontal"

    product = HiddenField(validator=Validator(required=True))

    quantity = SingleSelectField(label=l_("Quantity"), options=[],
                                 validator=IntValidator(min=1, required=True),
                                 container_attrs={'class': 'form-group'},
                                 label_attrs={'class': 'col-sm-12'},
                                 wrapper_attrs={'class': 'col-sm-4'},
                                 css_class="form-control -quantity")
    submit = None

    submit1 = SubmitButton(value=l_('Add to cart'), key='add_to_cart', name='action',
                          css_class='btn btn-block btn-success stroller2-buy-product-submit-button')
    submit2 = SubmitButton(value=l_('Buy now'), key='buy_now', name='action',
                           css_class='btn btn-block btn-success stroller2-buy-product-submit-button')

    def prepare(self):
        super(BuyProductForm, self).prepare()

        product_field = self.child.children.product
        quantity_field = self.child.children.quantity
        product = app_globals.shop.product.get(_id=product_field.value)
        opts = [({'value': c}, c) for c in range(1, product.configurations[0].qty + 1)]
        quantity_field.grouped_options = [(None, opts)]
