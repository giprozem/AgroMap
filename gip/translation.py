from modeltranslation.translator import register, TranslationOptions
from .models.conton import Conton
from .models.contour import LandType, ContourYear
from .models.culture import Culture
from .models.district import District
from .models.fertility import Fertility
from .models.orthophoto import OrthoPhoto
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


@register(District)
class DistrictTranslationOptions(TranslationOptions):
    fields = ('name', )


@register(Fertility)
class FertilityTranslationOptions(TranslationOptions):
    fields = ('name', )


@register(OrthoPhoto)
class OrthoPhotoTranslationOptions(TranslationOptions):
    fields = ('layer_name', )