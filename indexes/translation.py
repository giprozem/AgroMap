from modeltranslation.translator import register, TranslationOptions
import simple_history
from .models.actual_veg_index import IndexMeaning
from .models.actual_veg_index_logs import IndexCreatingReport
from .models.pasture import ProductivityClass
from .models.satelliteimage import SatelliteImageSource, SatelliteImageBand


@register(IndexMeaning)
class IndexMeaningTranslationOptions(TranslationOptions):
    """
    Defines the fields of the IndexMeaning model that need to be translated.
    """
    fields = ('description',)


@register(IndexCreatingReport)
class IndexCreatingReportTranslationOptions(TranslationOptions):
    """
    Defines the fields of the IndexCreatingReport model that need to be translated.
    """
    fields = ('process_error',)


@register(ProductivityClass)
class ProductivityClassTranslationOptions(TranslationOptions):
    """
    Defines the fields of the ProductivityClass model that need to be translated.
    """
    fields = ('name', 'description')


simple_history.register(ProductivityClass, inherit=True)


@register(SatelliteImageSource)
class SatelliteImageSourceTranslationOptions(TranslationOptions):
    """
    Defines the fields of the SatelliteImageSource model that need to be translated.
    """
    fields = ('name', 'description')


@register(SatelliteImageBand)
class SatelliteImageBandTranslationOptions(TranslationOptions):
    """
    Defines the fields of the SatelliteImageBand model that need to be translated.
    """
    fields = ('band_name', 'band_description')
