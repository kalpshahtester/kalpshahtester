from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 720, 170
BG = (247, 247, 242)
GRAPHITE = (23, 26, 23)
MUTED = (104, 112, 104)
GREEN = (39, 166, 106)
RED = (201, 90, 80)
AMBER = (201, 155, 56)
BLUE = (91, 155, 213)

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

steps = [
    ("DEFECT FOUND", RED),
    ("EVIDENCE", BLUE),
    ("BUG REPORTED", AMBER),
    ("FIXED", GREEN),
    ("RETEST", AMBER),
    ("VERIFIED", GREEN),
]

font = ImageFont.truetype(FONT, 14)
bold = ImageFont.truetype(BOLD, 18)
small = ImageFont.truetype(MONO, 11)

frames = []
for active in range(len(steps)):
    image = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(image)

    draw.rectangle((12, 12, W - 12, H - 12), outline=GRAPHITE, width=1)
    draw.text((24, 24), "BUG LIFECYCLE / QA-02", font=small, fill=MUTED)
    draw.text(
        (24, 45),
        "DEFECT → EVIDENCE → FIX → VERIFIED",
        font=bold,
        fill=GRAPHITE,
    )

    left = 24
    y = 92
    gap = 7
    box_width = (W - 48 - 5 * gap) // 6

    for index, (label, accent) in enumerate(steps):
        x = left + index * (box_width + gap)
        is_active = index == active
        # Keep intermediate states quiet; make VERIFIED the only strong terminal state.
        is_verified = index == len(steps) - 1
        fill = GREEN if is_verified else ((229, 232, 226) if is_active else (236, 238, 232))
        outline = GREEN if is_verified else ((180, 187, 179) if is_active else (205, 209, 202))
        text_color = (255, 255, 255) if is_verified else GRAPHITE

        draw.rounded_rectangle(
            (x, y, x + box_width, y + 38),
            radius=6,
            fill=fill,
            outline=outline,
            width=2 if is_verified else 1,
        )

        bounds = draw.textbbox((0, 0), label, font=font)
        text_width = bounds[2] - bounds[0]
        draw.text(
            (x + (box_width - text_width) // 2, y + 12),
            label,
            font=font,
            fill=text_color,
        )

    draw.text(
        (24, 143),
        "Evidence-first QA · reproduce → report → retest → verify",
        font=small,
        fill=MUTED,
    )
    frames.append(image)

output = Path("assets/process/bug-to-verified.gif")
output.parent.mkdir(parents=True, exist_ok=True)

frames[0].save(
    output,
    save_all=True,
    append_images=frames[1:],
    duration=[1200] * 5 + [3000],
    loop=0,
    optimize=True,
)

print(f"Generated {output} ({output.stat().st_size} bytes)")
