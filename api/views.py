"""API views
Generates all the necessary viewsets to serve the API

@author Stephen Young (me@hownowstephen.com)
"""

from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.core.validators import EmailValidator, ValidationError
from django.core.urlresolvers import reverse

# Django plugins
from rest_framework import viewsets, status
from rest_framework.decorators import link, action
from rest_framework.permissions import AllowAny
import rest_framework.filters
from rest_framework.response import Response
from rest_framework.views import APIView

from haystack.query import SearchQuerySet, SQ

from motsdits.models import Action, Item, MotDit, Question, Answer, Tag, Photo, Story, News, Comment
from motsdits import signals
from api.permissions import MotsditsPermissions, IsOwnerOrReadOnly, DefaultPermissions

import api.serializers.motsdits as motsdits_serializers
import api.serializers.accounts as accounts_serializers
from api.serializers.motsdits import motsdits_compact

# Pagination helper function
from pagination import get_paginated
import sorting
import re


class ItemViewSet(viewsets.ModelViewSet):
    '''Viewset for Mot-dit objects'''
    model = Item
    serializer_class = motsdits_serializers.ItemSerializer
    paginated_serializer = motsdits_serializers.PaginatedItemSerializer
    filter_backends = (rest_framework.filters.DjangoFilterBackend, )

    def list(self, request):
        '''Lists items'''

        queryset = sorting.sort(request, self.model.objects.all())
        objects = get_paginated(request, queryset)

        return Response(self.paginated_serializer(objects, context={'request': request}).data)

    @link()
    def related(self, request, pk=None):
        '''Recommend the motdit'''

        serializer = motsdits_serializers.PaginatedMotDitSerializer

        queryset = sorting.sort(request, MotDit.objects.filter(Q(what=pk) | Q(where=pk)))
        motsdits = get_paginated(request, queryset)

        return Response(serializer(motsdits, context={'request': request}).data)

    @link()
    def photos(self, request, pk=None):
        '''Retrieves a list of photos related to this item'''

        serializer = motsdits_compact.PaginatedCompactPhotoSerializer

        queryset = sorting.sort(request, Photo.objects.filter(Q(motdit__what=pk) | Q(motdit__where=pk)))
        photos = get_paginated(request, queryset)
        return Response(serializer(photos, context={'request': request}).data)


class ItemAutocomplete(APIView):
    '''Item Autocomplete view'''

    def get(self, request, name=None):
        '''Provides the autocomplete action for items'''
        return Response([item.name for item in Item.objects.filter(name__icontains=name)[:10]])


def normalize_item_value(value):
    '''Normalizes the value of an item - strips off articles and whitespace'''
    value = re.sub('^(un|une|des|le|la|les|a|en|au) ', '', value, flags=re.I)
    return value.strip()


def resolve_item(value, item_type, user=None, address=None, website=None):
    '''Given a value supplied to the API, resolve it to a discrete Item object'''

    item = None

    if isinstance(value, int):
        item = Item.objects.get(pk=value)
    elif value is not None:
        # Pre-clean the value
        value = value.strip()
        normalized = normalize_item_value(value)

        try:
            item = Item.objects.get(type=item_type, name__iexact=normalized)

            # Add address and website, if available
            if address and not item.address:
                item.address = address
            if website and not item.website:
                item.website = website

            if value != normalized and not item.display_name:
                item.display_name = value

            item.save()

        except Item.DoesNotExist:
            item = Item.objects.create(
                type=item_type,
                name=normalized,
                display_name=value if value != normalized else None,
                created_by=user,
                address=address,
                website=website
            )

    return item


def create_motdit(request, data, serializer_class=motsdits_serializers.MotDitSerializer):
    '''Attempts to create a motdit from a data dictionary - returns a Response object'''

    # action
    try:
        if isinstance(data.get('action'), int):
            verb = Action.objects.get(pk=data['action'])
        elif isinstance(data.get('action'), basestring):
            verb = Action.objects.get(verb=data['action'])
        else:
            return Response({'error': 'Must supply an action'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    except Action.DoesNotExist:
        return Response({'error': 'Action {} does not exist'.format(data['action'])}, status=status.HTTP_406_NOT_ACCEPTABLE)

    # Get the related what an where items
    what = resolve_item(data.get('what'), settings.WHAT, user=request.user)
    where = resolve_item(data.get('where'), settings.WHERE, user=request.user, address=data.get('address'), website=data.get('website'))

    if not what and not where:
        return Response({'error': 'Must supply at least one of what or where'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    try:
        with transaction.atomic():

            motdit_data = {
                'action': verb,
                'defaults': {'created_by': request.user}
            }

            if what:
                motdit_data['what'] = what
            if where:
                motdit_data['where'] = where

            # Create the motdit
            motdit, created = MotDit.objects.get_or_create(**motdit_data)

            if not created:
                # @TODO: Increase score every time this happens!
                pass

            # If a string is passed, we take tags as a comma separated list
            if isinstance(data.get('tags', []), basestring):
                tags = [t.strip() for t in data['tags'].split(',') if t.strip()]
            else:
                tags = data.get('tags')

            if isinstance(tags, list):
                for tag_name in tags:
                    try:
                        tag = Tag.objects.get(name__iexact=tag_name)
                    except Tag.DoesNotExist:
                        tag = Tag.objects.create(
                            name=tag_name,
                            created_by=request.user
                        )

                    # Add the tag to the what, if specified
                    if what:
                        what.tags.add(tag)

                    # And add the tag to the where as well
                    if where:
                        where.tags.add(tag)
            elif not tags:
                # allow passing tags: None to the endpoint
                pass
            else:
                raise ValueError('Tags must be supplied as a list or comma separated string')

            # Add a photo, if supplied
            if request.FILES.get('photo'):
                # Create the photo
                photo = Photo.objects.create(
                    picture=request.FILES['photo'],
                    motdit=motdit,
                    created_by=request.user
                )
            else:
                photo = None

            # Create story, if supplied
            if data.get('story'):
                story = Story.objects.create(
                    motdit=motdit,
                    text=data['story'],
                    created_by=request.user,
                    photo=photo
                )
            else:
                story = None

            # Finally, dispatch the creation signal
            signals.motdit_created.send(request.user.__class__, created_by=request.user, motdit=motdit, photo=photo, story=story)

            return Response(serializer_class(motdit, context={'request': request}).data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MotDitViewSet(viewsets.ModelViewSet):
    '''Viewset for Mot-dit objects'''
    model = MotDit
    serializer_class = motsdits_serializers.MotDitSerializer
    paginated_serializer = motsdits_serializers.PaginatedMotDitSerializer
    permission_classes = [DefaultPermissions, MotsditsPermissions]

    def list(self, request):
        '''Lists mots-dits'''

        queryset = sorting.sort(request, self.model.objects.all())
        objects = get_paginated(request, queryset)

        return Response(self.paginated_serializer(objects, context={'request': request}).data)

    @action(methods=['POST'])
    def flag(self, request, pk=None):
        '''Flag the mot-dit'''

        motdit = MotDit.objects.get(pk=pk)
        motdit.flags += 1
        motdit.save()
        return Response(status=status.HTTP_201_CREATED)

    @action(methods=['POST', 'DELETE'])
    def like(self, request, pk=None):
        '''Like or unlike a motdit'''

        motdit = MotDit.objects.get(pk=pk)

        # User wants to like this mot-dit
        if request.method == 'POST':
            motdit.likes.add(request.user)
            signals.motdit_liked.send(request.user.__class__, created_by=request.user, motdit=motdit)
            return Response(status=status.HTTP_201_CREATED)

        # Otherwise we can do a DELETE
        elif request.method == 'DELETE':
            motdit.likes.remove(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST', 'DELETE'])
    def favourite(self, request, pk=None):
        '''Like or unlike a motdit'''

        motdit = MotDit.objects.get(pk=pk)

        # User wants to like this mot-dit
        if request.method == 'POST':
            motdit.favourites.add(request.user)
            signals.motdit_favourited.send(request.user.__class__, created_by=request.user, motdit=motdit)
            return Response(status=status.HTTP_201_CREATED)

        # Otherwise we can do a DELETE
        elif request.method == 'DELETE':
            motdit.favourites.remove(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @link()
    def photos(self, request, pk=None):
        '''Retrieves a list of photos related to this item'''
        serializer = motsdits_compact.PaginatedCompactPhotoSerializer

        queryset = sorting.sort(request, Photo.objects.filter(motdit=pk))
        photos = get_paginated(request, queryset)

        return Response(serializer(photos, context={'request': request}).data)

    @link()
    def stories(self, request, pk=None):
        '''Retrieves a list of stories related to this item'''
        serializer = motsdits_compact.PaginatedCompactStorySerializer

        queryset = sorting.sort(request, Story.objects.filter(motdit=pk))
        stories = get_paginated(request, queryset)

        return Response(serializer(stories, context={'request': request}).data)

    def create(self, request):
        '''Create a MotDit object'''
        return create_motdit(request, request.DATA, serializer_class=self.serializer_class)

    def partial_update(self, request, pk=None):
        '''Allows for a PATCH request to the motdit'''

        motdit = MotDit.objects.get(pk=pk)

        if request.DATA.get('address'):
            motdit.where.address = request.DATA['address']

        if request.DATA.get('website'):
            motdit.where.website = request.DATA['website']

        signals.motdit_updated.send(request.user.__class__, created_by=request.user, motdit=motdit)

        return Response(self.serializer_class(motdit, context={'request': request}).data, status=status.HTTP_200_OK)


class QuestionViewSet(viewsets.ModelViewSet):
    '''Encapsulates the base motdit views'''

    model = Question
    serializer_class = motsdits_serializers.QuestionSerializer
    paginated_serializer = motsdits_serializers.PaginatedQuestionSerializer
    permission_classes = [DefaultPermissions, MotsditsPermissions]

    def list(self, request):
        '''Lists mots-dits'''

        queryset = sorting.sort(request, self.model.objects.all())
        objects = get_paginated(request, queryset)

        return Response(self.paginated_serializer(objects, context={'request': request}).data)

    def create(self, request):
        '''Create a Question object'''
        data = request.DATA

        # action
        try:
            if isinstance(data.get('action'), int):
                verb = Action.objects.get(pk=data['action'])
            elif isinstance(data.get('action'), basestring):
                verb = Action.objects.get(verb=data['action'])
            else:
                return Response({'error': 'Must supply an action'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Action.DoesNotExist:
            return Response({'error': 'Action {} does not exist'.format(data['action'])}, status=status.HTTP_406_NOT_ACCEPTABLE)

        # Get the related what an where items
        what = resolve_item(data.get('what'), settings.WHAT, user=request.user)
        where = resolve_item(data.get('where'), settings.WHERE, user=request.user, address=data.get('address'), website=data.get('website'))

        if not what and not where:
            return Response({'error': 'Must supply at least one of what or where'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        try:
            with transaction.atomic():

                # New questions are unique by the action, what, where and created_by
                question_data = {
                    'action': verb,
                    'created_by': request.user
                }

                if what:
                    question_data['what'] = what
                if where:
                    question_data['where'] = where

                # Create the motdit
                question, created = Question.objects.get_or_create(**question_data)

                if created:
                    # Finally, dispatch the ask signal
                    signals.question_asked.send(request.user.__class__, created_by=request.user, question=question)

                return Response(self.serializer_class(question, context={'request': request}).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET', 'POST'])
    def answers(self, request, pk=None):
        '''Allows users to post an answer to the question, either as a new motdit or as a motdit id'''

        # Load the relevant question
        question = Question.objects.get(pk=pk)

        # List all answers
        if request.method == 'GET':

            serializer = motsdits_compact.PaginatedCompactAnswerSerializer

            queryset = sorting.sort(request, Answer.objects.filter(question=question))
            objects = get_paginated(request, queryset)

            return Response(serializer(objects, context={'request': request}).data)

        # Create a new answer
        elif request.method == 'POST':

            serializer = motsdits_compact.CompactAnswerSerializer

            # Either supply a discrete motdit ID
            if isinstance(request.DATA['motdit'], int):
                motdit = MotDit.objects.get(pk=request.DATA['motdit'])
            else:

                try:
                    # Handle the response
                    response = create_motdit(request, request.DATA['motdit'])
                    motdit = MotDit.objects.get(pk=response.data['id'])

                except Exception as e:
                    return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            answer, created = Answer.objects.get_or_create(
                question=question,
                answer=motdit,
                created_by=request.user
            )

            if created:
                signals.question_answered.send(request.user.__class__, created_by=request.user, question=question, answer=answer, motdit=motdit)
                status_code = status.HTTP_201_CREATED
            else:
                status_code = status.HTTP_200_OK

            return Response(serializer(answer, context={'request': request}).data, status=status_code)


class AnswerViewSet(viewsets.ModelViewSet):
    '''Viewset for Answer objects'''
    model = Answer
    serializer_class = motsdits_serializers.AnswerSerializer
    paginated_serializer = motsdits_serializers.PaginatedAnswerSerializer
    permission_classes = [DefaultPermissions, IsOwnerOrReadOnly]

    def list(self, request):
        '''Lists items'''

        queryset = sorting.sort(request, self.model.objects.all())
        objects = get_paginated(request, queryset)

        return Response(self.paginated_serializer(objects, context={'request': request}).data)


class PhotoViewSet(viewsets.ModelViewSet):
    '''Viewset for Mot-dit objects'''

    model = Photo
    serializer_class = motsdits_serializers.PhotoSerializer
    paginated_serializer = motsdits_serializers.PaginatedPhotoSerializer
    permission_classes = [DefaultPermissions, IsOwnerOrReadOnly]

    def list(self, request):
        '''Lists photos'''

        queryset = sorting.sort(request, self.model.objects.all())
        objects = get_paginated(request, queryset)

        return Response(self.paginated_serializer(objects, context={'request': request}).data)

    def create(self, request):
        '''Create a Photo object'''
        data = request.DATA

        # Allow picture or photo as the key
        try:
            if 'picture' in request.FILES.keys():
                photo_file = request.FILES['picture']
            else:
                photo_file = request.FILES['photo']
        except KeyError:
            return Response({'error': 'Must supply a photo'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        # Create the photo
        photo = Photo.objects.create(
            picture=photo_file,
            motdit=MotDit.objects.get(pk=data['motdit']),
            created_by=request.user
        )

        return Response(self.serializer_class(photo, context={'request': request}).data, status=status.HTTP_201_CREATED)

    @action(methods=['POST', 'DELETE'])
    def like(self, request, pk=None):
        '''Like or unlike a photo'''

        photo = Photo.objects.get(pk=pk)

        # User wants to like this photo
        if request.method == 'POST':
            photo.likes.add(request.user)
            signals.photo_liked.send(request.user.__class__, created_by=request.user, motdit=photo.motdit, photo=photo)
            return Response(status=status.HTTP_201_CREATED)

        # Otherwise we can do a DELETE
        elif request.method == 'DELETE':
            photo.likes.remove(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)


class StoryViewSet(viewsets.ModelViewSet):
    '''Viewset for story objects'''

    model = Story
    serializer_class = motsdits_serializers.StorySerializer
    paginated_serializer = motsdits_serializers.PaginatedStorySerializer
    permission_classes = [DefaultPermissions, IsOwnerOrReadOnly]

    def list(self, request):
        '''Lists stories'''

        queryset = sorting.sort(request, self.model.objects.all())
        objects = get_paginated(request, queryset)

        return Response(self.paginated_serializer(objects, context={'request': request}).data)

    def create(self, request):
        '''Create a Story object'''

        # Create the story
        story = Story.objects.create(
            text=request.DATA['text'],
            motdit=MotDit.objects.get(pk=request.DATA['motdit']),
            created_by=request.user
        )

        return Response(self.serializer_class(story, context={'request': request}).data, status=status.HTTP_201_CREATED)

    @action(methods=['POST', 'DELETE'])
    def like(self, request, pk=None):
        '''Like or unlike a story'''

        story = Story.objects.get(pk=pk)

        # User wants to like this photo
        if request.method == 'POST':
            story.likes.add(request.user)
            signals.story_liked.send(request.user.__class__, created_by=request.user, motdit=story.motdit, story=story)
            return Response(status=status.HTTP_201_CREATED)

        # Otherwise we can do a DELETE
        elif request.method == 'DELETE':
            story.likes.remove(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)


class NewsViewSet(viewsets.ModelViewSet):
    '''Viewset for Mot-dit objects'''

    model = News
    serializer_class = motsdits_serializers.NewsSerializer
    paginated_serializer = motsdits_serializers.PaginatedNewsSerializer

    def list(self, request):
        '''Lists news'''

        queryset = sorting.sort(request, self.model.objects.all())
        objects = get_paginated(request, queryset)

        return Response(self.paginated_serializer(objects, context={'request': request}).data)

    @link()
    def comments(self, request, pk=None):
        '''Retrieves a list of stories related to this item'''
        # @TODO: Add pagination
        serializer = motsdits_compact.PaginatedCompactCommentSerializer

        queryset = sorting.sort(request, Comment.objects.filter(news_item=pk))
        comments = get_paginated(request, queryset)

        return Response(serializer(comments, context={'request': request}).data)


class CommentViewSet(viewsets.ModelViewSet):
    '''Viewset for Mot-dit objects'''

    model = Comment
    serializer_class = motsdits_serializers.CommentSerializer
    paginated_serializer = motsdits_serializers.PaginatedCommentSerializer
    permission_classes = [DefaultPermissions, IsOwnerOrReadOnly]

    def list(self, request):
        '''Lists comments'''

        queryset = sorting.sort(request, self.model.objects.all())
        objects = get_paginated(request, queryset)

        return Response(self.paginated_serializer(objects, context={'request': request}).data)

    def create(self, request):
        '''Create a Comment object'''

        if 'news_item' in request.DATA:
            news_item = request.DATA['news_item']
        else:
            news_item = request.DATA['news']

        # Create the story
        comment = Comment.objects.create(
            text=request.DATA['text'],
            news_item=News.objects.get(pk=news_item),
            created_by=request.user
        )

        return Response(self.serializer_class(comment, context={'request': request}).data, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ModelViewSet):
    '''Returns the subset of public data for the User model'''

    model = get_user_model()
    serializer_class = accounts_serializers.UserSerializer

    @link()
    def news(self, request, pk=None):
        '''Retrieves a list of news items this user has created'''
        serializer = motsdits_serializers.PaginatedNewsSerializer

        queryset = sorting.sort(request, News.objects.filter(created_by=pk))
        news = get_paginated(request, queryset)

        return Response(serializer(news, context={'request': request}).data)

    @link()
    def favourites(self, request, pk=None):
        '''Retrieves a list of motsdits this user has favourited'''
        serializer = motsdits_serializers.PaginatedMotDitSerializer

        queryset = sorting.sort(request, MotDit.objects.filter(favourites=pk))
        motsdits = get_paginated(request, queryset)

        return Response(serializer(motsdits, context={'request': request}).data)

    @link()
    def liked_motsdits(self, request, pk=None):
        '''Retrieves a list of motsdits this user has liked'''
        serializer = motsdits_serializers.PaginatedMotDitSerializer

        queryset = sorting.sort(request, MotDit.objects.filter(likes=pk))
        motsdits = get_paginated(request, queryset)

        return Response(serializer(motsdits, context={'request': request}).data)

    @link()
    def liked_photos(self, request, pk=None):
        '''Retrieves a list of motsdits this user has liked'''
        serializer = motsdits_serializers.PaginatedPhotoSerializer

        queryset = sorting.sort(request, Photo.objects.filter(likes=pk))
        photos = get_paginated(request, queryset)

        return Response(serializer(photos, context={'request': request}).data)

    @link()
    def liked_stories(self, request, pk=None):
        '''Retrieves a list of motsdits this user has liked'''
        serializer = motsdits_serializers.PaginatedStorySerializer

        queryset = sorting.sort(request, Story.objects.filter(likes=pk))
        stories = get_paginated(request, queryset)

        return Response(serializer(stories, context={'request': request}).data)

    @action(methods=['POST', 'DELETE'])
    def follow(self, request, pk=None):
        '''Follow or unfollow a user'''

        user = get_user_model().objects.get(pk=pk)

        if user == request.user:
            return Response({'error': 'You cannot follow yourself'}, status=status.HTTP_403_FORBIDDEN)

        # User wants to like this photo
        if request.method == 'POST':
            user.followers.add(request.user)
            return Response(status=status.HTTP_201_CREATED)

        # Otherwise we can do a DELETE
        elif request.method == 'DELETE':
            user.followers.remove(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @link()
    def following(self, request, pk=None):
        '''Retrieves a list of motsdits this user has liked'''
        serializer = accounts_serializers.PaginatedUserSerializer

        queryset = sorting.sort(request, get_user_model().objects.filter(followers=pk))
        users = get_paginated(request, queryset)

        return Response(serializer(users, context={'request': request}).data)

    @link()
    def followers(self, request, pk=None):
        '''Retrieves a list of motsdits this user has liked'''
        serializer = accounts_serializers.PaginatedUserSerializer

        queryset = sorting.sort(request, get_user_model().objects.filter(following=pk))
        users = get_paginated(request, queryset)

        return Response(serializer(users, context={'request': request}).data)


class UserSelf(APIView):
    '''User self view (convenience function for accessing the acting user)'''

    serializer = accounts_serializers.FullUserSerializer

    def get(self, request):
        '''Retrieves a more in-depth version of the user, since it is the authenticated user'''
        return Response(self.serializer(request.user, context={'request': request}).data)

    def patch(self, request):
        '''Allows for updating of the acting user'''

        try:
            if 'email' in request.DATA:
                EmailValidator()(request.DATA['email'])
                request.user.email = request.DATA['email']

            if 'first_name' in request.DATA:
                if not isinstance(request.DATA['first_name'], basestring):
                    raise ValidationError('first_name must be a string, not {}'.format(type(request.DATA['first_name'])))
                request.user.first_name = request.DATA['first_name']

            if 'last_name' in request.DATA:
                if not isinstance(request.DATA['last_name'], basestring):
                    raise ValidationError('last_name must be a string, not {}'.format(type(request.DATA['last_name'])))
                request.user.last_name = request.DATA['last_name']

            # Finally, save the user
            request.user.save()

            return Response(self.serializer(request.user, context={'request': request}).data)

        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserRegister(APIView):
    '''Register a user'''

    permission_classes = (AllowAny, )

    def post(self, request):
        '''POST a new user object to be registered'''

        try:
            with transaction.atomic():

                # Create a user
                try:
                    user = get_user_model()(
                        email=request.DATA['email'],
                        username=request.DATA['username'],
                        first_name=request.DATA['first_name'],
                        last_name=request.DATA['last_name'],
                    )

                    # Set the password (ensures it gets hashed properly)
                    user.set_password(request.DATA['password'])

                    if 'fb_token' in request.DATA:
                        user.fb_token = request.DATA['fb_token']

                    user.full_clean()
                    user.save()
                except (ValidationError, KeyError) as e:
                    return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

                # Default to sending of the email (otherwise we're doing something funky like tests)
                if request.DATA.get('send_email', True):
                    from django.core.mail import EmailMultiAlternatives

                    link = request.build_absolute_uri(reverse('validate-user', args=[user.validation_code]))
                    subject, from_email, to = 'Verifiez votre compte Mots-dits Quebec', 'accounts@motsditsquebec.com', user.email
                    text_content = 'Pour verifier, cliquez le lien ci-dessus {link}'.format(link=link)
                    html_content = 'Pour verifier, cliquez le lien ci-dessus<br /><br /><a href="{link}">{link}</a>'.format(link=link)
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()

                return Response({'success': True, 'id': user.id}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserValidate(APIView):
    '''Validate a user'''

    serializer = accounts_serializers.FullUserSerializer

    def get(self, request, validation_code=None):
        '''Visit the page of a validation code, and you're valid!'''

        try:
            user = get_user_model().objects.get(validation_code=validation_code)
            user.validated = True
            user.save()

            return Response(self.serializer(user).data)
        except get_user_model().DoesNotExist as e:
            return Response({'success': False, 'message': 'Invalid validation code'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MotDitSearch(APIView):
    '''Searches through mots-dits'''

    serializer = motsdits_serializers.PaginatedMotDitSearchSerializer

    def get(self, request):
        '''Gets a set of mot-dit search results from haystack'''

        query = request.QUERY_PARAMS.get('q')

        # try:
        queryset = SearchQuerySet().filter(SQ(content=query) | SQ(stories=query))
        objects = get_paginated(request, queryset)

        return Response(self.serializer(objects, context={'request': request}).data)
        # except Exception as e:
        #     return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
