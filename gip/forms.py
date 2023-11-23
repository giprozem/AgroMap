import logging

from django import forms
from django.utils.translation import gettext_lazy as _

from gip.services.shapefile import UploadAndExtractService
from gip.models import Contour


class ShapeFileUploadForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        data = self.cleaned_data["file"]

        if not (data.name.endswith(".zip") or data.name.endswith(".rar")):
            raise forms.ValidationError(_("The file must be a ZIP or RAR archive."))
        try:
            service = UploadAndExtractService(zip_file=data, model=Contour)
            service.execute()
        except Exception as e:
            raise forms.ValidationError(_(str(e)))

        return data


class ShapeFileExportAllData(forms.Form):
    def clean_file(self):
        pass
