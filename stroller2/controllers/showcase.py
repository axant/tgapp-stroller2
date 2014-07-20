# coding=utf-8
from __future__ import unicode_literals
from tg import TGController, expose, app_globals


class ShowcaseController(TGController):

    @expose('genshi:stroller2.templates.showcase.index')
    def index(self, **kw):
        products = app_globals.shop.product.get_many('product', query={'active': True}).all()
        return dict(products=products)

    @expose('genshi:stroller2.templates.showcase.product')
    def product(self, product, **kw):
        return dict(product=product)