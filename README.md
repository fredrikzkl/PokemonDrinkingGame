# Board Game Generator

A Python-based board game generator that creates printable game boards.

## Setup

1. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the generator:

```bash
python main.py
```

**Note:** Remember to activate the virtual environment (`source venv/bin/activate`) each time you work on the project.

## Project Structure

- `main.py` - Main entry point
- `src/` - Source code package
  - `tile.py` - Tile class definition
  - `engine.py` - Core game board generation logic
- `tiles/` - Directory for tile definitions and assets
  - `tiles.yaml` - **Your main tile definitions file** (edit this!)
  - `example_tiles.yaml` - Example tile definitions
  - `images/` - Tile image files
  - `load_tiles.py` - YAML tile loader
- `output/` - Generated board images and PDFs

## Usage

### Creating Boards with YAML (Recommended)

**1. Edit your tile definitions** in `tiles/tiles.yaml`:

```yaml
tiles:
  # Start tile
  - name: start
    text: "START"
    background_color: [200, 255, 200]  # Light green
    text_color: [0, 100, 0]
    width: 200
    height: 200

  # Tile with image
  - name: pikachu
    text: "Pikachu"
    image_path: "tiles/images/pikachu.png"
    background_color: [255, 255, 200]
    width: 200
    height: 200
```

**2. Generate your board:**

```bash
python main.py                    # Uses tiles/tiles.yaml (default)
python main.py tiles/my_board.yaml  # Use a specific YAML file
python main.py --example          # Create example board (no YAML)
```

**3. Check the output:**

- `output/board_tiles.png` - High-resolution image
- `output/board_tiles.pdf` - Printable PDF
