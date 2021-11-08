# Generated by Django 3.2.8 on 2021-11-01 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0013_searchrecord_ip'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parser',
            name='department',
        ),
        migrations.AddField(
            model_name='parsercategory',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='feed.department'),
        ),
    ]
