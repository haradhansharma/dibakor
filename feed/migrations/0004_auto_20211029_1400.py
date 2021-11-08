# Generated by Django 3.2.8 on 2021-10-29 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0003_alter_parseddata_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('conf_num', models.CharField(max_length=15)),
                ('confirmed', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='parseddata',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='parseddata',
            name='link',
            field=models.CharField(max_length=500, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='parseddata',
            name='pubdate',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='parseddata',
            name='title',
            field=models.CharField(max_length=500, null=True),
        ),
    ]