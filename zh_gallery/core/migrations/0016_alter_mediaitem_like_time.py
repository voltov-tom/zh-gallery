from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_alter_mediaitem_like_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediaitem',
            name='like_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
