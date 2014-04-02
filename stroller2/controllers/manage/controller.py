# coding=utf-8
from __future__ import unicode_literals
from tg import TGController, expose
from stroller2.controllers.manage.product import ManageProductController


class ManageController(TGController):
    product = ManageProductController()

    @expose()
    def index(self):
        return {}