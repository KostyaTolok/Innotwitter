# Generated by Django 4.1 on 2022-09-02 09:29

from django.conf import settings
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pages', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='follow_requests',
            field=models.ManyToManyField(blank=True, null=True, related_name='requests', to=settings.AUTH_USER_MODEL, verbose_name='Page follow requests'),
        ),
        migrations.AlterField(
            model_name='page',
            name='followers',
            field=models.ManyToManyField(blank=True, null=True, related_name='follows', to=settings.AUTH_USER_MODEL, verbose_name='Page followers'),
        ),
        migrations.AlterField(
            model_name='page',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True, verbose_name='Page uuid'),
        ),
    ]
