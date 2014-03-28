"""API urls
Generates all the necessary viewsets and url configurations to serve the API

@author Stephen Young (me@hownowstephen.com)
"""

from django.contrib.auth import get_user_model

# Django plugins
from rest_framework import viewsets
from rest_framework.decorators import link
import rest_framework.filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from motsdits.models import Item, MotDit

import serializers.accounts_full
import serializers.motsdits_full

import filters


class UserViewSet(viewsets.ModelViewSet):
    '''Returns the subset of public data for the User model'''
    model = get_user_model()
    serializer_class = serializers.accounts_full.UserSerializer
    paginate_by = 25
    paginate_by_param = 'limit'


class ItemViewSet(viewsets.ModelViewSet):
    '''Viewset for Mot-dit objects'''
    model = Item
    serializer_class = serializers.motsdits_full.ItemSerializer
    filter_backends = (rest_framework.filters.DjangoFilterBackend, )

    @link()
    def related(self, request, pk=None):
        '''Recommend the motdit'''

        serializer = serializers.motsdits_full.MotDitSerializer
        queryset = MotDit.objects.filter(Q(what=pk) | Q(where=pk))

        return Response(serializer(queryset).data)


class ItemAutocomplete(APIView):

    serializer_class = serializers.motsdits_full.ItemSerializer

    #@decorators.method_decorator(ensure_csrf_cookie)
    def get(self, request, name=None):
        '''Updates a user profile photo'''
        queryset = Item.objects.filter(name__istartswith=name)
        return Response(self.serializer_class(queryset).data)


class MotDitViewSet(viewsets.ModelViewSet):
    '''Viewset for Mot-dit objects'''
    model = MotDit
    serializer_class = serializers.motsdits_full.MotDitSerializer
    paginate_by = 25
    paginate_by_param = 'limit'
