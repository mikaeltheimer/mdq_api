from rest_framework import serializers, pagination
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    '''Creates a compact version of a User object'''

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', )


class PaginatedMotDitSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = UserSerializer


class FullUserSerializer(serializers.ModelSerializer):
    '''Creates a full version of a User object (to display only to the acting user)'''

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'email', )
