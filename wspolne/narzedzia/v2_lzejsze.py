"""LoRA v2-final na lzejszych wersjach modeli (ComfyUI, RTX 3080), prompty v2, seed 42+i - jak wiersze lzejsze w tabeli v1.
MOSS SFT (LoRA z Base), FLUX 3 destylat (z base), FLUX.2 Klein 4B destylat (z base), Krea 2 Turbo int8 (z Raw).
Pominiete: Qwen Q4 (lokalny GGUF to inny model niz 2512 - w v1 0 pkt, 195 s/obraz), wersje 1024 (v2 uczone tylko w 512).
Wynik: E:/ai/runpod/wyniki/output/gen_v2lekkie_<klucz>/samples/<czas>__000002000_<i>.jpg"""
import json, os, shutil, sys, time
from PIL import Image
sys.path.insert(0, "E:/ai"); sys.path.insert(0, "E:/ai/lora")
import silnik
import zestawienie_wf_bazowe as B
import dogeneruj_zestawienie_v1_lekkie as LK

P2 = json.load(open("E:/ai/lora/prompty_podglad_10_v2.json", encoding="utf-8")); LK.P = P2
LORY = "E:/ai/ComfyUI_windows_portable/ComfyUI/models/loras"; W = "E:/ai/runpod/wyniki/output"
for k in ("mossbase", "flux3base", "klein4b", "krea2raw"):
    src = f"{W}/swiat2d_{k}_budynki_v2final_512/swiat2d_{k}_budynki_v2final_512.safetensors"
    dst = f"{LORY}/swiat2d_v2f512_{k}_2000.safetensors"
    if not os.path.exists(dst): shutil.copy(src, dst)


def b(klucz, lora):
    def f(i):
        B.RES = 512; m = list(B.MOD[klucz]); m[4] = lora; return B.wf(tuple(m), P2[i], 42 + i)
    return f


def lk(klucz, lora):
    def f(i):
        w = LK.wf(klucz, i); w["lora"]["inputs"]["lora_name"] = lora; return w
    return f


WIERSZE = {"mosssft_512": b("zestawienie_moss_sft_lora_base512", "swiat2d_v2f512_mossbase_2000.safetensors"),
           "flux3destylat_512": b("zestawienie_flux3_destylat_lora_base512", "swiat2d_v2f512_flux3base_2000.safetensors"),
           "klein4bdestylat_512": lk("zestawienie_klein4b_destylat_lora_base512", "swiat2d_v2f512_klein4b_2000.safetensors"),
           "krea2turbo_512": lk("zestawienie_krea2turbo_lora_raw512", "swiat2d_v2f512_krea2raw_2000.safetensors")}
KOP = "E:/ai/wyniki/v2_lzejsze"; os.makedirs(KOP, exist_ok=True)
for k, f in WIERSZE.items():
    out = f"{W}/gen_v2lekkie_{k}/samples"; os.makedirs(out, exist_ok=True)
    for i in range(10):
        png = f"{KOP}/{k}_{i}.png"
        if not os.path.exists(png): silnik.generuj(f(i), png); print(k, i, flush=True)
        if not any(x.endswith(f"__000002000_{i}.jpg") for x in os.listdir(out)):
            Image.open(png).convert("RGB").save(f"{out}/{int(time.time() * 1000)}__000002000_{i}.jpg", quality=95)
print("KONIEC")
