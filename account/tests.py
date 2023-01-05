from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser
from rest_framework.authtoken.models import Token


class RegisterTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('user-create')
        data = {"username": "josua",
                "phone":1234123412,
                "email":"josua@gmail.com",
                'password':"josua123"
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class LoginTests(APITestCase):
    def setUp(self):
        self.user=CustomUser.objects.create_user(username="example",
        password="example@123",phone="1414141414",email="joa@gmail.com")

    def test_login(self):
        url = reverse('login-user')
        data = {
                "phone":1414141414,
               
                'password':"example@123"
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data['access'])
        self.token=response.data['access']
    
    
        # url = reverse('log-out')
        
        # self.client.credentials(HTTP_AUTHORIZATION='Token' + self.token)
        # response = self.client.post(url)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)