from django.db import models


def make_slug_from_name(name):
    return name.lower().replace("_", "-").replace(" ", "").replace("’", "").replace("'", "")


class MainCategory(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    class Meta:
        verbose_name_plural = 'Main categories'
        ordering = ['title']

    def save(self, *args, **kwargs):
        self.slug = make_slug_from_name(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return self.slug

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    category = models.ForeignKey(
        MainCategory,
        related_name='subcategory',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    image = models.ImageField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = make_slug_from_name(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Subcategories'
        ordering = ['title']

    def get_absolute_url(self):
        return self.slug

    def __str__(self):
        return f'{self.category}: {self.title}'


class MediaItem(models.Model):
    subcategory = models.ForeignKey(
        SubCategory,
        related_name='mediaitem',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField()
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = make_slug_from_name(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Media items'
        ordering = ['title']

    def get_absolute_url(self):
        return self.slug

    def __str__(self):
        return f'{self.subcategory}: {self.title}'
