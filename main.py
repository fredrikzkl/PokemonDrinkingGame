from src import BoardGameEngine
from assets.load_tiles import load_tiles_from_yaml
from assets.parse_layout import parse_layout, get_board_dimensions
import os
import sys


def create_board_from_yaml(yaml_file: str = "assets/tiles.yaml", layout_file: str = "assets/layout.txt"):
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
    
    # Initialize engine
    engine = BoardGameEngine(
        tile_width=200,
        tile_height=200,
        board_cols=board_cols,
        board_rows=board_rows,
        tile_spacing=10
    )
    
    # Place tiles according to layout pattern
    # Tile 1 (index 0) goes to position 01, tile 2 (index 1) goes to position 02, etc.
    placed_count = 0
    for tile_index, tile in enumerate(tiles):
        tile_number = tile_index + 1  # Tiles are 1-indexed in layout
        if tile_number in layout:
            row, col = layout[tile_number]
            engine.set_tile(row, col, tile.render())
            placed_count += 1
        else:
            print(f"Warning: Tile {tile_number} (index {tile_index}) not found in layout")
    
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
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        yaml_file = sys.argv[1]
        create_board_from_yaml(yaml_file)
    else:
        # Default: use assets/tiles.yaml
        create_board_from_yaml()
