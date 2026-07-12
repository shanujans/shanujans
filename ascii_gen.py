#!/usr/bin/env python3
"""
ascii_gen.py

Converts an image (shanujans.png) into ASCII art and outputs it as
SVG <tspan> lines suitable for embedding in the neofetch-style SVG card.

Usage:
    python ascii_gen.py [image_path] [output_width]

Defaults:
    image_path   = shanujans.png
    output_width = 48 (characters)
"""

import sys
from pathlib import Path
from PIL import Image, ImageEnhance

ROOT = Path(__file__).parent

ASCII_CHARS = " .:-=+*#%@"


def image_to_ascii(image_path: Path, width: int = 48) -> list[str]:
    img = Image.open(image_path).convert("L")

    img = ImageEnhance.Contrast(img).enhance(1.8)
    img = ImageEnhance.Brightness(img).enhance(1.1)

    aspect = img.height / img.width
    char_aspect = 0.5
    height = max(1, int(aspect * width * char_aspect))
    height = min(height, 30)

    img = img.resize((width, height))

    lines = []
    for y in range(height):
        row = ""
        for x in range(width):
            pixel = img.getpixel((x, y))
            idx = int(pixel / 255 * (len(ASCII_CHARS) - 1))
            row += ASCII_CHARS[idx]
        lines.append(row)
    return lines


def ascii_to_svg_tspans(lines: list[str], x: int = 20, y_start: int = 60, y_step: int = 20) -> str:
    tspans = []
    for i, line in enumerate(lines):
        y = y_start + i * y_step
        escaped = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        tspans.append(f'<tspan x="{x}" y="{y}">{escaped}</tspan>')
    return "\n".join(tspans)


def generate_ascii_fragment(image_path: Path, width: int = 48) -> str:
    lines = image_to_ascii(image_path, width)
    return ascii_to_svg_tspans(lines)


def main():
    image_path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "shanujans.png"
    width = int(sys.argv[2]) if len(sys.argv) > 2 else 48

    if not image_path.exists():
        print(f"ERROR: {image_path} not found", file=sys.stderr)
        sys.exit(1)

    fragment = generate_ascii_fragment(image_path, width)

    output = ROOT / "ascii_art.svg"
    output.write_text(fragment, encoding="utf-8")
    lines = fragment.count("\n") + 1
    print(f"Generated {lines} lines of ASCII art ({width} chars wide)")
    print(f"Written to {output}")


if __name__ == "__main__":
    main()
