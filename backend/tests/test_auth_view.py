"""test module for users_views"""
# from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from copy import copy
from backend.models import User

class TestAuthview(APITestCase):
    """ test for user detail views """
    user_data = {
        'email': 'kb@goat.com',
        'username': 'Kobe Bryant',
        'password': 'iamagod',
        'user_group': 'Student',
    }
    profile_data = {
        'school_name': 'THU',
    }

    def test_authentication(self):
        """ test authentication """
        # add user
        url1 = reverse('user-list')
        response1 = self.client.post(url1, self.user_data, format='json')
        # auth
        url2 = reverse('account-auth')
        data = {
            'username': 'Kobe Bryant',
            'password': 'iamagod'
        }
        response2 = self.client.post(url2, data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.data['token'], response2.data['token'])

        # user = User.objects.get(username=data['username'])