from modeltranslation.translator import register, TranslationOptions
import simple_history
from .models.conton import Conton
from .models.contour import LandType
from .models.culture import Culture
from .models.district import District
from .models.region import Region
from .models.soil import SoilClass, SoilProductivity
from gip.models.soil import SoilClassMap


@register(Conton)
class ContonTranslationOptions(TranslationOptions):
    fields = ('name',)


simple_history.register(Conton, inherit=True)


@register(LandType)
class LandTypeTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Culture)
class CultureTranslationOptions(TranslationOptions):
    fields = ('name',)


simple_history.register(Culture, inherit=True)


@register(District)
class DistrictTranslationOptions(TranslationOptions):
    fields = ('name',)


simple_history.register(District, inherit=True)


@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ('name',)


simple_history.register(Region, inherit=True)


@register(SoilClass)
class SoilClassTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)


simple_history.register(SoilClass, inherit=True)


@register(SoilProductivity)
class SoilProductivityTranslationOptions(TranslationOptions):
    fields = ('name',)


simple_history.register(SoilProductivity, inherit=True)


@register(SoilClassMap)
class SoilClassMapTranslationOptions(TranslationOptions):
    pass
