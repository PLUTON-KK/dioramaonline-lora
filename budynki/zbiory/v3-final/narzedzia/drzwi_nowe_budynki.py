"""Nowe obiekty test-v2 (4 modele): w obiektach wejsciowych (enterable) szuka kanonicznych drzwi (jak drzwi_krea.py, skala 0.5-4x),
sprawdza polozenie (srodek frontu) i dol na linii gruntu. Wynik: E:/ai/wyniki/nowe_budynki_drzwi.csv, nowe_budynki_drzwi_zoom.png (do recznej kontroli)."""
import csv, os, sys
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, "E:/ai/lora")
import nowe_budynki_krea_v2_test2 as T2
src = open("E:/ai/runpod/drzwi_krea.py", encoding="utf-8").read()
exec(src[:src.index("G = ")], ns := {})
znajdz, bbox_budynku = ns["znajdz"], ns["bbox_budynku"]
W = "E:/ai/wyniki/"
MODELE = [("krea", "Krea 2 Turbo int8", W + "nowe_budynki_krea_lora_v2-test-v2"), ("flux3d", "FLUX 3 Klein destylat", W + "nowe_budynki_flux3-klein-destylat_lora_v2-test-v2"),
          ("moss", "MOSS-Image SFT", W + "nowe_budynki_moss-image-sft_lora_v2-test-v2"), ("zimage", "Z-Image Turbo", W + "nowe_budynki_zimage-turbo_lora_v2-test-v2")]
WEJ = [i for i, e in enumerate(T2.L) if e[2] == "enterable"]
rows = []
for kod, nazwa, d in MODELE:
    for i in WEJ:
        for war in ("v2", "J", "K"):
            f = f"{d}/{war}_{i}.png"
            if not os.path.exists(f): continue
            im = Image.open(f).convert("RGB"); (sc, bb, skala), (bx0, by0, bx1, by1) = znajdz(im)
            cx = ((bb[0] + bb[2]) / 2 - bx0) / max(1, bx1 - bx0); dol = abs(bb[3] - by1) / max(1, by1 - by0)
            poz_ok = 0.25 <= cx <= 0.75; dol_ok = dol <= 0.12
            wer = "brak drzwi" if sc < 0.55 else "podmiana OK" if (poz_ok and dol_ok) else \
                  "do poprawy: " + ", ".join(x for x, ok in (("położenie", poz_ok), ("nie na ziemi", dol_ok)) if not ok)
            rows.append({"model": kod, "obiekt": T2.L[i][1], "i": i, "wariant": war, "pewnosc": round(sc, 2), "srodek_x": round(cx, 2), "dol": round(dol, 2),
                         "werdykt": wer, "plik": f, "bb": bb})
with open(W + "nowe_budynki_drzwi.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=[k for k in rows[0] if k != "bb"] + ["recznie"], extrasaction="ignore"); w.writeheader(); w.writerows(rows)
from collections import Counter
print(len(rows), Counter(r["werdykt"].split(":")[0] for r in rows))
for kod, *_ in MODELE: print(kod, Counter(r["werdykt"].split(":")[0] for r in rows if r["model"] == kod))
# powiekszenia okolic drzwi (wszystkie, z werdyktem) do recznej kontroli
S, cols = 200, 10; FS = ImageFont.truetype("arial.ttf", 12)
sh = Image.new("RGB", (cols * (S + 4), ((len(rows) + cols - 1) // cols) * (S + 30)), (40, 48, 36)); dr = ImageDraw.Draw(sh)
KOL = {"podmiana OK": (0, 255, 0), "brak drzwi": (255, 60, 60)}
for n, r in enumerate(rows):
    im = Image.open(r["plik"]).convert("RGB"); bb = r["bb"]; kol = KOL.get(r["werdykt"], (255, 200, 0))
    w_, h_ = bb[2] - bb[0], bb[3] - bb[1]; cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2; m = max(w_, h_) * 1.6
    v = im.copy(); ImageDraw.Draw(v).rectangle(bb, outline=kol, width=2)
    c = v.crop((int(cx - m), int(cy - m), int(cx + m), int(cy + m))).resize((S, S), Image.NEAREST)
    x, y = (n % cols) * (S + 4), (n // cols) * (S + 30); sh.paste(c, (x, y))
    dr.text((x + 2, y + S + 1), f"{n} {r['model']} {r['wariant']} {r['obiekt'][:16]}", font=FS, fill=(255, 230, 140)); dr.text((x + 2, y + S + 15), r["werdykt"][:28], font=FS, fill=kol)
sh.save(W + "nowe_budynki_drzwi_zoom.png"); print(sh.size)
