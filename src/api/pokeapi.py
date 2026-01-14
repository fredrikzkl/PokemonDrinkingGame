"""
PokeAPI integration for fetching Pokemon and item images.
"""

import requests
import os
from pathlib import Path
from typing import Optional, Tuple
from urllib.parse import urlparse


# Base URL for PokeAPI
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"


def _parse_api_path(path: str) -> Tuple[str, str]:
    """
    Parse a poke_api_image path into (type, name).
    
    Args:
        path: Path like "pokemon/pikachu" or "item/poke-ball"
              Falls back to "pokemon/{path}" if no prefix
    
    Returns:
        Tuple of (type, name) e.g. ("pokemon", "pikachu")
    """
    path = path.lower().strip()
    if "/" in path:
        parts = path.split("/", 1)
        return parts[0], parts[1]
    # Default to pokemon for backwards compatibility
    return "pokemon", path


def get_sprite_url(path: str) -> Optional[str]:
    """
    Get the sprite URL for a Pokemon or item.
    
    Args:
        path: Path like "pokemon/pikachu" or "item/poke-ball"
        
    Returns:
        URL to the sprite image, or None if not found
    """
    try:
        resource_type, name = _parse_api_path(path)
        url = f"{POKEAPI_BASE_URL}/{resource_type}/{name}"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Different sprite paths for different resource types
        if resource_type == "pokemon":
            sprite_url = data.get('sprites', {}).get('front_default')
        elif resource_type == "item":
            sprite_url = data.get('sprites', {}).get('default')
        else:
            sprite_url = data.get('sprites', {}).get('front_default') or data.get('sprites', {}).get('default')
        
        return sprite_url
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for '{path}': {e}")
        return None
    except KeyError as e:
        print(f"Error parsing data for '{path}': {e}")
        return None


# Backwards compatibility alias
def get_pokemon_sprite_url(pokemon_name: str) -> Optional[str]:
    """Legacy function - use get_sprite_url instead."""
    return get_sprite_url(f"pokemon/{pokemon_name}")


def fetch_pokemon_image(
    path: str,
    cache_dir: Optional[str] = None,
    use_cache: bool = True
) -> Optional[str]:
    """
    Fetch a Pokemon or item image from PokeAPI and optionally cache it locally.
    
    Args:
        path: Path like "pokemon/pikachu" or "item/poke-ball"
              (also accepts just "pikachu" for backwards compatibility)
        cache_dir: Directory to cache images (default: tiles/images/pokeapi/)
        use_cache: Whether to use cached images if available
        
    Returns:
        Path to the local image file, or None if fetch failed
    """
    resource_type, name = _parse_api_path(path)
    
    # Set up cache directory with subdirectory for resource type
    if cache_dir is None:
        project_root = Path(__file__).parent.parent.parent
        cache_dir = project_root / "tiles" / "images" / "pokeapi" / resource_type
    else:
        cache_dir = Path(cache_dir) / resource_type
    
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # Check cache first
    cached_path = cache_dir / f"{name}.png"
    if use_cache and cached_path.exists():
        return str(cached_path)
    
    # Fetch sprite URL
    sprite_url = get_sprite_url(path)
    if not sprite_url:
        return None
    
    # Download the image
    try:
        response = requests.get(sprite_url, timeout=10)
        response.raise_for_status()
        
        # Save to cache
        cached_path.write_bytes(response.content)
        print(f"✓ Downloaded and cached: {path} -> {cached_path}")
        
        return str(cached_path)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image for '{path}': {e}")
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
