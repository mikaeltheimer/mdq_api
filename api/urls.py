"""API urls
Generates all the necessary viewsets and url configurations to serve the API

@author Stephen Young (me@hownowstephen.com)
"""

from django.conf.urls import url, patterns, include

# Django plugins
from rest_framework import routers
import views

# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'motsdits', views.MotDitViewSet)
router.register(r'items', views.ItemViewSet)
router.register(r'photos', views.PhotoViewSet)
router.register(r'stories', views.StoryViewSet)
router.register(r'news', views.NewsViewSet)
router.register(r'comments', views.CommentViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns(
    '',

    # Custom autocomplete endpoint
    url(r'v2/items/autocomplete/(?P<name>[^/]+)/?', views.ItemAutocomplete.as_view()),
    url(r'v2/users/self/?', views.UserSelf.as_view()),

    # Registration and verification
    url(r'v2/users/register/?', views.UserRegister.as_view()),
    url(r'v2/users/validate/(?P<validation_code>[^/]+)/?', views.UserValidate.as_view()),

    # Basic API
    url(r'v2/', include(router.urls)),
)
