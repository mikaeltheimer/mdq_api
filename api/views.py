"""API views
Generates all the necessary viewsets to serve the API

@author Stephen Young (me@hownowstephen.com)
"""

from django.contrib.auth import get_user_model
from django.conf import settings

# Django plugins
from rest_framework import viewsets, status
from rest_framework.decorators import link, action
import rest_framework.filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from motsdits.models import Action, Item, MotDit, Tag, Photo, Story, News, Comment

import serializers.motsdits as motsdits_serializers
import serializers.motsdits.compact as motsdits_compact
import serializers.accounts as accounts_serializers

import filters


class ItemViewSet(viewsets.ModelViewSet):
    '''Viewset for Mot-dit objects'''
    model = Item
    serializer_class = motsdits_serializers.ItemSerializer
    filter_backends = (rest_framework.filters.DjangoFilterBackend, )

    @link()
    def related(self, request, pk=None):
        '''Recommend the motdit'''

        serializer = motsdits_serializers.MotDitSerializer
        queryset = MotDit.objects.filter(Q(what=pk) | Q(where=pk))

        return Response(serializer(queryset, many=True).data)

    @link()
    def photos(self, request, pk=None):
        '''Retrieves a list of photos related to this item'''

        # @TODO: Add pagination
        serializer = motsdits_compact.CompactPhotoSerializer
        queryset = Photo.objects.filter(Q(motdit__what=pk) | Q(motdit__where=pk))

        return Response(serializer(queryset, many=True).data)


class ItemAutocomplete(APIView):
    '''Item Autocomplete view'''

    #@decorators.method_decorator(ensure_csrf_cookie)
    def get(self, request, name=None):
        '''Provides the autocomplete action for items'''
        # @TODO: add filter params
        return Response([item.name for item in Item.objects.filter(name__icontains=name)[:10]])


def resolve_item(value, item_type, user=None):
    '''Given a value supplied to the API, resolve it to a discrete Item object'''

    item = None

    if isinstance(value, int):
        item = Item.objects.get(pk=value)
    elif value is not None:
        try:
            item = Item.objects.get(type=item_type, name__iexact=value)
        except Item.DoesNotExist:
            item = Item.objects.create(
                type=item_type,
                name=value,
                created_by=user
            )

    return item


class MotDitViewSet(viewsets.ModelViewSet):
    '''Viewset for Mot-dit objects'''
    model = MotDit
    serializer_class = motsdits_serializers.MotDitSerializer
    paginate_by = 25
    paginate_by_param = 'limit'

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
            return Response(status=status.HTTP_201_CREATED)

        # Otherwise we can do a DELETE
        elif request.method == 'DELETE':
            motdit.favourites.remove(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @link()
    def photos(self, request, pk=None):
        '''Retrieves a list of photos related to this item'''
        # @TODO: Add pagination
        serializer = motsdits_compact.CompactPhotoSerializer
        queryset = Photo.objects.filter(motdit=pk)
        return Response(serializer(queryset, many=True).data)

    @link()
    def stories(self, request, pk=None):
        '''Retrieves a list of stories related to this item'''
        # @TODO: Add pagination
        serializer = motsdits_compact.CompactStorySerializer
        queryset = Story.objects.filter(motdit=pk)
        return Response(serializer(queryset, many=True).data)

    def create(self, request):
        '''Create a MotDit object'''
        data = request.DATA

        # action
        if isinstance(data.get('action'), int):
            verb = Action.objects.get(pk=data['action'])
        elif isinstance(data.get('action'), basestring):
            verb = Action.objects.get(verb=data['action'])
        else:
            return Response({'error': 'Must supply an action'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        # Get the related what an where items
        what = resolve_item(data.get('what'), settings.WHAT, user=request.user)
        where = resolve_item(data.get('where'), settings.WHERE, user=request.user)

        if not what and not where:
            return Response({'error': 'Must supply at least one of what or where'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        # Create the motdit
        motdit, created = MotDit.objects.get_or_create(
            action=verb,
            what=what,
            where=where,
            defaults={
                'created_by': request.user
            }
        )

        if not created:
            # @TODO: Increase score every time this happens!
            pass

        if isinstance(data.get('tags', []), list):
            for tag_name in data.get('tags', []):
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
        else:
            return Response({'error': 'Tags must be supplied as a list of strings'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        return Response(self.serializer_class(motdit).data, status=status.HTTP_201_CREATED)


class PhotoViewSet(viewsets.ModelViewSet):
    '''Viewset for Mot-dit objects'''

    model = Photo
    serializer_class = motsdits_serializers.PhotoSerializer
    paginate_by = 25
    paginate_by_param = 'limit'

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

        return Response(self.serializer_class(photo).data, status=status.HTTP_201_CREATED)

    @action(methods=['POST', 'DELETE'])
    def like(self, request, pk=None):
        '''Like or unlike a photo'''

        photo = Photo.objects.get(pk=pk)

        # User wants to like this photo
        if request.method == 'POST':
            photo.likes.add(request.user)
            return Response(status=status.HTTP_201_CREATED)

        # Otherwise we can do a DELETE
        elif request.method == 'DELETE':
            photo.likes.remove(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)


class StoryViewSet(viewsets.ModelViewSet):
    '''Viewset for Mot-dit objects'''

    model = Story
    serializer_class = motsdits_serializers.StorySerializer
    paginate_by = 25
    paginate_by_param = 'limit'

    def create(self, request):
        '''Create a Story object'''

        # Create the story
        story = Story.objects.create(
            text=request.DATA['text'],
            motdit=MotDit.objects.get(pk=request.DATA['motdit']),
            created_by=request.user
        )

        return Response(self.serializer_class(story).data, status=status.HTTP_201_CREATED)

    @action(methods=['POST', 'DELETE'])
    def like(self, request, pk=None):
        '''Like or unlike a story'''

        story = Story.objects.get(pk=pk)

        # User wants to like this photo
        if request.method == 'POST':
            story.likes.add(request.user)
            return Response(status=status.HTTP_201_CREATED)

        # Otherwise we can do a DELETE
        elif request.method == 'DELETE':
            story.likes.remove(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)


class NewsViewSet(viewsets.ModelViewSet):
    '''Viewset for Mot-dit objects'''

    model = News
    serializer_class = motsdits_serializers.NewsSerializer
    paginate_by = 25
    paginate_by_param = 'limit'

    @link()
    def comments(self, request, pk=None):
        '''Retrieves a list of stories related to this item'''
        # @TODO: Add pagination
        serializer = motsdits_compact.CompactCommentSerializer
        queryset = Comment.objects.filter(news_item=pk)
        return Response(serializer(queryset, many=True).data)


class CommentViewSet(viewsets.ModelViewSet):
    '''Viewset for Mot-dit objects'''

    model = Comment
    serializer_class = motsdits_serializers.CommentSerializer
    paginate_by = 25
    paginate_by_param = 'limit'

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

        return Response(self.serializer_class(comment).data, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ModelViewSet):
    '''Returns the subset of public data for the User model'''

    model = get_user_model()
    serializer_class = accounts_serializers.UserSerializer
    paginate_by = 25
    paginate_by_param = 'limit'

    @link()
    def likes__motsdits(self, request, pk=None):
        '''Retrieves a list of motsdits this user has liked'''
        # @TODO: Add pagination
        serializer = motsdits_serializers.MotDitSerializer
        queryset = MotDit.objects.filter(likes=pk)
        return Response(serializer(queryset, many=True).data)

    @link()
    def likes__photos(self, request, pk=None):
        '''Retrieves a list of motsdits this user has liked'''
        # @TODO: Add pagination
        serializer = motsdits_serializers.PhotoSerializer
        queryset = Photo.objects.filter(likes=pk)
        return Response(serializer(queryset, many=True).data)

    @link()
    def likes__stories(self, request, pk=None):
        '''Retrieves a list of motsdits this user has liked'''
        # @TODO: Add pagination
        serializer = motsdits_serializers.StorySerializer
        queryset = Story.objects.filter(likes=pk)
        return Response(serializer(queryset, many=True).data)

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
