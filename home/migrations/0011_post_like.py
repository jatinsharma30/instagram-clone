# Generated by Django 3.2.8 on 2022-01-01 20:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_delete_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='like',
            field=models.ManyToManyField(related_name='like', to=settings.AUTH_USER_MODEL),
        ),
    ]
