# Generated by Django 3.1.2 on 2020-11-08 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_pints'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pints',
            old_name='pint_user',
            new_name='user',
        ),
    ]
