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
