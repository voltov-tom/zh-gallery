from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.utils.timezone import now
from slugify import slugify


class MainCategory(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255)

    class Meta:
        verbose_name_plural = 'Main categories'
        ordering = ['title']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f'/{self.slug}'

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
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255)
    image = models.ImageField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Subcategories'
        ordering = ['title']

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}'

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
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField()

    views = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    like_time = models.DateTimeField(auto_now=now())

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Media items'
        ordering = ['title']

    def get_absolute_url(self):
        return f'/{self.subcategory.category.slug}/{self.subcategory.slug}/{self.slug}'

    def __str__(self):
        return f'{self.id}, {self.subcategory}: {self.title}'

    @property
    def total_likes(self):
        return self.likes.count()


class MediaItemReview(models.Model):
    media_item = models.ForeignKey(MediaItem, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return f'{self.media_item}, {self.user}'


class About(models.Model):
    body = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'About'

    def __str__(self):
        return 'About'


@receiver(pre_save, sender=MediaItem)
def delete_old_image_on_update(sender, instance, **kwargs):
    """Удаляет старое изображение при обновлении MediaItem"""
    if instance.pk:  # Если это обновление существующей записи
        try:
            old_instance = MediaItem.objects.get(pk=instance.pk)

            # Если изображение изменилось и старое существует
            if (old_instance.image and
                    instance.image and
                    old_instance.image.name != instance.image.name):
                # Удаляем старое изображение из Nextcloud
                delete_file_from_nextcloud(old_instance.image.name)

        except MediaItem.DoesNotExist:
            pass


@receiver(post_delete, sender=MediaItem)
def delete_image_on_delete(sender, instance, **kwargs):
    """Удаляет изображение при удалении MediaItem"""
    if instance.image and instance.image.name:
        delete_file_from_nextcloud(instance.image.name)


def delete_file_from_nextcloud(filename):
    """Удаляет файл из Nextcloud"""
    from django.conf import settings
    from webdav3.client import Client

    try:
        config = settings.NEXTCLOUD_CONFIG
        client = Client({
            'webdav_hostname': config['webdav_hostname'],
            'webdav_login': config['webdav_login'],
            'webdav_password': config['webdav_password'],
            'webdav_root': config['webdav_root'],
        })

        # Удаляем файл
        client.clean(filename)

    except Exception:
        # Игнорируем ошибки (файл уже удален или недоступен)
        pass
