"""LoRA budynki v3 (z pelnych modeli: Krea 2 Raw, FLUX 3 Klein base) na lzejszych wersjach lokalnie (ComfyUI, RTX 3080):
Krea 2 Turbo int8 i FLUX 3 Klein destylat int8, 14 promptow testowych v3 (prompty_test_v3.py), seed 42+i, koncowa LoRA (krok 2000).
python v3_lzejsze.py [krea|flux3d]  -> E:/ai/wyniki/v3_lzejsze/<kod>_<i>.png"""
import os, shutil, sys
sys.path.insert(0, "E:/ai"); sys.path.insert(0, "E:/ai/lora")
import silnik
import prompty_test_v3 as PT
import zestawienie_wf_bazowe as B
import dogeneruj_zestawienie_v1_lekkie as LK
W = "E:/ai/runpod/wyniki/output"; LORY = "E:/ai/ComfyUI_windows_portable/ComfyUI/models/loras"; OUT = "E:/ai/wyniki/v3_lzejsze"; os.makedirs(OUT, exist_ok=True)
SRC = {"krea": "krea2raw", "flux3d": "flux3base"}
kody = sys.argv[1].split(",") if len(sys.argv) > 1 else ["krea", "flux3d"]
for kod in kody:
    src = f"{W}/swiat2d_{SRC[kod]}_budynki_v3_512/swiat2d_{SRC[kod]}_budynki_v3_512.safetensors"
    dst = f"swiat2d_v3_512_{SRC[kod]}_2000.safetensors"
    if not os.path.exists(f"{LORY}/{dst}"): shutil.copy(src, f"{LORY}/{dst}")
    for i, p in enumerate(PT.PROMPTY):
        png = f"{OUT}/{kod}_{i}.png"
        if os.path.exists(png): continue
        if kod == "krea":
            LK.P = {i: p}; w = LK.wf("zestawienie_krea2turbo_lora_raw512", i); w["lora"]["inputs"]["lora_name"] = dst
        else:
            B.RES = 512; m = list(B.MOD["zestawienie_flux3_destylat_lora_base512"]); m[4] = dst; w = B.wf(tuple(m), p, 42 + i)
        silnik.generuj(w, png); print(kod, i, PT.NAZWY[i], flush=True)
print("KONIEC")
