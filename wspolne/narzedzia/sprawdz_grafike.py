"""Walidator grafik Swiata 2D - lokalnie, bez AI (numpy + OpenCV). Kryteria wspolne ze strona gry (059-kryteria, ID P/K/D/B),
przy rozbieznosci pierwszenstwo maja zasady dioramaonline-lora (decyzja wlasciciela 2026-10-22).
Wynik kazdej kontroli: PASS / FAIL / SKIP (SKIP = nie da sie zmierzyc pewnie -> ocena wlasciciela, nigdy PASS).
Tolerancja pomiaru: max(2 px, 5% wartosci oczekiwanej).

Uzycie w kodzie:  wynik = sprawdz(closed_png, open_png=None, meta=None, typ="wejsciowy"|"dekoracyjny", zrodlo=None)
  closed_png / open_png - sprite w formacie gry (RGBA, 24 px = 1 m); meta - slownik metadanych dla gry (doors[], anchor, metric...);
  zrodlo - obraz przed kadrowaniem (np. wynik generatora 512 na magencie) do P2.
Heurystyki geometrii (K2-K4, P6) dzialaja na typowych bryłach z prostokatnym wierzchem; przy nietypowych zwracaja SKIP."""
import json, os
import numpy as np, cv2
from scipy import ndimage

PALETA_PLIK = r"E:\ai\skrzynka\odpowiedzi\world_palette.json"
PAL = np.array(json.load(open(PALETA_PLIK, encoding="utf-8-sig")), np.int32) if os.path.exists(PALETA_PLIK) else None
WYS_DRZWI, MODUL = 58, {"std-external-2": (59, 58, 51, 55)}   # modul: szer, wys, otwor szer, otwor wys


def tol(v): return max(2, 0.05 * v)


def wczytaj(p):
    from PIL import Image
    return np.array(Image.open(p).convert("RGBA")).astype(np.int32)


def z_magenty(p):
    """obraz generatora na tle magenta -> RGBA (tlo przezroczyste)"""
    from PIL import Image
    a = np.array(Image.open(p).convert("RGB")).astype(np.int32); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    tlo = (r > 150) & (b > 120) & (g < 120) & (r - g > 70) & (b - g > 50)
    al = np.where(ndimage.binary_opening(~tlo, iterations=1), 255, 0)
    return np.dstack([a, al])


# ---------- P: plik i piksele ----------
def p1(a):
    u = set(np.unique(a[..., 3]).tolist())
    return ("PASS", "") if u <= {0, 255} else ("FAIL", f"wartosci alfa poza 0/255: {len(u - {0, 255})}")


def p2(zrodlo):
    if zrodlo is None: return ("SKIP", "brak obrazu przed kadrowaniem")
    al = zrodlo[..., 3] > 0
    if al[0].any() or al[-1].any() or al[:, 0].any() or al[:, -1].any(): return ("FAIL", "obiekt dotyka krawedzi obrazu zrodlowego")
    return ("PASS", "")


def p3(a, otwor=None):
    tr = a[..., 3] == 0; pad = np.pad(tr, 1, constant_values=True)
    lab, n = ndimage.label(pad); zew = lab[0, 0]
    dziury = (lab > 0) & (lab != zew); dziury = dziury[1:-1, 1:-1]
    if otwor is not None:
        x, y, w, h = otwor; dziury[y:y + h, x:x + w] = False
    lab2, n2 = ndimage.label(dziury); roz = ndimage.sum(dziury, lab2, range(1, n2 + 1)) if n2 else []
    duze = [int(s) for s in roz if s >= 3]
    return ("PASS", "") if not duze else ("FAIL", f"{len(duze)} dziur w sylwetce (najwieksza {max(duze)} px)")


def p4(a):
    vis = a[..., 3] > 0; r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mag = vis & (r > 150) & (b > 150) & (g < 110) & (r - g > 80)
    rgb_tla = int(((a[..., 3] == 0) & (a[..., :3].sum(-1) > 0)).sum())
    if mag.sum() > 0: return ("FAIL", f"{int(mag.sum())} widocznych pikseli magenty (obwodka)")
    if rgb_tla: return ("FAIL", f"przezroczyste piksele z RGB != 0: {rgb_tla} (do wyzerowania przy zapisie)")
    return ("PASS", "")


def p5(a):
    if PAL is None: return ("SKIP", "brak palety")
    vis = a[..., 3] > 0; kol = np.unique(a[..., :3][vis], axis=0)
    obce = [c for c in kol if not (np.abs(PAL - c).sum(1) == 0).any()]
    return ("PASS", "") if not obce else ("FAIL", f"{len(obce)} kolorow spoza palety swiata")


def szerokosci(al):
    """dla kazdego wiersza: (lewo, prawo) skrajnych nieprzezroczystych pikseli albo None"""
    out = []
    for row in al:
        xs = np.where(row)[0]; out.append((xs[0], xs[-1]) if len(xs) else None)
    return out


def p6(a):
    """heurystyka podloza: dolny pas szerszy niz bryla i w szarym/bezowym (plyta, peron, kostka)"""
    al = a[..., 3] > 0; h, w = al.shape; s = szerokosci(al)
    srodek = [r[1] - r[0] for r in s[int(h * .45):int(h * .75)] if r]
    if not srodek: return ("SKIP", "brak bryly")
    ref = np.median(srodek); dol = [r for r in s[int(h * .93):] if r]
    if not dol: return ("SKIP", "")
    sz = max(r[1] - r[0] for r in dol)
    pas = a[int(h * .93):][al[int(h * .93):]][:, :3]
    nasyc = (pas.max(1) - pas.min(1)).mean() if len(pas) else 99
    if sz > ref * 1.10 and nasyc < 40: return ("SKIP", f"PODEJRZENIE podloza: dolny pas szerszy o {round((sz / ref - 1) * 100)}% i szary - ocen")
    return ("PASS", "")


# ---------- K: kamera i geometria ----------
def okap(a):
    """linia okapu: NAJWYZSZA silna pozioma krawedz (>= 50% najsilniejszej) w 10-75% wysokosci, rozciagnieta na >= 55% szerokosci bryly.
    Szukanie od gory: dolna krawedz dachu jest pierwsza dluga krawedz pod wierzchem (nizej sa markizy i okna)."""
    al = a[..., 3] > 0; h, w = al.shape
    g = cv2.cvtColor(a[..., :3].astype(np.uint8), cv2.COLOR_RGB2GRAY).astype(np.float32)
    dy = np.abs(np.diff(g, axis=0)); dy[~(al[1:] & al[:-1])] = 0
    ys = np.where(al.any(1))[0]; top = ys[0]
    sila = {}
    for y in range(max(int(h * .10), top + 4), int(h * .75)):
        cover = (dy[y] > 25).mean() / max(al[y].mean(), 1e-6)
        if al[y].mean() > 0.3 and cover > 0.55: sila[y] = dy[y].mean()
    if not sila: return None
    mx = max(sila.values())
    return min(y for y, v in sila.items() if v >= 0.5 * mx)


def k2(a):
    al = a[..., 3] > 0; h = al.shape[0]
    if al.sum() / al.size < 0.55: return ("SKIP", "bryla nieprostokatna"), None
    ys = np.where(al.any(1))[0]; top = ys[0]; y = okap(a)
    if y is None: return ("SKIP", "nie rozpoznano okapu"), None
    dach, front = y - top, h - y
    if dach >= front: return ("FAIL", f"dach {dach} px >= front {front} px"), y
    return ("PASS", f"dach {dach} px / front {front} px"), y


def k3(a, y_okap):
    """zbieganie dachu: gorna krawedz wierzchu (pierwszy wiersz o szer. >= 50% okapu - pomija anteny i nadbudowki) vs okap"""
    if y_okap is None: return ("SKIP", "nie rozpoznano dachu")
    al = a[..., 3] > 0; s = szerokosci(al); ys = np.where(al.any(1))[0]; top = ys[0]
    if y_okap - top < 6: return ("SKIP", "dach za niski do pomiaru")
    dol = [r for r in s[y_okap - 3: y_okap] if r]
    if not dol: return ("SKIP", "")
    ld, pd = np.median([r[0] for r in dol]), np.median([r[1] for r in dol]); sd = pd - ld
    wiersze = [(y, r) for y, r in enumerate(s[top:y_okap], top) if r and r[1] - r[0] >= 0.5 * sd]
    if not wiersze: return ("SKIP", "wierzch niejednolity")
    y0 = wiersze[0][0]; gora = [r for r in s[y0: y0 + 3] if r]
    lg, pg = np.median([r[0] for r in gora]), np.median([r[1] for r in gora]); sg = pg - lg; t = tol(sd)
    if sg < 0.8 * sd: return ("SKIP", f"wierzch {int(sg)} px przy okapie {int(sd)} px - raczej nadbudowka lub dwie bryly, ocen")
    if sd - sg > t: return ("FAIL", f"dach zweza sie do tylu: gora {int(sg)} px, okap {int(sd)} px")
    if abs(lg - ld) > t or abs(pg - pd) > t: return ("FAIL", f"boki dachu nie sa pionowe (przesuniecie {int(max(abs(lg - ld), abs(pg - pd)))} px)")
    return ("PASS", f"gora {int(sg)} px, okap {int(sd)} px")


def k4(a):
    """izometria/obrot: udzial skosnych (15-75 st.) odcinkow w obrysie sylwetki i w dlugich krawedziach wnetrza.
    Obraz zmniejszany do ok. 160 px, zeby schodki pikseli zlaly sie w linie."""
    al = (a[..., 3] > 0).astype(np.float32); h, w = al.shape; k = 160 / max(h, w)
    sz = (max(8, int(w * k)), max(8, int(h * k)))
    m = (cv2.resize(al, sz, interpolation=cv2.INTER_AREA) > 0.5).astype(np.uint8)
    g = cv2.resize(cv2.cvtColor(a[..., :3].astype(np.uint8), cv2.COLOR_RGB2GRAY), sz, interpolation=cv2.INTER_AREA); g[m == 0] = 0
    sk = cal = 0.0
    def dodaj(x1, y1, x2, y2):
        nonlocal sk, cal
        d = np.hypot(x2 - x1, y2 - y1); ang = abs(np.degrees(np.arctan2(y2 - y1, x2 - x1))) % 180; ang = min(ang, 180 - ang)
        cal += d; sk += d if 15 <= ang <= 75 else 0
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in cs:
        if cv2.contourArea(c) < 30: continue
        ap = cv2.approxPolyDP(c, 0.012 * cv2.arcLength(c, True), True)[:, 0]
        for i in range(len(ap)): dodaj(*ap[i], *ap[(i + 1) % len(ap)])
    L = cv2.HoughLinesP(cv2.Canny(g, 40, 120), 1, np.pi / 180, threshold=18, minLineLength=22, maxLineGap=4)
    if L is not None:
        for x1, y1, x2, y2 in L[:, 0]: dodaj(x1, y1, x2, y2)
    if not cal: return ("SKIP", "brak krawedzi")
    u = sk / cal
    if u > 0.25: return ("FAIL", f"skosy {round(u * 100)}% krawedzi (izometria/obrot)")
    if u < 0.12: return ("PASS", f"skosy {round(u * 100)}%")
    return ("SKIP", f"skosy {round(u * 100)}% - niejednoznaczne")


def k1(a, meta, typ):
    if typ == "wejsciowy" and meta and meta.get("doors"):
        p = meta["doors"][0]["placement"]; mw, mh = MODUL.get(meta["doors"][0]["module"], (59, 58, 0, 0))[:2]
        return ("PASS", "drzwi = modul 58 px") if mh == WYS_DRZWI else ("FAIL", f"wys. modulu {mh} px")
    if meta and meta.get("metric", {}).get("width_m"):
        ocz = meta["metric"]["width_m"] * 24; w = a.shape[1]
        return ("PASS", f"{w} px ~ {round(ocz)} px") if abs(w - ocz) <= tol(ocz) else ("FAIL", f"szer. {w} px, z metryki {round(ocz)} px")
    return ("SKIP", "brak punktu odniesienia skali")


# ---------- D / B: drzwi i typ ----------
def drzwi(c, o, meta, typ):
    w = {}
    if typ != "wejsciowy":
        ok = (o is None) and not (meta or {}).get("doors")
        w["B1"] = ("PASS", "") if ok else ("FAIL", "dekoracyjny ma wariant open albo doors[]")
        return w
    if not meta or not meta.get("doors"): return {k: ("FAIL", "brak doors[] w metadanych") for k in ("D1", "D2", "D3", "D4", "D5", "D6", "D7")}
    if o is None: w["D1"] = ("FAIL", "brak wariantu open")
    else: w["D1"] = ("PASS", "") if c.shape == o.shape else ("FAIL", f"rozne rozmiary closed {c.shape[1]}x{c.shape[0]} / open {o.shape[1]}x{o.shape[0]}")
    regs = []
    for d in meta["doors"]:
        cr, dw = d["changedRegion"], d["doorway"]; regs.append(cr)
        if o is not None and c.shape == o.shape:
            m = np.ones(c.shape[:2], bool); m[cr["y"]:cr["y"] + cr["h"], cr["x"]:cr["x"] + cr["w"]] = False
            w["D2"] = ("PASS", "") if (c[m] == o[m]).all() else ("FAIL", f"{int((c[m] != o[m]).any(-1).sum())} pikseli rozni sie poza changedRegion")
            ow = o[dw["y"]:dw["y"] + dw["h"], dw["x"]:dw["x"] + dw["w"], 3]; orr = o[cr["y"]:cr["y"] + cr["h"], cr["x"]:cr["x"] + cr["w"], 3]
            w["D4"] = ("PASS", "") if (ow == 0).any() and (orr == 255).any() else ("FAIL", "open bez otworu albo bez ramy")
            cc = c[cr["y"]:cr["y"] + cr["h"], cr["x"]:cr["x"] + cr["w"], 3]
            w["D5"] = ("PASS", "") if not ((cc == 0) & (orr > 0)).any() else ("FAIL", "w open pojawiaja sie piksele niewidoczne w closed")
        else:
            for k in ("D2", "D4", "D5"): w.setdefault(k, ("SKIP", "brak poprawnej pary closed/open"))
        cw = c[dw["y"]:dw["y"] + dw["h"], dw["x"]:dw["x"] + dw["w"], 3]
        w["D3"] = ("PASS", "") if cw.size and (cw == 255).all() else ("FAIL", "otwor w closed nie jest pelny")
        dol = d["placement"]["y"] + MODUL.get(d["module"], (59, 58))[1]; h = c.shape[0]
        w["D6"] = ("PASS", "") if 0 <= h - dol <= max(tol(h), 0.12 * h) else ("FAIL", f"dol drzwi {h - dol} px nad podstawa")
        md = MODUL.get(d["module"])
        w["D7"] = ("PASS", "") if md and dw["w"] == md[2] else ("FAIL", f"modul {d['module']}, otwor {dw['w']} px")
    if len(regs) > 1:
        nak = any(not (a["x"] + a["w"] <= b["x"] or b["x"] + b["w"] <= a["x"] or a["y"] + a["h"] <= b["y"] or b["y"] + b["h"] <= a["y"]) for i, a in enumerate(regs) for b in regs[i + 1:])
        w["D9"] = ("FAIL", "nakladajace sie changedRegion") if nak else ("PASS", "")
    w["D8"] = ("SKIP", "brak roofParts w metadanych") if not (meta or {}).get("roofParts") else ("SKIP", "D8 do zrobienia")
    return w


def metadane(meta, typ):
    if not meta: return ("FAIL", "brak metadanych")
    brak = [k for k in ("image", "anchor", "metric") if k not in meta]
    brak += [f"metric.{k}" for k in ("width_m", "depth_m", "height_m") if k not in meta.get("metric", {})]
    if "roofParts" not in meta: brak.append("roofParts")
    if typ == "wejsciowy" and not meta.get("doors"): brak.append("doors[]")
    return ("PASS", "") if not brak else ("FAIL", "brak: " + ", ".join(brak))


def sprawdz(closed_png, open_png=None, meta=None, typ="wejsciowy", zrodlo=None):
    c = wczytaj(closed_png) if isinstance(closed_png, str) else closed_png
    o = wczytaj(open_png) if isinstance(open_png, str) and os.path.exists(open_png) else None
    z = z_magenty(zrodlo) if isinstance(zrodlo, str) and os.path.exists(zrodlo) else None
    otw = None
    if meta and meta.get("doors"): d = meta["doors"][0]["doorway"]; otw = (d["x"], d["y"], d["w"], d["h"])
    w = {"P1": p1(c), "P2": p2(z), "P3": p3(c), "P4": p4(c), "P5": p5(c), "P6": p6(c)}
    w["K1"] = k1(c, meta, typ); w["K2"], yo = k2(c); w["K3"] = k3(c, yo); w["K4"] = k4(c)
    if w["K4"][0] == "FAIL" and w["K2"][0] == "SKIP":   # bryla bez rozpoznanego prostokatnego wierzchu: skosy moga byc konstrukcyjne (lopaty, kopuly, namioty)
        w["K4"] = ("SKIP", w["K4"][1] + " - bryla nietypowa, skosy moga byc konstrukcyjne")
    w.update(drzwi(c, o, meta, typ)); w["M"] = metadane(meta, typ)
    return w
