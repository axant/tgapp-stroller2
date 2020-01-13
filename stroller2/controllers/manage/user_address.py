# coding=utf-8
from __future__ import unicode_literals
from tgext.ecommerce.lib.exceptions import AlreadyExistingSlugException, AlreadyExistingSkuException
from tgext.ecommerce.lib.validators import ProductValidator
from stroller2.controllers.utils.temporary_photos import TemporaryPhotosUploader
from tg import TGController, expose, app_globals, validate, request, redirect
from stroller2.lib import get_new_product_form, get_edit_product_form,get_new_user_address_form
import tg
from tg.flash import flash
from tgext.datahelpers.utils import fail_with
from tgext.datahelpers.validators import validated_handler

from tgext.pluggable import plug_url
from tg.i18n import lazy_ugettext as l_, ugettext as _
from tgext.pluggable import app_model

class ManageUserAddressesController(TGController):
    photos = TemporaryPhotosUploader()

    @expose('stroller2.templates.manage.user_address.index')
    def index(self, **kw):
        user_id = tg.request.identity['user']._id
        addresses = app_model.UserAddress.query.find({'user_id':user_id}).first()
        return dict(addresses=addresses if addresses else [])

    @expose('stroller2.templates.manage.user_address.new')
    def new(self, **kw):
        validation_error = request.validation['exception']
        print "NEW"
        return dict(form = get_new_user_address_form(), action=plug_url('stroller2', '/manage/user_address/create'))

    @expose()
    @validate(get_new_product_form(), error_handler=new)
    def create(self, **kw):
        kw['type'] = 'product'
        bucket = self.photos.get_bucket()
        kw['product_photos'] = bucket.photos
        del kw['photos']
        try:
            app_globals.shop.product.create(**kw)
            flash(_('Product created'))
        except AlreadyExistingSlugException:
            flash(_('There is already a product with this slug'), 'error')
        except AlreadyExistingSkuException:
            flash(_('There is already a product with this SKU'), 'error')

        return redirect(plug_url('stroller2', '/manage/product/index'))

    @expose('stroller2.templates.manage.product.edit')
    @validate({'product_id': ProductValidator()}, error_handler=fail_with(404))
    def edit(self, product_id, **kw):
        validation_error = request.validation['exception']
        if validation_error is not None:
            fields = validation_error.widget.child.children
            fields.photos.value = {'photos': self.photos.current_photos()}
            value = {}
        else:
            self.photos.new_bucket()
            product = product_id
            value = dict(product_id=product._id, name=product.name[tg.config.lang],
                         description=product.description[tg.config.lang],
                         sku=product.configurations[0].sku,
                         price=product.configurations[0].price,
                         rate=product.configurations[0].rate,
                         vat=product.configurations[0].vat,
                         qty=product.configurations[0].qty,
                         weight=product.details.weight,
                         categories_ids=[str(category_id) for category_id in product.categories_ids],
                         photos={'photos': self.photos.recover_photos(product.details.product_photos)})
        return dict(form=get_edit_product_form(), value=value, action=plug_url('stroller2', '/manage/product/save'))


    @expose()
    @validate(get_edit_product_form(), error_handler=validated_handler(edit))
    def save(self, **kw):
        product = app_globals.shop.product.get(_id=kw.pop('product_id'))
        bucket = self.photos.get_bucket()
        kw['product_photos'] = bucket.photos
        product_info = dict(name=kw.pop('name'), description=kw.pop('description'), weight=kw.pop('weight'),
                            categories_ids=kw.pop('categories_ids'),
                            product_photos=kw.pop('product_photos'))
        del kw['photos']
        app_globals.shop.product.edit(product, **product_info)
        app_globals.shop.product.edit_configuration(product, 0, **kw)
        flash(_('Product edited'))
        return redirect(plug_url('stroller2', '/manage/product/index'))


    @expose()
    @validate({'product_id': ProductValidator()}, error_handler=fail_with(404))
    def delete(self, product_id):
        product = product_id
        app_globals.shop.product.delete(product)
        flash(_('Product deleted'))
        return redirect(plug_url('stroller2', '/manage/product/index'))

    @expose()
    @validate({'product_id': ProductValidator()})
    def publish(self, product_id):
        toggle = not product_id.published
        app_globals.shop.product.publish(product_id, toggle)
        return redirect(plug_url('stroller2', '/manage/product/index'))