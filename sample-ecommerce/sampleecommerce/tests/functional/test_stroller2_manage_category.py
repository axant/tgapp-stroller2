# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from nose.tools import eq_, ok_
from sampleecommerce.tests import TestController
from tgext.ecommerce.model.models import Category
from sampleecommerce.model import DBSession


class TestManageCategoryController(TestController):

    def setup(self):
        super(TestManageCategoryController, self).setUp()
        self.category = Category(
            name={'en': 'Categoria 1'},
            slug='cat-1',
            details='details',
            sort_weight=1
        )
        DBSession.flush()

    def test_category_index(self):
        response = self.app.get(
            '/commerce/manage/category',
            extra_environ=self.admin_environ,
            status=200
        )
        assert 'Categoria 1' in response.body.decode('utf-8')

    def test_create_category(self):
        response = self.app.get(
            '/commerce/manage/category/new',
            extra_environ=self.admin_environ,
            status=200
        )

        form = response.form
        form['name'] = 'Categoria 2'
        form['parent_id'] = str(self.category._id)

        submission = form.submit(
            extra_environ=self.admin_environ,
            status=302
        )
        redirection = submission.follow(
            extra_environ=self.admin_environ
        )
        assert 'Category created' in redirection.body.decode('utf-8')

    def test_edit_category(self):
        response = self.app.get(
            '/commerce/manage/category/edit',
            extra_environ=self.admin_environ,
            params=dict(category_id=str(self.category._id)),
            status=200
        )

        form = response.form
        form['name'] = 'Categoria 1 Modificata'
        submission = form.submit(
            extra_environ=self.admin_environ,
            status=302
        )
        redirection = submission.follow(
            extra_environ=self.admin_environ
        )
        assert 'Category edited' in redirection.body.decode('utf-8')

    def test_delete_category(self):
        response = self.app.get(
            '/commerce/manage/category/delete',
            params=dict(category_id=str(self.category._id)),
            extra_environ=self.admin_environ,
            status=302
        )

        redirection = response.follow(
            extra_environ=self.admin_environ,
            status=200
        )
        assert 'Category deleted' in redirection.body.decode('utf8')
