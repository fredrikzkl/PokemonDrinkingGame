from src import BoardGameEngine
from assets.load_tiles import load_tiles_from_yaml
import os
import sys


def create_board_from_yaml(yaml_file: str = "assets/tiles.yaml", board_cols: int = 4, board_rows: int = 4):
    """Create a board using tiles defined in a YAML file."""
    
    # Create output directory
    os.makedirs("output", exist_ok=True)
    
    # Load tiles from YAML
    tiles = load_tiles_from_yaml(yaml_file)
    
    print(f"Loaded {len(tiles)} tiles from {yaml_file}")
    
    # Initialize engine
    engine = BoardGameEngine(
        tile_width=200,
        tile_height=200,
        board_cols=board_cols,
        board_rows=board_rows,
        tile_spacing=10
    )
    
    # Place tiles on board
    tile_index = 0
    for row in range(board_rows):
        for col in range(board_cols):
            if tile_index < len(tiles):
                engine.set_tile(row, col, tiles[tile_index].render())
                tile_index += 1
            else:
                print(f"Warning: Not enough tiles! Need {board_rows * board_cols}, got {len(tiles)}")
                break
    
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
