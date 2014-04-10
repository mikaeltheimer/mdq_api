"""Provides a more generic interface for sorting of querysets

@author Stephen Young
"""
from django.db.models import Count


def sort(request, queryset):
    '''Sorts the queryset using the supplied request and sort keys'''

    if hasattr(queryset.model, 'sort_keys') and request.QUERY_PARAMS.get('order_by') in queryset.model.sort_keys:
        sort_key = request.QUERY_PARAMS.get('order_by')
        if isinstance(queryset.model.sort_keys[sort_key], Count):
            queryset.annotate(annotated_count_value=queryset.model.sort_keys[sort_key])
            sort_key = 'annotated_count_value'

        # Default to descending
        if request.QUERY_PARAMS.get('order', 'desc').lower() != 'asc':
            sort_key = '-{}'.format(sort_key)

        return queryset.order_by(sort_key)

    return queryset
