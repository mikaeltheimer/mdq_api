from rest_framework import serializers
from rest_framework import pagination

from motsdits.models import MotDit, Item, Answer, Photo, Story, News, Comment

from api.serializers.accounts import compact


class CompactItemSerializer(serializers.ModelSerializer):
    '''Creates a smaller version of an Opinion object'''

    class Meta:
        model = Item
        fields = ('id', 'name', 'score', )


class PaginatedCompactItemSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = CompactItemSerializer


class CompactMotDitSerializer(serializers.ModelSerializer):
    '''Serializer for mots-dits, less verbose'''

    action = serializers.SerializerMethodField('action_verb')
    what = CompactItemSerializer()
    where = CompactItemSerializer()

    likes = serializers.SerializerMethodField('count_likes')
    favourites = serializers.SerializerMethodField('count_favourites')
    user_likes = serializers.SerializerMethodField('does_user_like')

    class Meta:
        model = MotDit
        depth = 1
        fields = (
            'id',
            'action', 'what', 'where',
            'score', 'likes', 'favourites',
            'user_likes'
        )

    def does_user_like(self, obj):
        '''Check if the user likes this object'''
        if self.context.get('request'):
            return self.context['request'].user in obj.likes.all()

    def count_favourites(self, obj):
        '''Return the count of users that have favourited this motdit'''
        return obj.favourites.count()

    def count_likes(self, obj):
        '''Returns the count of users that like this motdit'''
        return obj.likes.count()

    def action_verb(self, obj):
        '''Flattens the action to just the verb'''
        return obj.action.verb


class PaginatedCompactMotDitSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = CompactMotDitSerializer


class CompactAnswerSerializer(serializers.ModelSerializer):
    '''Creates a small version of an Answer object'''

    created_by = compact.CompactUserSerializer()
    answer = CompactMotDitSerializer()

    class Meta:
        model = Answer
        fields = ('id', 'created_by', 'score', 'answer', )


class PaginatedCompactAnswerSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = CompactAnswerSerializer


class PhotoStorySerializer(serializers.ModelSerializer):
    '''A Story serializer specific to the story/photo relationship'''

    created_by = compact.CompactUserSerializer()
    user_likes = serializers.SerializerMethodField('does_user_like')

    class Meta:
        model = Story
        fields = ('id', 'text', 'created_by', 'score', 'user_likes', )

    def does_user_like(self, obj):
        '''Check if the user likes this object'''
        if self.context.get('request'):
            return self.context['request'].user in obj.likes.all()


class CompactPhotoSerializer(serializers.ModelSerializer):
    '''Creates a smaller version of a Photo object'''

    url = serializers.SerializerMethodField('get_picture_url')
    created_by = compact.CompactUserSerializer()

    user_likes = serializers.SerializerMethodField('does_user_like')
    story = PhotoStorySerializer()

    def get_picture_url(self, obj):
        '''Gets the url of the actual picture object'''
        return obj.picture.url

    class Meta:
        model = Photo
        fields = ('id', 'url', 'created_by', 'score', 'motdit', 'user_likes', 'story')

    def does_user_like(self, obj):
        '''Check if the user likes this object'''
        if self.context.get('request'):
            return self.context['request'].user in obj.likes.all()


class PaginatedCompactPhotoSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = CompactPhotoSerializer


class StoryPhotoSerializer(CompactPhotoSerializer):
    '''A photo serializer specific to the story/photo relationship'''

    class Meta:
        model = Photo
        fields = ('id', 'url', 'created_by', 'score', 'user_likes', )


class CompactStorySerializer(serializers.ModelSerializer):
    '''Creates a smaller version of a Story object'''

    created_by = compact.CompactUserSerializer()
    user_likes = serializers.SerializerMethodField('does_user_like')
    photo = StoryPhotoSerializer()

    class Meta:
        model = Story
        fields = ('id', 'text', 'created_by', 'score', 'motdit', 'user_likes', 'photo', )

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
