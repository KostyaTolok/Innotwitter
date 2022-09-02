from django.db import models
import uuid


class Tag(models.Model):
    name = models.CharField(verbose_name="Tag name", max_length=30, unique=True)

    def __str__(self):
        return "Tag " + self.name


class Page(models.Model):
    uuid = models.UUIDField(verbose_name="Page uuid", primary_key=True, max_length=30, unique=True, default=uuid.uuid4)
    name = models.CharField(verbose_name="Page name", max_length=80, blank=False)
    description = models.TextField(verbose_name="Page description", max_length=500)
    image_path = models.URLField(verbose_name="Page image path", null=True, blank=True)
    is_private = models.BooleanField(verbose_name="Is page private", default=False)
    unblock_date = models.DateTimeField(verbose_name="Page unblock date", null=True, blank=True)

    tags = models.ManyToManyField(Tag, verbose_name="Page tags", related_name='pages')
    owner = models.ForeignKey('users.User', verbose_name="Page owner", on_delete=models.CASCADE, related_name='pages')
    followers = models.ManyToManyField('users.User', verbose_name="Page followers", related_name='follows', blank=True)
    follow_requests = models.ManyToManyField('users.User', verbose_name="Page follow requests", related_name='requests',
                                             blank=True)

    def __str__(self):
        return "Page " + self.name
