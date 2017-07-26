# -*- coding: utf-8 -*-
#
# django-codenerix-pos
#
# Copyright 2017 Centrologic Computational Logistic Center S.L.
#
# Project URL : http://www.codenerix.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid

from django.db import models
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _

from jsonfield import JSONField

from codenerix_payments.models import PaymentRequest
from codenerix_invoicing.models_sales import SalesOrder

from codenerix.models import CodenerixModel

"""

Zones
    POS (pantalla fisica)
        Hardware Los que tengo (muchos)
        Hardware Los que puedo usar (muchos)
        token --- pos client (software instalado, minimo el id)

    Slot (mesas)


Hardware (ticket, dni, caja, dispositivo de firma, dispositivo de consulta)
    nombre
    configuracion
    tipo (ticket, dni, caja, firma, consulta)
    token
"""

# Changing this KEYS will affect to any client beacuse it is used for communication as a standard
KIND_POSHARDWARE = (
    ("TICKET", _("Ticket printer")),
    ("DNIE", _("DNIe card reader")),
    ("CASH", _("Cash drawer")),
    ("WEIGHT", _("Weight")),
    ("SIGN", _("Signature pad")),
    ("QUERY", _("Query service (Ex: Barcode)")),  # Barcode reader, Point of Information for clients, etc...
)


class POSZone(CodenerixModel):
    """
    Zone
    """
    name = models.CharField(_("Name"), max_length=250, blank=False, null=False, unique=True)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return u"{}".format(smart_text(self.name))

    def __fields__(self, info):
        fields = []
        fields.append(('name', _("Name")))
        return fields


class POSHardware(CodenerixModel):
    """
    Hardware
    """
    pos = models.ForeignKey("POS", related_name='hardwares', verbose_name=_("Hardware"), blank=True, null=True)
    kind = models.CharField(_("Kind"), max_length=6, choices=KIND_POSHARDWARE, blank=False, null=False)
    name = models.CharField(_("Name"), max_length=250, blank=False, null=False, unique=True)
    enable = models.BooleanField(_('Enable'), default=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    config = JSONField(_("config"))

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return u"{}".format(smart_text(self.name))

    def __fields__(self, info):
        fields = []
        fields.append(('pos', _("POS")))
        fields.append(('get_kind_display', _("Kind")))
        fields.append(('name', _("Name")))
        fields.append(('enable', _("Enable")))
        fields.append(('uuid', _("UUID")))
        fields.append(('config', _("Config")))
        return fields


class POS(CodenerixModel):
    '''
    Point of Service
    '''
    name = models.CharField(_("Name"), max_length=250, blank=False, null=False, unique=True)
    cid = models.CharField(_("CID"), max_length=20, blank=True, null=True, unique=True)
    token = models.CharField(_("Token"), max_length=40, blank=False, null=False, unique=True)
    zone = models.ForeignKey(POSZone, related_name='poss', verbose_name=_("Zone"))
    payments = models.ManyToManyField(PaymentRequest, related_name='poss', verbose_name=_("Payments"), blank=True, null=True)
    # Hardware that can use
    hardware = models.ManyToManyField(POSHardware, related_name='poss', verbose_name=_("Hardware it can use"), blank=True, null=True)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return u"{}".format(smart_text(self.name))

    def __fields__(self, info):
        fields = []
        fields.append(('zone', _("Zone")))
        fields.append(('name', _("Name")))
        fields.append(('cid', _("CID")))
        fields.append(('token', _("Token")))
        fields.append(('hardware', _("Hardware")))
        return fields


class POSSlot(CodenerixModel):
    '''
    Slots for Point of Service
    '''
    zone = models.ForeignKey(POSZone, related_name='slots', verbose_name=_("Zone"))
    name = models.CharField(_("Name"), max_length=250, blank=False, null=False, unique=True)
    orders = models.ManyToManyField(SalesOrder, related_name='slots', editable=False, verbose_name=_("Orders"))
    pos_x = models.IntegerField(_('Pos X'), null=True, blank=True, default=None, editable=False)
    pos_y = models.IntegerField(_('Pos Y'), null=True, blank=True, default=None, editable=False)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return u"{}".format(smart_text(self.name))

    def __fields__(self, info):
        fields = []
        fields.append(('zone', _("Zone")))
        fields.append(('name', _("Name")))
        fields.append(('orders', _("Orders")))
        return fields
