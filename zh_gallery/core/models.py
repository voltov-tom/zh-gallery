from django.db import models


class MainCategory(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    class Meta:
        verbose_name_plural = 'Main categories'
        ordering = ['title']

    def get_absolute_url(self):
        return self.slug

    def __str__(self):
        return self.title


class MediaItem(models.Model):
    category = models.ForeignKey(MainCategory, related_name='media_item', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField()
    description = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255)

    def get_absolute_url(self):
        return self.slug

    def __str__(self):
        return self.title
