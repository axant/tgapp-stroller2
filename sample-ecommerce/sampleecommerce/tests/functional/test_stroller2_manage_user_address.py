# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from nose.tools import eq_, ok_
from sampleecommerce.tests import TestController


class TestManageUserAddressController(TestController):

    def test_create_address(self):
        response = self.app.get(
            '/commerce/manage/address/new',
            extra_environ=self.admin_environ,
               status=200
        )

        form = response.form
        form['receiver'] = 'Mr. Mister',
        form['address'] = 'Viale Milano 69',
        form['city'] = 'Milano',
        form['province'] = 'MI',
        form['state'] = 'Lombardy',
        form['country'] = 'Italy',
        form['zip'] = '60049',
        form['details'] = 'Citofonare Ignazio'

        submission = form.submit(
            extra_environ=self.admin_environ,
            status=302
        )
        redirection = submission.follow(
            extra_environ=self.admin_environ
        )
        assert 'Viale Milano 69' in redirection.body.decode('utf-8')
