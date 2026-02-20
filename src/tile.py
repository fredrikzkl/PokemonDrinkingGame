import re
from PIL import Image, ImageDraw, ImageFont
from typing import Optional, Tuple, List
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
        image_anchor_bottom: bool = False,
        background_color: Tuple[int, int, int] | str = (255, 255, 255),
        text_color: Tuple[int, int, int] = (0, 0, 0),
        border_color: Tuple[int, int, int] = (0, 0, 0),
        border_width: int = 0,
        font_size: Optional[int] = None,
        footer: Optional[str] = None,
        background_image: Optional[str] = None,
        text_margin_top: int = 0,
        text_align: str = "center",
    ):
        self.width = width
        self.height = height
        self.header = header
        self.text = text
        self.image_path = image_path
        self.image_scale = image_scale
        self.image_margin_top = image_margin_top
        self.image_anchor_bottom = image_anchor_bottom
        self.background_color = background_color
        self.text_color = text_color
        self.border_color = border_color
        self.border_width = border_width
        self.font_size = font_size
        self.footer = footer
        self.background_image = background_image
        self.text_align = text_align
        self.text_margin_top = text_margin_top

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
            # Text uses gil.ttf (vector font - scales cleanly)
            font_path = fonts_dir / "gil.ttf"
            # font_path = fonts_dir / "pkmon_rby.ttf"  # pixel font - only looks good at specific sizes
            if font_path.exists():
                try:
                    return ImageFont.truetype(str(font_path), size)
                except Exception as e:
                    print(f"Warning: Could not load gil.ttf font: {e}")

        # Fallback to system font
        try:
            return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)
        except Exception:
            # Final fallback to default font
            return ImageFont.load_default()

    def _parse_styled_words(self, text: str) -> List[Tuple[str, bool]]:
        """Parse text with **bold** markers into [(word, is_bold), ...]."""
        segments = re.split(r"(\*\*.*?\*\*)", text)
        result = []
        for segment in segments:
            if not segment:
                continue
            is_bold = segment.startswith("**") and segment.endswith("**")
            clean = segment[2:-2] if is_bold else segment
            for word in clean.split():
                result.append((word, is_bold))
        return result

    def _group_line_segments(
        self, styled_line: List[Tuple[str, bool]]
    ) -> List[Tuple[str, bool]]:
        """Group consecutive words with same bold state into (text, is_bold) segments."""
        if not styled_line:
            return []
        segments = []
        current_bold = styled_line[0][1]
        current_words = [styled_line[0][0]]
        for word, is_bold in styled_line[1:]:
            if is_bold == current_bold:
                current_words.append(word)
            else:
                segments.append((" ".join(current_words), current_bold))
                current_bold = is_bold
                current_words = [word]
        segments.append((" ".join(current_words), current_bold))
        return segments

    def render(self) -> Image.Image:
        img = Image.new("RGB", (self.width, self.height), self.background_color)

        if self.background_image:
            try:
                bg_img = Image.open(self.background_image).convert("RGB")
                bg_img = bg_img.resize(
                    (self.width, self.height), Image.Resampling.LANCZOS
                )
                img.paste(bg_img, (0, 0))
            except Exception as e:
                print(f"Warning: Could not load background image {self.background_image}: {e}")

        draw = ImageDraw.Draw(img)

        # Draw border on all sides
        if self.border_width > 0:
            for i in range(self.border_width):
                draw.rectangle(
                    [i, i, self.width - 1 - i, self.height - 1 - i],
                    outline=self.border_color,
                )

        # Calculate header dimensions (needed for image positioning)
        header_height = 0
        header_font = None
        header_x = 0
        header_y = 0
        if self.header:
            try:
                header_font_size = min(self.width, self.height) // 8
                header_font = self._get_font(header_font_size, font_type="header")
                header_bbox = draw.textbbox((0, 0), self.header, font=header_font)
                header_height = header_bbox[3] - header_bbox[1]
                header_y = self.border_width + 20
                header_width = header_bbox[2] - header_bbox[0]
                header_x = (self.width - header_width) // 2
                header_height += 10
            except Exception as e:
                print(f"Warning: Could not calculate header: {e}")

        # Load and paste image (drawn before header/text so it's always behind)
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

                if self.image_anchor_bottom:
                    y_offset = self.height - tile_image.height
                elif self.image_margin_top is not None:
                    y_offset = self.image_margin_top
                elif self.header:
                    y_offset = self.border_width + header_height - 10
                else:
                    y_offset = self.border_width - 10

                # Convert to integer (allow negative values for positioning above border)
                y_offset = int(y_offset)

                # Paste with alpha channel support (transparency preserved)
                if tile_image.mode == "RGBA":
                    img.paste(tile_image, (x_offset, y_offset), tile_image)
                else:
                    img.paste(tile_image, (x_offset, y_offset))
            except Exception as e:
                print(f"Warning: Could not load image {self.image_path}: {e}")
                import traceback

                traceback.print_exc()

        # Draw header on top of image
        if self.header and header_font:
            draw.text(
                (header_x, header_y),
                self.header,
                fill=self.text_color,
                font=header_font,
            )

        # Draw text if provided
        if self.text:
            try:
                font_size = (
                    self.font_size
                    if self.font_size
                    else min(self.width, self.height) // 14
                )
                font = self._get_font(font_size, font_type="text")

                # Calculate available space for text
                padding = 10
                available_width = self.width - (padding * 2) - (self.border_width * 2)

                # Account for header space
                header_space = header_height if self.header else 0

                if self.image_path and self.image_anchor_bottom:
                    image_area_height = self.height // 2
                    available_height = image_area_height
                    text_y_start = header_space
                elif self.image_path:
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

                paragraphs = self.text.split("\n")
                styled_lines = []

                for paragraph in paragraphs:
                    stripped = paragraph.strip()
                    if not stripped or stripped == "\\n":
                        styled_lines.append(None)
                        continue

                    styled_words = self._parse_styled_words(paragraph)
                    current_line = []

                    for word, is_bold in styled_words:
                        test_text = " ".join(w for w, _ in current_line + [(word, is_bold)])
                        bbox = draw.textbbox((0, 0), test_text, font=font)
                        test_width = bbox[2] - bbox[0]

                        if test_width <= available_width:
                            current_line.append((word, is_bold))
                        else:
                            if current_line:
                                styled_lines.append(current_line)
                            current_line = [(word, is_bold)]

                    if current_line:
                        styled_lines.append(current_line)

                base_line_height = (
                    draw.textbbox((0, 0), "Ag", font=font)[3]
                    - draw.textbbox((0, 0), "Ag", font=font)[1]
                )
                line_height = int(base_line_height * 1.2)
                total_text_height = len(styled_lines) * line_height

                if self.image_path:
                    y = text_y_start + (available_height - total_text_height) // 2 + self.text_margin_top
                else:
                    y = (self.height - total_text_height) // 2 + self.text_margin_top

                for styled_line in styled_lines:
                    if styled_line is None:
                        y += line_height // 2
                        continue
                    line_text = " ".join(w for w, _ in styled_line)
                    bbox = draw.textbbox((0, 0), line_text, font=font)
                    total_width = bbox[2] - bbox[0]
                    padding = 10
                    if self.text_align == "left":
                        start_x = padding + self.border_width
                    else:
                        start_x = (self.width - total_width) // 2

                    segments = self._group_line_segments(styled_line)
                    char_pos = 0
                    for seg_idx, (seg_text, is_bold) in enumerate(segments):
                        prefix = line_text[:char_pos]
                        if prefix:
                            prefix_w = (
                                draw.textbbox((0, 0), prefix, font=font)[2]
                                - draw.textbbox((0, 0), prefix, font=font)[0]
                            )
                        else:
                            prefix_w = 0

                        seg_x = start_x + prefix_w
                        draw.text((seg_x, y), seg_text, fill=self.text_color, font=font)
                        if is_bold:
                            draw.text((seg_x + 1, y), seg_text, fill=self.text_color, font=font)

                        char_pos += len(seg_text)
                        if seg_idx < len(segments) - 1:
                            char_pos += 1

                    y += line_height

            except Exception as e:
                print(f"Warning: Could not render text: {e}")

        if self.footer:
            try:
                footer_font_size = min(self.width, self.height) // 10
                footer_font = self._get_font(footer_font_size, font_type="header")
                footer_bbox = draw.textbbox((0, 0), self.footer, font=footer_font)
                footer_width = footer_bbox[2] - footer_bbox[0]
                footer_height = footer_bbox[3] - footer_bbox[1]
                footer_x = (self.width - footer_width) // 2
                footer_y = self.height - footer_height - self.border_width - 20
                draw.text(
                    (footer_x, footer_y),
                    self.footer,
                    fill=self.text_color,
                    font=footer_font,
                )
            except Exception as e:
                print(f"Warning: Could not render footer: {e}")

        return img
