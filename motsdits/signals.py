"""Signal handlers for Motsdits models
@author Stephen Young (me@hownowstephen.com)
"""

from django.conf import settings
from django.dispatch import receiver, Signal
from django.db.models.signals import pre_save
from motsdits.models import News, Item

import requests
import json
from unidecode import unidecode


# MODEL SIGNALS
@receiver(pre_save, sender=Item)
def geocode_item(sender, instance, *args, **kwargs):
    '''Ensures that if an item has an address, we try to give it a lat/lng'''

    # Check if the address has changed
    if instance.pk:
        try:
            existing = Item.objects.get(pk=instance.pk)
            address_changed = existing.address == instance.address
        except Item.DoesNotExist:
            address_changed = True
    else:
        # If it's new, the address has necessarily changed
        address_changed = True

    # If the address has changed, or we don't already have a lat/lng pair
    if instance.address and (not instance.lat or not instance.lng or address_changed):

        try:
            # We always geocode in Quebec using google maps, to avoid ambiguity
            url = "http://maps.googleapis.com/maps/api/geocode/json?address={0},Quebec,Canada&sensor=false"
            geocoded = json.loads(requests.get(url.format(unidecode(instance.address.replace(' ', '+')))).content)

            instance.lat = float(geocoded['results'][0]['geometry']['location']['lat'])
            instance.lng = float(geocoded['results'][0]['geometry']['location']['lng'])

        except Exception:
            pass


# CUSTOM SIGNALS FOR NEWS
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

# Question signals
question_asked = Signal(providing_args=["created_by", "question"])
question_answered = Signal(providing_args=["created_by", "question", "answer"])


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

        motdit.score += 1
        motdit.save()


@receiver(photo_liked)
def handle_like_photo(created_by=None, motdit=None, photo=None, **kwargs):
    '''Handles generating news when liking a photo'''

    if created_by and photo:
        News.objects.create(action=settings.NEWS_LIKED_PHOTO, created_by=created_by, motdit=motdit, photo=photo)


@receiver(story_liked)
def handle_like_story(created_by=None, motdit=None, story=None, **kwargs):
    '''Handles generating news when liking a story'''

    if created_by and story:
        News.objects.create(action=settings.NEWS_LIKED_STORY, created_by=created_by, motdit=motdit, story=story)


@receiver(question_asked)
def handle_ask_question(created_by=None, question=None, **kwargs):
    '''Handles generating news when liking a story'''

    if created_by and question:
        News.objects.create(action=settings.NEWS_ASKED_QUESTION, created_by=created_by, question=question)


@receiver(question_answered)
def handle_answer_question(created_by=None, question=None, answer=None, motdit=None, **kwargs):
    '''Handles generating news when liking a story'''

    if created_by and question:
        News.objects.create(action=settings.NEWS_ANSWERED_QUESTION, created_by=created_by, question=question, answer=answer, motdit=motdit)
