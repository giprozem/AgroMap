from django.forms import ModelForm, Textarea
from indexes.models import IndexMeaning, IndexFact


class IndexMeaningForm(ModelForm):
    class Meta:
        model = IndexMeaning
        fields = '__all__'
        widgets = {
            'description': Textarea(attrs={'cols': 40, 'rows': 10})
        }
