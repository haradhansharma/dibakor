# Generated by Django 3.2.8 on 2021-11-04 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0018_alter_parser_ic_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='blocks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.ImageField(upload_to='blocks')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('position', models.CharField(max_length=256)),
            ],
        ),
    ]
