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

from codenerix_pos.models import POS


def get_POS(request):
    # Decide UUID
    uuid_pos = request.session.get('POS_client_UUID', None)
    if uuid_pos:
        pos = POS.objects.filter(uuid=uuid_pos).first()
    else:
        pos = None
        request.session['POS_client_UUID'] = None

    # Decide COMMIT
    commit = request.session.get('POS_client_COMMIT', None)
    if not commit:
        commit = None
        request.session['POS_client_COMMIT'] = None

    # Decide POS
    if pos:
        return {'uuid': str(pos.uuid), "POS": pos, "commit": commit}
    else:
        return {'uuid': '', "POS": None, "commit": commit}
