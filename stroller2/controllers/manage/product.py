# coding=utf-8
from __future__ import unicode_literals
from tg import TGController, expose
from stroller2.lib import get_new_product_form
from tgext.pluggable import plug_url


class ManageProductController(TGController):

    @expose()
    def index(self):
        return {}

    @expose('genshi:stroller2.templates.manage.product.new')
    def new(self):
        return dict(form=get_new_product_form(), action=plug_url('stroller2', 'manage/product/create'))