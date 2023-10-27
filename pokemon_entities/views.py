import django
import folium
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from pokemon_entities.models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    all_pokemons = Pokemon.objects.all()
    now_local = django.utils.timezone.localtime()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in PokemonEntity.objects.filter(appeared_at__lte=now_local, disappeared_at__gte=now_local):
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon_entity.pokemon.image.path
        )

    pokemons_on_page = []

    for pokemon in all_pokemons:
        try:
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'img_url': pokemon.image.url,
                'title_ru': pokemon.title,
            })
        except ValueError:
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'title_ru': pokemon.title,
            })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    select_pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    pokemon_id_int = int(pokemon_id)
    all_pokemon = Pokemon.objects.count()

    pokemon = {"pokemon_id": pokemon_id,
               "title_ru": select_pokemon.title,
               "title_en": select_pokemon.title_en,
               "title_jp": select_pokemon.title_jp,
               "description": select_pokemon.description,
               "img_url": select_pokemon.image.url,
               }

    if (pokemon_id_int == 1) & (all_pokemon == 1):
        pokemon = pokemon

    elif (pokemon_id_int == 1) & (all_pokemon > 1):
        pokemon_after = Pokemon.objects.get(id=(pokemon_id_int + 1))
        pokemon["next_evolution"] = {
            "title_ru": pokemon_after.title,
            "pokemon_id": pokemon_after.id,
            "img_url": pokemon_after.image.url
        }

    elif (pokemon_id_int > 1) & (pokemon_id_int < all_pokemon):
        pokemon_after = Pokemon.objects.get(id=(pokemon_id_int + 1))
        pokemon["previous_evolution"] = {
            "title_ru": select_pokemon.previous_evolution.title,
            "pokemon_id": select_pokemon.previous_evolution.id,
            "img_url": select_pokemon.previous_evolution.image.url
        }
        pokemon["next_evolution"] = {
            "title_ru": pokemon_after.title,
            "pokemon_id": pokemon_after.id,
            "img_url": pokemon_after.image.url
        }

    elif (pokemon_id_int > 1) & (pokemon_id_int == all_pokemon):
        pokemon["previous_evolution"] = {
            "title_ru": select_pokemon.previous_evolution.title,
            "pokemon_id": select_pokemon.previous_evolution.id,
            "img_url": select_pokemon.previous_evolution.image.url
        }

    now_local = django.utils.timezone.localtime()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in select_pokemon.entities.filter(appeared_at__lte=now_local, disappeared_at__gte=now_local):
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon_entity.pokemon.image.path
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
