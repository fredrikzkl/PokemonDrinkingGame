from src import BoardGameEngine
from assets.load_tiles import load_tiles_from_yaml
from assets.parse_layout import parse_layout, get_board_dimensions
from PIL import Image
import os
import sys


def rotate_tile_for_position(
    tile_image: Image.Image, row: int, col: int, total_rows: int, total_cols: int
) -> Image.Image:
    """
    Rotate tile based on its position so people around a table can read it.

    - Top row (row 0): Rotate 180°
    - Left column (col 0): Rotate 180°
    - Right column (col n-1): Rotate 90° clockwise (eastern)
    - Other tiles: No rotation
    """
    is_top = row == 0
    is_left = col == 0
    is_right = col == total_cols - 1

    # Priority: left column > top row > right column
    # Left column: 180° rotation
    if is_left:
        return tile_image.rotate(270, expand=True)
    # Top row: 180° rotation
    elif is_top:
        return tile_image.rotate(180, expand=True)
    # Right column (eastern): 90° clockwise
    elif is_right:
        return tile_image.rotate(90, expand=True)
    # All other tiles: no rotation
    else:
        return tile_image


def create_board_from_yaml(
    yaml_file: str = "assets/tiles.yaml",
    layout_file: str = "assets/layout.txt",
    tile_rotation: bool = False,
):
    """Create a board using tiles defined in a YAML file, following the layout pattern."""

    # Create output directory
    os.makedirs("output", exist_ok=True)

    # Load tiles from YAML
    tiles = load_tiles_from_yaml(yaml_file)

    print(f"Loaded {len(tiles)} tiles from {yaml_file}")

    # Parse layout to get tile positions
    layout = parse_layout(layout_file)
    board_rows, board_cols = get_board_dimensions(layout_file)

    print(f"Board layout: {board_rows}x{board_cols} (from {layout_file})")
    print(f"Layout defines {len(layout)} tile positions")

    if tile_rotation:
        print("Tile rotation enabled: tiles will be rotated for table play")

    # Initialize engine
    engine = BoardGameEngine(
        tile_width=200,
        tile_height=200,
        board_cols=board_cols,
        board_rows=board_rows,
        tile_spacing=5,  # Reduced spacing
    )

    # Place tiles according to layout pattern
    # Tile 1 (index 0) goes to position 01, tile 2 (index 1) goes to position 02, etc.
    placed_count = 0
    for tile_index, tile in enumerate(tiles):
        tile_number = tile_index + 1  # Tiles are 1-indexed in layout
        if tile_number in layout:
            row, col = layout[tile_number]
            tile_image = tile.render()

            # Apply rotation if flag is set
            if tile_rotation:
                tile_image = rotate_tile_for_position(
                    tile_image, row, col, board_rows, board_cols
                )

            engine.set_tile(row, col, tile_image)
            placed_count += 1
        else:
            print(
                f"Warning: Tile {tile_number} (index {tile_index}) not found in layout"
            )

    print(f"Placed {placed_count} tiles on board")

    # Export board
    output_name = os.path.splitext(os.path.basename(yaml_file))[0]
    engine.export_image(f"output/board_{output_name}.png", dpi=300)
    engine.export_pdf(f"output/board_{output_name}.pdf")

    print(f"\n✓ Board created from {yaml_file}!")
    print(f"Check the 'output' directory for:")
    print(f"  - board_{output_name}.png")
    print(f"  - board_{output_name}.pdf")


if __name__ == "__main__":
    print("Board Game Generator")
    print("=" * 50)

    # Parse command line arguments
    args = [
        arg
        for arg in sys.argv[1:]
        if not arg.startswith("--") and not arg.startswith("-")
    ]
    flags = [arg for arg in sys.argv[1:] if arg.startswith("--") or arg.startswith("-")]

    # Check for tile rotation flag
    tile_rotation = "--tileRotation" in flags or "-tileRotation" in flags

    # Get YAML file (first non-flag argument, or default)
    yaml_file = args[0] if args else "assets/tiles.yaml"

    create_board_from_yaml(yaml_file, tile_rotation=tile_rotation)
