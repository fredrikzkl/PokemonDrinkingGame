"""
Parse layout.txt to understand tile placement pattern.
"""

def _split_sections(layout_file: str):
    """Split layout file into sections separated by blank lines, ignoring comment lines."""
    with open(layout_file, 'r') as f:
        lines = [line for line in f.readlines() if not line.strip().startswith('#')]
    content = ''.join(lines)
    sections = [s.strip() for s in content.split('\n\n') if s.strip()]
    return sections


def parse_layout(layout_file: str = "assets/layout.txt"):
    """
    Parse the layout file and return a mapping of tile numbers to (row, col) positions.
    
    Returns:
        dict: {tile_number: (row, col), ...}
    """
    sections = _split_sections(layout_file)
    layout = {}

    for row_idx, line in enumerate(sections[0].splitlines()):
        cols = line.strip().split('-')
        for col_idx, cell in enumerate(cols):
            if cell != 'xx':
                try:
                    tile_num = int(cell)
                    layout[tile_num] = (row_idx, col_idx)
                except ValueError:
                    pass

    return layout


def parse_rotation_map(layout_file: str = "assets/layout.txt"):
    """
    Parse the rotation section of the layout file.

    Returns:
        dict: {(row, col): rotation_degrees, ...}
        Rotation values: 0 (D=down), 90 (R=right), 180 (U=up), 270 (L=left)
    """
    sections = _split_sections(layout_file)
    if len(sections) < 2:
        return {}

    rotation_map = {}
    direction_to_degrees = {'D': 0, 'U': 180, 'L': 270, 'R': 90}

    for row_idx, line in enumerate(sections[1].splitlines()):
        cols = line.strip().split('-')
        for col_idx, cell in enumerate(cols):
            cell = cell.strip()
            if cell in direction_to_degrees:
                rotation_map[(row_idx, col_idx)] = direction_to_degrees[cell]

    return rotation_map


def get_board_dimensions(layout_file: str = "assets/layout.txt"):
    """Get board dimensions from layout file."""
    sections = _split_sections(layout_file)
    lines = sections[0].splitlines()
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
