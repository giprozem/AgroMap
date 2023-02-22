from modeltranslation.translator import register, TranslationOptions
from .models.phase import Phase
from .models.vegetation_index import VegetationIndex


@register(Phase)
class PhaseTranslationOptions(TranslationOptions):
    fields = ('name', )


@register(VegetationIndex)
class VegetationIndexTranslationOptions(TranslationOptions):
    fields = ('name', 'description')
