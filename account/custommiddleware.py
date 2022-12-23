"""
File in which we have the middleware for Django for Authenticating API requests
"""
import json
from django.forms import ValidationError
import jwt
import logging
from environs import Env
from django.utils.functional import SimpleLazyObject
from rest_framework_simplejwt.backends import TokenBackend
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.middleware import get_user
key='django-insecure-9ebbq6g!m&-@lol5^^w4_3=1s4rnve!jcb6_mlc-yz^@)8u#x-'
class simplemiddle(MiddlewareMixin):
    def __init__(self,getrequest):
        self.response=getrequest

     
    def __call__(self,request):
        
        print("before request")
        
        if request.method == 'GET':
            print("get request")
            print("heloo")
          
            # jwt_token=request.headers.get('authorization')
           



            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            data = {'token': token}
            try:
                valid_data = TokenBackend(algorithm='HS256').decode(token,verify=False)
                user = valid_data['user_id']
                
                
                request.user = user
                print(request.user)
            except ValidationError as v:
                print("validation error", v)


            
        response=self.response(request)
        print("after request")
        return response



