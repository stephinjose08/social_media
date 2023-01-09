from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser,Profile
from rest_framework.authtoken.models import Token
from .api.serializers import ProfileSerializer

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
        


class ProfileTest(APITestCase):
    def setUp(self):
        self.user=CustomUser.objects.create_user(username="example",
        password="example@123",phone=1414141414,email="joa@gmail.com")
        url = reverse('login-user')
        data = {
                "phone":1414141414,
               
                "password":"example@123"
                }
        response=self.client.post(url, data, format='json')
        self.token=response.data['access']
        self.client.force_authenticate(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        

        self.user2=CustomUser.objects.create_user(username="example2",
        password="example@1234",phone=1414141410,email="jo@gmail.com")
        url = reverse('login-user')
        data = {
                "phone":1414141410,
               
                "password":"example@1234"
                }
        response=self.client.post(url, data, format='json')
        self.profile=Profile.objects.create(owner=self.user2,gender="female",work_at="pala")


    def test_ProfileCreate(self):
        url=reverse('profile-list')
        data={
            "owner":self.user.id,"gender":"male","work_at":"kklm"
        }
        # self.client.credentials(HTTP_AUTHORIZATION='Token' + self.token)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # print(response.content)
    def test_profileGet(self):

        data={
            "owner":self.user.id,"gender":"male","work_at":"kklm"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token' + self.token)
        self.client.post(reverse('profile-list'), data, format='json')
        url=reverse('profile-detail',args=(self.user.id,))
        response=self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.content)
    def test_ProfileUpdate(self):
       
        data={
            "gender":"male","work_at":"tvm"
        }
        url='profile'
        print("user")
        print(self.user2.username)
        url=reverse('profile-detail',args=(self.user2.id,))
      
        response=self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
       

