# Generated by Django 3.2.8 on 2021-10-29 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0004_auto_20211029_1400'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('subject', models.CharField(max_length=150)),
                ('contents', models.FileField(upload_to='uploaded_newsletters/')),
            ],
        ),
    ]
