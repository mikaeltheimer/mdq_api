from motsdits.models import MotDit, Item

from rest_framework import serializers
import accounts_compact
import motsdits_compact


class MotDitSerializer(serializers.ModelSerializer):
    '''Ensures that related objects get serialized'''

    created_by = accounts_compact.CompactUserSerializer()
    what = motsdits_compact.CompactItemSerializer()
    where = motsdits_compact.CompactItemSerializer()

    likes = serializers.SerializerMethodField('count_likes')
    favourites = serializers.SerializerMethodField('count_favourites')

    class Meta:
        model = MotDit
        depth = 1
        fields = ('id', 'created_by', 'what', 'where', 'score', 'likes', 'favourites', )

    def count_favourites(self, obj):
        return obj.favourites.count()

    def count_likes(self, obj):
        return obj.likes.count()


class ItemSerializer(serializers.ModelSerializer):
    '''Ensures that related objects get serialized'''

    created_by = accounts_compact.CompactUserSerializer()

    class Meta:
        model = Item
        depth = 1
        fields = ('id', 'created_by', 'what', 'where', 'score', )
