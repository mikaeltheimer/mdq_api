"""Signal handlers for Motsdits models
@author Stephen Young (me@hownowstephen.com)
"""

from django.conf import settings
from django.dispatch import receiver, Signal
from motsdits.models import News

# Correspond directly to NEWS_TYPE_CHOICES in settings.py

# Motdit signals
motdit_created = Signal(providing_args=["created_by", "motdit", "photo", "story"])
motdit_updated = Signal(providing_args=["created_by", "motdit"])
motdit_liked = Signal(providing_args=["created_by", "motdit"])
motdit_favourited = Signal(providing_args=["created_by", "motdit"])

# Photo signals
photo_liked = Signal(providing_args=["created_by", "photo"])

# Story signals
story_liked = Signal(providing_args=["created_by", "photo"])


# Signal handlers
@receiver(motdit_created)
def handle_create_motdit(created_by=None, motdit=None, photo=None, story=None, **kwargs):
    '''Handles creation of a motdit, increases score + generates a news item'''

    if created_by and motdit:
        News.objects.create(action=settings.NEWS_CREATED_MOTDIT, created_by=created_by, motdit=motdit, story=story, photo=photo)

        # and update the motdit score
        motdit.score += 1
        motdit.save()


@receiver(motdit_updated)
def handle_update_motdit(created_by=None, motdit=None, **kwargs):
    '''Handles generating news when updating a motdit'''

    if created_by and motdit:
        News.objects.create(action=settings.NEWS_UPDATED_MOTDIT, created_by=created_by, motdit=motdit)


@receiver(motdit_liked)
def handle_like_motdit(created_by=None, motdit=None, **kwargs):
    '''Handles generating news when liking a motdit'''

    if created_by and motdit:
        News.objects.create(action=settings.NEWS_LIKED_MOTDIT, created_by=created_by, motdit=motdit)


@receiver(motdit_favourited)
def handle_favourite_motdit(created_by=None, motdit=None, **kwargs):
    '''Handles generating news when liking a motdit'''

    if created_by and motdit:
        News.objects.create(action=settings.NEWS_FAVOURITED_MOTDIT, created_by=created_by, motdit=motdit)
