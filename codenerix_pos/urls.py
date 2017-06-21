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

from django.conf.urls import url
from .views import POSList, POSCreate, POSCreateModal, POSDetails, POSDetailsModal, POSUpdate, POSUpdateModal, POSDelete
from .views import POSSlotList, POSSlotCreate, POSSlotCreateModal, POSSlotDetails, POSSlotDetailsModal, POSSlotUpdate, POSSlotUpdateModal, POSSlotDelete

urlpatterns = [
    url(r'^poss$', POSList.as_view(), name='CDNX_pos_list'),
    url(r'^poss/add$', POSCreate.as_view(), name='CDNX_pos_add'),
    url(r'^poss/addmodal$', POSCreateModal.as_view(), name='CDNX_pos_addmodal'),
    url(r'^poss/(?P<pk>\w+)$', POSDetails.as_view(), name='CDNX_pos_details'),
    url(r'^poss/(?P<pk>\w+)/modal$', POSDetailsModal.as_view(), name='CDNX_pos_details'),
    url(r'^poss/(?P<pk>\w+)/edit$', POSUpdate.as_view(), name='CDNX_pos_edit'),
    url(r'^poss/(?P<pk>\w+)/editmodal$', POSUpdateModal.as_view(), name='CDNX_pos_editmodal'),
    url(r'^poss/(?P<pk>\w+)/delete$', POSDelete.as_view(), name='CDNX_pos_delete'),
    
    url(r'^posslots$', POSSlotList.as_view(), name='CDNX_posslot_list'),
    url(r'^posslots/add$', POSSlotCreate.as_view(), name='CDNX_posslot_add'),
    url(r'^posslots/addmodal$', POSSlotCreateModal.as_view(), name='CDNX_posslot_addmodal'),
    url(r'^posslots/(?P<pk>\w+)$', POSSlotDetails.as_view(), name='CDNX_posslot_details'),
    url(r'^posslots/(?P<pk>\w+)/modal$', POSSlotDetailsModal.as_view(), name='CDNX_posslot_details'),
    url(r'^posslots/(?P<pk>\w+)/edit$', POSSlotUpdate.as_view(), name='CDNX_posslot_edit'),
    url(r'^posslots/(?P<pk>\w+)/editmodal$', POSSlotUpdateModal.as_view(), name='CDNX_posslot_editmodal'),
    url(r'^posslots/(?P<pk>\w+)/delete$', POSSlotDelete.as_view(), name='CDNX_posslot_delete'),

]
