# Generated by Django 3.2.8 on 2021-12-28 05:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_posts'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Posts',
            new_name='Post',
        ),
    ]
