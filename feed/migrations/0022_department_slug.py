# Generated by Django 3.2.8 on 2021-11-05 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0021_exsite'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
