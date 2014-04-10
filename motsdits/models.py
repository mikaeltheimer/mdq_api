from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from datetime import datetime
from django.db.models import Q, Count

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
    verb = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.verb)


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

    @property
    def motsdits(self):
        '''Retrieves all the motsdits related to this model'''
        return MotDit.objects.filter(Q(what=self) | Q(where=self))


class MotDit(MDQBaseModel):
    '''Mots-dits are a grouping of action, items and photos'''

    sort_keys = {
        'created': datetime,
        'updated': datetime,
        'name': str,
        'likes': Count('likes'),
        'favourites': Count('favourites')
    }

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

    @property
    def tags(self):
        '''Returns the set of tags related to this motdit'''
        tags = set()

        if self.what:
            tags |= {tag for tag in self.what.tags.all()}
        if self.where:
            tags |= {tag for tag in self.where.tags.all()}

        return list(tags)


class Photo(MDQBaseModel):
    '''Photos for MDQ'''

    sort_keys = {
        'created': datetime,
        'updated': datetime,
        'likes': Count('likes')
    }

    picture = models.FileField(upload_to='motsditsv2')
    motdit = models.ForeignKey(MotDit, related_name='photos')


class Story(MDQBaseModel):
    '''Comment on a Mot-Dit'''

    sort_keys = {
        'created': datetime,
        'updated': datetime,
        'likes': Count('likes')
    }

    text = models.TextField()
    motdit = models.ForeignKey(MotDit, related_name='stories')

    @property
    def teaser(self):
        '''Returns a truncated version of the story'''
        if len(self.text) < 40:
            return self.text
        else:
            return self.text[:40] + '...'


class News(MDQBaseModel):
    '''News item'''

    action = models.CharField(max_length=50, choices=settings.NEWS_TYPE_CHOICES)

    # And related models
    motdit = models.ForeignKey(MotDit)
    photo = models.ForeignKey(Photo, null=True, blank=True)
    story = models.ForeignKey(Story, null=True, blank=True)

    def __str__(self):
        return str(self.action)


class Comment(MDQBaseModel):
    '''News comment'''

    sort_keys = {
        'created': datetime,
        'updated': datetime
    }

    text = models.TextField()
    news_item = models.ForeignKey(News, related_name='comments')

    @property
    def teaser(self):
        '''Returns a truncated version of the story'''
        if len(self.text) < 40:
            return self.text
        else:
            return self.text[:40] + '...'

    def __str__(self):
        return self.teaser
