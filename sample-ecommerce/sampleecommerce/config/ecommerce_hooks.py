# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import tw2.forms as twf
import tw2.core as twc
from tg.i18n import lazy_ugettext as l_


class EditOrderForm(twf.ListForm):
    css_class = 'admin-form'
    order_id = twf.HiddenField(key='_id')
    bill = twf.HiddenField(validator=twc.BoolValidator())

    class ShipmentInfo(twf.ListFieldSet):
        label = l_("Dati Spedizione")
        key = 'shipment_info'

        receiver = twf.TextField(validator=twc.Validator(required=True),
                                 css_class="form-control", label=l_("Destinatario"))
        address = twf.TextField(validator=twc.Validator(required=True),
                                css_class="form-control", label=l_("Indirizzo"))
        city = twf.TextField(validator=twc.Validator(required=True),
                             css_class="form-control", label=l_("Città"))
        province = twf.TextField(validator=twc.Validator(required=True),
                                 css_class="form-control", label=l_("Provincia"))
        zip_code = twf.TextField(validator=twc.Validator(required=True),
                                 css_class="form-control", label=l_("CAP"))
        country = twf.SingleSelectField(css_class="form-control", prompt_text=None, label=l_("Stato"),
                                        options=twc.Deferred(lambda: [('IT', l_('Stato'))]))

    class Details(twf.ListFieldSet):
        label = None
        key = 'details'

        email = twf.TextField(validator=twc.Validator(required=True),
                              css_class="form-control", label=l_("Email"))
        phone = twf.TextField(validator=twc.Validator(), css_class="form-control", label=l_("Telefono"))

    class BillInfo(twf.ListFieldSet):
        label = l_("Dati Fatturazione")
        key = 'bill_info'

        company = twf.TextField(css_class="form-control", label=l_("Ragione Sociale"))
        vat = twf.TextField(css_class="form-control", label=l_("Partita IVA"))
        fiscal_code = twf.TextField(css_class="form-control", label=l_("Codice Fiscale"))
        address = twf.TextField(css_class="form-control", label=l_("Indirizzo"))
        city = twf.TextField(css_class="form-control", label=l_("Città"))
        province = twf.TextField(css_class="form-control", label=l_("Provincia"))
        zip_code = twf.TextField(css_class="form-control", label=l_("CAP"))
        country = twf.SingleSelectField(css_class="form-control", prompt_text=None, label=l_("Stato"),
                                        options=twc.Deferred(lambda: [('IT', l_('Stato'))]))
    submit = twf.SubmitButton(value=l_('Salva'), css_class='form-control')

    def prepare(self):
        super(EditOrderForm, self).prepare()
        if not self.child.children.bill.value or self.child.children.bill.value == 'false':
            self.child.children.BillInfo.container_attrs = {'style':'display:none;'}