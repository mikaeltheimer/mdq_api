from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from datetime import datetime


ITEM_TYPE_CHOICES = (
    (settings.WHAT, 'What'),
    (settings.WHERE, 'Where')
)


class MDQBaseModel(models.Model):
    '''Base model for MQD objects'''

    class Meta:
        abstract = True

    # Approval flags, allows us to hide objects
    approved = models.BooleanField(default=True)
    flags = models.IntegerField(default=0)

    # Some timestamps for tracking usage
    created = models.DateTimeField(default=datetime.utcnow)
    updated = models.DateTimeField(default=datetime.utcnow)

    # Everything is created by somebody
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    # Static score, float to allow for some funky scoring models
    score = models.FloatField(default=0)


class Action(MDQBaseModel):
    '''Action objects, should only be created within the admin'''
    verb = models.CharField(max_length=255)

    def __str__(self):
        return self.verb


class Tag(MDQBaseModel):
    '''Tag object, related to items with a M2M'''
    name = models.CharField(max_length=255)


class Item(MDQBaseModel):
    '''A what/where object'''

    # Classify as either a what or a where
    type = models.CharField(max_length=5, choices=ITEM_TYPE_CHOICES)

    # Name of the item
    name = models.CharField(max_length=255)

    # Geo information
    address = models.TextField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)

    # Other identifying information
    website = models.URLField(null=True, blank=True)

    # Tags related to this specific item
    tags = models.ManyToManyField(Tag, null=True, blank=True)

    def __str__(self):
        '''Display version'''
        return "({}) {}".format(self.type, self.name)


class Photo(MDQBaseModel):
    '''Photos for MDQ'''

    picture = models.FileField(upload_to='motsditsv2')


class MotDit(MDQBaseModel):
    '''Mots-dits are a grouping of action, items and photos'''

    action = models.ForeignKey(Action)

    what = models.ForeignKey(Item, related_name='what')
    where = models.ForeignKey(Item, related_name='where')

    def __str__(self):
        '''Stringified version'''
        return "{} {} at {}".format(self.action, self.what, self.where)

    @property
    def favourites(self):
        '''Returns the number of times this mot-dit has been favourited'''
        return get_user_model().objects.filter(favourites=self).count()
