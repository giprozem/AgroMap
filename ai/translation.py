# Import necessary modules and classes from modeltranslation
from modeltranslation.translator import register, TranslationOptions
from ai.models.create_dataset import CreateDescription

# Register translation options for the CreateDescription model
@register(CreateDescription)
class CreateDescriptionTranslationOptions(TranslationOptions):
    # Specify the fields that should be translated
    fields = ('description',)
