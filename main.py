from src import BoardGameEngine
from assets.load_tiles import load_tiles_from_yaml
from assets.parse_layout import parse_layout, get_board_dimensions, get_tile_connections, parse_rotation_map
from PIL import Image
import os
import sys


TRANSPOSE_MAP = {
    90: Image.Transpose.ROTATE_90,
    180: Image.Transpose.ROTATE_180,
    270: Image.Transpose.ROTATE_270,
}

def rotate_tile(tile_image: Image.Image, degrees: int) -> Image.Image:
    """Rotate tile using lossless transpose for 90-degree increments."""
    if degrees == 0:
        return tile_image
    if degrees in TRANSPOSE_MAP:
        return tile_image.transpose(TRANSPOSE_MAP[degrees])
    return tile_image.rotate(degrees, expand=True)


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

    # Parse layout to get tile positions and connections
    layout = parse_layout(layout_file)
    board_rows, board_cols = get_board_dimensions(layout_file)
    tile_connections = get_tile_connections(layout_file)
    rotation_map = parse_rotation_map(layout_file) if tile_rotation else {}
    
    print(f"Board layout: {board_rows}x{board_cols} (from {layout_file})")
    print(f"Layout defines {len(layout)} tile positions")
    
    if tile_rotation:
        print(f"Tile rotation enabled: {len(rotation_map)} rotation entries loaded")
    
    # Initialize engine
    engine = BoardGameEngine(
        tile_width=300,
        tile_height=300,
        board_cols=board_cols,
        board_rows=board_rows,
        tile_spacing=0,  # No spacing between tiles
    )
    
    # Place tiles according to layout pattern
    # Tile 1 (index 0) goes to position 01, tile 2 (index 1) goes to position 02, etc.
    placed_count = 0
    for tile_index, tile in enumerate(tiles):
        tile_number = tile_index + 1  # Tiles are 1-indexed in layout
        if tile_number in layout:
            row, col = layout[tile_number]
            tile_image = tile.render()
            
            if tile_rotation and (row, col) in rotation_map:
                tile_image = rotate_tile(tile_image, rotation_map[(row, col)])
            
            engine.set_tile(row, col, tile_image)
            placed_count += 1
        else:
            print(
                f"Warning: Tile {tile_number} (index {tile_index}) not found in layout"
            )

    print(f"Placed {placed_count} tiles on board")

    # Export board
    suffix = "_rotated" if tile_rotation else ""
    output_name = os.path.splitext(os.path.basename(yaml_file))[0]
    engine.export_image(f"output/board_{output_name}{suffix}.png", dpi=300)
    engine.export_pdf(f"output/board_{output_name}{suffix}.pdf")

    print(f"\n✓ Board created from {yaml_file}!")
    print(f"  - board_{output_name}{suffix}.png")
    print(f"  - board_{output_name}{suffix}.pdf")


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
