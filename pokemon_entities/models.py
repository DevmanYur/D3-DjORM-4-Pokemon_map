from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField('Имя',max_length=200, default="")
    image = models.ImageField('Картинка', default="")
    def __str__(self):
        return f'{self.title}'

