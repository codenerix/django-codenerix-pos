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

import json
import uuid
import hashlib
import random
import string
from channels import Channel, Group

from django.db import models
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from django.conf import settings

from jsonfield import JSONField

from codenerix_payments.models import PaymentRequest

from codenerix.models import CodenerixModel
from codenerix_corporate.models import CorporateImage
from codenerix_products.models import ProductFinal
from codenerix_invoicing.models import BillingSeries
from codenerix_extensions.lib.cryptography import AESCipher

from codenerix.models import GenInterface
from codenerix.models_people import GenRole
from codenerix_extensions.helpers import get_external_method
from codenerix_storages.models import Storage, StorageZone
from codenerix_pos.settings import CDNX_POS_PERMISSIONS


"""
Plant
    Zones
    CorporateImage
    BillingSeries

Zones
    POS (pantalla fisica)
        Hardware Los que tengo (muchos)
        Hardware Los que puedo usar (muchos)
        token --- pos client (software instalado, minimo el id)
        Salable products (POSProduct)

    Slot (mesas)


Hardware (ticket, dni, caja, dispositivo de firma, dispositivo de consulta)
    nombre
    configuracion
    tipo (ticket, dni, caja, firma, consulta)
    token
"""

# Changing this KEYS will affect to any client beacuse it is used for communication as a standard
KIND_POSHARDWARE_TICKET = "TICKET"
KIND_POSHARDWARE_DNIE = "DNIE"
KIND_POSHARDWARE_CASH = "CASH"
KIND_POSHARDWARE_WEIGHT = "WEIGHT"
KIND_POSHARDWARE_SIGN = "SIGN"
KIND_POSHARDWARE_QUERY = "QUERY"

KIND_POSHARDWARE = (
    (KIND_POSHARDWARE_TICKET, _("Ticket printer")),
    (KIND_POSHARDWARE_DNIE, _("DNIe card reader")),
    (KIND_POSHARDWARE_CASH, _("Cash drawer")),
    (KIND_POSHARDWARE_WEIGHT, _("Weight")),
    (KIND_POSHARDWARE_SIGN, _("Signature pad")),
    (KIND_POSHARDWARE_QUERY, _("Query service (Ex: Barcode)")),  # Barcode reader, Point of Information for clients, etc...
)


def keymaker():
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(32))


class POSPlant(CodenerixModel):
    """
    Plant
    """
    corporate_image = models.ForeignKey(CorporateImage, related_name='posplants', verbose_name=_("Corporate image"), blank=False, null=False, on_delete=models.CASCADE)
    billing_series = models.ForeignKey(BillingSeries, related_name='posplants', verbose_name='Billing series', blank=False, null=False, on_delete=models.CASCADE)
    name = models.CharField(_("Name"), max_length=250, blank=False, null=False, unique=True)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return u"{}".format(smart_text(self.name))

    def __fields__(self, info):
        fields = []
        fields.append(('name', _("Name")))
        return fields


class POSZone(CodenerixModel):
    """
    Zone
    """
    plant = models.ForeignKey(POSPlant, related_name='zones', verbose_name=_("Plant"), blank=False, null=False, on_delete=models.CASCADE)
    name = models.CharField(_("Name"), max_length=250, blank=False, null=False, unique=True)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return u"{}".format(smart_text(self.name))

    def __fields__(self, info):
        fields = []
        fields.append(('plant', _("Plant")))
        fields.append(('name', _("Name")))
        return fields


class POSHardware(CodenerixModel):
    """
    Hardware
    """
    pos = models.ForeignKey("POS", related_name='hardwares', verbose_name=_("POS"), blank=True, null=True, on_delete=models.CASCADE)
    kind = models.CharField(_("Kind"), max_length=6, choices=KIND_POSHARDWARE, blank=False, null=False)
    name = models.CharField(_("Name"), max_length=250, blank=False, null=False)
    enable = models.BooleanField(_('Enable'), default=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    key = models.CharField(_("Key"), max_length=32, blank=False, null=False, unique=True, editable=False, default=keymaker)
    profile = models.CharField(_("Profile"), max_length=30, blank=True, null=False, default='CONFIG')
    config = JSONField(_("config"), blank=True, null=True)
    value = JSONField(_("config"), blank=True, null=True)

    class Meta(CodenerixModel.Meta):
        unique_together = ('pos', 'kind', 'name')

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return u"{}: {} ({})".format(smart_text(self.pos.name), smart_text(self.name), smart_text(self.kind))

    def __fields__(self, info):
        fields = []
        fields.append(('pos', _("POS")))
        fields.append(('get_kind_display', _("Kind")))
        fields.append(('name', _("Name")))
        fields.append(('enable', _("Enable")))
        fields.append(('uuid', _("UUID")))
        fields.append(('key', _("Key")))
        fields.append(('profile', _("Profile")))
        fields.append(('config', _("Config")))
        fields.append(('value', _("Value")))
        return fields

    def get_config(self):
        if self.profile == 'CONFIG':
            return self.config
        else:
            return getattr(settings, 'POSHARDWARE_PROFILE', {}).get(self.kind, {}).get(self.profile, {})

    def save(self, *args, **kwargs):
        if 'doreset' in kwargs:
            doreset = kwargs.pop('doreset')
        else:
            doreset = True

        result = super(POSHardware, self).save(*args, **kwargs)
        if doreset:
            try:
                self.pos.reset_client()
            except IOError:
                pass
        return result

    def recv(self, msg):
        # Save result in database
        self.value = msg
        self.save(doreset=False)

        # Define final message to all groups
        finalmsg = {}
        finalmsg['action'] = 'subscription'
        finalmsg['data'] = msg

        # Notify all groups about this message
        data = self.pos.build_msg(finalmsg, broadcast=self.uuid.hex, key=self.key)
        Group(self.uuid.hex).send({'text': data})

    def send(self, msg=None, ref=None):
        '''
        Example of msg for each POSHARDWARE:
            TICKET: {'data': 'print this text, process thid dictionary or take my money'}
            CASH:   {'data': '...ANYTHING except None to open the Cash Drawer...' }
            DNIE:   {'data': '...ANYTHING except None to get again data from DNIe if connected...' }
            WEIGHT: {'data': '...ANYTHING except None to get the value of the last wegith' }
            OTHERS: {'data': '...ANYTHING you need to communicate to the device'}
        '''
        if self.kind in ['CASH', 'DNIE', 'WEIGHT']:
            data = 'DOIT'
        else:
            if msg is not None:
                data = msg
            else:
                raise IOError("Nothing to say to the remote endpoint???")

        # Say it to send this message
        self.pos.send(data, ref, self.uuid)


class POSGroupProduct(CodenerixModel):
    """
    Salable group products in the POS
    """
    name = models.CharField(_("Name"), max_length=80, null=False, blank=False)
    enable = models.BooleanField(_('Enable'), default=True)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return u"{} ({})".format(smart_text(self.name), smart_text(self.enable))

    def __fields__(self, info):
        fields = []
        fields.append(('name', _("Name")))
        fields.append(('enable', _("Enable")))
        return fields

    def lock_delete(self):
        if self.poss.exists():
            return _("Cannot delete POS group product model, relationship between POS group product and POS")
        else:
            return super(POSGroupProduct, self).lock_delete()


class POS(CodenerixModel):
    '''
    Point of Service
    '''
    name = models.CharField(_("Name"), max_length=250, blank=False, null=False, unique=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    key = models.CharField(_("Key"), max_length=32, blank=False, null=False, unique=True, editable=False, default=keymaker)
    zone = models.ForeignKey(POSZone, related_name='poss', verbose_name=_("Zone"), on_delete=models.CASCADE)
    group_product = models.ForeignKey(POSGroupProduct, related_name='poss', verbose_name=_("Group product"), on_delete=models.CASCADE)
    payments = models.ManyToManyField(PaymentRequest, related_name='poss', verbose_name=_("Payments"), blank=True)
    channel = models.CharField(_("Channel"), max_length=50, blank=True, null=True, unique=True, editable=False)
    commit = models.CharField(_("Commit"), max_length=40, blank=True, null=True, default="LATEST")
    # Hardware that can use
    hardware = models.ManyToManyField(POSHardware, related_name='poss', verbose_name=_("Hardware it can use"), blank=True)
    # Storage stock
    storage_stock = models.ManyToManyField(Storage, related_name='poss_storage_stock', verbose_name=_("Storages where the stock is subtracted"), blank=True)
    # Storate query
    storage_query = models.ManyToManyField(Storage, related_name='poss_storage_query', verbose_name=_("Storages where you can consult"), blank=True)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return u"{}".format(smart_text(self.name))

    def __fields__(self, info):
        fields = []
        fields.append(('zone', _("Zone")))
        fields.append(('name', _("Name")))
        fields.append(('uuid', _("UUID")))
        fields.append(('key', _("Key")))
        fields.append(('channel', _("Channel")))
        fields.append(('hardware', _("Hardware")))
        fields.append(('storage_stock', _("Storages where the stock is subtracted")))
        fields.append(('storage_query', _("Storages where you can consult")))
        fields.append(('commit', _("Commit")))
        return fields

    def have_cash_drawer(self):
        return self.hardware.filter(kind=KIND_POSHARDWARE_CASH).exists()

    def save(self, *args, **kwargs):
        if 'doreset' in kwargs:
            doreset = kwargs.pop('doreset')
        else:
            doreset = True
        result = super(POS, self).save(*args, **kwargs)
        if self.channel and doreset:
            try:
                self.reset_client()
            except IOError:
                pass
        return result

    def reset_client(self):
        self.send({'action': 'reset'})

    def ping(self, uid=None):
        if uid is None:
            uidtxt = None
        else:
            uidtxt = uid.hex
        ref = hashlib.sha1(uuid.uuid4().hex.encode('utf-8')).hexdigest()
        self.send({'action': 'ping', 'ref': ref, 'uuid': uidtxt})
        return ref

    def build_msg(self, data, ref=None, uid=None, broadcast=None, key=None):

        if uid:
            # Message for some client
            message = {
                'action': 'msg',
                'message': {
                    'data': data,
                },
                'uuid': uid.hex,
            }
        else:
            # Message for the server
            message = data

        # Choose key
        if broadcast is None or key is None:
            key = self.key

        # Send message
        crypto = AESCipher()
        msg = json.dumps({'request': message, 'ref': ref})
        request = crypto.encrypt(msg, key).decode('utf-8')
        struct = {'message': request}
        if broadcast:
            struct['broadcast'] = broadcast
        data = json.dumps(struct)

        # Return result
        return data

    def send(self, data, ref=None, uid=None, broadcast=None, key=None):

        if self.channel:
            data = self.build_msg(data, ref, uid, broadcast, key)
            Channel(self.channel).send({'text': data})
        else:
            raise IOError("No channel available for this POS")


class POSSlot(CodenerixModel):
    '''
    Slots for Point of Service
    '''
    zone = models.ForeignKey(POSZone, related_name='slots', verbose_name=_("Zone"), on_delete=models.CASCADE)
    name = models.CharField(_("Name"), max_length=250, blank=False, null=False, unique=True)
    # orders = models.ManyToManyField(SalesOrder, related_name='slots', editable=False, verbose_name=_("Orders"))
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
        # fields.append(('orders', _("Orders")))
        return fields


class POSProduct(CodenerixModel):
    """
    Salable products in the POS
    """
    group_product = models.ForeignKey(POSGroupProduct, related_name='posproducts', verbose_name=_("Group Product"), on_delete=models.CASCADE)
    product_final = models.ForeignKey(ProductFinal, related_name='posproducts', verbose_name=_("Product"), on_delete=models.CASCADE)
    enable = models.BooleanField(_('Enable'), default=True)

    class Meta(CodenerixModel.Meta):
        unique_together = (("group_product", "product_final"))

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return u"{} {}".format(smart_text(self.group_product), smart_text(self.product_final))

    def __fields__(self, info):
        fields = []
        fields.append(('group_product', _("Group Product")))
        fields.append(('product_final', _("Product")))
        fields.append(('enable', _("Enable")))
        return fields


class POSLog(CodenerixModel):
    """
    LOG for POS
    """
    pos = models.ForeignKey(POS, related_name='logs', verbose_name=_("POS"), editable=False, null=True, on_delete=models.CASCADE)
    poshw = models.ForeignKey(POSHardware, related_name='logs', verbose_name=_("POS"), editable=False, null=True, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    log = JSONField(_("LOG"), blank=True, null=True)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return self.uuid.hex

    def __fields__(self, info):
        fields = []
        fields.append(('created', _("Created")))
        fields.append(('uuid', _("UUID")))
        fields.append(('pos', _("POS")))
        fields.append(('poshw', _("POSHardware")))
        fields.append(('log', _("Log")))
        return fields

    def __searchF__(self, info):

        # Build both lists
        poss = [(pos.pk, pos.name) for pos in POS.objects.all()]
        poshws = [(poshw.pk, poshw.name) for poshw in POSHardware.objects.all()]

        tf = {}
        tf['uuid'] = (_('UUID'), lambda x: Q(uuid__icontains=x), 'input')
        tf['pos'] = (_('POS'), lambda x: Q(pos__pk=x), poss)
        tf['poshw'] = (_('Hardware'), lambda x: Q(poshw__pk=x), poshws)
        return tf


# ############################
class ABSTRACT_GenPOSOperator(models.Model):  # META: Abstract class

    class Meta(object):
        abstract = True


class POSOperator(GenRole, CodenerixModel):
    class CodenerixMeta:
        abstract = ABSTRACT_GenPOSOperator
        rol_groups = {
            'POSOperator': CDNX_POS_PERMISSIONS['operator'],
        }
        rol_permissions = [
        ]

        force_methods = {
            'foreignkey_posoperator': ('CDNX_get_fk_info_posoperator', _('---')),
        }

    pos = models.ManyToManyField(POS, related_name='pos_operators', verbose_name=_('POS'))
    enable = models.BooleanField(_("Enable"), blank=False, null=False, default=True)

    @staticmethod
    def foreignkey_external():
        return get_external_method(POSOperator, POSOperator.CodenerixMeta.force_methods['foreignkey_posoperator'][0])

    def __unicode__(self):
        return u"{}".format(smart_text(self.pk))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('pos', _("POS")))
        fields.append(('enable', _("Enable")))
        fields = get_external_method(POSOperator, '__fields_posoperator__', info, fields)
        return fields


# operators
class GenPOSOperator(GenInterface, ABSTRACT_GenPOSOperator):  # META: Abstract class
    pos_operator = models.OneToOneField(POSOperator, related_name='external', verbose_name=_("POS Operator"), null=True, on_delete=models.SET_NULL, blank=True)
    # Storage Zone Operable is used to specify from/to StorageZone the POSOperator can move stock
    storage_zone_operable = models.ManyToManyField(StorageZone, related_name='external', verbose_name=_("Storage Zone Operable"), blank=True)

    class Meta(GenInterface.Meta, ABSTRACT_GenPOSOperator.Meta):
        abstract = True

    @classmethod
    def permissions(cls):
        # group = 'POSOperator'
        # perms = []
        print(cls.posoperator.field.related_model)

        return None

        # print({group: {'gperm': None, 'dperm': perms, 'model': None},})
