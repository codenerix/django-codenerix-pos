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

    def authenticate(self, username=None, token=None, PointOfSales=None):
        try:
            # Get the requested username
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user and user.last_name == hashlib.sha1(token).hexdigest()[:30] and POS.objects.filter(pos_operators__enable=True, pos_operators__external__user=user):
            answer = user
        else:

            # Username not found, not accepting the authentication request
            answer = None

        # Return answer
        return answer


class POSAuthMiddleware(object):
    def __init__(self, get_response=None):
        self.get_response = get_response

    def process_request(self, request):
        # By default we are not in authtoken
        request.authtoken = False
        # Get body
        # body = request.body
        # Get token
        token = request.GET.get("passwd", request.POST.get("passwd", ""))
        # If the user is authenticated and shouldn't be
        if token:
            username = request.GET.get("username", request.POST.get("username", None))
            POS = request.GET.get("POS", request.POST.get("POS", None))
            # json = request.GET.get("json", request.POST.get("json", body))
            # Authenticate user
            user = authenticate(username=username, token=token, PointOfSales=POS)
            
            if user:
                # Set we are in authtoken
                request.authtoken = True
                # Log user in
                login(request, user)
                # Disable CSRF checks
                setattr(request, '_dont_enforce_csrf_checks', True)
                json_details = request.GET.get("authjson_details", request.POST.get("authjson_details", False))
                if json_details in ['true', '1', 't', True]:
                    json_details = True
                else:
                    json_details = False
                request.json_details = json_details

    def __call__(self, request):

        # Code to be executed for each request before the view (and later middleware) are called.
        self.process_request(request)

        # Get response
        response = self.get_response(request)

        # Code to be executed for each request/response after the view is called
        # ... pass ...

        # Return response
        return response
