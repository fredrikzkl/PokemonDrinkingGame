from src import BoardGameEngine
from src.tile import Tile
from assets.load_tiles import load_tiles_from_yaml
from assets.parse_layout import parse_layout, get_board_dimensions, get_tile_connections, parse_rotation_map, parse_special_tiles
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os
import re
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


def parse_rules_section(rules_file: str, section_name: str) -> str:
    """Extract a section from rules.md by heading name."""
    with open(rules_file) as f:
        content = f.read()

    pattern = rf"## {re.escape(section_name)}\s*\n(.*?)(?=\n#+ |\Z)"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""


def render_info_panel(header: str, body: str, width: int, height: int) -> Image.Image:
    """Render a free-form info panel with header and body text at native resolution."""
    w, h = width, height
    project_root = Path(__file__).parent
    fonts_dir = project_root / "assets" / "fonts"

    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    def get_font(size, font_type="text"):
        if font_type == "header":
            path = fonts_dir / "gbboot.ttf"
        else:
            path = fonts_dir / "gil.TTF"
        try:
            return ImageFont.truetype(str(path), size)
        except Exception:
            return ImageFont.load_default()

    header_font = get_font(w // 10, "header")
    hbox = draw.textbbox((0, 0), header, font=header_font)
    hx = (w - (hbox[2] - hbox[0])) // 2
    draw.text((hx, 10), header, fill=(0, 0, 0), font=header_font)
    y = hbox[3] - hbox[1] + 40

    body_font = get_font(w // 18)
    padding = 16
    available_width = w - padding * 2
    line_h = draw.textbbox((0, 0), "Ag", font=body_font)[3] + 4

    def parse_styled(text):
        """Parse text into [(word, is_bold), ...]"""
        segments = re.split(r"(\*\*.*?\*\*)", text)
        result = []
        for seg in segments:
            if not seg:
                continue
            bold = seg.startswith("**") and seg.endswith("**")
            clean = seg[2:-2] if bold else seg
            for w in clean.split():
                result.append((w, bold))
        return result

    def draw_styled_line(styled_words, x, y):
        plain = " ".join(w for w, _ in styled_words)
        cursor_x = x
        for i, (word, bold) in enumerate(styled_words):
            prefix = " ".join(w for w, _ in styled_words[:i])
            if prefix:
                prefix += " "
            px = draw.textbbox((0, 0), prefix, font=body_font)[2] - draw.textbbox((0, 0), prefix, font=body_font)[0]
            wx = x + px
            draw.text((wx, y), word, fill=(0, 0, 0), font=body_font)
            if bold:
                draw.text((wx + 1, y), word, fill=(0, 0, 0), font=body_font)
                draw.text((wx + 2, y), word, fill=(0, 0, 0), font=body_font)

    for line in body.split("\n"):
        stripped = line.strip()
        if not stripped:
            y += 6
            continue

        styled_words = parse_styled(stripped)
        current_line = []

        for word, bold in styled_words:
            test_text = " ".join(w for w, _ in current_line + [(word, bold)])
            tw = draw.textbbox((0, 0), test_text, font=body_font)[2] - draw.textbbox((0, 0), test_text, font=body_font)[0]
            if tw <= available_width:
                current_line.append((word, bold))
            else:
                if current_line:
                    draw_styled_line(current_line, padding, y)
                    y += line_h
                current_line = [(word, bold)]

        if current_line:
            draw_styled_line(current_line, padding, y)
            y += line_h

    return img


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
        tile_width=600,
        tile_height=600,
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

    # Render board, then overlay info panels
    board = engine.render_board()

    # Draw top and left border
    from PIL import ImageDraw as ID
    board_draw = ID.Draw(board)
    board_draw.line([(0, 0), (board.width - 1, 0)], fill=(0, 0, 0))
    board_draw.line([(0, 0), (0, board.height - 1)], fill=(0, 0, 0))

    # Place special info panels in the center area
    special_tiles = parse_special_tiles(layout_file)
    rules_file = "docs/rules.md"

    special_config = {
        "ru": ("Rules", "Basics", 2),
        "tb": ("Trainer Battle", "Trainer Battle", 2),
        "gb": ("Gym Battle", "Gym Mechanics", 2),
        "it": ("Items", "Items", 1),
    }

    tw, th = engine.tile_width, engine.tile_height
    for code, (header, section, height_tiles) in special_config.items():
        if code in special_tiles:
            anchor_row, anchor_col = special_tiles[code]
            body = parse_rules_section(rules_file, section)
            if body:
                panel_w = tw
                panel_h = th * height_tiles
                panel = render_info_panel(header, body, panel_w, panel_h)
                px = anchor_col * tw
                py = anchor_row * th
                board.paste(panel, (px, py))
                print(f"Placed info panel '{code}' ({header}) at pixel ({px}, {py}), size {panel_w}x{panel_h}")

    # Export
    suffix = "_rotated" if tile_rotation else ""
    output_name = os.path.splitext(os.path.basename(yaml_file))[0]

    os.makedirs("output", exist_ok=True)
    png_path = f"output/board_{output_name}{suffix}.png"
    board.save(png_path, dpi=(300, 300))
    print(f"Board exported to {png_path} ({board.width}x{board.height}px, 300 DPI)")

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
