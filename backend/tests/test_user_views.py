"""test module for users_views"""
# from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from copy import copy
from backend.models import User
from backend.models import UserPermissions

class UserListViewTest(APITestCase):
    """ test for user views """
    user_data = {
        'email': 'kb@goat.com',
        'username': 'Kobe Bryant',
        'password': 'iamagod',
        'user_group': 'Student',
    }
    profile_data = {
        'school_name': 'THU',
    }

    @classmethod
    def setUpTestData(cls):
        UserPermissions.objects.create(
            group_name="Student",
        )
        UserPermissions.objects.create(
            group_name="Admin",
            view_students=True,
            create_students=True,
            edit_students=True,
            ban_students=True,
        )
        UserPermissions.objects.create(
            group_name="SuperAdmin",
            view_students=True,
            create_students=True,
            edit_students=True,
            ban_students=True,
            promote_students=True,
            view_admins=True,
            create_admins=True,
            edit_admins=True,
            ban_admins=True,
        )

    def test_create_student_without_profile(self):
        """ test creating an user account"""
        print(len(UserPermissions.objects.count()))
        url = reverse('user-list')
        data = copy(self.user_data)

        response = self.client.post(url, data, format='json')
        user = User.objects.all()[0]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'Kobe Bryant')

    def test_create_student_with_profile(self):
        """ test creating an user account"""
        url = reverse('user-list')
        data = copy(self.user_data)
        data['profile'] = self.profile_data

        response = self.client.post(url, data, format='json')
        user = User.objects.all()[0]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, 'Kobe Bryant')

    def test_get_user_list(self):
        """ test getting a list of students """
        url = reverse('user-list')
        data = copy(self.user_data)
        self.client.post(url, data, format='json')
        data['username'] = 'Lebron James'
        self.client.post(url, data, format='json')
        
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


# class UserDetailTest(APITestCase):
#     """ test for user detail views """
#     user_data = {
#         'email': 'kb@goat.com',
#         'username': 'Kobe Bryant',
#         'password': 'iamagod',
#         'user_group': 'Student',
#     }
#     profile_data = {
#         'school_name': 'THU',
#     }

#     def setUp(self):
#         UserPermissions.objects.create(
#             group_name="Student",
#         )
#         UserPermissions.objects.create(
#             group_name="Admin",
#             view_students=True,
#             create_students=True,
#             edit_students=True,
#             ban_students=True,
#         )
#         UserPermissions.objects.create(
#             group_name="SuperAdmin",
#             view_students=True,
#             create_students=True,
#             edit_students=True,
#             ban_students=True,
#             promote_students=True,
#             view_admins=True,
#             create_admins=True,
#             edit_admins=True,
#             ban_admins=True,
#         )

#     def test_retrieve(self):
#         """ test retrieve user """
#         # add user
#         url1 = reverse('user-list')
#         self.client.post(url1, self.user_data, format='json')
#         # auth
#         url2 = reverse('account-auth')
#         data = {
#             'username': 'Kobe Bryant',
#             'password': 'iamagod'
#         }
#         response2 = self.client.post(url2, data, format='json')
#         # get student detail
#         user_id = response2.data['id']
#         url3 = reverse('user-detail', args=[user_id])
#         response3 = self.client.get(url3)
#         self.assertEqual(response3.status_code, status.HTTP_200_OK)
#         self.assertEqual(response3.data['username'], response2.data['username'])