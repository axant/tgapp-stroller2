# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from nose.tools import eq_, ok_
from sampleecommerce.tests import TestController
from tgext.ecommerce.model.models import Category, Product
from sampleecommerce.model import DBSession
from datetime import datetime, timedelta

class TestManageProductController(TestController):

    def setup(self):
        super(TestManageProductController, self).setUp()
        self.category = Category(
            name={'en': 'Categoria 1'},
            slug='cat-1',
            details='details',
            sort_weight=1
        )
        # self.product = Product(
        #     type='type',
        #     name={'en': 'Prodotto 1'},
        #     category_id=self.category._id,
        #     categories_ids=[self.category._id, ],
        #     description={'en': 'descrizione'},
        #     slug='product-1',
        #     details={'details': 'first detail'},
        #     active=True,
        #     published=True,
        #     valid_from=datetime.utcnow() - timedelta(days=1),
        #     valid_to=datetime.utcnow() + timedelta(days=90),
        #     configurations=[{
        #         'sku': 'sku',
        #         'variety': {'en': 'variety 1'},
        #         'price': 10.0,
        #         'rate': 22.0,
        #         'vat': 2.2,
        #         'qty': 10,
        #         'initial_quantity': 10
        #     }]
        # )
        DBSession.flush()

    def test_product_index(self):
        response = self.app.get(
            '/commerce/manage/product',
            extra_environ=self.admin_environ,
            status=200
        )
        response.showbrowser()
        assert 'New product' in response.body.decode('utf-8')


