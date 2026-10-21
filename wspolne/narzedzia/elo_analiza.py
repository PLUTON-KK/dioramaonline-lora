"""Analiza glosow z pojedynkow: liczba, Elo (jak strona), Bradley-Terry, zgodnosc z ocenami D/S/s, przedzialy (bootstrap)."""
import json, glob, random, collections, math
V = []
for f in glob.glob("E:/ai/runpod/elo_glosy/glosy/*.json"): V += json.load(open(f, encoding="utf-8"))["v"]
V.sort(key=lambda x: x[3])
D = "E:/ai/runpod/ranking_oceny_akt/ocena"; PKT = {"dobre": 2, "srednie": 1, "slabe": 0}
def ocena(k):
    rid, j = k.split("|"); z, w = rid.split("__", 1)
    try: return json.load(open(f"{D}/{z}__{w}__{j}.json", encoding="utf-8")).get("ocena")
    except Exception: return None
wyn = collections.Counter(v[2] for v in V); n = collections.Counter()
for a, b, *_ in V: n[a] += 1; n[b] += 1
print("glosow:", len(V), "| lewy/prawy/remis/oba slabe:", wyn[1], wyn[2], wyn[0], wyn[3])
print("obrazow z >=1 porownaniem:", len(n), "z 430; srednio porownan na obraz:", round(sum(n.values()) / 430, 2), "; rozklad:", sorted(collections.Counter(n.values()).items()))
print("strona lewa wygrywa:", round(wyn[1] / max(1, wyn[1] + wyn[2]) * 100), "%")
# zgodnosc z ocenami
zg = nz = rem = 0
for a, b, w, _ in V:
    oa, ob = ocena(a), ocena(b)
    if oa is None or ob is None or PKT[oa] == PKT[ob] or w in (0, 3): continue
    lep = a if PKT[oa] > PKT[ob] else b; wyg = a if w == 1 else b
    zg += lep == wyg; nz += lep != wyg
print(f"zgodnosc z Twoimi ocenami D/S/s (pary z rozna ocena, bez remisow): {zg}/{zg+nz} = {round(zg/max(1,zg+nz)*100)}%")
# remisy/oba slabe wg ocen
c = collections.Counter()
for a, b, w, _ in V:
    if w == 3: c[(ocena(a), ocena(b))] += 1
print("'oba slabe' a oceny:", dict(c.most_common(6)))
def elo(VV):
    e = collections.defaultdict(lambda: 1500.0)
    for a, b, w, *_ in VV:
        ea = 1 / (1 + 10 ** ((e[b] - e[a]) / 400)); sa = 1 if w == 1 else 0 if w == 2 else .5; e[a] += 32 * (sa - ea); e[b] -= 32 * (sa - ea)
    return e
def wiersze(e):
    r = collections.defaultdict(list)
    for k in n: r[k.split("|")[0]].append(e[k])
    return {k: sum(x) / len(x) for k, x in r.items()}
E = wiersze(elo(V))
# bootstrap: losowanie glosow ze zwracaniem + losowa kolejnosc
B = collections.defaultdict(list)
for _ in range(300):
    s = [random.choice(V) for _ in V]; random.shuffle(s)
    for k, x in wiersze(elo(s)).items(): B[k].append(x)
oc_w = collections.defaultdict(list)
for rid in E:
    z, w = rid.split("__", 1)
    for j in range(10):
        o = ocena(f"{rid}|{j}")
        if o: oc_w[rid].append(PKT[o])
print(f"\n{'wiersz':52} Elo   90% przedzial   por.  pkt z ocen")
for k, x in sorted(E.items(), key=lambda t: -t[1]):
    b = sorted(B[k]); lo, hi = b[int(.05 * len(b))], b[int(.95 * len(b)) - 1]
    print(f"{k:52} {x:5.0f}  {lo:5.0f}–{hi:5.0f}   {sum(n[i] for i in n if i.startswith(k+'|')):3}   {sum(oc_w[k])}")
