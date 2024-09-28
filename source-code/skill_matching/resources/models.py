from django.db import models
from common.models import BaseModel


class ResourceDetail(BaseModel):
    """
    This model class would be used to keep all resource related informations.
    """

    name = models.CharField(max_length=512)
    skills = models.JSONField()
    from_date = models.DateField()
    to_date = models.DateField()

    def __str__(self):
        return self.name


class ProjectDetail(BaseModel):
    """
    This model class would be used to keep all project related informations.
    """

    name = models.CharField(max_length=512)

    def __str__(self):
        return self.name


class TaskInfo(BaseModel):
    """
    This model class would be used to keep all tasks related informations.
    """

    project = models.ForeignKey(ProjectDetail, on_delete=models.CASCADE)
    name = models.CharField(max_length=512)
    skills = models.JSONField()
    from_date = models.DateField()
    to_date = models.DateField()

    def __str__(self):
        return self.name
