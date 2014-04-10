from rest_framework import serializers
from rest_framework import pagination

from motsdits.models import Item, Photo, Story, News, Comment

from api.serializers.accounts import compact


class CompactItemSerializer(serializers.ModelSerializer):
    '''Creates a smaller version of an Opinion object'''

    class Meta:
        model = Item
        fields = ('id', 'name', 'score', )


class PaginatedCompactItemSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = CompactItemSerializer


class CompactPhotoSerializer(serializers.ModelSerializer):
    '''Creates a smaller version of a Photo object'''

    url = serializers.SerializerMethodField('get_picture_url')
    created_by = compact.CompactUserSerializer()

    user_likes = serializers.SerializerMethodField('does_user_like')

    def get_picture_url(self, obj):
        '''Gets the url of the actual picture object'''
        return obj.picture.url

    class Meta:
        model = Photo
        fields = ('id', 'url', 'created_by', 'score', 'motdit', 'user_likes')

    def does_user_like(self, obj):
        '''Check if the user likes this object'''
        if self.context.get('request'):
            return self.context['request'].user in obj.likes.all()


class PaginatedCompactPhotoSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = CompactPhotoSerializer


class CompactStorySerializer(serializers.ModelSerializer):
    '''Creates a smaller version of a Story object'''

    created_by = compact.CompactUserSerializer()
    user_likes = serializers.SerializerMethodField('does_user_like')

    class Meta:
        model = Story
        fields = ('id', 'text', 'created_by', 'score', 'motdit', 'user_likes', )

    def does_user_like(self, obj):
        '''Check if the user likes this object'''
        if self.context.get('request'):
            return self.context['request'].user in obj.likes.all()


class PaginatedCompactStorySerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = CompactStorySerializer


class CompactNewsSerializer(serializers.ModelSerializer):
    '''A smaller version of a News object'''

    class Meta:
        model = News
        fields = ('id', 'action', 'created_by', 'score', )


class PaginatedCompactNewsSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = CompactNewsSerializer


class CompactCommentSerializer(serializers.ModelSerializer):
    '''Creates a smaller version of a Photo object'''

    created_by = compact.CompactUserSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'text', 'created_by', 'score', 'news_item', )


class PaginatedCompactCommentSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = CompactCommentSerializer
