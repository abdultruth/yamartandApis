# Generated by Django 4.1.2 on 2022-12-14 18:54

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0002_review'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Review',
            new_name='ReviewRating',
        ),
    ]
