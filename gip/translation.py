from modeltranslation.translator import register, TranslationOptions
import simple_history
from gip.models.conton import Conton
from gip.models.contour import LandType
from gip.models.culture import Culture
from gip.models.district import District
from gip.models.region import Region
from gip.models.soil import SoilClass, SoilProductivity, SoilClassMap
from gip.models.contact_information import Department, ContactInformation


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


@register(Department)
class SoilProductivityTranslationOptions(TranslationOptions):
    fields = ('name', )


@register(ContactInformation)
class SoilProductivityTranslationOptions(TranslationOptions):
    fields = ('title', 'address')
