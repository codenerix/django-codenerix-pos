# -*- coding: utf-8 -*-
#
# django-codenerix-pos
#
# Codenerix GNU
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

from django.urls import re_path as url
from django.views.generic import TemplateView

from .views import POSZoneList, POSZoneCreate, POSZoneCreateModal, POSZoneUpdate, POSZoneUpdateModal, POSZoneDelete, POSZoneDetails
from .views import POSHardwareList, POSHardwareCreate, POSHardwareCreateModal, POSHardwareUpdate, POSHardwareUpdateModal, POSHardwareDelete, POSHardwareSubList, POSHardwareDetails, POSHardwareDetailModal
from .views import POSHardwareForeign, POSHardwareProfiles
from .views import POSList, POSCreate, POSCreateModal, POSUpdate, POSUpdateModal, POSDelete, POSSubList, POSDetails, POSDetailModal, POSCommits
from .views import POSSlotList, POSSlotCreate, POSSlotCreateModal, POSSlotUpdate, POSSlotUpdateModal, POSSlotDelete, POSSlotSubList, POSSlotDetails, POSSlotDetailModal
from .views import POSPlantList, POSPlantCreate, POSPlantCreateModal, POSPlantUpdate, POSPlantUpdateModal, POSPlantDelete, POSPlantDetails
from .views import POSProductList, POSProductCreate, POSProductCreateModal, POSProductUpdate, POSProductUpdateModal, POSProductDelete, POSProductSubList, POSProductDetails, POSProductDetailModal
from .views import POSLogList
from .views import POSOperatorList, POSOperatorCreate, POSOperatorCreateModal, POSOperatorUpdate, POSOperatorUpdateModal, POSOperatorDelete, POSOperatorSubList, POSOperatorDetails, POSOperatorDetailModal
from .views import POSSession
from .views import POSGroupProductList, POSGroupProductCreate, POSGroupProductCreateModal, POSGroupProductUpdate, POSGroupProductUpdateModal, POSGroupProductDelete, POSGroupProductSubList, POSGroupProductDetails, POSGroupProductDetailModal
from .views import POSSlotForeign
from .views import OpenCashRegister


class ExampleView(TemplateView):

    template_name = "codenerix_pos/example.html"

    def get_context_data(self, **kwargs):
        context = super(ExampleView, self).get_context_data(**kwargs)
        context['url'] = self.request.META.get("HTTP_HOST")
        return context


urlpatterns = [
    url(r'^example$', ExampleView.as_view(), name='CDNX_pos_example'),

    url(r'^posplants$', POSPlantList.as_view(), name='CDNX_posplants_list'),
    url(r'^posplants/add$', POSPlantCreate.as_view(), name='CDNX_posplants_add'),
    url(r'^posplants/addmodal$', POSPlantCreateModal.as_view(), name='CDNX_posplants_addmodal'),
    url(r'^posplants/(?P<pk>\w+)$', POSPlantDetails.as_view(), name='CDNX_posplants_details'),
    url(r'^posplants/(?P<pk>\w+)/edit$', POSPlantUpdate.as_view(), name='CDNX_posplants_edit'),
    url(r'^posplants/(?P<pk>\w+)/editmodal$', POSPlantUpdateModal.as_view(), name='CDNX_posplants_editmodal'),
    url(r'^posplants/(?P<pk>\w+)/delete$', POSPlantDelete.as_view(), name='CDNX_posplants_delete'),


    url(r'^poszones$', POSZoneList.as_view(), name='CDNX_poszones_list'),
    url(r'^poszones/add$', POSZoneCreate.as_view(), name='CDNX_poszones_add'),
    url(r'^poszones/addmodal$', POSZoneCreateModal.as_view(), name='CDNX_poszones_addmodal'),
    url(r'^poszones/(?P<pk>\w+)$', POSZoneDetails.as_view(), name='CDNX_poszones_details'),
    url(r'^poszones/(?P<pk>\w+)/edit$', POSZoneUpdate.as_view(), name='CDNX_poszones_edit'),
    url(r'^poszones/(?P<pk>\w+)/editmodal$', POSZoneUpdateModal.as_view(), name='CDNX_poszones_editmodal'),
    url(r'^poszones/(?P<pk>\w+)/delete$', POSZoneDelete.as_view(), name='CDNX_poszones_delete'),


    url(r'^poshardwares$', POSHardwareList.as_view(), name='CDNX_poshardwares_list'),
    url(r'^poshardwares/add$', POSHardwareCreate.as_view(), name='CDNX_poshardwares_add'),
    url(r'^poshardwares/addmodal$', POSHardwareCreateModal.as_view(), name='CDNX_poshardwares_addmodal'),
    url(r'^poshardwares/(?P<pk>\w+)$', POSHardwareDetails.as_view(), name='CDNX_poshardwares_details'),
    url(r'^poshardwares/(?P<pk>\w+)/edit$', POSHardwareUpdate.as_view(), name='CDNX_poshardwares_edit'),
    url(r'^poshardwares/(?P<pk>\w+)/editmodal$', POSHardwareUpdateModal.as_view(), name='CDNX_poshardwares_editmodal'),
    url(r'^poshardwares/(?P<pk>\w+)/delete$', POSHardwareDelete.as_view(), name='CDNX_poshardwares_delete'),
    url(r'^poshardwares/(?P<pk>\w+)/sublist$', POSHardwareSubList.as_view(), name='CDNX_poshardwares_sublist'),
    url(r'^poshardwares/(?P<pk>\w+)/sublist/add$', POSHardwareCreateModal.as_view(), name='CDNX_poshardwares_sublist_add'),
    url(r'^poshardwares/(?P<pk>\w+)/sublist/addmodal$', POSHardwareCreateModal.as_view(), name='CDNX_poshardwares_sublist_addmodal'),
    url(r'^poshardwares/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', POSHardwareDetailModal.as_view(), name='CDNX_poshardwares_sublist_details'),
    url(r'^poshardwares/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', POSHardwareUpdateModal.as_view(), name='CDNX_poshardwares_sublist_edit'),
    url(r'^poshardwares/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', POSHardwareUpdateModal.as_view(), name='CDNX_poshardwares_sublist_editmodal'),
    url(r'^poshardwares/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', POSHardwareDelete.as_view(), name='CDNX_poshardwares_sublist_delete'),
    url(r'^poshardwares/foreign/(?P<search>[\w\W]+|\*)$', POSHardwareForeign.as_view(), name='CDNX_poshardwares_foreign'),
    url(r'^poshardwares/profiles/(?P<search>[\w\W]+|\*)$', POSHardwareProfiles.as_view(), name='CDNX_poshardwares_profiles'),


    url(r'^poss$', POSList.as_view(), name='CDNX_poss_list'),
    url(r'^poss/add$', POSCreate.as_view(), name='CDNX_poss_add'),
    url(r'^poss/addmodal$', POSCreateModal.as_view(), name='CDNX_poss_addmodal'),
    url(r'^poss/(?P<pk>\w+)$', POSDetails.as_view(), name='CDNX_poss_details'),
    url(r'^poss/(?P<pk>\w+)/edit$', POSUpdate.as_view(), name='CDNX_poss_edit'),
    url(r'^poss/(?P<pk>\w+)/editmodal$', POSUpdateModal.as_view(), name='CDNX_poss_editmodal'),
    url(r'^poss/(?P<pk>\w+)/delete$', POSDelete.as_view(), name='CDNX_poss_delete'),
    url(r'^poss/(?P<pk>\w+)/sublist$', POSSubList.as_view(), name='CDNX_poss_sublist'),
    url(r'^poss/(?P<pk>\w+)/sublist/add$', POSCreateModal.as_view(), name='CDNX_poss_sublist_add'),
    url(r'^poss/(?P<pk>\w+)/sublist/addmodal$', POSCreateModal.as_view(), name='CDNX_poss_sublist_addmodal'),
    url(r'^poss/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', POSDetailModal.as_view(), name='CDNX_poss_sublist_details'),
    url(r'^poss/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', POSUpdateModal.as_view(), name='CDNX_poss_sublist_edit'),
    url(r'^poss/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', POSUpdateModal.as_view(), name='CDNX_poss_sublist_editmodal'),
    url(r'^poss/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', POSDelete.as_view(), name='CDNX_poss_sublist_delete'),
    url(r'^poss/commits/(?P<search>[\w\W]+|\*)$', POSCommits.as_view(), name='CDNX_poss_commits'),


    url(r'^posslots$', POSSlotList.as_view(), name='CDNX_posslots_list'),
    url(r'^posslots/add$', POSSlotCreate.as_view(), name='CDNX_posslots_add'),
    url(r'^posslots/addmodal$', POSSlotCreateModal.as_view(), name='CDNX_posslots_addmodal'),
    url(r'^posslots/(?P<pk>\w+)$', POSSlotDetails.as_view(), name='CDNX_posslots_details'),
    url(r'^posslots/(?P<pk>\w+)/edit$', POSSlotUpdate.as_view(), name='CDNX_posslots_edit'),
    url(r'^posslots/(?P<pk>\w+)/editmodal$', POSSlotUpdateModal.as_view(), name='CDNX_posslots_editmodal'),
    url(r'^posslots/(?P<pk>\w+)/delete$', POSSlotDelete.as_view(), name='CDNX_posslots_delete'),
    url(r'^posslots/(?P<pk>\w+)/sublist$', POSSlotSubList.as_view(), name='CDNX_posslots_sublist'),
    url(r'^posslots/(?P<pk>\w+)/sublist/add$', POSSlotCreateModal.as_view(), name='CDNX_posslots_sublist_add'),
    url(r'^posslots/(?P<pk>\w+)/sublist/addmodal$', POSSlotCreateModal.as_view(), name='CDNX_posslots_sublist_addmodal'),
    url(r'^posslots/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', POSSlotDetailModal.as_view(), name='CDNX_posslots_sublist_details'),
    url(r'^posslots/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', POSSlotUpdateModal.as_view(), name='CDNX_posslots_sublist_edit'),
    url(r'^posslots/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', POSSlotUpdateModal.as_view(), name='CDNX_posslots_sublist_editmodal'),
    url(r'^posslots/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', POSSlotDelete.as_view(), name='CDNX_posslots_sublist_delete'),
    url(r'^posslots/foreign/(?P<search>[\w\W]+|\*)$', POSSlotForeign.as_view(), name='CDNX_posslots_foreign'),

    url(r'^posproducts$', POSProductList.as_view(), name='CDNX_posproducts_list'),
    url(r'^posproducts/add$', POSProductCreate.as_view(), name='CDNX_posproducts_add'),
    url(r'^posproducts/addmodal$', POSProductCreateModal.as_view(), name='CDNX_posproducts_addmodal'),
    url(r'^posproducts/(?P<pk>\w+)$', POSProductDetails.as_view(), name='CDNX_posproducts_details'),
    url(r'^posproducts/(?P<pk>\w+)/edit$', POSProductUpdate.as_view(), name='CDNX_posproducts_edit'),
    url(r'^posproducts/(?P<pk>\w+)/editmodal$', POSProductUpdateModal.as_view(), name='CDNX_posproducts_editmodal'),
    url(r'^posproducts/(?P<pk>\w+)/delete$', POSProductDelete.as_view(), name='CDNX_posproducts_delete'),
    url(r'^posproducts/(?P<pk>\w+)/sublist$', POSProductSubList.as_view(), name='CDNX_posproducts_sublist'),
    url(r'^posproducts/(?P<pk>\w+)/sublist/add$', POSProductCreateModal.as_view(), name='CDNX_posproducts_sublist_add'),
    url(r'^posproducts/(?P<pk>\w+)/sublist/addmodal$', POSProductCreateModal.as_view(), name='CDNX_posproducts_sublist_addmodal'),
    url(r'^posproducts/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', POSProductDetailModal.as_view(), name='CDNX_posproducts_sublist_details'),
    url(r'^posproducts/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', POSProductUpdateModal.as_view(), name='CDNX_posproducts_sublist_edit'),
    url(r'^posproducts/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', POSProductUpdateModal.as_view(), name='CDNX_posproducts_sublist_editmodal'),
    url(r'^posproducts/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', POSProductDelete.as_view(), name='CDNX_posproducts_sublist_delete'),

    url(r'^poslogs$', POSLogList.as_view(), name='CDNX_poslogs_list'),

    url(r'^posoperators$', POSOperatorList.as_view(), name='CDNX_posoperators_list'),
    url(r'^posoperators/add$', POSOperatorCreate.as_view(), name='CDNX_posoperators_add'),
    url(r'^posoperators/addmodal$', POSOperatorCreateModal.as_view(), name='CDNX_posoperators_addmodal'),
    url(r'^posoperators/(?P<pk>\w+)$', POSOperatorDetails.as_view(), name='CDNX_posoperators_details'),
    url(r'^posoperators/(?P<pk>\w+)/edit$', POSOperatorUpdate.as_view(), name='CDNX_posoperators_edit'),
    url(r'^posoperators/(?P<pk>\w+)/editmodal$', POSOperatorUpdateModal.as_view(), name='CDNX_posoperators_editmodal'),
    url(r'^posoperators/(?P<pk>\w+)/delete$', POSOperatorDelete.as_view(), name='CDNX_posoperators_delete'),
    url(r'^posoperators/(?P<pk>\w+)/sublist$', POSOperatorSubList.as_view(), name='CDNX_posoperators_sublist'),
    url(r'^posoperators/(?P<pk>\w+)/sublist/add$', POSOperatorCreateModal.as_view(), name='CDNX_posoperators_sublist_add'),
    url(r'^posoperators/(?P<pk>\w+)/sublist/addmodal$', POSOperatorCreateModal.as_view(), name='CDNX_posoperators_sublist_addmodal'),
    url(r'^posoperators/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', POSOperatorDetailModal.as_view(), name='CDNX_posoperators_sublist_details'),
    url(r'^posoperators/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', POSOperatorUpdateModal.as_view(), name='CDNX_posoperators_sublist_edit'),
    url(r'^posoperators/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', POSOperatorUpdateModal.as_view(), name='CDNX_posoperators_sublist_editmodal'),
    url(r'^posoperators/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', POSOperatorDelete.as_view(), name='CDNX_posoperators_sublist_delete'),

    url(r'^pos_session$', POSSession.as_view(), name='CDNX_pos_session'),


    # POSGroupProduct
    url(r'^posgroupproducts$', POSGroupProductList.as_view(), name='CDNX_posgroupproducts_list'),
    url(r'^posgroupproducts/add$', POSGroupProductCreate.as_view(), name='CDNX_posgroupproducts_add'),
    url(r'^posgroupproducts/addmodal$', POSGroupProductCreateModal.as_view(), name='CDNX_posgroupproducts_addmodal'),
    url(r'^posgroupproducts/(?P<pk>\w+)$', POSGroupProductDetails.as_view(), name='CDNX_posgroupproducts_details'),
    url(r'^posgroupproducts/(?P<pk>\w+)/edit$', POSGroupProductUpdate.as_view(), name='CDNX_posgroupproducts_edit'),
    url(r'^posgroupproducts/(?P<pk>\w+)/editmodal$', POSGroupProductUpdateModal.as_view(), name='CDNX_posgroupproducts_editmodal'),
    url(r'^posgroupproducts/(?P<pk>\w+)/delete$', POSGroupProductDelete.as_view(), name='CDNX_posgroupproducts_delete'),
    url(r'^posgroupproducts/(?P<pk>\w+)/sublist$', POSGroupProductSubList.as_view(), name='CDNX_posgroupproducts_sublist'),
    url(r'^posgroupproducts/(?P<pk>\w+)/sublist/add$', POSGroupProductCreateModal.as_view(), name='CDNX_posgroupproducts_sublist_add'),
    url(r'^posgroupproducts/(?P<pk>\w+)/sublist/addmodal$', POSGroupProductCreateModal.as_view(), name='CDNX_posgroupproducts_sublist_addmodal'),
    url(r'^posgroupproducts/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', POSGroupProductDetailModal.as_view(), name='CDNX_posgroupproducts_sublist_details'),
    url(r'^posgroupproducts/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', POSGroupProductUpdateModal.as_view(), name='CDNX_posgroupproducts_sublist_edit'),
    url(r'^posgroupproducts/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', POSGroupProductUpdateModal.as_view(), name='CDNX_posgroupproducts_sublist_editmodal'),
    url(r'^posgroupproducts/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', POSGroupProductDelete.as_view(), name='CDNX_posgroupproducts_sublist_delete'),

    # Utilities
    url(r'^open_cash_register$', OpenCashRegister.as_view(), name='CDNX_POS_open_cash_register'),
    url(r'^open_cash_register/$', OpenCashRegister.as_view(), name='CDNX_POS_open_cash_register_'),
]
