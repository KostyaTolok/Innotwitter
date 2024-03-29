# Generated by Django 4.1 on 2022-09-02 08:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=180, verbose_name='Post content')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Post date of creation')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Post update date')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='pages.page', verbose_name='Post page')),
                ('reply_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='replies', to='posts.post', verbose_name='Post replies to')),
            ],
        ),
    ]
