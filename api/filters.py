from django import forms
import django_filters
from motsdits.models import Item


class AutocompleteFilter(django_filters.Filter):
    '''Provides sorting params'''

    field_class = forms.CharField

    def filter(self, qs, value):
        '''Searches for the query'''
        if value.strip():
            qs = qs.filter(name__istartswith=value)

        return qs


class UserFilter(django_filters.FilterSet):

    name = AutocompleteFilter(name='autocomplete', label='autocomplete')

    class Meta:
        model = Item
        fields = ['name']
