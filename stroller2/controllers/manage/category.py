# coding=utf-8
from __future__ import unicode_literals
from tgext.ecommerce.lib.exceptions import CategoryAssignedToProductException
from stroller2.lib import get_new_category_form, get_edit_category_form
from tg import expose, TGController, app_globals, validate, redirect, flash
import tg
from tgext.pluggable import plug_url
from tg.i18n import lazy_ugettext as l_, ugettext as _



class ManageCategoryController(TGController):
    @expose('genshi:stroller2.templates.manage.category.index')
    def index(self, **kw):
        categories = app_globals.shop.category.get_all().all()
        return dict(categories=categories)

    @expose('genshi:stroller2.templates.manage.category.new')
    def new(self, **kw):
        return dict(form=get_new_category_form(), action=plug_url('stroller2', '/manage/category/create'))

    @expose()
    @validate(get_new_category_form(), error_handler=index)
    def create(self, **kw):
        kw['parent'] = app_globals.shop.category.get(kw.pop('parent_id'))
        app_globals.shop.category.create(**kw)
        flash(_('Category created'))
        return redirect(plug_url('stroller2', '/manage/category/index'))

    @expose('genshi:stroller2.templates.manage.category.edit')
    def edit(self, **kw):
        category = app_globals.shop.category.get(kw['category_id'])
        return dict(form=get_edit_category_form(), action=plug_url('stroller2', '/manage/category/save'),
                    value=dict(category_id=category._id, name=category.name[tg.config.lang],
                               parent_id=category.parent))

    @expose()
    @validate(get_edit_category_form(), error_handler=index)
    def save(self, **kw):
        kw['parent'] = app_globals.shop.category.get(kw.pop('parent_id'))
        kw['_id'] = kw.pop('category_id')
        app_globals.shop.category.edit(**kw)
        flash(_('Category edited'))
        return redirect(plug_url('stroller2', '/manage/category/index'))

    @expose()
    def delete(self, category_id, **kw):
        try:
            app_globals.shop.category.delete(category_id)
            flash(_('Category deleted'))
        except CategoryAssignedToProductException:
            flash(_('Is impossible to delete a category assigned to product'), 'error')
        return redirect(plug_url('stroller2', '/manage/category/index'))
