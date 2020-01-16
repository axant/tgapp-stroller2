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
        # self.category = self.shopmanager.category.create(
        #     'Categoria 1', slug='cat-1', sort_weight=1
        # )
        self.category = Category(
            name={'en': 'Categoria 1'},
            slug='cat-1',
            details='details',
            sort_weight=1
        )
        DBSession.flush()
        self.proddata = {
            'name': 'Prodotto 1', 'description': 'Descr Prod1', 'sku': 'SKUPROD1',
            'categories_ids': [str(self.category._id), ], 'price': 10, 'rate': 22, 'vat': 2.2, 'qty': 10,
            'weight': 1000, 'type': 'product'}

    def tests_create_product(self):
        response = self.app.get(
            '/commerce/manage/product/new',
            extra_environ=self.admin_environ,
            status=200
        )
        form = response.form
        form['name'] = self.proddata['name']
        form['description'] = self.proddata['description']
        form['categories_ids'] = self.proddata['categories_ids']
        form['sku'] = self.proddata['sku']
        form['price'] = self.proddata['price']
        form['rate'] = self.proddata['rate']
        form['vat'] = self.proddata['vat']
        form['qty'] = self.proddata['qty']
        form['weight'] = self.proddata['weight']

        submission = form.submit(
            extra_environ=self.admin_environ,
            status=302
        )
        redirection = submission.follow(
            extra_environ=self.admin_environ
        )
        redirection.showbrowser()
        assert self.proddata['name'] in redirection.body.decode('utf-8')


    def test_product_index(self):
        response = self.app.get(
            '/commerce/manage/product',
            extra_environ=self.admin_environ,
            status=200
        )
        response.showbrowser()
        assert 'New product' in response.body.decode('utf-8')


