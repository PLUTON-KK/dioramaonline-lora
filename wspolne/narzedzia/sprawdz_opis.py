"""Walidator opisow i promptow wg wspolne/schemat_opisow.json (obowiazuje od v4).
python sprawdz_opis.py <plik .txt | katalog z .txt | "tekst opisu">  -> lista bledow, kod wyjscia 1 gdy sa bledy.
W skryptach: from sprawdz_opis import sprawdz; bledy = sprawdz(opis)"""
import json, os, re, sys
S = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "schemat_opisow.json"), encoding="utf-8"))
OKR = S["dopisek_okragle"]
ROZM = {k: re.compile("^" + re.escape(v).replace(r"\{w\}", r"[\d.]+").replace(r"\{h\}", r"[\d.]+").replace(r"\{d\}", r"[\d.]+") + "$") for k, v in S["rozmiar"].items()}
ZAKAZ = re.compile(r"\b(" + "|".join(re.escape(z) for z in S["zakazane_slowa"]) + r")\b", re.I)
SPICZ = re.compile(r"\b(pointed|dome|domed|conical|tent|pyramid|gable|spire|half-round)\b", re.I)


def koncowki(kat, uzd=False):
    out = {}
    for k in S["kategorie"][kat]["koncowki"]:
        e = S["koncowki"][k]; warianty = [e]
        if k in ("front", "front_plaski"): warianty.append(e.replace(", isolated on", f", {OKR}, isolated on"))
        for w in warianty:
            out[w] = k
            out[w.replace(*S["styl_uzdatniony"]["zamiana"])] = k
    return out


def sprawdz(t):
    t = t.strip(); b = []
    if not t.startswith("swiat2d style, "): return ["brak poczatku 'swiat2d style, '"]
    czesci = t[len("swiat2d style, "):].split(", ", 3)
    if len(czesci) < 4: return ["za malo czesci: kategoria, podtyp, rozmiar, opis"]
    kat, pod, rozm, reszta = czesci
    if kat not in S["kategorie"]: return [f"nieznana kategoria '{kat}' (dozwolone: {', '.join(S['kategorie'])})"]
    K = S["kategorie"][kat]
    if pod not in K["podtypy"]: b.append(f"nieznany podtyp '{pod}' dla '{kat}' (dozwolone: {', '.join(K['podtypy'])})")
    if not ROZM[K["rozmiar"]].match(rozm): b.append(f"rozmiar '{rozm}' niezgodny ze wzorem '{S['rozmiar'][K['rozmiar']]}'")
    kon = next((k for k in sorted(koncowki(kat), key=len, reverse=True) if t.endswith(" " + k)), None)
    if not kon: b.append(f"koncowka spoza listy dla '{kat}' (dozwolone: {', '.join(K['koncowki'])})"); opis = reszta
    else: opis = reszta[: -len(kon)].rstrip()
    if ZAKAZ.search(t): b.append(f"zakazane slowo: '{ZAKAZ.search(t).group(0)}'")
    if kon and "flat rectangular roof" in kon and SPICZ.search(opis) and not re.search(r"rising above|tower part|bell tower", opis):
        b.append(f"plaski dach w koncowce, a w opisie '{SPICZ.search(opis).group(0)}' - uzyj koncowki 'front'")
    if kat == "building" and pod == "enterable" and not any(d in opis for d in S["drzwi_wejsciowe"]): b.append("budynek wejsciowy bez standardowego opisu drzwi")
    if kat != "building" and "front facade" in t: b.append("'front facade' tylko dla building")
    if "realistic materials and proportions" in opis and kon and not kon.startswith("Semi-realistic"): b.append("materialy (K) bez stylu 'Semi-realistic'")
    return b


if __name__ == "__main__":
    a = sys.argv[1]; pliki = []
    if os.path.isdir(a): pliki = [os.path.join(a, f) for f in sorted(os.listdir(a)) if f.endswith(".txt")]
    elif os.path.isfile(a): pliki = [a]
    zle = 0
    for nazwa, t in ([(p, open(p, encoding="utf-8").read()) for p in pliki] if pliki else [("tekst", a)]):
        b = sprawdz(t)
        if b: zle += 1; print(nazwa, "->", "; ".join(b))
    print("bledne:", zle); sys.exit(1 if zle else 0)
