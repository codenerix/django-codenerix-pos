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

from django.db import models
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _

from codenerix_payments.models import PaymentRequest
from codenerix_invoicing.models import SalesOrder

from codenerix.models import CodenerixModel


class POS(CodenerixModel):
    '''
    Point of Service
    '''
    name = models.CharField(_("Name"), max_length=250, blank=False, null=False, unique=True)
    services  = models.CharField(_("Services"), max_length=250, blank=False, null=False, unique=True)
    cid  = models.CharField(_("CID"), max_length=250, blank=False, null=False, unique=True)
    key  = models.CharField(_("KEY"), max_length=250, blank=False, null=False, unique=True)
    payments = models.ManyToManyField(PaymentRequest, related_name='pos')

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return u"{}".format(smart_text(self.name))

    def __fields__(self, info):
        fields = []
        fields.append(('name', _("Name")))
        fields.append(('services', _("Services")))
        fields.append(('cid', _("CID")))
        fields.append(('key', _("Key")))
        return fields


class POSslots(CodenerixModel):
    '''
    Slots for Point of Service
    '''
    pos = models.ForeignKey(POS, related_name='slots')
    name = models.CharField(_("Name"), max_length=250, blank=False, null=False, unique=True)
    orders = models.ManyToManyField(SalesOrder, related_name='posslot')
    pos_x = models.IntegerField(_('Pos X'), null=False, blank=False)
    pos_y = models.IntegerField(_('Pos Y'), null=False, blank=False)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return u"{}".format(smart_text(self.name))

    def __fields__(self, info):
        fields = []
        fields.append(('name', _("Name")))
        fields.append(('services', _("Services")))
        fields.append(('cid', _("CID")))
        fields.append(('key', _("Key")))
        return fields

