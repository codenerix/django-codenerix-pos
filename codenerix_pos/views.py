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

from django.db.models import Q
from django.utils.translation import ugettext as _

from codenerix.views import GenList, GenCreate, GenCreateModal, GenUpdate, GenUpdateModal, GenDelete, GenDetail, GenDetailModal

from .models import POSZone, POSHardware, POS, POSSlot
from .forms import POSZoneForm, POSHardwareForm, POSForm, POSSlotForm


# ###########################################
# POSZone
class POSZoneList(GenList):
    model = POSZone
    extra_context = {'menu': ['pos', 'poszone'], 'bread': [_('POS'), _('POSZone'), ]}


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
    extra_context = {'menu': ['pos', 'poshardware'], 'bread': [_('POS'), _('POSHardware'), ]}


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
    extra_context = {'menu': ['pos', 'poshardware'], 'bread': [_('POS'), _('POSHardware'), ]}

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
    form_class = POSForm


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
    extra_context = {'menu': ['pos', 'posslot'], 'bread': [_('POS'), _('POSSlot'), ]}


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
    extra_context = {'menu': ['pos', 'posslot'], 'bread': [_('POS'), _('POSSlot'), ]}

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
