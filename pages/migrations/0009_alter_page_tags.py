# Generated by Django 4.1.1 on 2022-09-14 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0008_alter_page_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, related_name='pages', to='pages.tag', verbose_name='Page tags'),
        ),
    ]
