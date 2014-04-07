from rest_framework import serializers
from motsdits.models import Item, Photo, Story, News, Comment

from api.serializers.accounts import compact


class CompactItemSerializer(serializers.ModelSerializer):
    '''Creates a smaller version of an Opinion object'''

    class Meta:
        model = Item
        fields = ('id', 'name', 'score', )


class CompactPhotoSerializer(serializers.ModelSerializer):
    '''Creates a smaller version of a Photo object'''

    url = serializers.SerializerMethodField('get_picture_url')
    created_by = compact.CompactUserSerializer()

    def get_picture_url(self, obj):
        '''Gets the url of the actual picture object'''
        return obj.picture.url

    class Meta:
        model = Photo
        fields = ('id', 'url', 'created_by', 'score', 'motdit', )


class CompactStorySerializer(serializers.ModelSerializer):
    '''Creates a smaller version of a Story object'''

    created_by = compact.CompactUserSerializer()

    class Meta:
        model = Story
        fields = ('id', 'text', 'created_by', 'score', 'motdit', )


class CompactNewsSerializer(serializers.ModelSerializer):
    '''A smaller version of a News object'''

    class Meta:
        model = News
        fields = ('id', 'action', 'created_by', 'score', )


class CompactCommentSerializer(serializers.ModelSerializer):
    '''Creates a smaller version of a Photo object'''

    created_by = compact.CompactUserSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'text', 'created_by', 'score', 'news_item', )
