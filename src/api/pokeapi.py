"""
PokeAPI integration for fetching Pokemon images.
"""

import requests
import os
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse


# Base URL for PokeAPI
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/pokemon"


def get_pokemon_sprite_url(pokemon_name: str) -> Optional[str]:
    """
    Get the front_default sprite URL for a Pokemon.
    
    Args:
        pokemon_name: Name of the Pokemon (e.g., "rattata", "pikachu")
        
    Returns:
        URL to the sprite image, or None if not found
    """
    try:
        pokemon_name = pokemon_name.lower().strip()
        url = f"{POKEAPI_BASE_URL}/{pokemon_name}"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        sprite_url = data.get('sprites', {}).get('front_default')
        
        return sprite_url
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Pokemon data for '{pokemon_name}': {e}")
        return None
    except KeyError as e:
        print(f"Error parsing Pokemon data for '{pokemon_name}': {e}")
        return None


def fetch_pokemon_image(
    pokemon_name: str,
    cache_dir: Optional[str] = None,
    use_cache: bool = True
) -> Optional[str]:
    """
    Fetch a Pokemon image from PokeAPI and optionally cache it locally.
    
    Args:
        pokemon_name: Name of the Pokemon (e.g., "rattata", "pikachu")
        cache_dir: Directory to cache images (default: tiles/images/pokeapi/)
        use_cache: Whether to use cached images if available
        
    Returns:
        Path to the local image file, or None if fetch failed
    """
    pokemon_name = pokemon_name.lower().strip()
    
    # Set up cache directory
    if cache_dir is None:
        project_root = Path(__file__).parent.parent.parent
        cache_dir = project_root / "tiles" / "images" / "pokeapi"
    else:
        cache_dir = Path(cache_dir)
    
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # Check cache first
    cached_path = cache_dir / f"{pokemon_name}.png"
    if use_cache and cached_path.exists():
        return str(cached_path)
    
    # Fetch sprite URL
    sprite_url = get_pokemon_sprite_url(pokemon_name)
    if not sprite_url:
        return None
    
    # Download the image
    try:
        response = requests.get(sprite_url, timeout=10)
        response.raise_for_status()
        
        # Save to cache
        cached_path.write_bytes(response.content)
        print(f"✓ Downloaded and cached: {pokemon_name} -> {cached_path}")
        
        return str(cached_path)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image for '{pokemon_name}': {e}")
        return None


def batch_fetch_pokemon_images(
    pokemon_names: list[str],
    cache_dir: Optional[str] = None,
    use_cache: bool = True
) -> dict[str, Optional[str]]:
    """
    Fetch multiple Pokemon images at once.
    
    Args:
        pokemon_names: List of Pokemon names
        cache_dir: Directory to cache images
        use_cache: Whether to use cached images if available
        
    Returns:
        Dictionary mapping Pokemon names to image paths (or None if failed)
    """
    results = {}
    for name in pokemon_names:
        results[name] = fetch_pokemon_image(name, cache_dir, use_cache)
    return results
