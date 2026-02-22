"""
Load tiles from YAML configuration files.
"""

import sys
import os
from pathlib import Path

# Add project root to path so we can import src
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

import yaml
from typing import List, Dict, Any
from src import Tile
from src.api import fetch_pokemon_image
from src import styles


def load_tiles_from_yaml(yaml_path: str) -> List[Tile]:
    """
    Load tiles from a YAML file.

    Args:
        yaml_path: Path to YAML file (relative to project root or absolute)

    Returns:
        List of Tile objects
    """
    # Resolve path relative to project root if needed
    if not os.path.isabs(yaml_path):
        project_root = Path(__file__).parent.parent
        yaml_path = project_root / yaml_path
        # If file doesn't exist, try assets/ directory
        if not yaml_path.exists() and not str(yaml_path).startswith("assets"):
            assets_path = project_root / "assets" / Path(yaml_path).name
            if assets_path.exists():
                yaml_path = assets_path

    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)

    tiles = []
    for tile_def in data.get("tiles", []):
        # Handle PokeAPI images first (takes precedence over image_path)
        image_path = None
        if "poke_api_image" in tile_def:
            pokemon_name = tile_def["poke_api_image"]
            cached_path = fetch_pokemon_image(pokemon_name)
            if cached_path:
                image_path = cached_path
            else:
                print(f"Warning: Could not fetch Pokemon image for '{pokemon_name}'")
        elif "local_image" in tile_def:
            project_root = Path(__file__).parent.parent
            image_path = str(project_root / "assets" / "images" / "local" / tile_def["local_image"])
        elif "image_path" in tile_def:
            image_path = tile_def.get("image_path")
            if image_path and not os.path.isabs(image_path):
                project_root = Path(__file__).parent.parent
                image_path = str(project_root / image_path)

        background_image = None
        if "local_background_image" in tile_def:
            project_root = Path(__file__).parent.parent
            background_image = str(project_root / "assets" / "images" / "local" / tile_def["local_background_image"])

        def resolve_color(color_value):
            if isinstance(color_value, str):
                # Remove $ or @ prefix if present
                color_name = color_value.lstrip("$@")
                # Try to get from styles.COLORS
                if hasattr(styles, "COLORS") and color_name in styles.COLORS:
                    return styles.COLORS[color_name]
                # Try get_color function
                try:
                    return styles.get_color(color_name)
                except (KeyError, AttributeError):
                    pass
                # If not found, return as-is (might be a hex color or other format)
                return color_value
            elif isinstance(color_value, list):
                # It's already an RGB list, convert to tuple
                return tuple(color_value)
            return color_value

        bg_color = tile_def.get("background_color", [255, 255, 255])
        text_color = tile_def.get("text_color", [0, 0, 0])
        border_color = tile_def.get("border_color", [0, 0, 0])

        # Resolve color references
        bg_color = resolve_color(bg_color)
        text_color = resolve_color(text_color)
        border_color = resolve_color(border_color)

        # Ensure colors are tuples
        if isinstance(bg_color, (list, tuple)) and len(bg_color) == 3:
            bg_color = tuple(bg_color)
        if isinstance(text_color, (list, tuple)) and len(text_color) == 3:
            text_color = tuple(text_color)
        if isinstance(border_color, (list, tuple)) and len(border_color) == 3:
            border_color = tuple(border_color)

        # Create tile with all provided parameters
        tile = Tile(
            width=tile_def.get("width", 600),
            height=tile_def.get("height", 600),
            header=tile_def.get("header"),
            text=tile_def.get("text"),
            image_path=image_path,
            image_scale=tile_def.get("image_scale", 0.8),
            image_margin_top=tile_def.get("image_margin_top"),
            image_anchor_bottom=tile_def.get("image_anchor_bottom", False),
            background_color=bg_color
            if isinstance(bg_color, tuple)
            else (255, 255, 255),
            text_color=text_color if isinstance(text_color, tuple) else (0, 0, 0),
            border_color=border_color if isinstance(border_color, tuple) else (0, 0, 0),
            border_width=tile_def.get("border_width", 1),
            font_size=tile_def.get("font_size"),
            footer=tile_def.get("footer"),
            background_image=background_image,
            text_margin_top=tile_def.get("text_margin_top", 0),
            text_align=tile_def.get("text_align", "center"),
        )
        tiles.append(tile)

    return tiles


def load_tiles_by_name(yaml_path: str, names: List[str]) -> List[Tile]:
    """
    Load specific tiles by name from a YAML file.

    Args:
        yaml_path: Path to YAML file
        names: List of tile names to load

    Returns:
        List of Tile objects
    """
    if not os.path.isabs(yaml_path):
        project_root = Path(__file__).parent.parent
        yaml_path = project_root / yaml_path

    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)

    tiles = []
    tile_dict = {tile_def.get("name"): tile_def for tile_def in data.get("tiles", [])}

    for name in names:
        if name in tile_dict:
            tile_def = tile_dict[name]

            image_path = None
            if "poke_api_image" in tile_def:
                pokemon_name = tile_def["poke_api_image"]
                cached_path = fetch_pokemon_image(pokemon_name)
                if cached_path:
                    image_path = cached_path
                else:
                    print(
                        f"Warning: Could not fetch Pokemon image for '{pokemon_name}'"
                    )
            elif "local_image" in tile_def:
                project_root = Path(__file__).parent.parent
                image_path = str(project_root / "assets" / "images" / "local" / tile_def["local_image"])
            elif "image_path" in tile_def:
                image_path = tile_def.get("image_path")
                if image_path and not os.path.isabs(image_path):
                    project_root = Path(__file__).parent.parent
                    image_path = str(project_root / image_path)

            background_image = None
            if "local_background_image" in tile_def:
                project_root = Path(__file__).parent.parent
                background_image = str(project_root / "assets" / "images" / "local" / tile_def["local_background_image"])

            def resolve_color(color_value):
                if isinstance(color_value, str):
                    color_name = color_value.lstrip("$@")
                    if hasattr(styles, "COLORS") and color_name in styles.COLORS:
                        return styles.COLORS[color_name]
                    try:
                        return styles.get_color(color_name)
                    except (KeyError, AttributeError):
                        pass
                    return color_value
                elif isinstance(color_value, list):
                    return tuple(color_value)
                return color_value

            bg_color = resolve_color(tile_def.get("background_color", [255, 255, 255]))
            text_color = resolve_color(tile_def.get("text_color", [0, 0, 0]))
            border_color = resolve_color(tile_def.get("border_color", [0, 0, 0]))

            if isinstance(bg_color, (list, tuple)) and len(bg_color) == 3:
                bg_color = tuple(bg_color)
            if isinstance(text_color, (list, tuple)) and len(text_color) == 3:
                text_color = tuple(text_color)
            if isinstance(border_color, (list, tuple)) and len(border_color) == 3:
                border_color = tuple(border_color)

            tile = Tile(
                width=tile_def.get("width", 600),
                height=tile_def.get("height", 600),
                header=tile_def.get("header"),
                text=tile_def.get("text"),
                image_path=image_path,
                image_scale=tile_def.get("image_scale", 0.8),
                image_margin_top=tile_def.get("image_margin_top"),
                image_anchor_bottom=tile_def.get("image_anchor_bottom", False),
                background_color=bg_color
                if isinstance(bg_color, tuple)
                else (255, 255, 255),
                text_color=text_color if isinstance(text_color, tuple) else (0, 0, 0),
                border_color=border_color
                if isinstance(border_color, tuple)
                else (0, 0, 0),
                border_width=tile_def.get("border_width", 1),
                font_size=tile_def.get("font_size"),
                footer=tile_def.get("footer"),
                background_image=background_image,
                text_margin_top=tile_def.get("text_margin_top", 0),
                text_align=tile_def.get("text_align", "center"),
            )
            tiles.append(tile)
        else:
            print(f"Warning: Tile '{name}' not found in {yaml_path}")

    return tiles


def preview_tiles_from_yaml(yaml_path: str, output_dir: str = None):
    """
    Load tiles from YAML and save preview images.

    Args:
        yaml_path: Path to YAML file
        output_dir: Directory to save preview images (default: tiles/output/)
    """
    tiles = load_tiles_from_yaml(yaml_path)

    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    print(f"Loading {len(tiles)} tiles from {yaml_path}...")

    for i, tile in enumerate(tiles):
        img = tile.render()
        output_path = os.path.join(output_dir, f"tile_{i + 1}.png")
        img.save(output_path)
        print(f"  ✓ Saved: {output_path}")

    print(f"\nAll tiles saved to: {output_dir}")


if __name__ == "__main__":
    import sys

    yaml_file = sys.argv[1] if len(sys.argv) > 1 else "tiles/example_tiles.yaml"
    preview_tiles_from_yaml(yaml_file)
