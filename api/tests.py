# coding: utf-8
# from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import status
from rest_framework.test import APITestCase

from motsdits.models import MotDit, Item, Question, Photo, Story, News
from api.serializers import motsdits as motsdits_serializers
import json

from datetime import datetime, timedelta


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
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access_token'])

    def post_anon(*args, **kwargs):
        '''Add an anonymous posting util (post without credentials)'''
        credentials = api_client._credentials
        api_client._credentials = {}
        response = api_client.post(*args, **kwargs)
        api_client._credentials = credentials
        return response

    api_client.post_anon = post_anon


class MDQApiTest(APITestCase):
    '''Provides common setup for the MDQ API'''

    def setUp(self):
        '''Sets up the necessary access token'''

        # Default client
        self.user = get_user_model().objects.get(username='admin')
        ensure_access_token(self.client, self.user)

        # And an alt user client
        self.alt_user = get_user_model().objects.get(username='otheruser')
        self.alt_client = self.client_class()
        ensure_access_token(self.alt_client, self.alt_user)


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
        self.assertEqual(sorted([m['id'] for m in response.data['results']]), ids)

    def test_item_photos(self):
        '''Test the item photos list'''

        item = Item.objects.get(pk=1)
        ids = [motdit.id for motdit in item.motsdits]
        response = self.client.get('/api/v2/items/1/photos/')

        for photo in response.data['results']:
            self.assertIn(photo.motdit, ids)


class MotDitTests(MDQApiTest):
    '''Tests for the mot-dit API'''

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

    def test_create_partial_motdit(self):
        '''Create a motdit with only what or only where'''
        action = 'eat'
        tags = sorted(['fries', 'cheese curds', 'poutine', 'delicious'])

        response = self.client.post('/api/v2/motsdits/', {
            'where': 'la banquise',
            'action': action,
            'tags': tags
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post('/api/v2/motsdits/', {
            'what': 'la banquise',
            'action': action,
            'tags': tags
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_motdit_with_no_tags(self):
        '''Create a motdit with no tags'''

        response = self.client.post('/api/v2/motsdits/', {
            'what': 'la banquise',
            'action': 'eat',
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_motdit_with_story(self):
        '''Ensures that we can create a motdit with a story'''

        my_story = 'I ate so many things here'
        response = self.client.post('/api/v2/motsdits/', {
            'what': 'brunch',
            'where': 'vieux port steakhouse',
            'action': 'eat',
            'tags': ['brunch', 'sunday'],
            'story': my_story
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        story = Story.objects.get(motdit__pk=response.data['id'])
        self.assertEqual(story.text, my_story)

    def test_create_motdit_with_story_and_accents(self):
        '''Ensures that we can create a motdit with a story'''

        my_story = u"J'ai mangé plein d'affaires"
        response = self.client.post('/api/v2/motsdits/', {
            'what': 'du vélo',
            'where': 'velodrome',
            'action': 'eat',
            'tags': ['weekend', 'activité', 'bon workout'],
            'story': my_story
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        story = Story.objects.get(motdit__pk=response.data['id'])
        self.assertEqual(story.text, my_story)

    def test_create_motdit_anon(self):
        '''Ensures that we can create a motdit with a story'''

        response = self.client.post_anon('/api/v2/motsdits/', {
            'what': 'pizza',
            'where': 'pizzatown',
            'action': 'eat',
            'tags': ['pizza', 'town'],
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_motdit_with_photo(self):
        '''Ensures we can create a motdit with a photo'''

        with open('../data/auxvivres.jpg') as testfile:
            response = self.client.post('/api/v2/motsdits/', {
                'what': 'vegan',
                'where': 'aux vivres',
                'action': 'eat',
                'tags': 'vegan times, awesomeness',
                'photo': testfile
            }, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # as long as it exists, we're good to go
        Photo.objects.get(motdit=response.data['id'])

    def test_create_duplicate_motdit(self):
        '''Tests what happens when we create a duplicate motdit object (should always return the same motdit, but still create the sub-objects)'''

        # Create it once
        response = self.client.post('/api/v2/motsdits/', {
            'what': 'snack',
            'where': 'the mall',
            'action': 'eat',
            'tags': 'boring',
            'story': 'this is the first story'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        motdit1 = response.data['id']

        # And create it again
        response = self.client.post('/api/v2/motsdits/', {
            'what': 'Snack',
            'where': 'the Mall ',
            'action': 'eat',
            'tags': 'exciting',
            'story': 'this is the second story'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        motdit2 = response.data['id']

        self.assertEqual(motdit1, motdit2)

        motdit = MotDit.objects.get(pk=motdit1)

        # Make sure the tags got created
        self.assertEqual(
            ['boring', 'exciting'],
            sorted(t.name for t in motdit.tags)
        )

        # Make sure the stories got created
        self.assertEqual(
            ['this is the first story', 'this is the second story'],
            sorted(s.text for s in Story.objects.filter(motdit=motdit2))
        )

    def test_transaction_failure_motdit(self):
        '''Test that if the motdit transaction doesn't get to the end, the motdit doesn't get created'''

        motdit_count = MotDit.objects.count()
        story_count = Story.objects.count()

         # Create it once
        response = self.client.post('/api/v2/motsdits/', {
            'what': 'tasty snacks',
            'where': 'everywhere that is great',
            'action': 'eat',
            'tags': {'this': 1, 'will': 2, 'fail': 3},
            'story': 'so this one time, i had some snacks...'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(MotDit.objects.count(), motdit_count)
        self.assertEqual(Story.objects.count(), story_count)

    def test_delete_motdit(self):
        '''Testing deleting of a motdit'''

        response = self.client.delete('/api/v2/motsdits/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_motdits(self):
        '''Test to make sure the list view returns the right data'''

        response = self.client.get('/api/v2/motsdits/')
        self.assertEqual(response.data['count'], MotDit.objects.count())

        class request:
            user = self.user

        manually_serialized = motsdits_serializers.MotDitSerializer(MotDit.objects.all(), many=True, context={'request': request}).data
        self.assertEqual(response.data['results'], manually_serialized)

    def test_list_motdits_sorted(self):
        '''Test to make sure the list view returns the right data'''

        response = self.client.get('/api/v2/motsdits/?order_by=likes')

        likes = [motdit['likes'] for motdit in response.data['results']]

        # Make sure the like count is sorted
        self.assertEqual(likes, sorted(likes, reverse=True))

    def test_flag_motdit(self):
        '''Tests that flagging a motdit sets the flag value 1 higher'''

        flags = MotDit.objects.get(pk=1).flags

        response = self.client.post('/api/v2/motsdits/1/flag/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MotDit.objects.get(pk=1).flags, flags + 1)

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

    def test_motdit_photos(self):
        '''Tests listing of photos for a motdit'''

        response = self.client.get('/api/v2/motsdits/1/photos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Make sure it only returns photos for MotDit #1
        for photo in response.data['results']:
            self.assertEqual(photo.motdit, 1)

    def test_motdit_stories(self):
        '''Tests listing of stories for a motdit'''

        response = self.client.get('/api/v2/motsdits/1/stories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Make sure it only returns photos for MotDit #1
        for story in response.data['results']:
            self.assertEqual(story.motdit, 1)

    def test_motdit_news(self):
        '''Tests listing of news for a motdit'''

        response = self.client.get('/api/v2/motsdits/1/news/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Make sure it only returns news for MotDit #1
        for news in response.data['results']:
            self.assertEqual(news.motdit, 1)

    def test_favourite_motdit(self):
        '''Performs a "like" of the mot-dit by the admin user'''

        response = self.client.post('/api/v2/motsdits/1/favourite/', format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        motdit = MotDit.objects.get(pk=1)
        self.assertIn(self.user, motdit.favourites.all())

    def test_unfavourite_motdit(self):
        '''Performs an unlike action on a MotDit'''

        # Delete the like
        response = self.client.delete('/api/v2/motsdits/1/favourite/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # And verify that the delete worked
        motdit = MotDit.objects.get(pk=1)
        self.assertNotIn(self.user, motdit.favourites.all())

    def test_motdit_combine(self):
        '''Ensure mots-dits get properly combined when created'''

        response = self.client.post('/api/v2/motsdits/', {
            'what': 'a poutine',
            'where': 'la banquise',
            'action': 'eat',
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        motdit1 = response.data['id']

        response = self.client.post('/api/v2/motsdits/', {
            'what': 'poutine',
            'where': 'banquise',
            'action': 'eat',
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], motdit1)

    def test_motdit_score(self):
        '''Create a motdit and make sure it only scores once'''

        response = self.client.post('/api/v2/motsdits/', {
            'what': 'la trattoria',
            'action': 'eat',
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        score = MotDit.objects.get(pk=response.data['id']).score

        response = self.client.post('/api/v2/motsdits/', {
            'what': 'la trattoria',
            'action': 'eat',
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MotDit.objects.get(pk=response.data['id']).score, score)


class PhotoTests(MDQApiTest):
    '''Tests for the photo API'''

    fixtures = ['test_oauth.json', 'test_accounts.json', 'test_motsdits.json', 'test_photos.json']

    def test_create_photo(self):
        '''Create a photo'''

        with open('motsditsv2/auxvivres.jpg') as fp:
            photo_obj = {
                'motdit': 1,
                'picture': fp
            }

            response = self.client.post('/api/v2/photos/', photo_obj, format='multipart')

            # Make sure it was created and linked to the proper motdit
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data['motdit']['id'], 1)

    def test_delete_photo(self):
        '''Delete a photo'''

        response = self.client.delete('/api/v2/photos/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Photo.objects.filter(pk=1).count(), 0)

    def test_delete_other_user_photo(self):
        '''Tests deletion of a story created by another user'''
        response = self.client.delete('/api/v2/photos/2/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_like_photo(self):
        '''Performs a "like" of the mot-dit by the admin user'''

        response = self.client.post('/api/v2/photos/1/like/', format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        photo = Photo.objects.get(pk=1)
        self.assertIn(self.user, photo.likes.all())

    def test_unlike_photo(self):
        '''Performs an unlike action on a Photo'''

        self.user.liked_photos.add(Photo.objects.get(pk=1))

        # Delete the like
        response = self.client.delete('/api/v2/photos/1/like/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # And verify that the delete worked
        photo = Photo.objects.get(pk=1)
        self.assertNotIn(self.user, photo.likes.all())


class StoryTests(MDQApiTest):
    '''Tests for the story API'''

    fixtures = ['test_oauth.json', 'test_accounts.json', 'test_motsdits.json', 'test_stories.json']

    def test_create_story(self):
        '''Tests the creation of a new story'''

        test_story = 'this is a sample story'

        response = self.client.post('/api/v2/stories/', {
            'text': test_story,
            'motdit': 1
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['text'], 'this is a sample story')

    def test_delete_story(self):
        '''Tests the deletion of a story'''

        response = self.client.delete('/api/v2/stories/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Story.objects.filter(pk=1).count(), 0)

    def test_delete_other_user_story(self):
        '''Tests deletion of a story created by another user'''
        response = self.client.delete('/api/v2/stories/2/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_like_story(self):
        '''Tests liking of stories'''

        response = self.client.post('/api/v2/stories/1/like/', format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        story = Story.objects.get(pk=1)
        self.assertIn(self.user, story.likes.all())

    def test_unlike_story(self):
        '''Tests unliking of a story'''

        self.user.liked_stories.add(Story.objects.get(pk=1))

        # Delete a like
        response = self.client.delete('/api/v2/stories/1/like/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # And verify that the delete worked
        story = Story.objects.get(pk=1)
        self.assertNotIn(self.user, story.likes.all())


class NewsTests(MDQApiTest):
    '''Tests for the news API'''

    fixtures = ['test_oauth.json', 'test_accounts.json', 'test_motsdits.json', 'test_photos.json', 'test_news.json', 'test_comments.json', 'test_stories.json', 'test_questions.json']

    def test_news_comments(self):
        '''Tests retrieving all comments for a news item'''

        response = self.client.get('/api/v2/news/1/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # And make sure that each comment returned is related to this news item
        for comment in response.data['results']:
            self.assertEqual(comment['news_item'], 1)

    def test_create_motdit_news(self):
        '''Tests that news gets generated when creating a motdit, whether or not you're the first'''

        # Create it
        response = self.client.post('/api/v2/motsdits/', {
            'what': 'la banquise',
            'action': 'eat',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # only get recent news items (ensures one got created)
        news_item = News.objects.filter(
            action=settings.NEWS_CREATED_MOTDIT,
            created__gt=datetime.utcnow() - timedelta(minutes=1)
        ).order_by('-id')[0]

        self.assertEqual(news_item.action, settings.NEWS_CREATED_MOTDIT)
        self.assertEqual(news_item.created_by, self.user)
        self.assertEqual(news_item.motdit.id, response.data['id'])

        # Make sure the alt user can actually create stuff
        self.alt_user.validated = True
        self.alt_user.save()

        # Create it again
        response = self.alt_client.post('/api/v2/motsdits/', {
            'what': 'la banquise',
            'action': 'eat',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        news_item = News.objects.filter(
            action=settings.NEWS_CREATED_MOTDIT,
            created__gt=datetime.utcnow() - timedelta(minutes=1)
        ).order_by('-id')[0]

        self.assertEqual(news_item.action, settings.NEWS_CREATED_MOTDIT)
        self.assertEqual(news_item.created_by, self.alt_user)
        self.assertEqual(news_item.motdit.id, response.data['id'])

    def test_update_motdit_news(self):
        '''Tests that news gets generated when updating a motdit'''

        response = self.client.patch('/api/v2/motsdits/1/', {
            'address': '1234 Fake Street'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        news_item = News.objects.filter(
            action=settings.NEWS_UPDATED_MOTDIT,
            created__gt=datetime.utcnow() - timedelta(minutes=1)
        ).order_by('-id')[0]
        self.assertEqual(news_item.created_by, self.user)
        self.assertEqual(news_item.motdit.id, response.data['id'])

    def test_like_motdit_news(self):
        '''Tests that a news item is generated when you like a motdit'''

        TEST_PK = 1

        response = self.client.post('/api/v2/motsdits/{pk}/like/'.format(pk=TEST_PK), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        news_item = News.objects.filter(
            action=settings.NEWS_LIKED_MOTDIT,
            created__gt=datetime.utcnow() - timedelta(minutes=1)
        ).order_by('-id')[0]
        self.assertEqual(news_item.created_by, self.user)
        self.assertEqual(news_item.motdit.id, TEST_PK)

    def test_favourite_motdit_news(self):
        '''Tests that a news item is generated when you favourite a motdit'''

        TEST_PK = 1

        response = self.client.post('/api/v2/motsdits/{pk}/favourite/'.format(pk=TEST_PK), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        news_item = News.objects.filter(
            action=settings.NEWS_FAVOURITED_MOTDIT,
            created__gt=datetime.utcnow() - timedelta(minutes=1)
        ).order_by('-id')[0]
        self.assertEqual(news_item.created_by, self.user)
        self.assertEqual(news_item.motdit.id, TEST_PK)

    def test_like_photo_news(self):
        '''Tests that a news item is generated when you like a photo'''

        TEST_PK = 1

        response = self.client.post('/api/v2/photos/{pk}/like/'.format(pk=TEST_PK), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        news_item = News.objects.filter(
            action=settings.NEWS_LIKED_PHOTO,
            created__gt=datetime.utcnow() - timedelta(minutes=1)
        ).order_by('-id')[0]
        self.assertEqual(news_item.created_by, self.user)
        self.assertEqual(news_item.photo.id, TEST_PK)

    def test_like_story_news(self):
        '''Tests that a news item is generated when you like a story'''

        TEST_PK = 1

        response = self.client.post('/api/v2/stories/{pk}/like/'.format(pk=TEST_PK), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        news_item = News.objects.filter(
            action=settings.NEWS_LIKED_STORY,
            created__gt=datetime.utcnow() - timedelta(minutes=1)
        ).order_by('-id')[0]
        self.assertEqual(news_item.created_by, self.user)
        self.assertEqual(news_item.story.id, TEST_PK)

    def test_ask_question_news(self):
        '''Tests that a news item is generated when you ask a question'''

        response = self.client.post('/api/v2/questions/', {
            'what': 'a poutine',
            'where': 'montreal',
            'action': 'eat'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        question_id = response.data['id']

        news_item = News.objects.filter(
            action=settings.NEWS_ASKED_QUESTION,
            created__gt=datetime.utcnow() - timedelta(minutes=1)
        ).order_by('-id')[0]
        self.assertEqual(news_item.created_by, self.user)
        self.assertEqual(news_item.question.id, question_id)

    def test_answer_question_news(self):
        '''Tests that a news item is created when you answer a question'''

        TEST_PK = 1
        ANSWER_MOTDIT = 6

        response = self.client.post('/api/v2/questions/{pk}/answers/'.format(pk=TEST_PK), {
            'motdit': ANSWER_MOTDIT
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        answer_id = response.data['id']

        news_item = News.objects.filter(
            action=settings.NEWS_ANSWERED_QUESTION,
            created__gt=datetime.utcnow() - timedelta(minutes=1)
        ).order_by('-id')[0]
        self.assertEqual(news_item.created_by, self.user)
        self.assertEqual(news_item.answer.id, answer_id)
        self.assertEqual(news_item.question.id, TEST_PK)
        self.assertEqual(news_item.motdit.id, ANSWER_MOTDIT)


class CommentTests(MDQApiTest):
    '''Tests for the comment API'''

    fixtures = ['test_oauth.json', 'test_accounts.json', 'test_motsdits.json', 'test_news.json', 'test_comments.json']

    def test_create_comment(self):
        '''Tests that we can create a comment'''

        test_comment = 'this is a comment on a news item'

        response = self.client.post('/api/v2/comments/', {
            'text': test_comment,
            'news': 1
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['text'], test_comment)


class UserTests(MDQApiTest):
    '''Tests for interaction with the User API'''

    fixtures = ['test_oauth.json', 'test_accounts.json']

    def test_unverified_user_action(self):
        '''Tries to perform an action that an unverified user should not be able to do'''

        action = 'eat'
        tags = sorted(['fries', 'cheese curds', 'poutine', 'delicious'])

        response = self.alt_client.post('/api/v2/motsdits/', {
            'what': 'a poutine',
            'where': 'la banquise',
            'action': action,
            'tags': tags
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_follow_user(self):
        '''Tests creating a new following link with a user'''

        response = self.client.post('/api/v2/users/2/follow/', format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(pk=2)
        self.assertIn(self.user, user.followers.all())

    def test_follow_self(self):
        '''Tests following yourself (shouldnt be allowed)'''
        response = self.client.post('/api/v2/users/{}/follow/'.format(self.user.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unfollow_user(self):
        '''Tests deleting a following link with a user'''

        self.user.following.add(get_user_model().objects.get(pk=2))

        # Delete a like
        response = self.client.delete('/api/v2/users/2/follow/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # And verify that the delete worked
        user = get_user_model().objects.get(pk=2)
        self.assertNotIn(self.user, user.followers.all())

    def test_load_self(self):
        '''Tests the self loading endpoint'''
        response = self.client.get('/api/v2/users/self', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_update_self(self):
        '''Tests a PUT to the self endpoint'''

        test_email = 'abc@123.com'
        test_email_fail = 'this email fails'
        test_fname = 'firsty'
        test_lname = 'lasty'

        # Set the email
        response = self.client.patch('/api/v2/users/self', {
            'email': test_email
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = get_user_model().objects.get(pk=self.user.pk)
        self.assertEqual(user.email, test_email)

        # Set an invalid email
        response = self.client.patch('/api/v2/users/self', {
            'email': test_email_fail
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user = get_user_model().objects.get(pk=self.user.pk)
        self.assertNotEqual(user.email, test_email_fail)

        # Set name of the user
        response = self.client.patch('/api/v2/users/self', {
            'first_name': test_fname,
            'last_name': test_lname
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = get_user_model().objects.get(pk=self.user.pk)
        self.assertEqual(user.first_name, test_fname)
        self.assertEqual(user.last_name, test_lname)

        # Test invalid first name setting
        response = self.client.patch('/api/v2/users/self', {
            'first_name': 1
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # And invalid last name setting
        response = self.client.patch('/api/v2/users/self', {
            'last_name': 1
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_set_avatar(self):

        # And invalid last name setting
        with open('../data/auxvivres.jpg') as testfile:
            response = self.client.patch('/api/v2/users/self', {
                'avatar': testfile
            }, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            user = get_user_model().objects.get(pk=self.user.pk)
            self.assertNotEqual(user.avatar, None)

    def test_registration_create(self):
        '''Tests the user registration flow'''

        # Test creating a good user
        response = self.client.post_anon('/api/v2/users/register', {
            'email': 'unused@motsditsquebec.com',
            'username': 'mr_unused',
            'password': '123456',
            'first_name': 'test',
            'last_name': 'user',
            'send_email': False
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Tests that fail creating a user

        ## Bad email
        response = self.client.post_anon('/api/v2/users/register', {
            'email': 'invalid_email',
            'username': 'mr_unused2',
            'password': '123456',
            'first_name': 'test',
            'last_name': 'user',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        ## Conflicting username
        response = self.client.post_anon('/api/v2/users/register', {
            'email': 'unused2@motsditsquebec.com',
            'username': 'otheruser',
            'password': '123456',
            'first_name': 'test',
            'last_name': 'user',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        ## Conflicting email
        response = self.client.post_anon('/api/v2/users/register', {
            'email': 'other@motsditsquebec.com',
            'username': 'test',
            'password': '123456',
            'first_name': 'test',
            'last_name': 'user',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        ## Missing data
        response = self.client.post_anon('/api/v2/users/register', {
            'email': 'unused2@motsditsquebec.com',
            'username': 'test',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_validate(self):
        '''Registers a user and then activates using the validation key'''

        # Create a good user
        response = self.client.post_anon('/api/v2/users/register', {
            'email': 'unused@motsditsquebec.com',
            'username': 'mr_unused',
            'password': '123456',
            'first_name': 'test',
            'last_name': 'user',
            'send_email': False
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user_id = response.data['id']

        validation_code = get_user_model().objects.get(pk=user_id, validated=False).validation_code

        response = self.client.get('/api/v2/users/validate/{}'.format(validation_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # And check that the user is now valid
        valid_user = get_user_model().objects.get(pk=user_id)
        self.assertTrue(valid_user.validated)
        self.assertTrue(valid_user.is_active)

    def test_registration_avatar(self):
        '''Tests the user registration flow'''

        # Test creating a user w/ avatar
        with open('../data/auxvivres.jpg') as testfile:
            response = self.client.post_anon('/api/v2/users/register', {
                'email': 'unused@motsditsquebec.com',
                'username': 'mr_unused',
                'password': '123456',
                'first_name': 'test',
                'last_name': 'user',
                'send_email': False,
                'avatar': testfile
            }, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            user = get_user_model().objects.get(pk=response.data['id'])
            self.assertNotEqual(user.avatar, None)
            # @TODO: Compare to the testfile value


class QuestionTests(MDQApiTest):
    '''Tests for the mot-dit API'''

    fixtures = ['test_oauth.json', 'test_accounts.json', 'test_motsdits.json', 'test_questions.json', 'test_answers.json']

    def test_create_question(self):
        '''Ensure we can create a question'''

        response = self.client.post('/api/v2/questions/', {
            'what': 'a poutine',
            'where': 'montreal',
            'action': 'eat'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # @TODO: more checks here

    def test_answer_question_by_id(self):
        '''Ensure we can answer a question'''

        response = self.client.post('/api/v2/questions/1/answers/', {
            'motdit': 6
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        question = Question.objects.get(pk=1)

        # Make sure the answer is in there
        self.assertIn(response.data['id'], [answer.pk for answer in question.answers.all()])

    def test_answer_question_with_motdit(self):
        '''Ensure we can answer a question with a fresh motdit'''

        response = self.client.post('/api/v2/questions/1/answers/', {
            'motdit': {
                'what': 'some donuts',
                'where': 'chez boris',
                'action': 'eat',
                'tags': ['noms', 'so great', 'wow']
            }
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        question = Question.objects.get(pk=1)

        # Make sure the answer is in there
        self.assertIn(response.data['id'], [answer.pk for answer in question.answers.all()])
