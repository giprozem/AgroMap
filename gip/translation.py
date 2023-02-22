from modeltranslation.translator import register, TranslationOptions
from .models.conton import Conton
from .models.contour import LandType, ContourYear
from .models.culture import Culture

@register(Conton)
class ContonTranslationOptions(TranslationOptions):
    fields = ('name', )


@register(LandType)
class LandTypeTranslationOptions(TranslationOptions):
    fields = ('name', )


@register(ContourYear)
class ContourYearTranslationOptions(TranslationOptions):
    fields = ('productivity', )


@register(Culture)
class CultureTranslationOptions(TranslationOptions):
    fields = ('name', )