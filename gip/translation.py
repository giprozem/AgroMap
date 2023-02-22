from modeltranslation.translator import register, TranslationOptions
from .models.conton import Conton


@register(Conton)
class ContonTranslationOptions(TranslationOptions):
    fields = ('name', )

