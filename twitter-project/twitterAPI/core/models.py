from django.db import models
import uuid


class TwitterAccount(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    username = models.CharField(max_length=200, null=True, blank=True)
    orientation = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.username
