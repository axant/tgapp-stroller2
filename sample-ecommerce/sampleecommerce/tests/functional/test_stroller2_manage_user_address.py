# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from nose.tools import eq_, ok_
from sampleecommerce.tests import TestController
from sampleecommerce.model import DBSession
from tgext.pluggable import app_model


class TestManageUserAddressController(TestController):

    def setUp(self):
        super(TestManageUserAddressController, self).setUp()
        self.address = app_model.UserAddress(
            user_id=app_model.User.query.find({'user_name': 'manager'}).first()._id,
            shipping_address={
                'receiver': 'Ms. Miss',
                'address': 'Viale Roma 99',
                'city': 'Roma',
                'province': 'RM',
                'state': 'Lazio',
                'country': 'Italy',
                'zip': '20049',
                'details': 'Citofonare Fiorella'
            }
        )
        DBSession.flush()

    def test_create_and_index_address(self):
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
        redirection.showbrowser()
        assert 'Viale Milano 69' in redirection.body.decode('utf-8')
        assert 'Viale Roma 99' in redirection.body.decode('utf-8')
        assert 'New address' in redirection.body.decode('utf-8')

    def test_edit_address(self):
        response = self.app.get(
            '/commerce/manage/address/edit',
            extra_environ=self.admin_environ,
            params=dict(address_id=str(self.address._id)),
            status=200
        )
        form = response.form
        form['receiver'] = self.address.shipping_address['receiver'] + ' modificato'
        form['address'] = self.address.shipping_address['address'] + ' modificato'
        form['city'] = self.address.shipping_address['city'] + ' modificato'
        form['province'] = self.address.shipping_address['province'] + ' modificato'
        form['state'] = self.address.shipping_address['state'] + ' modificato'
        form['country'] = self.address.shipping_address['country'] + ' modificato'
        form['zip'] = self.address.shipping_address['zip'] + ' modificato'
        form['details'] = self.address.shipping_address['details'] + ' modificato'

        submission = form.submit(
            extra_environ=self.admin_environ,
            status=302
        )

        redirection = submission.follow(
            extra_environ=self.admin_environ,
            status=200
        )

        assert 'Viale Roma 99 modificato' in redirection.body.decode('utf-8')
        assert 'Address updated succesfully' in redirection.body.decode('utf-8')

    def test_delete_address(self):
        response = self.app.get(
            '/commerce/manage/address/delete',
            params=dict(address_id=str(self.address._id)),
            extra_environ=self.admin_environ,
            status=302
        )
        redirection = response.follow(
            extra_environ=self.admin_environ,
            status=200
        )
        assert 'Viale Roma 99' not in redirection.body.decode('utf-8')
        assert 'Address deleted' in redirection.body.decode('utf-8')
