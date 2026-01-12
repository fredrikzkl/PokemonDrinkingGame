from PIL import Image, ImageDraw, ImageFont
from typing import Optional, Tuple


class Tile:
    def __init__(
        self,
        width: int = 200,
        height: int = 100,
        header: Optional[str] = None,
        text: Optional[str] = None,
        image_path: Optional[str] = None,
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
        self.background_color = background_color
        self.text_color = text_color
        self.border_color = border_color
        self.border_width = border_width

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

        # Draw header
        # TODO

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

                # Resize image to fill tile width (accounting for borders)
                target_width = self.width - (self.border_width * 2)

                # Calculate height to maintain aspect ratio
                aspect_ratio = tile_image.height / tile_image.width
                target_height = int(target_width * aspect_ratio)

                # Resize image to fill width
                tile_image = tile_image.resize(
                    (target_width, target_height), Image.Resampling.LANCZOS
                )

                # Center horizontally, position vertically
                x_offset = (self.width - tile_image.width) // 2

                # Position image at the very top (to account for white padding in sprites)
                y_offset = self.border_width  # Right at the border, at the top

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
                # Try to use a nice font, fallback to default if not available
                try:
                    font_size = (
                        min(self.width, self.height) // 12
                    )  # Slightly smaller for wrapping
                    font = ImageFont.truetype(
                        "/System/Library/Fonts/Helvetica.ttc", font_size
                    )
                except:
                    font = ImageFont.load_default()

                # Calculate available space for text
                padding = 10
                available_width = self.width - (padding * 2) - (self.border_width * 2)

                # If image exists, reserve space at top; text goes at bottom
                if self.image_path:
                    # Reserve space for image at top
                    image_area_height = self.height // 2
                    available_height = (
                        self.height - image_area_height - padding - self.border_width
                    )
                    text_y_start = image_area_height + padding
                else:
                    # Text can use full height
                    available_height = (
                        self.height - (padding * 2) - (self.border_width * 2)
                    )
                    text_y_start = padding + self.border_width

                # Wrap text to fit within available width
                words = self.text.split()
                lines = []
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

                # Add the last line
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
