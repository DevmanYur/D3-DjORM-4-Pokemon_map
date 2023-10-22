from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField('Имя',max_length=200, default="")
    title_en = models.CharField('Имя на английском',max_length=200, default="", blank=True)
    title_jp = models.CharField('Имя на японском', max_length=200, default="", blank=True)
    description = models.CharField('Описание',max_length=5000, default="", blank=True)
    image = models.ImageField('Картинка',default="")
    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, verbose_name='Покемон', on_delete=models.CASCADE)
    lat = models.FloatField('Широта')
    lon = models.FloatField('Долгота')
    appeared_at = models.DateTimeField('Дата и время появления')
    disappeared_at = models.DateTimeField('Дата и время исчезновения')
    level = models.IntegerField('Уровень',null=True, blank=True, default=0)
    health = models.IntegerField('Здоровье',null=True, blank=True, default=0)
    strength = models.IntegerField('Атака',null=True, blank=True, default=0)
    defence = models.IntegerField('Защита',null=True, blank=True, default=0)
    stamina = models.IntegerField('Выносливость',null=True, blank=True, default=0)

    def __str__(self):
        return f'{self.pokemon.title, self.lat, self.lon}'

