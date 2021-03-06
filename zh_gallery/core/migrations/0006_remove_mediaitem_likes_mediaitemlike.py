# Generated by Django 4.0 on 2022-01-15 14:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0005_mediaitemreview'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mediaitem',
            name='likes',
        ),
        migrations.CreateModel(
            name='MediaItemLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked', models.ManyToManyField(related_name='user_like', to=settings.AUTH_USER_MODEL)),
                ('media_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes',
                                                 to='core.mediaitem')),
            ],
        ),
    ]
