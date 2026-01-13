from PIL import Image, ImageDraw, ImageFont
from typing import Optional, Tuple
from pathlib import Path


class Tile:
    def __init__(
        self,
        width: int = 200,
        height: int = 100,
        header: Optional[str] = None,
        text: Optional[str] = None,
        image_path: Optional[str] = None,
        image_scale: float = 0.8,
        image_margin_top: Optional[int] = None,
        background_color: Tuple[int, int, int] | str = (255, 255, 255),
        text_color: Tuple[int, int, int] = (0, 0, 0),
        border_color: Tuple[int, int, int] = (0, 0, 0),
        border_width: int = 2,
    ):
        self.width = width
        self.height = height
        self.header = header
        self.text = text
        self.image_path = image_path
        self.image_scale = image_scale
        self.image_margin_top = image_margin_top
        self.background_color = background_color
        self.text_color = text_color
        self.border_color = border_color
        self.border_width = border_width

    def _get_font(self, size: int, font_type: str = "text") -> ImageFont.ImageFont:
        """
        Get font based on type: header uses gbboot.ttf, text uses pokemon_classic.ttf.

        Args:
            size: Font size in points
            font_type: "header" or "text" (default: "text")

        Returns:
            PIL ImageFont object
        """
        project_root = Path(__file__).parent.parent
        fonts_dir = project_root / "assets" / "fonts"

        if font_type == "header":
            # Header uses gbboot.ttf
            font_path = fonts_dir / "gbboot.ttf"
            if font_path.exists():
                try:
                    return ImageFont.truetype(str(font_path), size)
                except Exception as e:
                    print(f"Warning: Could not load gbboot.ttf font: {e}")
        else:
            # Text uses pokemon_classic.ttf
            font_path = fonts_dir / "gil.ttf"
            if font_path.exists():
                try:
                    return ImageFont.truetype(str(font_path), size)
                except Exception as e:
                    print(f"Warning: Could not load pokemon_classic.ttf font: {e}")

        # Fallback to system font
        try:
            return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)
        except Exception:
            # Final fallback to default font
            return ImageFont.load_default()

    def render(self) -> Image.Image:
        # Create base image
        img = Image.new("RGB", (self.width, self.height), self.background_color)
        draw = ImageDraw.Draw(img)

        # Draw border
        if self.border_width > 0:
            for i in range(self.border_width):
                draw.rectangle(
                    [i, i, self.width - 1 - i, self.height - 1 - i],
                    outline=self.border_color,
                )

        # Draw header at the top
        header_height = 0
        if self.header:
            try:
                # Use gbboot.ttf for header
                header_font_size = min(self.width, self.height) // 8
                header_font = self._get_font(header_font_size, font_type="header")

                # Calculate header height
                header_bbox = draw.textbbox((0, 0), self.header, font=header_font)
                header_height = header_bbox[3] - header_bbox[1]
                header_y = self.border_width + 20  # More padding from border/top

                # Center header horizontally
                header_bbox = draw.textbbox((0, 0), self.header, font=header_font)
                header_width = header_bbox[2] - header_bbox[0]
                header_x = (self.width - header_width) // 2

                # Then draw main text on top
                draw.text(
                    (header_x, header_y),
                    self.header,
                    fill=self.text_color,
                    font=header_font,
                )

                # Add some spacing after header
                header_height += 10
            except Exception as e:
                print(f"Warning: Could not render header: {e}")
                import traceback

                traceback.print_exc()

        # Load and paste image if provided
        if self.image_path:
            try:
                tile_image = Image.open(self.image_path)

                # Convert to RGBA if image has transparency (handles P mode with transparency)
                if tile_image.mode in ("P", "LA"):
                    # Convert palette/grayscale with alpha to RGBA
                    tile_image = tile_image.convert("RGBA")
                elif tile_image.mode != "RGBA":
                    # Convert RGB to RGBA (add full opacity alpha channel)
                    tile_image = tile_image.convert("RGBA")

                # Resize image using scale parameter
                base_width = self.width - (self.border_width * 2)
                target_width = int(base_width * self.image_scale)

                # Calculate height to maintain aspect ratio
                aspect_ratio = tile_image.height / tile_image.width
                target_height = int(target_width * aspect_ratio)

                # Resize image
                tile_image = tile_image.resize(
                    (target_width, target_height), Image.Resampling.LANCZOS
                )

                # Center horizontally, position vertically
                x_offset = (self.width - tile_image.width) // 2

                # Position image using margin_top parameter or default behavior
                if self.image_margin_top is not None:
                    # Use explicit margin_top value
                    y_offset = self.image_margin_top
                elif self.header:
                    # Default: position right after header with -10 margin
                    y_offset = self.border_width + header_height - 10
                else:
                    # Default: position at top with -10 margin
                    y_offset = self.border_width - 10

                # Ensure y_offset doesn't go negative (clamp to 0 minimum) and is an integer
                y_offset = max(0, int(y_offset))

                # Paste with alpha channel support (transparency preserved)
                if tile_image.mode == "RGBA":
                    img.paste(tile_image, (x_offset, y_offset), tile_image)
                else:
                    img.paste(tile_image, (x_offset, y_offset))
            except Exception as e:
                print(f"Warning: Could not load image {self.image_path}: {e}")
                import traceback

                traceback.print_exc()

        # Draw text if provided
        if self.text:
            try:
                font_size = min(self.width, self.height) // 13
                font = self._get_font(font_size, font_type="text")

                # Calculate available space for text
                padding = 10
                available_width = self.width - (padding * 2) - (self.border_width * 2)

                # Account for header space
                header_space = header_height if self.header else 0

                # If image exists, reserve space at top; text goes at bottom
                if self.image_path:
                    # Reserve space for image at top
                    image_area_height = self.height // 2
                    available_height = (
                        self.height
                        - image_area_height
                        - padding
                        - self.border_width
                        - header_space
                    )
                    text_y_start = image_area_height + padding
                else:
                    # Text can use remaining height after header
                    available_height = (
                        self.height - (padding * 2) - self.border_width - header_space
                    )
                    text_y_start = padding + self.border_width + header_space

                # First split by explicit newlines (\n), then wrap each paragraph
                paragraphs = self.text.split("\n")
                lines = []

                for paragraph in paragraphs:
                    # Wrap each paragraph to fit within available width
                    words = paragraph.split()
                    current_line = []

                    for word in words:
                        # Test if adding this word would exceed width
                        test_line = " ".join(current_line + [word])
                        bbox = draw.textbbox((0, 0), test_line, font=font)
                        test_width = bbox[2] - bbox[0]

                        if test_width <= available_width:
                            current_line.append(word)
                        else:
                            # Current line is full, start a new one
                            if current_line:
                                lines.append(" ".join(current_line))
                            current_line = [word]

                    # Add the last line of this paragraph
                    if current_line:
                        lines.append(" ".join(current_line))

                # Calculate total text height
                line_height = (
                    draw.textbbox((0, 0), "Ag", font=font)[3]
                    - draw.textbbox((0, 0), "Ag", font=font)[1]
                )
                total_text_height = len(lines) * line_height

                # Center text vertically within available space
                if self.image_path:
                    # Text at bottom, but centered horizontally
                    y = text_y_start + (available_height - total_text_height) // 2
                else:
                    # Center vertically in full tile
                    y = (self.height - total_text_height) // 2

                # Draw each line, centered horizontally
                for line in lines:
                    bbox = draw.textbbox((0, 0), line, font=font)
                    text_width = bbox[2] - bbox[0]
                    x = (self.width - text_width) // 2
                    draw.text((x, y), line, fill=self.text_color, font=font)
                    y += line_height

            except Exception as e:
                print(f"Warning: Could not render text: {e}")

        return img
