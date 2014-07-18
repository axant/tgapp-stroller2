# coding=utf-8
from __future__ import unicode_literals
from tg import TGController, expose, app_globals, validate
from stroller2.lib import get_new_product_form
from tgext.pluggable import plug_url


class ManageProductController(TGController):

    @expose('genshi:stroller2.templates.manage.product.index')
    def index(self, **kw):
        print 'olol'
        products = app_globals.shop.product.get_many('product', {'active': True}).all()
        return dict(product=products)

    @expose('genshi:stroller2.templates.manage.product.new')
    def new(self, **kw):
        return dict(form=get_new_product_form(), action=plug_url('stroller2', 'manage/product/create'))

    @expose()
    @validate(get_new_product_form(), error_handler=index)
    def create(self, **kw):
        kw['type'] = 'product'
        app_globals.shop.product.create(kw)