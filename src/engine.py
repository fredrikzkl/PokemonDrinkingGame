"""
Board game engine for combining tiles into a printable game board.
"""

from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from typing import List, Tuple, Optional
import os


def mm_to_pixels(mm: float, dpi: int = 300) -> int:
    """
    Convert millimeters to pixels at given DPI.

    Args:
        mm: Size in millimeters
        dpi: Dots per inch

    Returns:
        Size in pixels
    """
    inches = mm / 25.4
    return int(inches * dpi)


def mm_to_points(mm: float) -> float:
    """
    Convert millimeters to points (for PDF).
    1 point = 1/72 inch, 1 inch = 25.4 mm

    Args:
        mm: Size in millimeters

    Returns:
        Size in points
    """
    inches = mm / 25.4
    return inches * 72


class BoardGameEngine:
    def __init__(
        self,
        tile_width: int = 200,
        tile_height: int = 200,
        board_cols: int = 4,
        board_rows: int = 4,
        tile_spacing: int = 10,
    ):
        """
        Initialize the board game engine.

        Args:
            tile_width: Width of each tile in pixels
            tile_height: Height of each tile in pixels
            board_cols: Number of columns in the board
            board_rows: Number of rows in the board
            tile_spacing: Spacing between tiles in pixels
        """
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.board_cols = board_cols
        self.board_rows = board_rows
        self.tile_spacing = tile_spacing
        self.tiles: List[List[Optional[Image.Image]]] = []

        # Initialize empty board
        self._initialize_board()

    def _initialize_board(self):
        """Initialize an empty board grid."""
        self.tiles = [
            [None for _ in range(self.board_cols)] for _ in range(self.board_rows)
        ]

    def set_tile(self, row: int, col: int, tile_image: Image.Image):
        """
        Set a tile at a specific position.

        Args:
            row: Row index (0-based)
            col: Column index (0-based)
            tile_image: PIL Image of the tile
        """
        if 0 <= row < self.board_rows and 0 <= col < self.board_cols:
            if tile_image.size != (self.tile_width, self.tile_height):
                tile_image = tile_image.resize(
                    (self.tile_width, self.tile_height), Image.Resampling.LANCZOS
                )
            self.tiles[row][col] = tile_image
        else:
            raise IndexError(f"Position ({row}, {col}) is out of bounds")

    def render_board(self) -> Image.Image:
        """
        Render the complete board as a single image.

        Returns:
            PIL Image of the complete board
        """
        # Calculate board dimensions
        board_width = (
            self.board_cols * self.tile_width
            + (self.board_cols - 1) * self.tile_spacing
        )
        board_height = (
            self.board_rows * self.tile_height
            + (self.board_rows - 1) * self.tile_spacing
        )

        # Create board image
        board = Image.new("RGB", (board_width, board_height), (255, 255, 255))

        # Paste tiles onto board
        for row in range(self.board_rows):
            for col in range(self.board_cols):
                if self.tiles[row][col] is not None:
                    x = col * (self.tile_width + self.tile_spacing)
                    y = row * (self.tile_height + self.tile_spacing)
                    board.paste(self.tiles[row][col], (x, y))

        return board

    def export_image(self, output_path: str, dpi: int = 300):
        """
        Export the board as an image. Tiles are already rendered at their
        target pixel size, so no upscaling is done.

        Args:
            output_path: Path to save the image
            dpi: DPI metadata tag (for print sizing, does not change pixels)
        """
        board = self.render_board()

        os.makedirs(
            os.path.dirname(output_path) if os.path.dirname(output_path) else ".",
            exist_ok=True,
        )

        board.save(output_path, dpi=(dpi, dpi))
        print(f"Board exported to {output_path} ({board.width}x{board.height}px, {dpi} DPI)")

    def export_image_exact_size(
        self, output_path: str, width_mm: float, height_mm: float, dpi: int = 300
    ):
        """
        Export the board at an exact physical size.

        Args:
            output_path: Path to save the image
            width_mm: Output width in millimeters
            height_mm: Output height in millimeters
            dpi: Dots per inch for print quality (300 or 600 recommended)
        """
        board = self.render_board()

        # Calculate target pixel dimensions
        target_width_px = mm_to_pixels(width_mm, dpi)
        target_height_px = mm_to_pixels(height_mm, dpi)

        # Resize board to exact dimensions
        board_resized = board.resize(
            (target_width_px, target_height_px), Image.Resampling.LANCZOS
        )

        # Ensure output directory exists
        os.makedirs(
            os.path.dirname(output_path) if os.path.dirname(output_path) else ".",
            exist_ok=True,
        )

        board_resized.save(output_path, dpi=(dpi, dpi))
        print(
            f"Board exported to {output_path} at {width_mm}x{height_mm}mm ({dpi} DPI)"
        )
        print(f"  Pixel dimensions: {target_width_px}x{target_height_px}px")

    def export_pdf(self, output_path: str, page_size: Tuple[float, float] = A4):
        """
        Export the board as a PDF using ReportLab.

        Args:
            output_path: Path to save the PDF
            page_size: Page size tuple (width, height) in points
        """
        board = self.render_board()

        # Ensure output directory exists
        os.makedirs(
            os.path.dirname(output_path) if os.path.dirname(output_path) else ".",
            exist_ok=True,
        )

        # Create PDF
        c = canvas.Canvas(output_path, pagesize=page_size)
        page_width, page_height = page_size

        # Calculate scaling to fit board on page
        scale_x = page_width / board.width
        scale_y = page_height / board.height
        scale = min(scale_x, scale_y) * 0.95  # 95% to add some margin

        # Center the board
        scaled_width = board.width * scale
        scaled_height = board.height * scale
        x_offset = (page_width - scaled_width) / 2
        y_offset = (page_height - scaled_height) / 2

        # Convert PIL Image to format ReportLab can use
        img_reader = ImageReader(board)

        # Draw the board
        c.drawImage(
            img_reader, x_offset, y_offset, width=scaled_width, height=scaled_height
        )

        c.save()
        print(f"Board exported to PDF: {output_path}")

    def export_pdf_exact_size(
        self, output_path: str, width_mm: float, height_mm: float
    ):
        """
        Export the board as a PDF at exact physical size.

        Args:
            output_path: Path to save the PDF
            width_mm: Output width in millimeters
            height_mm: Output height in millimeters
        """
        board = self.render_board()

        # Ensure output directory exists
        os.makedirs(
            os.path.dirname(output_path) if os.path.dirname(output_path) else ".",
            exist_ok=True,
        )

        # Convert mm to points for PDF
        page_width_pt = mm_to_points(width_mm)
        page_height_pt = mm_to_points(height_mm)
        page_size = (page_width_pt, page_height_pt)

        # Create PDF with exact size
        c = canvas.Canvas(output_path, pagesize=page_size)

        # Scale board to fit exactly on the page
        scale_x = page_width_pt / board.width
        scale_y = page_height_pt / board.height
        scale = min(scale_x, scale_y)

        # Center the board
        scaled_width = board.width * scale
        scaled_height = board.height * scale
        x_offset = (page_width_pt - scaled_width) / 2
        y_offset = (page_height_pt - scaled_height) / 2

        # Convert PIL Image to format ReportLab can use
        img_reader = ImageReader(board)

        # Draw the board
        c.drawImage(
            img_reader, x_offset, y_offset, width=scaled_width, height=scaled_height
        )

        c.save()
        print(f"Board exported to PDF: {output_path} at {width_mm}x{height_mm}mm")
