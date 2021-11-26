# Generated by Django 3.2.6 on 2021-11-25 14:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipofday',
            name='responded_users',
            field=models.ManyToManyField(related_name='responded_users', to=settings.AUTH_USER_MODEL),
        ),
    ]