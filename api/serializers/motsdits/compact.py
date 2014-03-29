from rest_framework import serializers
from motsdits.models import Item


class CompactItemSerializer(serializers.ModelSerializer):
    '''Creates a smaller version of an Opinion object'''

    class Meta:
        model = Item
        fields = ('id', 'name', 'score', )
