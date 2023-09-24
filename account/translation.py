from modeltranslation.translator import register, TranslationOptions
from account.models.account import Notifications

# Register the translation options for the Notifications model.
@register(Notifications)
class NotificationsTranslationOptions(TranslationOptions):
    # Specify the fields that should be translated for the Notifications model.
    fields = ('text',)