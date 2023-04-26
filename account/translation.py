from modeltranslation.translator import register, TranslationOptions
from account.models.account import Notifications


@register(Notifications)
class NotificationsTranslationOptions(TranslationOptions):
    fields = ('text',)
