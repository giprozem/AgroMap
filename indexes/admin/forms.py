from django.forms import ModelForm, Textarea
from indexes.models import IndexMeaning


# Define the ModelForm
class IndexMeaningForm(ModelForm):
    class Meta:
        model = IndexMeaning  # The model this form is tied to
        fields = '__all__'  # Include all fields from the model in the form
        widgets = {
            'description': Textarea(attrs={'cols': 40, 'rows': 10})
        }
