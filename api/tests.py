# from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from motsdits.models import MotDit, Item, Photo
from api.serializers import motsdits as motsdits_serializers
import json

from django.db.models import Q


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


class MDQApiTest(APITestCase):
    '''Provides common setup for the MDQ API'''

    def setUp(self):
        '''Sets up the necessary access token'''
        self.user = get_user_model().objects.get(username='admin')
        ensure_access_token(self.client, self.user)


class ItemTests(MDQApiTest):
    '''Tests for the item API'''

    fixtures = ['test_oauth.json', 'test_accounts.json', 'test_motsdits.json']

    def test_autocomplete(self):
        '''Tests that autocomplete returns the proper items'''

        items = [i.name for i in Item.objects.all()]

        for query in ('test', 'test%20what'):

            response = self.client.get('/api/v2/items/autocomplete/{}/'.format(query))

            test_items = sorted(i for i in items if i.lower().startswith(query.replace('%20', ' ')))

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(sorted(response.data), test_items)

    def test_update_item(self):
        '''Tests pushing an update to an item'''

        test_address = "1234 fake street"
        test_website = 'http://valid-website.com'

        response = self.client.patch('/api/v2/items/1/', {
            'address': test_address,
            'website': test_website
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['address'], test_address)
        self.assertEqual(response.data['website'], test_website)

    def test_item_related(self):
        '''Tests the related motsdits list of an item'''

        item = Item.objects.get(pk=1)

        ids = sorted([m.id for m in MotDit.objects.filter(Q(what=item) | Q(where=item))])
        response = self.client.get('/api/v2/items/1/related/')
        self.assertEqual(sorted([m['id'] for m in response.data]), ids)


class MotDitTests(MDQApiTest):
    '''Tests for the mot-dit modules'''

    fixtures = ['test_oauth.json', 'test_accounts.json', 'test_motsdits.json']

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

        response = self.client.post('/api/v2/motsdits/1/like/', format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        motdit = MotDit.objects.get(pk=1)
        self.assertIn(self.user, motdit.likes.all())

    def test_unlike_motdit(self):
        '''Performs an unlike action on a MotDit'''

        # Delete the like
        response = self.client.delete('/api/v2/motsdits/1/like/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # And verify that the delete worked
        motdit = MotDit.objects.get(pk=1)
        self.assertNotIn(self.user, motdit.likes.all())


class PhotoTests(MDQApiTest):
    '''Tests for the mot-dit modules'''

    fixtures = ['test_oauth.json', 'test_accounts.json', 'test_motsdits.json', 'test_photos.json']

    def test_create_photo(self):
        '''Create a photo'''

        with open('motsditsv2/auxvivres.jpg') as fp:
            photo_obj = {
                'motdit': 1,
                'picture': fp.read()
            }

            response = self.client.post('/api/v2/photos/', photo_obj, format='multipart')

            print response.content

            # Make sure it was created and linked to the proper motdit
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data['motdit']['id'], 1)

    def test_delete_photo(self):
        '''Delete a photo'''

        response = self.client.delete('/api/v2/photos/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Photo.objects.filter(pk=1).count(), 0)

    def test_like_photo(self):
        '''Performs a "like" of the mot-dit by the admin user'''

        response = self.client.post('/api/v2/photos/1/like/', format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        photo = Photo.objects.get(pk=1)
        self.assertIn(self.user, photo.likes.all())

    def test_unlike_motdit(self):
        '''Performs an unlike action on a MotDit'''

        # Delete the like
        response = self.client.delete('/api/v2/photos/1/like/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # And verify that the delete worked
        photo = Photo.objects.get(pk=1)
        self.assertNotIn(self.user, photo.likes.all())
