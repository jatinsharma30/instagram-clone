# Generated by Django 3.2.8 on 2021-12-31 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_follow'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follow',
            old_name='follows',
            new_name='follow',
        ),
    ]
