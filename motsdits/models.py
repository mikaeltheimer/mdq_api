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

    def save(self, *args, **kwargs):
        '''Always set the updated field before saving'''
        self.updated = datetime.utcnow()
        return models.Model.save(self, *args, **kwargs)


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
    display_name = models.CharField(max_length=255, null=True, blank=True)

    # Geo information
    address = models.TextField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)

    # Other identifying information
    website = models.URLField(null=True, blank=True)

    # Tags related to this specific item
    tags = models.ManyToManyField(Tag, null=True, blank=True)

    def __unicode__(self):
        '''Display version'''
        return u"({}) {}".format(self.type, self.name)

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
        'favourites': Count('favourites'),
        'score': int
    }

    action = models.ForeignKey(Action)

    what = models.ForeignKey(Item, related_name='what', null=True)
    where = models.ForeignKey(Item, related_name='where', null=True)

    def __unicode__(self):
        '''Stringified version'''
        return u"{} {} at {}".format(self.action, self.what, self.where)

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

    def recalculate_score(self):
        '''Recalculates the score for this Mot-Dit'''
        # @TODO: move all score calculations here


class Question(MotDit):
    '''A question is identical to a mot-dit except that it gets paired with a set of answer objects'''


class Answer(MDQBaseModel):
    '''An individual answer, tied directly to a MotDit object - tracks creation, creator etc.'''

    question = models.ForeignKey(Question, related_name='answers')
    answer = models.ForeignKey(MotDit, related_name='answer_to')


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
    photo = models.OneToOneField(Photo, null=True, blank=True)

    @property
    def teaser(self):
        '''Returns a truncated version of the story'''
        if len(self.text) < 40:
            return self.text
        else:
            return self.text[:40] + '...'


class News(MDQBaseModel):
    '''News item'''

    sort_keys = {
        'created': datetime,
        'updated': datetime,
        'likes': Count('likes'),
        'score': int
    }

    action = models.CharField(max_length=50, choices=settings.NEWS_TYPE_CHOICES)

    # And related models
    motdit = models.ForeignKey(MotDit, null=True, blank=True)
    photo = models.ForeignKey(Photo, null=True, blank=True)
    story = models.ForeignKey(Story, null=True, blank=True)
    user = models.ForeignKey(get_user_model(), null=True, blank=True, related_name='news_about')

    question = models.ForeignKey(Question, null=True, blank=True, related_name='news_about')
    answer = models.ForeignKey(Answer, null=True, blank=True, related_name='news_about')

    def __unicode__(self):
        return unicode(self.action)


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

    def __unicode__(self):
        return self.teaser
