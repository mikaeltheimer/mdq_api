from motsdits.models import MotDit, Item, Photo

from rest_framework import serializers

import api.serializers.accounts.compact as accounts_compact
import compact as motsdits_compact


class MotDitSerializer(serializers.ModelSerializer):
    '''Ensures that related objects get serialized'''

    created_by = accounts_compact.CompactUserSerializer()

    action = serializers.SerializerMethodField('action_verb')
    what = motsdits_compact.CompactItemSerializer()
    where = motsdits_compact.CompactItemSerializer()

    likes = serializers.SerializerMethodField('count_likes')
    favourites = serializers.SerializerMethodField('count_favourites')

    tags = serializers.SerializerMethodField('aggregate_tags')

    class Meta:
        model = MotDit
        depth = 1
        fields = (
            'id', 'created_by',
            'action', 'what', 'where',
            'score', 'likes', 'favourites',
            'tags',
        )

    def count_favourites(self, obj):
        '''Return the count of users that have favourited this motdit'''
        return obj.favourites.count()

    def count_likes(self, obj):
        '''Returns the count of users that like this motdit'''
        return obj.likes.count()

    def action_verb(self, obj):
        '''Flattens the action to just the verb'''
        return obj.action.verb

    def aggregate_tags(self, obj):
        '''Aggregates all the tags for the motdit'''
        tags = set()

        if obj.what:
            tags |= {tag.name for tag in obj.what.tags.all()}
        if obj.where:
            tags |= {tag.name for tag in obj.where.tags.all()}

        return list(tags)


class ItemSerializer(serializers.ModelSerializer):
    '''Ensures that related objects get serialized'''

    created_by = accounts_compact.CompactUserSerializer()

    class Meta:
        model = Item
        depth = 1
        fields = ('id', 'name', 'address', 'website', 'tags', 'created_by', 'score', )


class PhotoSerializer(serializers.ModelSerializer):
    '''Serializes the photo object'''

    url = serializers.SerializerMethodField('get_picture_url')
    motdit = MotDitSerializer()
    created_by = accounts_compact.CompactUserSerializer()

    def get_picture_url(self, obj):
        '''Gets the url of the actual picture object'''
        return obj.picture.url

    class Meta:
        model = Photo
        depth = 1
        fields = ('id', 'url', 'created_by', 'motdit', )
