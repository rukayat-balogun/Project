# Generated by Django 4.2.16 on 2024-11-12 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='title',
            field=models.CharField(blank=True, help_text='Title of the image', max_length=100),
        ),
    ]
