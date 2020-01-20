# coding=utf-8
from __future__ import unicode_literals
from tg import TGController, expose, validate, request, redirect
from stroller2.lib import get_edit_user_address_form, get_new_user_address_form
import tg
from tg.flash import flash
from tgext.datahelpers.utils import fail_with
from tgext.datahelpers.validators import validated_handler
from tgext.pluggable import plug_url
from tg.i18n import ugettext as _
from tgext.pluggable import app_model
from bson import ObjectId


class ManageUserAddressesController(TGController):

    @expose('stroller2.templates.manage.user_address.index')
    def index(self, **kw):
        user_id = tg.request.identity['user']._id
        addresses = app_model.UserAddress.query.find({'user_id': user_id}).all()
        return dict(addresses=addresses if addresses else [])

    @expose('stroller2.templates.manage.user_address.new')
    def new(self, **kw):
        validation_error = request.validation.exception
        return dict(
            form=get_new_user_address_form(),
            action=plug_url('stroller2', '/manage/address/create')
        )

    @expose()
    @validate(get_new_user_address_form(), error_handler=new)
    def create(self, **kw):
        user_id = tg.request.identity['user']._id
        new_address = app_model.UserAddress(
            user_id=user_id,
            shipping_address={
                'receiver': kw.get('receiver'),
                'address': kw.get('address'),
                'city': kw.get('city'),
                'province': kw.get('province'),
                'state': kw.get('state'),
                'country': kw.get('country'),
                'zip': kw.get('zip'),
                'details': kw.get('details')
            }
        )
        image = app_model.AvatarImage(
            image=kw.get('image'),
            address_id=new_address._id
        )
        flash(_('User address created'))
        return redirect(plug_url('stroller2', '/manage/address/index'))

    @expose('stroller2.templates.manage.product.edit')
    def edit(self, address_id, **kw):
        address = app_model.UserAddress.query.find({'_id': ObjectId(address_id)}).first()
        if address is None:
            flash(_('Address not find'))
            return redirect(plug_url('stroller2', '/manage/user_address/index'))

        value = {
            'address_id': str(address._id),
            'receiver': address.shipping_address['receiver'],
            'address': address.shipping_address['address'],
            'city': address.shipping_address['city'],
            'province': address.shipping_address['province'],
            'state': address.shipping_address['state'],
            'country': address.shipping_address['country'],
            'zip': address.shipping_address['zip'],
            'details': address.shipping_address['details']
        }
        return dict(
            form=get_edit_user_address_form(),
            value=value,
            action=plug_url('stroller2', '/manage/address/save'))

    @expose()
    @validate(get_edit_user_address_form(), error_handler=validated_handler(edit))
    def save(self, **kw):
        app_model.UserAddress.query.update(
            {'_id': ObjectId(kw.get('address_id'))},
            {'$set': {
                'shipping_address': {
                    'receiver': kw.get('receiver'),
                    'address': kw.get('address'),
                    'city': kw.get('city'),
                    'province': kw.get('province'),
                    'state': kw.get('state'),
                    'country': kw.get('country'),
                    'zip': kw.get('zip'),
                    'details': kw.get('details')
                }
            }}
        )
        flash(_('Address updated succesfully'))
        return redirect(plug_url('stroller2', '/manage/address/index'))

    @expose()
    def delete(self, address_id):
        app_model.UserAddress.query.remove({'_id': ObjectId(address_id)})
        flash(_('Address deleted'))
        return redirect(plug_url('stroller2', '/manage/address/index'))
