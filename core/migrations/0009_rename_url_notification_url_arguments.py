# Generated by Django 3.2.6 on 2021-12-07 22:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20211207_2117'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='url',
            new_name='url_arguments',
        ),
    ]