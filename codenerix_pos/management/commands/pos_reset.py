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


from django.core.management.base import BaseCommand

from codenerix.lib.debugger import Debugger
from codenerix_pos.models import POS


class Command(BaseCommand, Debugger):

    # Show this when the user types help
    help = "Reset all channels from CODENERIX POS"

    def handle(self, *args, **options):

        # Autoconfigure Debugger
        self.set_name("CODENERIX-POS")
        self.set_debug()
        self.debug("Resetting POS:", color='blue')

        # Get all users from the system
        for pos in POS.objects.filter(channel__isnull=False):
            self.debug("    - {}: {}".format(pos.name, pos.uuid), color='yellow')
            pos.reset_client()
            pos.channel = None
            pos.save()
