"""
API modules for fetching external resources.
"""

from .pokeapi import fetch_pokemon_image, get_pokemon_sprite_url

__all__ = ['fetch_pokemon_image', 'get_pokemon_sprite_url']
