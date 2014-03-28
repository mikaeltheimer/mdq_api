from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

# Using the standard RequestFactory API to create a form POST request


class ItemTests(APITestCase):

    def test_update_item(self):
        pass


class MotDitTests(APITestCase):
    '''Tests for the mot-dit modules'''

    factory = APIRequestFactory()

    def test_create_motdit(self):
        '''Ensure we can create a motdit'''
        request = factory.post('/notes/', {'title': 'new idea'})


    def test_delete_motdit(self):
        pass

    def test_list_motdits(self):
        pass

    def test_like_motdit(self):
        pass
