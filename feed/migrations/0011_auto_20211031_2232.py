# Generated by Django 3.2.8 on 2021-10-31 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0010_alter_parseddata_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parsercategory',
            name='department',
        ),
        migrations.AddField(
            model_name='parser',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='feed.department'),
        ),
    ]
