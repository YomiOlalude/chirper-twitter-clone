from django.test import TestCase
from .models import Chirp
from django.contrib.auth import get_user_model
import unittest

# Create your tests here.

User = get_user_model()

class ChirpTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username="seyi", password="password")
        User.objects.create_user(username="bugsi", password="password")
        User.objects.create(username="yomi", password="password")

    def test_user_created(self):
        user = User.objects.get(username="yomi")
        self.assertEqual(user.username, "yomi")
        
