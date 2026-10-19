#!/usr/bin/env python3
"""
Batch-update legacy Necesse wall/door spritesheets.

Folder layout expected:
    legacy/   ← old spritesheets
    current/  ← new template spritesheets (same filenames)
    output/   ← results will be written here

Usage:
    python batch_update_walls.py
"""

import os
import sys
from pathlib import Path
from PIL import Image

# ------------------------------------------------------------------
# Configuration – change these paths if your folders live elsewhere
# ------------------------------------------------------------------
LEGACY_DIR  = Path("legacy")
CURRENT_DIR = Path("current")
OUTPUT_DIR  = Path("output")

# ------------------------------------------------------------------
# The update logic (same as your final single-file script)
# ------------------------------------------------------------------
def update_spritesheet(legacy_path: Path, current_path: Path, output_path: Path) -> None:
    legacy  = Image.open(legacy_path).convert("RGBA")
    current = Image.open(current_path).convert("RGBA")

    new_sheet = current.copy()

    def make_transparent(w: int, h: int) -> Image.Image:
        return Image.new("RGBA", (w, h), (0, 0, 0, 0))

    # 1. Walls
    wall_box = (0, 0, 64, 128)
    wall_w = wall_box[2] - wall_box[0]
    wall_h = wall_box[3] - wall_box[1]

    new_sheet.paste(make_transparent(wall_w, wall_h), (wall_box[0], wall_box[1]))
    walls = legacy.crop(wall_box)
    new_sheet.paste(walls, (0, 0), walls)

    # 2. Doorframes

    # Clear the whole door area once
    new_sheet.paste(make_transparent(8 * 32, 4 * 32), (96, 0))

    doorframe_mappings = [
        # horizontal frames
        ((16, 40, 48, 56), (96, 112)),
        ((16, 40, 48, 56), (128, 112)),
        ((16, 40, 48, 56), (224, 112)),
        ((16, 40, 48, 56), (256, 112)),

        # vertical frame on left
        ((0, 16, 16, 48), (174, 96)),
        ((0, 16, 16, 48), (206, 96)),

        # vertical frame on right
        ((48, 16, 64, 48), (290, 96)),
        ((48, 16, 64, 48), (322, 96)),
    ]
    
    for src_box, dest_pos in doorframe_mappings:
        doorframe = legacy.crop(src_box)
        new_sheet.paste(doorframe, dest_pos, doorframe)

    # 3. Doors
    door_mappings = [
        # Example mappings – replace these with the exact regions you measured
        # Format: (src_left, src_top, src_right, src_bottom), (dest_x, dest_y)

        # Front-facing, handle on right side
        ((64, 64, 96, 128), (224, 58)),
        ((64, 64, 96, 128), (320, 58)),

        # Front-facing, handle on left side
        ((160, 0, 192, 64), (96, 58)),
        ((160, 0, 192, 64), (192, 40)),

        # Side-facing, on right side
        ((96, 64, 128, 192), (128, 58)),
        ((96, 64, 128, 192), (160, 58)),

        # Side-facing, on left side
        ((96, 0, 128, 64), (256, 58)),
        ((96, 0, 128, 64), (288, 58)),
    ]

    for src_box, dest_pos in door_mappings:
        door = legacy.crop(src_box)
        new_sheet.paste(door, dest_pos, door)

    # 3. Windows stay untouched (copied from current)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    new_sheet.save(output_path, "PNG")
    print(f"  ✓ {legacy_path.name}  →  {output_path}")


# ------------------------------------------------------------------
# Batch processing
# ------------------------------------------------------------------
def main():
    if not LEGACY_DIR.is_dir():
        print(f"Error: legacy folder not found: {LEGACY_DIR.resolve()}")
        sys.exit(1)
    if not CURRENT_DIR.is_dir():
        print(f"Error: current folder not found: {CURRENT_DIR.resolve()}")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Collect all PNG files in the legacy folder
    legacy_files = sorted(LEGACY_DIR.glob("*.png")) + sorted(LEGACY_DIR.glob("*.PNG"))

    if not legacy_files:
        print("No PNG files found in the legacy folder.")
        sys.exit(0)

    print(f"Found {len(legacy_files)} file(s) in legacy/ …\n")

    success = 0
    skipped = 0

    for legacy_path in legacy_files:
        name = legacy_path.name
        current_path = CURRENT_DIR / name
        output_path  = OUTPUT_DIR  / name

        if not current_path.is_file():
            print(f"  ✗ Skipping {name}  (no matching file in current/)")
            skipped += 1
            continue

        try:
            update_spritesheet(legacy_path, current_path, output_path)
            success += 1
        except Exception as e:
            print(f"  ✗ Failed {name}: {e}")
            skipped += 1

    print(f"\nDone.  {success} updated,  {skipped} skipped.")
    print(f"Results are in: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()