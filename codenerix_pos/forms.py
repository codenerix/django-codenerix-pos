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

from django import forms
from django.utils.translation import ugettext_lazy as _

from codenerix.forms import GenModelForm

from .models import POSZone, POSHardware, POS, POSSlot, POSPlant, POSProduct


class POSPlantForm(GenModelForm):
    class Meta:
        model = POSPlant
        exclude = []

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['corporate_image', 6],
                ['billing_series', 6],
                ['name', 6],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (
                _('Details'), 12,
                ['corporate_image', 6],
                ['billing_series', 6],
                ['name', 6],
            )
        ]
        return g


class POSZoneForm(GenModelForm):
    class Meta:
        model = POSZone
        exclude = []

    def __groups__(self):
        return [
            (
                _('Details'), 12,
                ['name', 6],
                ['plant', 6],
            )
        ]

    @staticmethod
    def __groups_details__():
        return [
            (
                _('Details'), 12,
                ['name', 6],
                ['plant', 6],
            )
        ]


class POSHardwareForm(GenModelForm):
    class Meta:
        model = POSHardware
        exclude = ['value']

    def __groups__(self):
        return [
            (
                _('Details'), 12,
                ['pos', 4],
                ['kind', 4],
                ['name', 4],
                ['enable', 6],
                ['config', 12],
            )
        ]

    @staticmethod
    def __groups_details__():
        return [
            (
                _('Details'), 12,
                ['pos', 6],
                ['kind', 6],
                ['name', 6],
                ['enable', 6],
                ['uuid', 6],
                ['config', 6],
                ['value', 6],
            )
        ]


class POSFormCreate(GenModelForm):
    key = forms.CharField(min_length=32, max_length=32, widget=forms.widgets.HiddenInput(), required=True)

    class Meta:
        model = POS
        exclude = ['payments', 'uuid']

    def __groups__(self):
        return [
            (
                _('Details'), 12,
                ['name', 3],
                ['zone', 3],
                ['hardware', 3],
            )
        ]


class POSForm(GenModelForm):
    key = forms.CharField(label=_("Key"), min_length=32, max_length=32, widget=forms.widgets.Input(), required=True)

    class Meta:
        model = POS
        exclude = ['payments', 'uuid']

    def __groups__(self):
        return [
            (
                _('Details'), 12,
                ['name', 4],
                ['key', 4],
                ['zone', 6],
                ['hardware', 6],
            )
        ]

    @staticmethod
    def __groups_details__():
        return [
            (
                _('Details'), 12,
                ['name', 6],
                ['uuid', 6],
                ['key', 6],
                ['zone', 6],
                ['hardware', 6],
                ['payments', 6],
            )
        ]


class POSSlotForm(GenModelForm):
    class Meta:
        model = POSSlot
        exclude = []

    def __groups__(self):
        return [
            (
                _('Details'), 12,
                ['zone', 6],
                ['name', 6],
            )
        ]

    @staticmethod
    def __groups_details__():
        return [
            (
                _('Details'), 12,
                ['zone', 6],
                ['name', 6],
                ['orders', 6],
                ['pos_x', 6],
                ['pos_y', 6],
            )
        ]


class POSProductForm(GenModelForm):
    class Meta:
        model = POSProduct
        exclude = []

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['pos', 6],
                ['product', 6],
                ['enable', 6],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (
                _('Details'), 12,
                ['pos', 6],
                ['product', 6],
                ['enable', 6],
            )
        ]
        return g
