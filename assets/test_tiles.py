"""
Easy script to create and test individual tiles.
Place your images in the tiles/images/ folder and test them here.
"""

import sys
import os

# Add project root to path so we can import src.poke_game
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src import Tile


def create_test_tile(
    text: str = None,
    image_path: str = None,
    background_color: tuple = (255, 255, 255),
    text_color: tuple = (0, 0, 0),
    width: int = 200,
    height: int = 200,
    output_name: str = "test_tile"
):
    """
    Create and save a single tile for testing.
    
    Args:
        text: Text to display on tile
        image_path: Path to image (relative to project root or absolute)
        background_color: RGB background color tuple
        text_color: RGB text color tuple
        width: Tile width in pixels
        height: Tile height in pixels
        output_name: Name for output file (without extension)
    """
    # Create output directory
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # If image_path is relative and in tiles/images/, make it relative to project root
    if image_path and not os.path.isabs(image_path):
        if not image_path.startswith('tiles/images/'):
            # Try to find it in tiles/images/
            images_dir = os.path.join(os.path.dirname(__file__), 'images')
            potential_path = os.path.join(images_dir, image_path)
            if os.path.exists(potential_path):
                image_path = potential_path
            elif os.path.exists(image_path):
                pass  # Use as-is
            else:
                # Try relative to project root
                project_root = os.path.dirname(os.path.dirname(__file__))
                image_path = os.path.join(project_root, image_path)
    
    # Create tile
    tile = Tile(
        width=width,
        height=height,
        text=text,
        image_path=image_path,
        background_color=background_color,
        text_color=text_color
    )
    
    # Render and save
    img = tile.render()
    output_path = os.path.join(output_dir, f"{output_name}.png")
    img.save(output_path)
    
    print(f"✓ Tile saved to: {output_path}")
    return output_path


def create_multiple_test_tiles():
    """Create several example tiles for testing."""
    
    print("Creating test tiles...")
    print("=" * 50)
    
    # Tile 1: Text only
    create_test_tile(
        text="START",
        background_color=(200, 255, 200),
        text_color=(0, 100, 0),
        output_name="tile_text_only"
    )
    
    # Tile 2: Different colors
    create_test_tile(
        text="GO",
        background_color=(255, 200, 200),
        text_color=(100, 0, 0),
        output_name="tile_red"
    )
    
    # Tile 3: Blue tile
    create_test_tile(
        text="Tile 3",
        background_color=(200, 200, 255),
        text_color=(0, 0, 100),
        output_name="tile_blue"
    )
    
    # Tile 4: With image (if you have one)
    # Uncomment and update the path when you have an image:
    # create_test_tile(
    #     text="Pokemon",
    #     image_path="tiles/images/pikachu.png",  # Update with your image
    #     background_color=(255, 255, 200),
    #     output_name="tile_with_image"
    # )
    
    print("\n" + "=" * 50)
    print("All test tiles created!")
    print(f"Check: {os.path.join(os.path.dirname(__file__), 'output')}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Custom tile creation from command line
        # Usage: python test_tiles.py "Text" [image_path] [bg_r] [bg_g] [bg_b]
        text = sys.argv[1]
        image_path = sys.argv[2] if len(sys.argv) > 2 else None
        bg_color = tuple(map(int, sys.argv[3:6])) if len(sys.argv) > 5 else (255, 255, 255)
        
        create_test_tile(
            text=text,
            image_path=image_path,
            background_color=bg_color,
            output_name="custom_tile"
        )
    else:
        # Create example tiles
        create_multiple_test_tiles()
