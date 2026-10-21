"""Porownania LoRA v1 -> repo: oceny wlasciciela (ranking_oceny_akt), ranking, najlepsze modele per budynek, CSV ocen.
Pisze README.md + oceny.csv w budynki/porownania/<folder>/ (obrazy kopiuje osobno)."""
import csv, glob, json, os

REPO = "E:/ai/dioramaonline-lora/budynki/porownania"
T = ["kwiaciarnia", "hotel", "stacja karetek", "budka z lodami", "dom turkusowy", "latarnia z domkiem", "szklarnia", "obserwatorium", "weterynarz", "kino"]
CZ = json.load(open("E:/ai/wyniki/zestawienie_comfy/czasy_3080.json", encoding="utf-8"))
ZA_DUZY = {"swiat2d_qwenimage2512_budynki_v1final_512", "swiat2d_qwenedit2511_budynki_v1final_512", "swiat2d_krea2raw_budynki_v1final_512"}
oceny = {}
for f in glob.glob("E:/ai/runpod/ranking_oceny_akt/ocena/*.json"):
    z, w, b = os.path.basename(f)[:-5].split("__"); oceny[(z, w, int(b))] = json.load(open(f, encoding="utf-8")).get("ocena")
PKT = {"dobre": 2, "srednie": 1, "slabe": 0}; PL = {"dobre": "dobre", "srednie": "średnie", "slabe": "słabe", None: "–"}


def wiersze_v1v1():
    src = open("E:/ai/runpod/zestawienie_v1.py", encoding="utf-8").read(); ns = {}; exec(src[:src.index("\nT = [")], ns)
    return [(os.path.basename(k), m, f"{lora}, {res} px", g) for m, lora, res, k, g in ns["WIERSZE"]]


def wiersze_v1v2():
    src = open("E:/ai/runpod/zestawienie_v1_prompty_v2.py", encoding="utf-8").read(); ns = {}; exec(src[:src.index("\nT = [")], ns)
    return [(k, m, f"{lora}, {res} px", s) for m, lora, res, k, s in ns["WIERSZE"]]


def czas(w):
    return "za duży" if w in ZA_DUZY else (f"{CZ[w]:.0f} s" if CZ.get(w, 0) >= 10 else f"{CZ[w]:.1f} s") if w in CZ else ""


def raport(zid, wiersze, folder, naglowek, z_czasem):
    rows = []
    for w, m, war, skad in wiersze:
        o = [oceny.get((zid, w, b)) for b in range(10)]
        rows.append({"w": w, "model": m, "war": war, "skad": skad, "o": o, "pkt": sum(PKT.get(x, 0) for x in o),
                     "d": o.count("dobre"), "m": o.count("srednie"), "s": o.count("slabe")})
    rows.sort(key=lambda r: (-r["pkt"], -r["d"], r["s"]))
    md = [naglowek, "", "## Ranking", "", "Oceny właściciela: każdy z 10 budynków testowych w każdym wierszu oznaczony jako dobre / średnie / słabe. Punkty: dobre 2, średnie 1, słabe 0 (maks. 20).", ""]
    md.append("| # | model | LoRA, rozdzielczość | trening LoRA / generowanie obrazu | punkty | dobre | średnie | słabe |" + (" RTX 3080 / obraz |" if z_czasem else ""))
    md.append("|---|---|---|---|---|---|---|---|" + ("---|" if z_czasem else ""))
    for i, r in enumerate(rows, 1):
        md.append(f"| {i} | {r['model']} | {r['war']} | {r['skad']} | **{r['pkt']}** | {r['d']} | {r['m']} | {r['s']} |" + (f" {czas(r['w'])} |" if z_czasem else ""))
    md += ["", "## Budynki: które modele narysowały je dobrze", "", "| budynek | dobre | średnie | słabe | oceniony jako „dobre” u |", "|---|---|---|---|---|"]
    for b, nb in enumerate(T):
        d = [r for r in rows if r["o"][b] == "dobre"]
        md.append(f"| {nb} | {len(d)} | {sum(r['o'][b] == 'srednie' for r in rows)} | {sum(r['o'][b] == 'slabe' for r in rows)} | "
                  + (", ".join(f"{r['model']} ({r['war'].split(', ')[-1]})" for r in d) or "–") + " |")
    with open(f"{REPO}/{folder}/oceny.csv", "w", newline="", encoding="utf-8-sig") as f:
        wr = csv.writer(f, delimiter=";"); wr.writerow(["model", "lora_rozdzielczosc", "skad_obraz"] + T + ["punkty"])
        for r in rows: wr.writerow([r["model"], r["war"], r["skad"]] + [PL[x] for x in r["o"]] + [r["pkt"]])
    return md, rows


# --- v1 na promptach v1
md, r1 = raport("v1v1", wiersze_v1v1(), "2026-10-21_lora-v1_prompty-v1",
    "# LoRA v1 na promptach v1 (2026-10-21)\n\n![zestawienie](zestawienie.png)\n\n"
    "- Wiersz: model bazowy + LoRA budynki v1 + rozdzielczość. Kolumna: budynek testowy ([prompty v1](../../testy/prompty_v1.json)). Opisy LoRA: [`../../modele/v1/`](../../modele/v1/).\n"
    "- Obrazy: podgląd z treningu (ai-toolkit, krok 2000, seed 42+i), a gdzie go nie było lub LoRA użyta na innej wersji modelu – ComfyUI na RTX 3080, ten sam prompt i seed.\n"
    "- Czas RTX 3080: jeden obraz po wczytaniu modelu. „Za duży”: model w pełnej precyzji nie mieści się w 10 GB VRAM + 32 GB RAM.\n"
    "- Prompty v1 mają dwa znane błędy: „a small side door” przy stacji karetek i zaprzeczenie przy budce z lodami (poprawione w v2).", True)
drz = list(csv.DictReader(open("E:/ai/runpod/wyniki/drzwi_v1.csv", encoding="utf-8-sig"), delimiter=";"))
ok = sum(r["werdykt"] == "podmiana OK" for r in drz); brak = sum(r["werdykt"] == "brak drzwi" for r in drz)
md += ["", "## Drzwi w budynkach wejściowych", "", "![drzwi](drzwi.png)", "",
       f"Automatyczne wyszukanie kanonicznych drzwi gry (std-external-2) w 7 budynkach wejściowych każdego wiersza ({len(drz)} obrazów): "
       f"{ok} – drzwi w miejscu z promptu i na linii gruntu (podmiana możliwa), {len(drz) - ok - brak} – inne położenie lub nad gruntem, {brak} – brak drzwi. "
       "Rozmiar nie blokuje podmiany: budynek skaluje się tak, żeby drzwi miały 58 px. Wyniki per obraz: [`drzwi.csv`](drzwi.csv). Wykrywanie automatyczne – może się mylić (np. trafić w okno).",
       "", "Pliki: [`oceny.csv`](oceny.csv) – ocena każdego obrazu.", "", "## Nowe seedy", "",
       "Słabsze budynki z 3 najlepszych wierszy wygenerowane ponownie z 5 nowymi seedami, z ocenami: [`nowe-seedy/`](nowe-seedy/).", "",
       "## Latarnia i realizm", "", "Testy promptów na Z-Image Turbo: latarnia (kamera dla okrągłych, „realistic shading”, „semi-realistic pixel art”) i szklarnia z płaskim szklanym dachem: [`latarnia-i-realizm/`](latarnia-i-realizm/)."]
open(f"{REPO}/2026-10-21_lora-v1_prompty-v1/README.md", "w", encoding="utf-8", newline="\n").write("\n".join(md) + "\n")

# --- v1 na promptach v2
md, r2 = raport("v1v2", wiersze_v1v2(), "2026-10-21_lora-v1_prompty-v2",
    "# LoRA v1 na promptach v2 (2026-10-21)\n\n![zestawienie](zestawienie.png)\n\n"
    "- Te same LoRA v1, seedy i ustawienia co w [porównaniu na promptach v1](../2026-10-21_lora-v1_prompty-v1/); zmieniony tylko tekst promptów ([prompty v2](../../testy/prompty_v2.json): rozmiar w metrach, drzwi stacji karetek na froncie, budka bez zaprzeczenia).\n"
    "- Obrazy: RunPod (ai-toolkit, bf16, LoRA wczytana, bez uczenia); FLUX 3 i FLUX.2 Klein w wersji destylowanej – ComfyUI na RTX 3080 (ai-toolkit ich nie wczytuje).\n"
    "- LoRA v1 nie widziała w opisach rozmiarów w metrach – to test samych promptów, nie zbioru v2.", False)
MAP = {"zimageturbo_512": "swiat2d_zimage_budynki_v1final_512", "zimageturbo_1024": "swiat2d_zimage_budynki_v1final_1024_bf16", "zimagebase_512": "swiat2d_zimagebase_budynki_v1final_512",
       "mossbase_512": "swiat2d_moss_base_budynki_v1final_512", "mosssft_512": "zestawienie_moss_sft_lora_base512", "mossbase_1024": "swiat2d_moss_budynki_v1final_1024_bf16",
       "mosssft_1024": "zestawienie_moss_sft_lora_base1024", "flux3base_512": "swiat2d_flux3_base_budynki_v1final_512", "flux3destylat_512": "zestawienie_flux3_destylat_lora_base512",
       "flux3base_1024": "swiat2d_flux3_budynki_v1final_1024_bf16", "flux3destylat_1024": "zestawienie_flux3_destylat_lora_base1024", "klein4bbase_512": "swiat2d_klein4b_budynki_v1final_512",
       "klein4bdestylat_512": "zestawienie_klein4b_destylat_lora_base512", "qwenimage2512_512": "swiat2d_qwenimage2512_budynki_v1final_512",
       "qwenedit2511_512": "swiat2d_qwenedit2511_budynki_v1final_512", "krea2raw_512": "swiat2d_krea2raw_budynki_v1final_512", "krea2turbo_512": "zestawienie_krea2turbo_lora_raw512"}
v1 = {r["w"]: r["pkt"] for r in r1}
md += ["", "## Zmiana względem promptów v1", "", f"Suma punktów 17 wspólnych wierszy: prompty v1 {sum(v1[MAP[r['w']]] for r in r2)}, prompty v2 {sum(r['pkt'] for r in r2)}.",
       "Porównanie wiersz do wiersza nie zawsze jest 1:1: część wierszy v1 generowana w ComfyUI (int8), w v2 na RunPod (bf16).", "",
       "| model | LoRA, rozdzielczość | prompty v1 | prompty v2 | zmiana |", "|---|---|---|---|---|"] + [f"| {r['model']} | {r['war']} | {v1[MAP[r['w']]]} | {r['pkt']} | {r['pkt'] - v1[MAP[r['w']]]:+d} |" for r in r2] + ["", "Pliki: [`oceny.csv`](oceny.csv)."]
open(f"{REPO}/2026-10-21_lora-v1_prompty-v2/README.md", "w", encoding="utf-8", newline="\n").write("\n".join(md) + "\n")
print("ok", len(r1), len(r2))
