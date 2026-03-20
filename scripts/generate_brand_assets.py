from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[1]
DOC_ROOTS = [ROOT / "docs", ROOT / "docs_es"]
SIZE = (1200, 630)

NAVY_900 = (14, 34, 56)
NAVY_800 = (22, 50, 79)
NAVY_700 = (36, 72, 108)
SKY_500 = (143, 191, 232)
SKY_200 = (216, 236, 251)
MIST_50 = (246, 250, 254)
WHITE = (255, 255, 255)


def make_gradient(size: tuple[int, int], top: tuple[int, int, int], bottom: tuple[int, int, int]) -> Image.Image:
    width, height = size
    image = Image.new("RGB", size, top)
    pixels = image.load()

    for y in range(height):
        ratio = y / max(height - 1, 1)
        color = tuple(
            int(top[index] * (1 - ratio) + bottom[index] * ratio) for index in range(3)
        )
        for x in range(width):
            pixels[x, y] = color

    return image


def rounded_paste(background: Image.Image, overlay: Image.Image, box: tuple[int, int], radius: int) -> None:
    mask = Image.new("L", overlay.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, overlay.width, overlay.height), radius=radius, fill=255)
    background.paste(overlay, box, mask)


def add_glow(canvas: Image.Image, color: tuple[int, int, int], box: tuple[int, int, int, int], blur: int, alpha: int) -> None:
    glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow)
    draw.ellipse(box, fill=(*color, alpha))
    glow = glow.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(glow)


def add_brand_corner(canvas: Image.Image, monogram_path: Path) -> None:
    monogram = Image.open(monogram_path).convert("RGBA")
    monogram = ImageOps.contain(monogram, (72, 72))
    chip = Image.new("RGBA", (118, 86), (255, 255, 255, 0))
    draw = ImageDraw.Draw(chip)
    draw.rounded_rectangle((0, 0, 118, 86), radius=26, fill=(255, 255, 255, 208))
    chip.alpha_composite(monogram, ((118 - monogram.width) // 2, (86 - monogram.height) // 2))
    canvas.alpha_composite(chip, (64, 48))


def build_base(monogram_path: Path) -> Image.Image:
    base = make_gradient(SIZE, NAVY_900, NAVY_800).convert("RGBA")
    add_glow(base, SKY_500, (730, -40, 1320, 440), blur=48, alpha=76)
    add_glow(base, SKY_200, (-120, 250, 420, 860), blur=56, alpha=42)
    add_brand_corner(base, monogram_path)

    panel = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(panel)
    draw.rounded_rectangle((54, 112, 1148, 574), radius=36, outline=(255, 255, 255, 24), width=1)
    panel = panel.filter(ImageFilter.GaussianBlur(0))
    base.alpha_composite(panel)
    return base


def build_profile_cover(doc_root: Path) -> None:
    monogram_path = doc_root / "assets" / "ae-monogram.png"
    portrait_path = doc_root / "assets" / "andres-espinosa.png"

    portrait = Image.open(portrait_path).convert("RGB")
    portrait = ImageOps.fit(portrait, (380, 470), method=Image.Resampling.LANCZOS, centering=(0.5, 0.2))

    base = build_base(monogram_path)

    accent = Image.new("RGBA", (420, 470), (0, 0, 0, 0))
    accent_draw = ImageDraw.Draw(accent)
    accent_draw.rounded_rectangle((0, 0, 420, 470), radius=34, fill=(216, 236, 251, 22), outline=(255, 255, 255, 28))
    accent_draw.rounded_rectangle((42, 290, 252, 338), radius=24, fill=(143, 191, 232, 210))
    accent_draw.rounded_rectangle((42, 354, 292, 402), radius=24, fill=(255, 255, 255, 74))
    accent_draw.rounded_rectangle((42, 418, 222, 452), radius=18, fill=(255, 255, 255, 42))
    base.alpha_composite(accent, (700, 92))

    portrait_rgba = portrait.convert("RGBA")
    rounded_paste(base, portrait_rgba, (734, 112), radius=30)

    left = Image.new("RGBA", (500, 260), (0, 0, 0, 0))
    draw = ImageDraw.Draw(left)
    draw.rounded_rectangle((0, 0, 308, 56), radius=28, fill=(255, 255, 255, 28))
    draw.rounded_rectangle((0, 82, 420, 130), radius=24, fill=(255, 255, 255, 20))
    draw.rounded_rectangle((0, 150, 356, 198), radius=24, fill=(255, 255, 255, 18))
    draw.rounded_rectangle((0, 218, 236, 254), radius=18, fill=(143, 191, 232, 172))
    base.alpha_composite(left, (120, 176))

    output = doc_root / "assets" / "andres-espinosa-cover.jpg"
    base.convert("RGB").save(output, quality=90, optimize=True, progressive=True)


def build_email_cover(doc_root: Path) -> None:
    monogram_path = doc_root / "assets" / "ae-monogram.png"
    base = build_base(monogram_path)
    draw = ImageDraw.Draw(base)

    draw.rounded_rectangle((116, 176, 530, 468), radius=34, fill=(255, 255, 255, 224))
    draw.rounded_rectangle((596, 162, 1042, 486), radius=34, fill=(255, 255, 255, 36), outline=(255, 255, 255, 28))

    draw.rounded_rectangle((160, 228, 484, 380), radius=22, outline=NAVY_800 + (255,), width=6, fill=(246, 250, 254, 255))
    draw.line((160, 228, 322, 336, 484, 228), fill=NAVY_800, width=6)

    for index, y in enumerate((212, 278, 344)):
        fill = (143, 191, 232, 196) if index == 0 else (255, 255, 255, 82)
        draw.rounded_rectangle((640, y, 980, y + 48), radius=18, fill=fill)
        draw.rounded_rectangle((1004, y + 6, 1040, y + 42), radius=18, fill=(216, 236, 251, 164))

    draw.line((532, 304, 596, 236), fill=SKY_500, width=8)
    draw.line((532, 304, 596, 302), fill=SKY_500, width=8)
    draw.line((532, 304, 596, 370), fill=SKY_500, width=8)

    for dot_x, dot_y in ((532, 304), (596, 236), (596, 302), (596, 370), (1004, 236), (1004, 302), (1004, 368)):
        draw.ellipse((dot_x - 8, dot_y - 8, dot_x + 8, dot_y + 8), fill=SKY_200)

    output = doc_root / "assets" / "diagrams" / "email-automation-architecture.png"
    base.convert("RGB").save(output, optimize=True)


def build_rag_cover(doc_root: Path) -> None:
    monogram_path = doc_root / "assets" / "ae-monogram.png"
    base = build_base(monogram_path)
    draw = ImageDraw.Draw(base)

    draw.rounded_rectangle((108, 162, 516, 504), radius=34, fill=(255, 255, 255, 220))
    draw.rounded_rectangle((170, 216, 454, 270), radius=20, fill=(216, 236, 251, 255))
    draw.rounded_rectangle((190, 230, 346, 246), radius=8, fill=NAVY_700)
    draw.rounded_rectangle((190, 252, 424, 268), radius=8, fill=(120, 154, 188))
    draw.ellipse((392, 214, 450, 272), outline=NAVY_800, width=6)
    draw.line((438, 262, 472, 296), fill=NAVY_800, width=6)

    for y in (208, 286, 364):
        draw.rounded_rectangle((632, y, 1032, y + 58), radius=20, fill=(255, 255, 255, 40))
        draw.rounded_rectangle((660, y + 16, 874, y + 30), radius=7, fill=SKY_200)
        draw.rounded_rectangle((660, y + 36, 944, y + 48), radius=6, fill=(255, 255, 255, 72))
        draw.rounded_rectangle((964, y + 14, 1004, y + 44), radius=16, fill=(143, 191, 232, 170))

    for center in ((604, 236), (580, 318), (612, 398), (560, 446), (720, 430), (792, 478)):
        draw.ellipse((center[0] - 8, center[1] - 8, center[0] + 8, center[1] + 8), fill=SKY_500)

    draw.line((516, 254, 604, 236), fill=SKY_500, width=6)
    draw.line((516, 334, 580, 318), fill=SKY_500, width=6)
    draw.line((516, 414, 612, 398), fill=SKY_500, width=6)

    output = doc_root / "assets" / "diagrams" / "rag-hybrid-search-architecture.png"
    base.convert("RGB").save(output, optimize=True)


def build_api_cover(doc_root: Path) -> None:
    monogram_path = doc_root / "assets" / "ae-monogram.png"
    base = build_base(monogram_path)
    draw = ImageDraw.Draw(base)

    draw.rounded_rectangle((128, 176, 418, 454), radius=32, fill=(255, 255, 255, 224))
    draw.rounded_rectangle((490, 150, 1076, 482), radius=36, fill=(255, 255, 255, 34), outline=(255, 255, 255, 24))

    for y in (226, 302, 378):
        draw.rounded_rectangle((554, y, 954, y + 48), radius=18, fill=(255, 255, 255, 28))
        draw.rounded_rectangle((574, y + 15, 764, y + 29), radius=7, fill=SKY_200)
        draw.rounded_rectangle((574, y + 34, 894, y + 44), radius=6, fill=(255, 255, 255, 78))

    draw.rounded_rectangle((182, 226, 364, 272), radius=18, fill=(143, 191, 232, 198))
    draw.rounded_rectangle((182, 300, 364, 346), radius=18, fill=(255, 255, 255, 78))
    draw.rounded_rectangle((182, 374, 364, 420), radius=18, fill=(255, 255, 255, 54))

    for point in ((418, 248), (506, 248), (418, 324), (506, 324), (418, 400), (506, 400), (974, 248), (974, 324), (974, 400)):
        draw.ellipse((point[0] - 8, point[1] - 8, point[0] + 8, point[1] + 8), fill=SKY_500)

    draw.line((418, 248, 506, 248, 506, 324, 418, 324), fill=SKY_500, width=6)
    draw.line((506, 324, 418, 400, 506, 400), fill=SKY_500, width=6)
    draw.line((974, 248, 1018, 248), fill=SKY_200, width=6)
    draw.line((974, 324, 1018, 324), fill=SKY_200, width=6)
    draw.line((974, 400, 1018, 400), fill=SKY_200, width=6)

    output = doc_root / "assets" / "diagrams" / "ai-api-platform-architecture.png"
    base.convert("RGB").save(output, optimize=True)


def build_portrait_jpg(doc_root: Path) -> None:
    portrait = Image.open(doc_root / "assets" / "andres-espinosa.png").convert("RGB")
    portrait.save(doc_root / "assets" / "andres-espinosa.jpg", quality=90, optimize=True, progressive=True)


def main() -> None:
    for doc_root in DOC_ROOTS:
        build_portrait_jpg(doc_root)
        build_profile_cover(doc_root)
        build_email_cover(doc_root)
        build_rag_cover(doc_root)
        build_api_cover(doc_root)


if __name__ == "__main__":
    main()
