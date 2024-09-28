from uuid import uuid4
from django.db import models


# Create your models here.
class BaseModel(models.Model):
    """Abstract base class"""

    id = models.CharField(
        primary_key=True, unique=True, editable=False, max_length=36, default=uuid4
    )
    created_ts = models.DateTimeField(auto_now_add=True)
    update_ts = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.id)

    class Meta:
        abstract = True

    @classmethod
    def create(cls, **kwargs):
        obj = cls(**kwargs)
        obj.save()
        return obj
