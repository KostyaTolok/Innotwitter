# Generated by Django 4.1.1 on 2022-09-13 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_alter_page_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='image_path',
        ),
        migrations.AddField(
            model_name='page',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Page image path'),
        ),
    ]
