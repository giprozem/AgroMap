from modeltranslation.translator import register, TranslationOptions
import simple_history
from gip.models.conton import Conton
from gip.models.contour import LandType
from gip.models.culture import Culture, CultureType
from gip.models.district import District
from gip.models.region import Region
from gip.models.soil import SoilClass, SoilProductivity, SoilClassMap
from gip.models.contact_information import Department, ContactInformation


# Register translation options for the "Conton" model.
@register(Conton)
class ContonTranslationOptions(TranslationOptions):
    fields = ('name',)

# Register the "Conton" model with simple history for version tracking.
simple_history.register(Conton, inherit=True)

# Register translation options for the "LandType" model.
@register(LandType)
class LandTypeTranslationOptions(TranslationOptions):
    fields = ('name',)

# Register translation options for the "Culture" model.
@register(Culture)
class CultureTranslationOptions(TranslationOptions):
    fields = ('name',)

# Register the "Culture" model with simple history for version tracking.
simple_history.register(Culture, inherit=True)

# Register translation options for the "District" model.
@register(District)
class DistrictTranslationOptions(TranslationOptions):
    fields = ('name',)

# Register the "District" model with simple history for version tracking.
simple_history.register(District, inherit=True)

# Register translation options for the "Region" model.
@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ('name',)

# Register the "Region" model with simple history for version tracking.
simple_history.register(Region, inherit=True)

# Register translation options for the "SoilClass" model.
@register(SoilClass)
class SoilClassTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)

# Register the "SoilClass" model with simple history for version tracking.
simple_history.register(SoilClass, inherit=True)

# Register translation options for the "SoilProductivity" model.
@register(SoilProductivity)
class SoilProductivityTranslationOptions(TranslationOptions):
    fields = ('name',)

# Register the "SoilProductivity" model with simple history for version tracking.
simple_history.register(SoilProductivity, inherit=True)

# Register translation options for the "SoilClassMap" model.
@register(SoilClassMap)
class SoilClassMapTranslationOptions(TranslationOptions):
    pass

# Register translation options for the "Department" model.
@register(Department)
class SoilProductivityTranslationOptions(TranslationOptions):
    fields = ('name',)

# Register translation options for the "ContactInformation" model.
@register(ContactInformation)
class SoilProductivityTranslationOptions(TranslationOptions):
    fields = ('title', 'address')

@register(CultureType)
class CultureTypeTranslationOptions(TranslationOptions):
    fields = ("name", )