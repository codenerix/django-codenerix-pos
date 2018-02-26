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
import hashlib
import requests

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.db.models.fields import FieldDoesNotExist
from django.forms.utils import ErrorList
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import View
from django.db.models import Count
from django.conf import settings

from codenerix.views import GenList, GenCreate, GenCreateModal, GenUpdate, GenUpdateModal, GenDelete, GenDetail, GenDetailModal, GenForeignKey
from codenerix_extensions.views import GenCreateBridge, GenUpdateBridge

from .models import POSZone, POSHardware, POS, POSSlot, POSPlant, POSProduct, POSLog, POSOperator, POSGroupProduct
from .forms import POSZoneForm, POSHardwareForm, POSForm, POSSlotForm, POSPlantForm, POSProductForm, POSProductFormGroup, POSOperatorForm, POSGroupProductForm


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
    annotations = {
        'where': Count('poss'),
    }
    gentrans = {
        'warning_toomany': _('Too many POSs are using this hardware!'),
        'warning_toomany_total': _('Total POSs'),
        'warning_notused': _('No POS is using this hardware!'),
    }
    default_ordering = ["pos__name", "kind", "name"]

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
        fields.append(('where', None))
        return fields


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


class POSHardwareForeign(GenForeignKey):
    model = POSHardware
    label = '{pos__name} - {name} - {kind}'

    def get_foreign(self, queryset, search, filters):
        # Filter with search string
        qsobject = Q(name__icontains=search)
        qsobject = Q(uuid__icontains=search)
        qsobject = Q(key__icontains=search)
        qsobject = Q(pos__name__icontains=search)

        queryset = queryset.filter(qsobject)

        return queryset


class POSHardwareProfiles(GenForeignKey):
    model = POSHardware

    def get_label(self, pk):
        if pk == 'CONFIG':
            return _("Use config field")
        else:
            profiles = getattr(settings, 'POSHARDWARE_PROFILE', {})
            for kind in profiles:
                for hwkey in profiles[kind]:
                    if hwkey == pk:
                        name = profiles[kind][hwkey].get('name', None)
                        if name:
                            return name
                        else:
                            return pk

    def get(self, request, *args, **kwargs):
        # Build answer
        answer = [{'id': None, 'label': '---------'}]
        filterstxt = request.GET.get('filter', '{}')
        filters = json.loads(filterstxt)
        kind = filters.get('kind', None)
        # This will be the last option
        answer.append({'id': 'CONFIG', 'label': _('Use config field')})
        profiles = getattr(settings, 'POSHARDWARE_PROFILE', {}).get(kind, {})
        for key in profiles:
            answer.append({'id': key, 'label': profiles[key].get('name', key)})

        # Convert the answer to JSON
        json_answer = json.dumps({
            'clear': [],
            'rows': answer,
            'readonly': [],
        })

        # Return response
        return HttpResponse(json_answer, content_type='application/json')


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


class POSCommits(GenForeignKey):
    model = POS

    def get_label(self, pk):
        if pk == 'LATEST':
            return _("Latest configuration")
        else:
            return pk

    def get(self, request, *args, **kwargs):
        # Build answer
        answer = [{'id': None, 'label': '---------'}]

        # This will be the last option
        answer.append({'id': 'LATEST', 'label': _('Latest configuration')})

        # Get all hashes
        url = "https://api.github.com/repos/codenerix/django-codenerix-pos-client/commits"
        r = requests.get(url, params={})
        if not r.raise_for_status():
            # Read the answer$
            data = r.json()
            count = 0
            for commit in data:
                hashkey = commit.get('sha', None)
                if hashkey:
                    answer.append({'id': hashkey, 'label': hashkey})
                    count += 1
                    if count == 10:
                        break

        # Add one last option saying it has more
        if len(data) > 10:
            answer.append({'id': None, 'label': '...'})

        # Convert the answer to JSON
        json_answer = json.dumps({
            'clear': [],
            'rows': answer,
            'readonly': [],
        })

        # Return response
        return HttpResponse(json_answer, content_type='application/json')


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


class POSSlotForeign(GenForeignKey):
    model = POSSlot
    label = '{name}'

    def get_foreign(self, queryset, search, filters):
        # Filter with search string
        qsobject = Q(name__icontains=search)

        queryset = queryset.filter(qsobject)

        slot = filters.get('slot', None)

        if slot:
            queryset = queryset.filter(
                Q(zone__poss__pk=slot)
            )

        return queryset


# ###########################################
# POSProduct
class POSProductList(GenList):
    model = POSProduct
    extra_context = {'menu': ['pos', 'posproduct'], 'bread': [_('POS'), _('Product')]}
    default_ordering = ["group_product__name", ]


class POSProductCreate(GenCreate):
    model = POSProduct
    form_class = POSProductForm


class POSProductCreateModal(GenCreateModal, POSProductCreate):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__group_pk = kwargs.get('pk', None)
        if self.__group_pk:
            self.form_class = POSProductFormGroup
        return super(POSProductCreateModal, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.__group_pk:
            group_product = POSGroupProduct.objects.get(pk=self.__group_pk)
            form.instance.group_product = group_product

        try:
            with transaction.atomic():
                result = super(POSProductCreateModal, self).form_valid(form)
        except IntegrityError as e:
            errors = form._errors.setdefault("product_final", ErrorList())
            errors.append(e)
            return self.form_invalid(form)
        return result


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
        limit['link'] = Q(group_product__pk=pk)
        return limit

    def __fields__(self, info):
        fields = []
        fields.append(('product_final', _("Product")))
        fields.append(('enable', _("Enable")))
        return fields


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


# ###########################################
# POSOperator
class POSOperatorList(GenList):
    model = POSOperator
    extra_context = {'menu': ['people', 'POSOperator'], 'bread': [_('People'), _('POSOperator')]}


class POSOperatorCreate(GenCreate, GenCreateBridge):
    model = POSOperator
    form_class = POSOperatorForm

    def form_valid(self, form):
        field = 'codenerix_external_field'
        model = POSOperator
        related_field = 'pos_operator'
        error_message = [
            _("The selected entry is already a operator, select another entry!"),
            _("The selected entry is not available anymore, please, try again!")
        ]

        external = self.request.POST.get('codenerix_external_field', None)
        password1 = self.request.POST.get('password1', None)
        password2 = self.request.POST.get('password2', None)
        if external is None:
            errors = form._errors.setdefault("codenerix_external_field", ErrorList())
            errors.append(_("Not related to a user"))
            return super(POSOperatorCreate, self).form_invalid(form)
        else:
            model_tmp = None
            for related in self.model._meta.related_objects:
                related_model = related.related_model
                try:
                    if related_model._meta.get_field('pos_operator'):
                        model_tmp = related_model
                        break
                except FieldDoesNotExist:
                    pass
            if model_tmp:
                operator = model_tmp.objects.filter(pk=external).first()
                if operator is None or operator.user is None:
                    errors = form._errors.setdefault("codenerix_external_field", ErrorList())
                    errors.append(_("Not related to a user"))
                    return super(POSOperatorCreate, self).form_invalid(form)
            else:
                errors = form._errors.setdefault("codenerix_external_field", ErrorList())
                errors.append(_("Not related to a user"))
                return super(POSOperatorCreate, self).form_invalid(form)

        if password1 is None or password2 is None:
            errors = form._errors.setdefault("password1", ErrorList())
            errors.append(_("Passwords required"))
            return super(POSOperatorCreate, self).form_invalid(form)
        if password1 != password2:
            errors = form._errors.setdefault("password1", ErrorList())
            errors.append(_("Passwords do not match"))
            return super(POSOperatorCreate, self).form_invalid(form)

        try:
            # python 2.7
            operator.user.last_name = hashlib.sha1(password1.encode()).hexdigest()[:30]
        except TypeError:
            # python 3.x
            password1_str = bytes(password1, encoding='utf-8')
            operator.user.last_name = hashlib.sha1(password1_str.encode()).hexdigest()[:30]
        operator.user.save()
        return self.form_valid_bridge(form, field, model, related_field, error_message)


class POSOperatorCreateModal(GenCreateModal, POSOperatorCreate):
    pass


class POSOperatorUpdate(GenUpdate, GenUpdateBridge):
    model = POSOperator
    form_class = POSOperatorForm

    def get_form(self, form_class=None):
        form = super(POSOperatorUpdate, self).get_form(form_class)
        # initial external field
        form.fields['codenerix_external_field'].initial = form.instance.external
        return form

    def form_valid(self, form):
        field = 'codenerix_external_field'
        model = POSOperator
        related_field = 'pos_operator'
        error_message = [
            _("The selected entry is not available anymore, please, try again!")
        ]
        external = self.request.POST.get('codenerix_external_field', None)
        password1 = self.request.POST.get('password1', None)
        password2 = self.request.POST.get('password2', None)

        if external is None:
            errors = form._errors.setdefault("codenerix_external_field", ErrorList())
            errors.append(_("Not related to a user"))
            return super(POSOperatorUpdate, self).form_invalid(form)
        else:
            model_tmp = None
            for related in self.model._meta.related_objects:
                related_model = related.related_model
                try:
                    if related_model._meta.get_field('pos_operator'):
                        model_tmp = related_model
                        break
                except FieldDoesNotExist:
                    pass
            if model_tmp:
                operator = model_tmp.objects.filter(pk=external).first()
                if operator is None or operator.user is None:
                    errors = form._errors.setdefault("codenerix_external_field", ErrorList())
                    errors.append(_("Not related to a user"))
                    return super(POSOperatorUpdate, self).form_invalid(form)
            else:
                errors = form._errors.setdefault("codenerix_external_field", ErrorList())
                errors.append(_("Not related to a user"))
                return super(POSOperatorUpdate, self).form_invalid(form)

        if password1 != password2:
            errors = form._errors.setdefault("password1", ErrorList())
            errors.append(_("Passwords do not match"))
            return super(POSOperatorUpdate, self).form_invalid(form)

        if password1:
            operator.user.last_name = hashlib.sha1(password1.encode()).hexdigest()[:30]
            operator.user.save()
        return self.form_valid_bridge(form, field, model, related_field, error_message)


class POSOperatorUpdateModal(GenUpdateModal, POSOperatorUpdate):
    pass


class POSOperatorDelete(GenDelete):
    model = POSOperator


class POSOperatorSubList(GenList):
    model = POSOperator
    extra_context = {'menu': ['people', 'POSOperator'], 'bread': [_('People'), _('POSOperator')]}

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(person__pk=pk)
        return limit


class POSOperatorDetails(GenDetail):
    model = POSOperator
    groups = POSOperatorForm.__groups_details__()


class POSOperatorDetailModal(GenDetailModal, POSOperatorDetails):
    pass


class POSSession(View):
    def post(self, request, *args, **kwargs):
        context = {}
        old_uuid = self.request.session.get('POS_client_UUID', None)
        new_uuid = request.POST.get('uuid', None)
        commit = request.POST.get('commit', None)

        if old_uuid and new_uuid and old_uuid != new_uuid:
            context['msg'] = 'KO'
            context['txt'] = 'UUID changed. {} => {}'.format(old_uuid, new_uuid)
        else:
            context['msg'] = 'OK'
            context['posname'] = ''
            context['commit'] = commit
            if new_uuid:
                pos = POS.objects.filter(uuid=new_uuid).first()
                if pos:
                    context['posname'] = pos.name

        request.session['POS_client_UUID'] = new_uuid
        request.session['POS_client_COMMIT'] = commit
        json_answer = json.dumps(context)
        return HttpResponse(json_answer, content_type='application/json')


# ###########################################
# POSGroupProduct
class POSGroupProductList(GenList):
    model = POSGroupProduct
    show_details = True
    extra_context = {'menu': ['pos', 'posgroupproduct'], 'bread': [_('POS'), _('POSGroupProduct')]}


class POSGroupProductCreate(GenCreate):
    model = POSGroupProduct
    form_class = POSGroupProductForm


class POSGroupProductCreateModal(GenCreateModal, POSGroupProductCreate):
    pass


class POSGroupProductUpdate(GenUpdate):
    model = POSGroupProduct
    form_class = POSGroupProductForm


class POSGroupProductUpdateModal(GenUpdateModal, POSGroupProductUpdate):
    pass


class POSGroupProductDelete(GenDelete):
    model = POSGroupProduct


class POSGroupProductSubList(GenList):
    model = POSGroupProduct
    show_details = False
    extra_context = {'menu': ['pos', 'POSGroupProduct'], 'bread': [_('POS'), _('POSGroupProduct')]}

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(xxxxxxx__pk=pk)
        return limit


class POSGroupProductDetails(GenDetail):
    model = POSGroupProduct
    groups = POSGroupProductForm.__groups_details__()
    tabs = [
        {'id': 'products', 'name': _('Products'), 'ws': 'CDNX_posproducts_sublist', 'rows': 'base'},
    ]


class POSGroupProductDetailModal(GenDetailModal, POSGroupProductDetails):
    pass
