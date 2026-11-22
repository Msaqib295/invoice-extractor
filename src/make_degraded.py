import sys
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps

OUT = Path("samples_degraded")
OUT.mkdir(exist_ok=True)

for path in sys.argv[1:]:
    img = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    stem = Path(path).stem
    img.filter(ImageFilter.GaussianBlur(img.width / 800)).save(OUT / f"{stem}_blur_light.png")
    img.filter(ImageFilter.GaussianBlur(img.width / 300)).save(OUT / f"{stem}_blur_heavy.png")
    img.resize((img.width // 3, img.height // 3)).save(OUT / f"{stem}_lowres.png")