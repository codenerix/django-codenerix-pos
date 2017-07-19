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
from django.views.generic import TemplateView

from .views import POSZoneList, POSZoneCreate, POSZoneCreateModal, POSZoneUpdate, POSZoneUpdateModal, POSZoneDelete, POSZoneDetails
from .views import POSHardwareList, POSHardwareCreate, POSHardwareCreateModal, POSHardwareUpdate, POSHardwareUpdateModal, POSHardwareDelete, POSHardwareSubList, POSHardwareDetails, POSHardwareDetailModal
from .views import POSList, POSCreate, POSCreateModal, POSUpdate, POSUpdateModal, POSDelete, POSSubList, POSDetails, POSDetailModal
from .views import POSSlotList, POSSlotCreate, POSSlotCreateModal, POSSlotUpdate, POSSlotUpdateModal, POSSlotDelete, POSSlotSubList, POSSlotDetails, POSSlotDetailModal


urlpatterns = [
    url(r'^example$', TemplateView.as_view(template_name='codenerix_pos/example.html'), name='CDNX_pos_example'),
    
    url(r'^poszones$', POSZoneList.as_view(), name='poszones_list'),
    url(r'^poszones/add$', POSZoneCreate.as_view(), name='poszones_add'),
    url(r'^poszones/addmodal$', POSZoneCreateModal.as_view(), name='poszones_addmodal'),
    url(r'^poszones/(?P<pk>\w+)$', POSZoneDetails.as_view(), name='poszones_details'),
    url(r'^poszones/(?P<pk>\w+)/edit$', POSZoneUpdate.as_view(), name='poszones_edit'),
    url(r'^poszones/(?P<pk>\w+)/editmodal$', POSZoneUpdateModal.as_view(), name='poszones_editmodal'),
    url(r'^poszones/(?P<pk>\w+)/delete$', POSZoneDelete.as_view(), name='poszones_delete'),


    url(r'^poshardwares$', POSHardwareList.as_view(), name='poshardwares_list'),
    url(r'^poshardwares/add$', POSHardwareCreate.as_view(), name='poshardwares_add'),
    url(r'^poshardwares/addmodal$', POSHardwareCreateModal.as_view(), name='poshardwares_addmodal'),
    url(r'^poshardwares/(?P<pk>\w+)$', POSHardwareDetails.as_view(), name='poshardwares_details'),
    url(r'^poshardwares/(?P<pk>\w+)/edit$', POSHardwareUpdate.as_view(), name='poshardwares_edit'),
    url(r'^poshardwares/(?P<pk>\w+)/editmodal$', POSHardwareUpdateModal.as_view(), name='poshardwares_editmodal'),
    url(r'^poshardwares/(?P<pk>\w+)/delete$', POSHardwareDelete.as_view(), name='poshardwares_delete'),
    url(r'^poshardwares/(?P<pk>\w+)/sublist$', POSHardwareSubList.as_view(), name='poshardwares_sublist'),
    url(r'^poshardwares/(?P<pk>\w+)/sublist/add$', POSHardwareCreateModal.as_view(), name='poshardwares_sublist_add'),
    url(r'^poshardwares/(?P<pk>\w+)/sublist/addmodal$', POSHardwareCreateModal.as_view(), name='poshardwares_sublist_addmodal'),
    url(r'^poshardwares/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', POSHardwareDetailModal.as_view(), name='poshardwares_sublist_details'),
    url(r'^poshardwares/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', POSHardwareUpdateModal.as_view(), name='poshardwares_sublist_edit'),
    url(r'^poshardwares/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', POSHardwareUpdateModal.as_view(), name='poshardwares_sublist_editmodal'),
    url(r'^poshardwares/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', POSHardwareDelete.as_view(), name='poshardwares_sublist_delete'),


    url(r'^poss$', POSList.as_view(), name='poss_list'),
    url(r'^poss/add$', POSCreate.as_view(), name='poss_add'),
    url(r'^poss/addmodal$', POSCreateModal.as_view(), name='poss_addmodal'),
    url(r'^poss/(?P<pk>\w+)$', POSDetails.as_view(), name='poss_details'),
    url(r'^poss/(?P<pk>\w+)/edit$', POSUpdate.as_view(), name='poss_edit'),
    url(r'^poss/(?P<pk>\w+)/editmodal$', POSUpdateModal.as_view(), name='poss_editmodal'),
    url(r'^poss/(?P<pk>\w+)/delete$', POSDelete.as_view(), name='poss_delete'),
    url(r'^poss/(?P<pk>\w+)/sublist$', POSSubList.as_view(), name='poss_sublist'),
    url(r'^poss/(?P<pk>\w+)/sublist/add$', POSCreateModal.as_view(), name='poss_sublist_add'),
    url(r'^poss/(?P<pk>\w+)/sublist/addmodal$', POSCreateModal.as_view(), name='poss_sublist_addmodal'),
    url(r'^poss/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', POSDetailModal.as_view(), name='poss_sublist_details'),
    url(r'^poss/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', POSUpdateModal.as_view(), name='poss_sublist_edit'),
    url(r'^poss/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', POSUpdateModal.as_view(), name='poss_sublist_editmodal'),
    url(r'^poss/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', POSDelete.as_view(), name='poss_sublist_delete'),


    url(r'^posslots$', POSSlotList.as_view(), name='posslots_list'),
    url(r'^posslots/add$', POSSlotCreate.as_view(), name='posslots_add'),
    url(r'^posslots/addmodal$', POSSlotCreateModal.as_view(), name='posslots_addmodal'),
    url(r'^posslots/(?P<pk>\w+)$', POSSlotDetails.as_view(), name='posslots_details'),
    url(r'^posslots/(?P<pk>\w+)/edit$', POSSlotUpdate.as_view(), name='posslots_edit'),
    url(r'^posslots/(?P<pk>\w+)/editmodal$', POSSlotUpdateModal.as_view(), name='posslots_editmodal'),
    url(r'^posslots/(?P<pk>\w+)/delete$', POSSlotDelete.as_view(), name='posslots_delete'),
    url(r'^posslots/(?P<pk>\w+)/sublist$', POSSlotSubList.as_view(), name='posslots_sublist'),
    url(r'^posslots/(?P<pk>\w+)/sublist/add$', POSSlotCreateModal.as_view(), name='posslots_sublist_add'),
    url(r'^posslots/(?P<pk>\w+)/sublist/addmodal$', POSSlotCreateModal.as_view(), name='posslots_sublist_addmodal'),
    url(r'^posslots/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', POSSlotDetailModal.as_view(), name='posslots_sublist_details'),
    url(r'^posslots/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', POSSlotUpdateModal.as_view(), name='posslots_sublist_edit'),
    url(r'^posslots/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', POSSlotUpdateModal.as_view(), name='posslots_sublist_editmodal'),
    url(r'^posslots/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', POSSlotDelete.as_view(), name='posslots_sublist_delete'),

]
