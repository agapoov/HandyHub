from django.test import TestCase

from users.models import Skill, User
from django.urls import reverse
from http import HTTPStatus


class CatalogViewTests(TestCase):
    def setUp(self):
        skill1 = Skill.objects.create(name='Skill1', slug='skill1')
        skill2 = Skill.objects.create(name='Skill2', slug='skill2')
        skill3 = Skill.objects.create(name='Skill3', slug='skill3')
        worker1 = User.objects.create_user(
            username='TestUsername1',
            email='example@yandex.ru',
            password='Password123123',
        )
        worker1.skills.add(skill1)

        worker2 = User.objects.create_user(
            username='TestUsername2',
            email='example@yahoo.ru',
            password='Password123123',
        )
        worker2.skills.add(skill2, skill3)
        worker3 = User.objects.create_user(
            username='TestUsername3',
            email='example@mail.ru',
            password='Passowrd12213',
        )
        worker3.skills.add(skill1, skill2, skill3)
        self.path = reverse('jobs:index')

    def test_catalog_view(self):
        """Test successfully rendering catalog"""
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_catalog_view_with_skills(self):
        """Test successfully rendering catalog with skills"""
        response = self.client.get(self.path, kwargs={'skills_slug': 'skill3'})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'TestUsername3')
