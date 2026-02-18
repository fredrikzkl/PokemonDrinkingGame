"""
Parse layout.txt to understand tile placement pattern.
"""

def parse_layout(layout_file: str = "assets/layout.txt"):
    """
    Parse the layout file and return a mapping of tile numbers to (row, col) positions.
    
    Returns:
        dict: {tile_number: (row, col), ...}
    """
    with open(layout_file, 'r') as f:
        lines = f.readlines()
    
    layout = {}
    rows = len(lines)
    
    for row_idx, line in enumerate(lines):
        cols = line.strip().split('-')
        for col_idx, cell in enumerate(cols):
            if cell != 'xx':
                try:
                    tile_num = int(cell)
                    layout[tile_num] = (row_idx, col_idx)
                except ValueError:
                    pass
    
    return layout


def get_board_dimensions(layout_file: str = "assets/layout.txt"):
    """Get board dimensions from layout file."""
    with open(layout_file, 'r') as f:
        lines = f.readlines()
    
    rows = len(lines)
    cols = len(lines[0].strip().split('-'))
    
    return rows, cols


def get_tile_connections(layout_file: str = "assets/layout.txt"):
    """
    Determine which direction each tile connects to the next tile.
    
    Returns:
        dict: {tile_number: {'north': bool, 'south': bool, 'east': bool, 'west': bool}, ...}
    """
    layout = parse_layout(layout_file)
    connections = {}
    
    # Get all tile numbers in order
    tile_numbers = sorted(layout.keys())
    
    for i, tile_num in enumerate(tile_numbers):
        row, col = layout[tile_num]
        
        # Find next tile in sequence
        next_tile_num = tile_numbers[(i + 1) % len(tile_numbers)]
        next_row, next_col = layout[next_tile_num]
        
        # Determine direction to next tile
        row_diff = next_row - row
        col_diff = next_col - col
        
        # Initialize borders (all True = thick border)
        borders = {
            'north': True,  # Top border
            'south': True,  # Bottom border
            'east': True,   # Right border
            'west': True    # Left border
        }
        
        # Remove border in direction of movement
        if row_diff < 0:  # Moving north (up)
            borders['north'] = False
        elif row_diff > 0:  # Moving south (down)
            borders['south'] = False
        elif col_diff > 0:  # Moving east (right)
            borders['east'] = False
        elif col_diff < 0:  # Moving west (left)
            borders['west'] = False
        
        connections[tile_num] = borders
    
    return connections
