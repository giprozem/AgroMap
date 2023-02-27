from modeltranslation.translator import register, TranslationOptions
import simple_history
from .models.conton import Conton
from .models.contour import LandType
from .models.culture import Culture
from .models.district import District
from .models.fertility import Fertility
from .models.orthophoto import OrthoPhoto
from .models.region import Region
from .models.soil import SoilClass, SoilProductivity
from .models.village import Village


@register(Conton)
class ContonTranslationOptions(TranslationOptions):
    fields = ('name', )

simple_history.register(Conton, inherit=True)

@register(LandType)
class LandTypeTranslationOptions(TranslationOptions):
    fields = ('name', )


@register(Culture)
class CultureTranslationOptions(TranslationOptions):
    fields = ('name', )

simple_history.register(Culture, inherit=True)

@register(District)
class DistrictTranslationOptions(TranslationOptions):
    fields = ('name', )

simple_history.register(District, inherit=True)

@register(Fertility)
class FertilityTranslationOptions(TranslationOptions):
    fields = ('name', )

simple_history.register(Fertility, inherit=True)

@register(OrthoPhoto)
class OrthoPhotoTranslationOptions(TranslationOptions):
    fields = ('layer_name', )

simple_history.register(OrthoPhoto, inherit=True)

@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ('name', )

simple_history.register(Region, inherit=True)

@register(SoilClass)
class SoilClassTranslationOptions(TranslationOptions):
    fields = ('name', )

simple_history.register(SoilClass, inherit=True)

@register(SoilProductivity)
class SoilProductivityTranslationOptions(TranslationOptions):
    fields = ('name', )

simple_history.register(SoilProductivity, inherit=True)

@register(Village)
class VillageTranslationOptions(TranslationOptions):
    fields = ('name', )

simple_history.register(Village, inherit=True)