# -*- coding: utf-8 -*-

"""WebHelpers used in tgapp-stroller2."""

#from webhelpers import date, feedgenerator, html, number, misc, text
from markupsafe import Markup
from tgext.pluggable import plug_url


def bold(text):
    return Markup('<strong>%s</strong>' % text)


def stroller2_product_url(product):
    return plug_url('stroller2', '/product/%s' % product.slug)

def stroller2_product_share_url(product):
    return plug_url('stroller2', '/product/share/%s' % product.slug)