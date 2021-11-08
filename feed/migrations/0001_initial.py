# Generated by Django 3.2.8 on 2021-10-27 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Parser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parser_type', models.CharField(choices=[('rss', 'RSS'), ('youtube', 'Youtube'), ('url', 'URL')], default='rss', max_length=500)),
                ('feed_name', models.CharField(max_length=256)),
                ('feed_url', models.URLField()),
                ('activate', models.BooleanField(default=True)),
            ],
        ),
    ]