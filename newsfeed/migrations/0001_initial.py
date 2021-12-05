# Generated by Django 3.2.6 on 2021-12-05 22:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HelpRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('text_content', models.CharField(max_length=300)),
                ('tags', models.CharField(max_length=300, null=True)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('slug', models.SlugField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_request_help_set', to=settings.AUTH_USER_MODEL)),
                ('responded_users', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responded_request_help_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('author', 'title')},
            },
        ),
    ]