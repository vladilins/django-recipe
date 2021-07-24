from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users Api"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test create user"""
        payload = (
            'email': 'test@test.com',
            'password': 'test',
            'name': 'test'
        )
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
      """Test creating user that exists fails"""
      payload = {'email': 'test@test.com', 'password': 'test'}
      create_user(**payload)

      res = self.client.post(CREATE_USER_URL, payload)

      self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
      