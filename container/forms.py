from django.forms import ModelForm

from container.models import ImageBin


class ImageBinForm(ModelForm):
    class Meta:
        model = ImageBin
        fields = ('image', )


class LastImageBinForm(ModelForm):
    class Meta:
        model = ImageBin
        fields = '__all__'
