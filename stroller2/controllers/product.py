# coding=utf-8
from __future__ import unicode_literals
from bson import ObjectId
from stroller2.lib import get_buy_product_form

from tg import expose, app_globals, abort, lurl, validate, redirect, request, require, TGController
from tg.flash import flash
from tg.i18n import lazy_ugettext as l_, ugettext as _
from tg.predicates import not_anonymous
from datetime import datetime
from tgext.ecommerce.lib.exceptions import CartLockedException
from tgext.pluggable import plug_url


class ProductController(TGController):

    @expose('genshi:stroller2.templates.product.product')
    def _default(self, slug=None, product=None, *args, **kw):
        product = app_globals.shop.product.get(slug=slug, _id=product)
        if product is None:
            abort(404, 'Product not found')

        return dict(product=product, buy_form=get_buy_product_form(),
                    action=plug_url('stroller2', '/product/add_to_cart'),
                    active=self._product_is_active(product))

    @require(not_anonymous())
    @expose()
    @validate(get_buy_product_form(), error_handler=_default)
    def add_to_cart(self, product=None, quantity=1, **kw):
        print kw
        return
        product = app_globals.shop.product.get(_id=product)
        if product is None:
            abort(404, 'Product not found')
        try:
            cart = app_globals.shop.cart.create_or_get(request.identity['user'].user_id)
        except CartLockedException:
            flash(_('The cart is unavailable, try again later'), 'error')
            return redirect('/product/%s' % product.slug)
        if not app_globals.shop.product.buy(cart, product, 0, quantity):
            flash(_('The product is sold out'), 'error')
        else:
            flash(_('Product %s added to cart') % product.i18n_name)
        return redirect('/product/%s' % product.slug)

    @classmethod
    def _product_is_active(cls, product):
        if product is None:
            return False

        if not product.active:
            return False

        return product.configurations[0].qty > 0


    @expose('tavolaclandestina.templates.product.product')
    def share(self, slug=None, product=None, *args, **kw):
        product = app_globals.shop.product.get(slug=slug, _id=product)
        if product is None:
            abort(404, 'Product not found')

        return dict(product=product, buy_form=get_buy_product_form(),
                    action=plug_url('stroller2', '/product/add_to_cart'),
                    active=self._product_is_active(product))