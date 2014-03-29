# from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from motsdits.models import MotDit
from api.serializers import motsdits as motsdits_serializers
import json


NEW_PASSWORD = 'password'


def ensure_access_token(api_client, user):
    '''Loads an access token to add to requests'''
    from provider.oauth2.models import Client
    client = Client.objects.all()[0]

    # Set a new password so we have direct access to the value
    user.set_password(NEW_PASSWORD)
    user.save()

    grant_data = {
        'client_id': client.client_id,
        'client_secret': client.client_secret,
        'grant_type': 'password',
        'username': user.email,
        'password': NEW_PASSWORD
    }

    # Request an access token
    response = api_client.post("/oauth2/access_token/", grant_data, format='multipart')
    data = json.loads(response.content)
    return api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access_token'])


class ItemTests(APITestCase):

    def test_update_item(self):
        '''Tests pushing an update to an item'''


class MotDitTests(APITestCase):
    '''Tests for the mot-dit modules'''

    fixtures = ['test_oauth.json', 'test_accounts.json', 'test_motsdits.json']

    def setUp(self):
        '''Sets up the necessary access token'''
        user = get_user_model().objects.get(username='admin')
        ensure_access_token(self.client, user)

    def test_create_motdit(self):
        '''Ensure we can create a motdit'''

        action = 'eat'
        tags = sorted(['fries', 'cheese curds', 'poutine', 'delicious'])

        response = self.client.post('/api/v2/motsdits/', {
            'what': 'a poutine',
            'where': 'la banquise',
            'action': action,
            'tags': tags
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(sorted(response.data['tags']), tags)
        self.assertEqual(response.data['action'].lower(), action)

    def test_delete_motdit(self):
        '''Testing deleting of a motdit'''

        response = self.client.delete('/api/v2/motsdits/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_motdits(self):
        '''Test to make sure the list view returns the right data'''

        response = self.client.get('/api/v2/motsdits/')
        self.assertEqual(response.data['count'], MotDit.objects.count())

        manually_serialized = motsdits_serializers.MotDitSerializer(MotDit.objects.all(), many=True).data
        self.assertEqual(response.data['results'], manually_serialized)

    def test_like_motdit(self):
        '''Performs a "like" of the mot-dit by the admin user'''

        # Load user
        user = get_user_model().objects.get(username='admin')
        self.client.force_authenticate(user=user)

        response = self.client.post('/api/v2/motsdits/1/like/', format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        motdit = MotDit.objects.get(pk=1)
        self.assertIn(user, motdit.likes.all())

    def test_unlike_motdit(self):
        '''Performs an unlike action on a MotDit'''

        # Load user
        user = get_user_model().objects.get(username='admin')
        self.client.force_authenticate(user=user)

        # Delete the like
        response = self.client.delete('/api/v2/motsdits/1/like/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # And verify that the delete worked
        motdit = MotDit.objects.get(pk=1)
        self.assertNotIn(user, motdit.likes.all())
