from django.db import models


class NewUser(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name