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

import random
import string

from django.db.models import Q
from django.utils.translation import ugettext as _

from codenerix.views import GenList, GenCreate, GenCreateModal, GenUpdate, GenUpdateModal, GenDelete, GenDetail, GenDetailModal

from .models import POSZone, POSHardware, POS, POSSlot, POSPlant, POSProduct, POSLog
from .forms import POSZoneForm, POSHardwareForm, POSForm, POSFormCreate, POSSlotForm, POSPlantForm, POSProductForm


# ###########################################
# POSPlant
class POSPlantList(GenList):
    model = POSPlant
    extra_context = {'menu': ['pos', 'posplant'], 'bread': [_('POS'), _('Plant')]}


class POSPlantCreate(GenCreate):
    model = POSPlant
    form_class = POSPlantForm


class POSPlantCreateModal(GenCreateModal, POSPlantCreate):
    pass


class POSPlantUpdate(GenUpdate):
    model = POSPlant
    form_class = POSPlantForm


class POSPlantUpdateModal(GenUpdateModal, POSPlantUpdate):
    pass


class POSPlantDelete(GenDelete):
    model = POSPlant


class POSPlantDetails(GenDetail):
    model = POSPlant
    groups = POSPlantForm.__groups_details__()


# ###########################################
# POSZone
class POSZoneList(GenList):
    model = POSZone
    extra_context = {'menu': ['pos', 'poszone'], 'bread': [_('POS'), _('Zone'), ]}


class POSZoneCreate(GenCreate):
    model = POSZone
    form_class = POSZoneForm


class POSZoneCreateModal(GenCreateModal, POSZoneCreate):
    pass


class POSZoneUpdate(GenUpdate):
    model = POSZone
    form_class = POSZoneForm


class POSZoneUpdateModal(GenUpdateModal, POSZoneUpdate):
    pass


class POSZoneDelete(GenDelete):
    model = POSZone


class POSZoneDetails(GenDetail):
    model = POSZone
    groups = POSZoneForm.__groups_details__()


# ###########################################
# POSHardware
class POSHardwareList(GenList):
    model = POSHardware
    extra_context = {'menu': ['pos', 'poshardware'], 'bread': [_('POS'), _('Hardware'), ]}


class POSHardwareCreate(GenCreate):
    model = POSHardware
    form_class = POSHardwareForm


class POSHardwareCreateModal(GenCreateModal, POSHardwareCreate):
    pass


class POSHardwareUpdate(GenUpdate):
    model = POSHardware
    form_class = POSHardwareForm


class POSHardwareUpdateModal(GenUpdateModal, POSHardwareUpdate):
    pass


class POSHardwareDelete(GenDelete):
    model = POSHardware


class POSHardwareSubList(GenList):
    model = POSHardware
    extra_context = {'menu': ['pos', 'poshardware'], 'bread': [_('POS'), _('Hardware'), ]}

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(pos__pk=pk)
        return limit


class POSHardwareDetails(GenDetail):
    model = POSHardware
    groups = POSHardwareForm.__groups_details__()


class POSHardwareDetailModal(GenDetailModal, POSHardwareDetails):
    pass


# ###########################################
# POS
class POSList(GenList):
    model = POS
    extra_context = {'menu': ['pos', 'pos'], 'bread': [_('POS'), _('POS'), ]}


class POSCreate(GenCreate):
    model = POS
    form_class = POSFormCreate

    def get_form(self, *args, **kwargs):
        form = super(POSCreate, self).get_form(*args, **kwargs)
        form.fields["key"].initial = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(32))
        return form


class POSCreateModal(GenCreateModal, POSCreate):
    pass


class POSUpdate(GenUpdate):
    model = POS
    form_class = POSForm


class POSUpdateModal(GenUpdateModal, POSUpdate):
    pass


class POSDelete(GenDelete):
    model = POS


class POSSubList(GenList):
    model = POS
    extra_context = {'menu': ['pos', 'pos'], 'bread': [_('POS'), _('POS'), ]}

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(zone__pk=pk)
        return limit


class POSDetails(GenDetail):
    model = POS
    groups = POSForm.__groups_details__()


class POSDetailModal(GenDetailModal, POSDetails):
    pass


# ###########################################
# POSSlot
class POSSlotList(GenList):
    model = POSSlot
    extra_context = {'menu': ['pos', 'posslot'], 'bread': [_('POS'), _('Slot'), ]}


class POSSlotCreate(GenCreate):
    model = POSSlot
    form_class = POSSlotForm


class POSSlotCreateModal(GenCreateModal, POSSlotCreate):
    pass


class POSSlotUpdate(GenUpdate):
    model = POSSlot
    form_class = POSSlotForm


class POSSlotUpdateModal(GenUpdateModal, POSSlotUpdate):
    pass


class POSSlotDelete(GenDelete):
    model = POSSlot


class POSSlotSubList(GenList):
    model = POSSlot
    extra_context = {'menu': ['pos', 'posslot'], 'bread': [_('POS'), _('Slot'), ]}

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(zone__pk=pk)
        return limit


class POSSlotDetails(GenDetail):
    model = POSSlot
    groups = POSSlotForm.__groups_details__()


class POSSlotDetailModal(GenDetailModal, POSSlotDetails):
    pass


# ###########################################
# POSProduct
class POSProductList(GenList):
    model = POSProduct
    extra_context = {'menu': ['pos', 'posproduct'], 'bread': [_('POS'), _('Product')]}


class POSProductCreate(GenCreate):
    model = POSProduct
    form_class = POSProductForm


class POSProductCreateModal(GenCreateModal, POSProductCreate):
    pass


class POSProductUpdate(GenUpdate):
    model = POSProduct
    form_class = POSProductForm


class POSProductUpdateModal(GenUpdateModal, POSProductUpdate):
    pass


class POSProductDelete(GenDelete):
    model = POSProduct


class POSProductSubList(GenList):
    model = POSProduct
    extra_context = {'menu': ['POSProduct', 'people'], 'bread': [_('POSProduct'), _('People')]}

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(pos__pk=pk)
        return limit


class POSProductDetails(GenDetail):
    model = POSProduct
    groups = POSProductForm.__groups_details__()


class POSProductDetailModal(GenDetailModal, POSProductDetails):
    pass


# ###########################################
# POSLog
class POSLogList(GenList):
    model = POSLog
    extra_context = {'menu': ['pos', 'poslog'], 'bread': [_('POS'), _('Log')]}
    default_ordering = '-pk'
    linkadd = False
    linkedit = False
    search_filter_button = True
