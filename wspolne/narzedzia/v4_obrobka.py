"""Obrobka sprite'ow v4 (q3ok 2026-10-22), bez AI:
- despill(): usuwa fioletowo-rozowe zabarwienie od magenty tla z pikseli przy krawedzi sylwetki (zachowuje jasnosc) -
  usuwa 'fioletowy kontur' po wycinaniu magenty w starych sprite'ach i nowych obrazach;
- mapuj(): mapowanie na palete 128 w przestrzeni Lab (roznica widziana okiem) + czyszczenie pojedynczych odstajacych pikseli
  (jednolite powierzchnie nie rozpadaja sie na plamy);
- fioletowa_obwodka(): kontrola do walidatora - udzial pikseli brzegu z zabarwieniem od magenty.
Paleta: wspolne/paleta128.json."""
import json, os
import numpy as np
from scipy import ndimage

PALETA = np.array(json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "paleta128.json"), encoding="utf-8"))["kolory"], dtype=np.int32)


def lab(rgb):
    c = np.asarray(rgb, float) / 255; c = np.where(c > 0.04045, ((c + 0.055) / 1.055) ** 2.4, c / 12.92)
    xyz = c @ np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]]).T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


def _spill(rgb):
    r, g, b = [rgb[..., k].astype(int) for k in range(3)]
    return np.clip(np.minimum(r, b) - g, 0, None), (np.abs(r - b) < 70)


def despill(rgb, al, szer=3):
    """Piksele w pasie `szer` px od krawedzi sylwetki z zabarwieniem od magenty (R i B wyraznie ponad G) -> neutralne o tej samej jasnosci,
    lekko zblizone do koloru wnetrza obok (zeby kontur nie byl martwo szary)."""
    al = al > 0; brzeg = al & ~ndimage.binary_erosion(al, iterations=szer)
    sp, podobne = _spill(rgb); zly = brzeg & podobne & (sp > 10)
    if not zly.any(): return rgb.copy()
    out = rgb.astype(float).copy(); Y = (0.299 * out[..., 0] + 0.587 * out[..., 1] + 0.114 * out[..., 2])
    wn = al & ~zly                                                    # najblizszy 'czysty' piksel wnetrza
    _, idx = ndimage.distance_transform_edt(~wn, return_indices=True); sasiad = out[idx[0], idx[1]]
    Ys = (0.299 * sasiad[..., 0] + 0.587 * sasiad[..., 1] + 0.114 * sasiad[..., 2])[..., None]
    nowy = Y[..., None] + 0.35 * (sasiad - Ys)                         # jasnosc oryginalu + odrobina barwy sasiada
    out[zly] = nowy[zly]
    return np.clip(np.round(out), 0, 255).astype(np.uint8)


def mapuj(rgb, al, paleta=PALETA, czysc=True):
    """Najblizszy kolor palety w Lab; potem pojedyncze piksele rozne od >= 3 z 4 sasiadow (ktorzy sa zgodni) -> kolor sasiadow."""
    Lp = lab(paleta); L = lab(rgb.reshape(-1, 3))
    idx = np.empty(len(L), int)
    for i in range(0, len(L), 20000):
        d = ((L[i:i + 20000, None, :] - Lp[None]) ** 2).sum(-1); idx[i:i + 20000] = d.argmin(1)
    idx = idx.reshape(rgb.shape[:2]); m = al > 0
    if czysc:
        for _ in range(2):
            p = np.pad(idx, 1, mode="edge"); pm = np.pad(m, 1)
            sas = np.stack([p[:-2, 1:-1], p[2:, 1:-1], p[1:-1, :-2], p[1:-1, 2:]]); sm = np.stack([pm[:-2, 1:-1], pm[2:, 1:-1], pm[1:-1, :-2], pm[1:-1, 2:]])
            nowe = idx.copy()
            for k in range(4):
                zg = ((sas == sas[k]) & sm).sum(0)
                pop = m & sm[k] & (zg >= 3) & (sas[k] != idx) & ((sas == idx[None]) & sm).sum(0).__eq__(0)
                nowe[pop] = sas[k][pop]
            idx = nowe
    out = paleta[idx].astype(np.uint8); out[~m] = 0
    return out


def fioletowa_obwodka(rgb, al, szer=2):
    """Udzial pikseli pasa brzegowego z zabarwieniem od magenty (0-1). Walidator: > 0.05 = FAIL."""
    al = al > 0; brzeg = al & ~ndimage.binary_erosion(al, iterations=szer)
    sp, podobne = _spill(rgb); return float((brzeg & podobne & (sp > 10)).sum() / max(1, brzeg.sum()))
