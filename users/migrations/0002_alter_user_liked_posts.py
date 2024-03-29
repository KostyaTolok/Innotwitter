# Generated by Django 4.1 on 2022-09-02 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_alter_post_reply_to'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='liked_posts',
            field=models.ManyToManyField(blank=True, null=True, related_name='likes', to='posts.post', verbose_name='Posts liked by user'),
        ),
    ]
