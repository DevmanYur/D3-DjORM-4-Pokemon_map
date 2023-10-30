from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField('Имя', max_length=200)
    title_en = models.CharField('Имя на английском', max_length=200, blank=True)
    title_jp = models.CharField('Имя на японском', max_length=200, blank=True)
    description = models.TextField('Описание', max_length=5000, blank=True)
    image = models.ImageField('Картинка')
    previous_evolution = models.ForeignKey("Pokemon", verbose_name="Из кого эволюционировал", on_delete=models.CASCADE,
                                           null=True, blank=True, related_name="evolutions")

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, verbose_name='Покемон', on_delete=models.CASCADE,
                                related_name="entities")
    lat = models.FloatField('Широта')
    lon = models.FloatField('Долгота')
    appeared_at = models.DateTimeField('Дата и время появления')
    disappeared_at = models.DateTimeField('Дата и время исчезновения')
    level = models.IntegerField('Уровень', null=True, blank=True)
    health = models.IntegerField('Здоровье', null=True, blank=True)
    strength = models.IntegerField('Атака', null=True, blank=True)
    defence = models.IntegerField('Защита', null=True, blank=True)
    stamina = models.IntegerField('Выносливость', null=True, blank=True)

    def __str__(self):
        return f'{self.pokemon.title, self.lat, self.lon}'
