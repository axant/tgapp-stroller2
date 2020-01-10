from __future__ import unicode_literals

from nose.tools import eq_, ok_

from sampleecommerce.tests import TestController
from tgext.ecommerce.model.models import Category
from sampleecommerce.model import DBSession


class TestManageCategoryController(TestController):

    def setup(self):
        super(TestManageCategoryController, self).setUp()
        c = Category(
            name='Categoria 1',
            slug='cat-1',
            details='details',
            sort_weight=1
        )
        DBSession.flush()
        DBSession.clear()
 