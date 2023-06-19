from modeltranslation.translator import register, TranslationOptions
import simple_history
from .models.actual_veg_index import IndexMeaning
from .models.actual_veg_index_logs import IndexCreatingReport
from .models.pasture import ProductivityClass
from .models.satelliteimage import SatelliteImageSource, SatelliteImageBand


@register(IndexMeaning)
class IndexMeaningTranslationOptions(TranslationOptions):
    fields = ('description',)


@register(IndexCreatingReport)
class IndexCreatingReportTranslationOptions(TranslationOptions):
    fields = ('process_error',)


@register(ProductivityClass)
class ProductivityClassTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


simple_history.register(ProductivityClass, inherit=True)


@register(SatelliteImageSource)
class SatelliteImageSourceTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(SatelliteImageBand)
class SatelliteImageBandTranslationOptions(TranslationOptions):
    fields = ('band_name', 'band_description')
