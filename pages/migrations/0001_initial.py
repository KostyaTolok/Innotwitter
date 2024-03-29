# Generated by Django 4.1 on 2022-09-02 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('uuid', models.UUIDField(primary_key=True, serialize=False, unique=True, verbose_name='Page uuid')),
                ('name', models.CharField(max_length=80, verbose_name='Page name')),
                ('description', models.TextField(max_length=500, verbose_name='Page description')),
                ('image_path', models.URLField(blank=True, null=True, verbose_name='Page image path')),
                ('is_private', models.BooleanField(default=False, verbose_name='Is page private')),
                ('unblock_date', models.DateTimeField(blank=True, null=True, verbose_name='Page unblock date')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='Tag name')),
            ],
        ),
    ]
