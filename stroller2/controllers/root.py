# coding=utf-8
from __future__ import unicode_literals

from tg import TGController
from tg import expose, flash, require, url, lurl, request, redirect, validate
from stroller2.controllers.manage.controller import ManageController


class RootController(TGController):
    manage = ManageController()

    @expose('stroller2.templates.index')
    def index(self):
        return dict()
