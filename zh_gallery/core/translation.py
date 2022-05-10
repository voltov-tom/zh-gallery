from modeltranslation.translator import register, TranslationOptions
from .models import About, MainCategory, SubCategory, MediaItem


@register(About)
class AboutTranslationOptions(TranslationOptions):
    fields = 'body',


@register(MainCategory)
class MainCategoryTranslationOptions(TranslationOptions):
    fields = 'title',


@register(SubCategory)
class SubCategoryTranslationOptions(TranslationOptions):
    fields = 'title', 'description',


@register(MediaItem)
class MediaItemTranslationOptions(TranslationOptions):
    fields = 'title', 'description',
