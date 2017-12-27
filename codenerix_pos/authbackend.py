# -*- coding: utf-8 -*-
import hashlib
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User  # , Group
from django.contrib.auth import authenticate, login
from codenerix_pos.models import POS


class POSAuth(ModelBackend):
    '''
    Authentication system based on a Token key
    '''

    def authenticate(self, request=None, username=None, pincode=None, PointOfSales=None):
        try:
            # Get the requested username
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user and user.last_name == hashlib.sha1(pincode.encode()).hexdigest()[:30] and POS.objects.filter(pos_operators__enable=True, pos_operators__external__user=user):
            answer = user
        else:

            # Username not found, not accepting the authentication request
            answer = None

        # Return answer
        return answer
