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

from motsdits.models import Action, Item, MotDit, Tag

import serializers.motsdits as motsdits_serializers
import serializers.accounts as accounts_serializers

import filters


class UserViewSet(viewsets.ModelViewSet):
    '''Returns the subset of public data for the User model'''
    model = get_user_model()
    serializer_class = accounts_serializers.UserSerializer
    paginate_by = 25
    paginate_by_param = 'limit'


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

        return Response(serializer(queryset).data)


class ItemAutocomplete(APIView):

    serializer_class = motsdits_serializers.ItemSerializer

    #@decorators.method_decorator(ensure_csrf_cookie)
    def get(self, request, name=None):
        '''Updates a user profile photo'''

        queryset = Item.objects.filter(name__icontains=name)
        return Response(self.serializer_class(queryset).data)


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

    @action(methods=['POST', 'DELETE'])
    def like(self, request, pk=None):
        '''Like or unlike a motdit'''

        # User wants to like this mot-dit
        if request.method == 'POST':
            motdit = MotDit.objects.get(pk=pk)
            motdit.likes.add(request.user)
            return Response(status=status.HTTP_201_CREATED)

        # Otherwise we can do a DELETE
        elif request.method == 'DELETE':
            motdit = MotDit.objects.get(pk=pk)
            motdit.likes.remove(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)

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
