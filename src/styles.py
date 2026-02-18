"""
Color Pallett: https://bulbapedia.bulbagarden.net/wiki/Color_palette_(Generations_I%E2%80%93II)
"""

COLORS = {
    "gym": (255, 201, 16),
    "viridian_forest": (120, 192, 120),
    "rock_tunnel": (200, 176, 112),
    "pokemon_tower": (216, 160, 208),
    "silph_co": (144, 176, 224),
    "safari_zone": (184, 192, 88),
    "seafoam_islands": (0, 160, 232),
    "optional_stop": (200, 200, 200),
}

# Text colors
TEXT_COLORS = {
    "default": (0, 0, 0),  # Black
}


def get_color(color_name: str) -> tuple[int, int, int]:
    return COLORS[color_name]
