from django.db import models

class Currency(models.Model):
    id = models.CharField(primary_key=True, max_length=8)
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name