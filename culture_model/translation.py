from modeltranslation.translator import register, TranslationOptions
from .models.phase import Phase
from .models.vegetation_index import VegetationIndex

# Register translation options for the Phase model
@register(Phase)
class PhaseTranslationOptions(TranslationOptions):
    fields = ('name', )

# Register translation options for the VegetationIndex model
@register(VegetationIndex)
class VegetationIndexTranslationOptions(TranslationOptions):
    fields = ('name', 'description')
