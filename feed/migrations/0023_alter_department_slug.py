# Generated by Django 3.2.8 on 2021-11-05 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0022_department_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='slug',
            field=models.SlugField(default='', unique=True),
            preserve_default=False,
        ),
    ]