from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings


def get_paginated(request, queryset):
    '''Retrieves a paginated version of the queryset'''

    per_page = request.QUERY_PARAMS.get(settings.REST_FRAMEWORK['PAGINATE_BY_PARAM'], settings.REST_FRAMEWORK['PAGINATE_BY'])

    if per_page > settings.REST_FRAMEWORK['MAX_PAGINATE_BY']:
        per_page = settings.REST_FRAMEWORK['MAX_PAGINATE_BY']

    paginator = Paginator(queryset, per_page)

    page = request.QUERY_PARAMS.get('page')

    try:
        return paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        return paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999),
        # deliver last page of results.
        return paginator.page(paginator.num_pages)
