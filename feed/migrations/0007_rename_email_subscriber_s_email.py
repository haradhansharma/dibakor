# Generated by Django 3.2.8 on 2021-10-31 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0006_auto_20211031_1640'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscriber',
            old_name='email',
            new_name='s_email',
        ),
    ]
