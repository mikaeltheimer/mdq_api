from rest_framework import serializers, pagination
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    '''Creates a compact version of a User object'''

    avatar = serializers.SerializerMethodField('get_avatar_url')

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'avatar', )

    def get_avatar_url(self, obj):
        '''Gets the url of the actual avatar object'''
        if obj.avatar:
            return obj.avatar.url


class PaginatedUserSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = UserSerializer


class FullUserSerializer(serializers.ModelSerializer):
    '''Creates a full version of a User object (to display only to the acting user)'''

    avatar = serializers.SerializerMethodField('get_avatar_url')

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'avatar', )

    def get_avatar_url(self, obj):
        '''Gets the url of the actual avatar object'''
        if obj.avatar:
            return obj.avatar.url
