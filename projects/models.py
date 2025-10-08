from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    coordinator = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title
