# Generated by Django 3.2.6 on 2021-12-05 22:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('communities', '0020_rename_requestforhelp_helprequest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='helprequest',
            name='responded_users',
        ),
        migrations.AddField(
            model_name='helprequest',
            name='responded_users',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responded_request_help_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
