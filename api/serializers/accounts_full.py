from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    '''Creates a compact version of a User object'''

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', )
