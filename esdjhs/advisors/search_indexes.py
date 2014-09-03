import datetime
from haystack import indexes
from advisors.models import Advisor


class AdvisorIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=False)
    first_name = indexes.CharField(model_attr='first_name')
    last_name = indexes.CharField(model_attr='last_name')
    crd = indexes.IntegerField(model_attr='crd')
    pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Advisor

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())
