# Generated by Django 3.2.8 on 2021-10-31 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0008_auto_20211031_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parseddata',
            name='link',
            field=models.URLField(max_length=500, null=True, unique=True),
        ),
    ]
