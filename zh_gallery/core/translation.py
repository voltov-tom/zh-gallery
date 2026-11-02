from modeltranslation.translator import TranslationOptions, register

from .models import About, MainCategory, MediaItem, SubCategory


@register(About)
class AboutTranslationOptions(TranslationOptions):
    fields = ("body",)


@register(MainCategory)
class MainCategoryTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(SubCategory)
class SubCategoryTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "description",
    )


@register(MediaItem)
class MediaItemTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "description",
    )
