from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField('Имя',max_length=200, default="")
