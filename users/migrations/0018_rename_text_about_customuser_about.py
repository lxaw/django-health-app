# Generated by Django 3.2.10 on 2022-01-03 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_alter_customuser_is_pod_plus_member'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='text_about',
            new_name='about',
        ),
    ]