from modeltranslation.translator import register, TranslationOptions
from ai.models.create_dataset import CreateDescription


@register(CreateDescription)
class CreateDescriptionTranslationOptions(TranslationOptions):
    fields = ('description',)
