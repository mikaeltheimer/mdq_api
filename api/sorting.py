"""Provides a more generic interface for sorting of querysets

@author Stephen Young
"""

from django.conf import settings
from django.db.models import Count, Q
from motsdits.models import Action, MotDit


def geonear(queryset, lat, lng, distance=100):
    '''Returns a queryset of everything within <distance> of the supplied <lat>,<lng> pair'''

    from django.db import connection
    cursor = connection.cursor()

    cursor.execute("""SELECT id, (
        6371 * acos( cos( radians({lat}) ) * cos( radians( lat ) ) *
        cos( radians( lng ) - radians({lng}) ) + sin( radians({lat}) ) *
        sin( radians( lat ) ) ) )
        AS distance FROM motsdits_item HAVING distance < {distance}
        ORDER BY distance ASC""".format(lat=lat, lng=lng, distance=distance))

    # All IDs of nearby values, sorted by distance to the lat,lng pair
    nearest = [row[0] for row in cursor.fetchall()]

    return queryset.filter(Q(what__in=nearest) | Q(where__in=nearest))


def sort(request, queryset):
    '''Sorts the queryset using the supplied request and sort keys'''

    if queryset.model == MotDit:
        if request.QUERY_PARAMS.get('action'):
            action = Action.objects.get(verb=request.QUERY_PARAMS.get('action'))
            queryset = queryset.filter(action=action)

    if hasattr(queryset.model, 'sort_keys') and request.QUERY_PARAMS.get('order_by') in queryset.model.sort_keys:
        sort_key = request.QUERY_PARAMS.get('order_by')
        if isinstance(queryset.model.sort_keys[sort_key], Count):
            queryset = queryset.annotate(annotated_count_value=queryset.model.sort_keys[sort_key])
            sort_key = 'annotated_count_value'

        # Default to descending
        if request.QUERY_PARAMS.get('order', 'desc').lower() != 'asc':
            sort_key = '-{}'.format(sort_key)
        return queryset.order_by(sort_key)

    # Specific additional parameters to support
    elif request.QUERY_PARAMS.get('nearby') and queryset.model == MotDit:
        # Extract the latitude + longitude
        lat, lng = map(float, request.QUERY_PARAMS.get('nearby').split(','))
        return geonear(queryset, lat, lng, request.QUERY_PARAMS.get('radius', settings.DEFAULT_SEARCH_RADIUS))

    return queryset
