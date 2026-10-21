"""Powiekszenia okolic wykrytych drzwi (do recznej weryfikacji) - drzwi_krea.csv."""
import csv, glob
from PIL import Image, ImageDraw, ImageFont
exec(open("drzwi_krea.py", encoding="utf-8").read().rsplit("rows, kom = [], []", 1)[0])
R = list(csv.DictReader(open("wyniki/drzwi_krea.csv", encoding="utf-8-sig"), delimiter=";"))
fn = dict(ZEST); kl = {v[0]: k for k, v in WEJ.items()}
S = 230; FS = ImageFont.truetype("arial.ttf", 13); cols = 8
sh = Image.new("RGB", (cols * (S + 4), ((len(R) + cols - 1) // cols) * (S + 34)), (40, 48, 36)); d = ImageDraw.Draw(sh)
for n, r in enumerate(R):
    im = Image.open(fn[r["zestaw"]](kl[r["budynek"]])).convert("RGB"); (sc, bb, _), _ = znajdz(im)
    w, h = bb[2] - bb[0], bb[3] - bb[1]; cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2; m = max(w, h) * 1.4
    v = im.copy(); ImageDraw.Draw(v).rectangle(bb, outline=(0, 255, 0), width=2)
    c = v.crop((int(cx - m), int(cy - m), int(cx + m), int(cy + m))).resize((S, S), Image.NEAREST)
    x, y = (n % cols) * (S + 4), (n // cols) * (S + 34); sh.paste(c, (x, y))
    d.text((x + 2, y + S + 2), f"{n}: {r['budynek']}", font=FS, fill=(255, 230, 140)); d.text((x + 2, y + S + 17), r["zestaw"].replace("LoRA ", "").replace(" · ", " "), font=FS, fill=(200, 210, 190))
sh.save("wyniki/drzwi_krea_zoom.png"); print(sh.size)
