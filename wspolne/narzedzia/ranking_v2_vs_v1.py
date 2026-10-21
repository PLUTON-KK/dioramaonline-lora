"""Ranking LoRA v2-final / prompty v2 vs LoRA v1 / prompty v2 (te same prompty, seed 42+i). Oceny z ranking_oceny_akt."""
import json, os
D = "E:/ai/runpod/ranking_oceny_akt/ocena"; PKT = {"dobre": 2, "srednie": 1, "slabe": 0}
T = ["kwiaciarnia", "hotel", "stacja karetek", "budka z lodami", "dom turkusowy", "latarnia", "szklarnia", "obserwatorium", "weterynarz", "kino"]
PARY = [("Z-Image Turbo 512", "v2_zimageturbo", "zimageturbo_512"), ("Z-Image Base 512", "v2_zimagebase", "zimagebase_512"),
        ("MOSS Base 512", "v2_mossbase", "mossbase_512"), ("MOSS SFT 512", "v2l_mosssft_512", "mosssft_512"),
        ("FLUX 3 Klein base 512", "v2_flux3base", "flux3base_512"), ("FLUX 3 destylat 512", "v2l_flux3destylat_512", "flux3destylat_512"),
        ("Klein 4B base 512", "v2_klein4b", "klein4bbase_512"), ("Klein 4B destylat 512", "v2l_klein4bdestylat_512", "klein4bdestylat_512"),
        ("Qwen-Image 2512", "v2_qwenimage2512", "qwenimage2512_512"), ("Krea 2 Raw 512", "v2_krea2raw", "krea2raw_512"),
        ("Krea 2 Turbo 512", "v2l_krea2turbo_512", "krea2turbo_512")]
def oc(z, w, i):
    f = f"{D}/{z}__{w}__{i}.json"
    return json.load(open(f, encoding="utf-8")).get("ocena") if os.path.exists(f) else None
L = {"dobre": "D", "srednie": "S", "slabe": "s", None: "."}
s1 = s2 = 0; bud = [[0, 0] for _ in T]
print(f"{'model':24} v1  v2  zm   v1 kafle     v2 kafle   nieocen.v2")
for n, a, b in PARY:
    o2 = [oc("v2v2", a, i) for i in range(10)]; o1 = [oc("v1v2", b, i) for i in range(10)]
    p2 = sum(PKT.get(x, 0) for x in o2); p1 = sum(PKT.get(x, 0) for x in o1); s1 += p1; s2 += p2
    for i in range(10): bud[i][0] += PKT.get(o1[i], 0); bud[i][1] += PKT.get(o2[i], 0)
    print(f"{n:24} {p1:2}  {p2:2}  {p2-p1:+3}   {''.join(L[x] for x in o1)}   {''.join(L[x] for x in o2)}   {o2.count(None)}")
print(f"{'SUMA':24} {s1}  {s2}  {s2-s1:+}")
print("\nbudynek            v1  v2")
for t, (x, y) in zip(T, bud): print(f"{t:18} {x:2}  {y:2}  {y-x:+}")
