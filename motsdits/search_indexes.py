"""Haystack indexes, to allow searching through models

@author Stephen Young (me@hownowstephen.com)
"""

import datetime
from haystack import indexes
from motsdits.models import MotDit


class MotDitIndex(indexes.SearchIndex, indexes.Indexable):
    '''A searchable index for a MotDit'''

    text = indexes.CharField(document=True, use_template=True)
    stories = indexes.CharField(use_template=True, boost=0.2)

    def get_model(self):
        return MotDit

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(updated__lte=datetime.datetime.now())
