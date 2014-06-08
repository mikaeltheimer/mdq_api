from rest_framework import serializers
from django.contrib.auth import get_user_model


class CompactUserSerializer(serializers.ModelSerializer):
    '''Creates a compact version of a User object'''

    avatar = serializers.SerializerMethodField('get_avatar_url')

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'avatar', )

    def get_avatar_url(self, obj):
        '''Gets the url of the actual avatar object'''
        if obj.avatar:
            return obj.avatar.url
