# Generated by Django 3.2.8 on 2021-11-01 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0011_auto_20211031_2232'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.CharField(max_length=256)),
            ],
        ),
    ]
