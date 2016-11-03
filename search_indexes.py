import datetime
from haystack import indexes
from models import Machine


class ModuleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    content_auto = indexes.EdgeNgramField(use_template=True)

    def get_model(self):
        return Machine

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
