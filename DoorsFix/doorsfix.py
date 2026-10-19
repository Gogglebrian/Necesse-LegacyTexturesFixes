#!/usr/bin/env python3
"""
Update legacy Necesse wall/door spritesheet to the newer template layout.
Windows (and their under-alpha colors) stay exactly as in the current sheet.
"""

import sys
from PIL import Image

def update_spritesheet(legacy_path: str, current_path: str, output_path: str) -> None:
    legacy  = Image.open(legacy_path).convert("RGBA")
    current = Image.open(current_path).convert("RGBA")

    # ------------------------------------------------------------------
    # Start with an exact copy of the current sheet.
    # This keeps every window sprite and every transparent-pixel RGB value
    # identical to woodwall_current.png.
    # ------------------------------------------------------------------
    new_sheet = current.copy()

    # ------------------------------------------------------------------
    # Helper: create a fully transparent rectangle of a given size
    # ------------------------------------------------------------------
    def make_transparent(w: int, h: int) -> Image.Image:
        return Image.new("RGBA", (w, h), (0, 0, 0, 0))

    # ------------------------------------------------------------------
    # 1. Walls – overwrite with the legacy walls (same position)
    # ------------------------------------------------------------------
    wall_box = (0, 0, 64, 128)          # adjust if needed
    wall_w = wall_box[2] - wall_box[0]
    wall_h = wall_box[3] - wall_box[1]

    # Clear the area first
    new_sheet.paste(make_transparent(wall_w, wall_h), (wall_box[0], wall_box[1]))
    walls = legacy.crop(wall_box)
    new_sheet.paste(walls, (0, 0), walls)

    # ------------------------------------------------------------------
    # 2. Doorframes – Assemble some new programmer art from the wall tops
    # ------------------------------------------------------------------

    # clear the door area
    new_sheet.paste(make_transparent(8 * 32, 4 * 32), (96, 0))

    doorframe_mappings = [
        #horizontal frames
        ((16, 40, 48, 56), (96, 112)),
        ((16, 40, 48, 56), (128, 112)),
        ((16, 40, 48, 56), (224, 112)),
        ((16, 40, 48, 56), (256, 112)),

        #vertical frame on left
        ((0, 16, 16, 48), (174, 96)),
        ((0, 16, 16, 48), (206, 96)),

        #vertical frame on right
        ((48, 16, 64, 48), (290, 96)),
        ((48, 16, 64, 48), (322, 96)),
    ]

    for src_box, dest_pos in doorframe_mappings:
        doorframe = legacy.crop(src_box)
        new_sheet.paste(doorframe, dest_pos, doorframe)

    # ------------------------------------------------------------------
    # 3. Doors – overwrite the new template positions with legacy door art
    # ------------------------------------------------------------------
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

    # ------------------------------------------------------------------
    # 4. Windows are already perfect because we started from `current`.
    #    No extra paste needed.
    # ------------------------------------------------------------------

    new_sheet.save(output_path, "PNG")
    print(f"Saved → {output_path}")
    print(f"Size: {new_sheet.size}  Mode: {new_sheet.mode}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python update_woodwall.py <legacy.png> <current.png> <output.png>")
        sys.exit(1)
    update_spritesheet(sys.argv[1], sys.argv[2], sys.argv[3])