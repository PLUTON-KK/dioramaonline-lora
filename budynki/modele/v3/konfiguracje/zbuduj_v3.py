"""Pakiety RunPod: LoRA budynki v3-final, 512, bf16 bez kwantyzacji (jeden pakiet = jedna maszyna). Zbior: E:/ai/lora/lora-budynki-v3/train_512 (88).
Podglady co 250 krokow: 14 promptow testowych v3 (E:/ai/lora/prompty_test_v3.py: 7 obiektow zwykle + uzdatnione K), seed 42+i.
Karty: najmniejsze, na ktorych model + koder tekstu miesci sie w VRAM bez zrzucania do RAM (low_vram False), z zapasem na 48 GB."""
import json, os, shutil, sys
import yaml
sys.path.insert(0, "E:/ai/lora")
import prompty_test_v3 as PT
R = "E:/ai/runpod"; SRC = "E:/ai/lora/lora-budynki-v3"
ZT = {"extras_name_or_path": "Tongyi-MAI/Z-Image-Turbo", "assistant_lora_path": "ostris/zimage_turbo_training_adapter/zimage_turbo_training_adapter_v2.safetensors"}
G24 = "NVIDIA RTX A5000,NVIDIA GeForce RTX 4090,SECURE:NVIDIA RTX A5000,NVIDIA RTX A6000,NVIDIA A40"          # 24 GB, awaryjnie 48 GB
G48 = "NVIDIA RTX A6000,NVIDIA A40,SECURE:NVIDIA RTX A6000,SECURE:NVIDIA A40,NVIDIA L40,NVIDIA RTX 6000 Ada Generation"
M = {  # kod: (repo, arch, kroki treningu, kroki podgladu, guidance, dodatki, karty)
    "zimageturbo": ("Tongyi-MAI/Z-Image-Turbo", "zimage", 3000, 8, 1, ZT, G24),            # 6B (12 GB) + Qwen3-4B
    "flux3base": ("black-forest-labs/flux-3-image-klein-base", "flux3", 2000, 50, 3.5, {}, G24),   # ~5,8B (12 GB) + Qwen3-VL-4B
    "mossbase": ("OpenMOSS-Team/MOSS-Image-Base", "moss_image", 2000, 30, 4, {}, G48),   # ~5,4B + koder Qwen3.5-9B (18 GB) -> 48
    "krea2raw": ("krea/Krea-2-Raw", "krea2", 2000, 30, 3.5, {}, G48),                     # ~13,5B (27 GB) -> 48
}
plan = []
for kod, (repo, arch, kroki, ks, gs, extra, gpus) in M.items():
    D = f"{R}/pakiet_v3_{kod}"; shutil.rmtree(D, ignore_errors=True); os.makedirs(f"{D}/dataset/img")
    for f in os.listdir(f"{SRC}/train_512"): shutil.copy(f"{SRC}/train_512/{f}", f"{D}/dataset/img/{f}")
    ds = {"folder_path": "/workspace/pakiet/dataset/img", "caption_ext": "txt", "caption_dropout_rate": 0.0, "shuffle_tokens": False, "cache_latents_to_disk": True, "resolution": [512]}
    sample = {"sampler": "flowmatch", "sample_every": 250, "width": 512, "height": 512, "neg": "", "seed": 42, "walk_seed": True, "guidance_scale": gs, "sample_steps": ks, "prompts": PT.PROMPTY}
    name = f"swiat2d_{kod}_budynki_v3_512"
    cfg = {"job": "extension", "config": {"name": name, "process": [{
        "type": "sd_trainer", "training_folder": "/workspace/output", "device": "cuda:0", "trigger_word": "swiat2d style",
        "network": {"type": "lora", "linear": 16, "linear_alpha": 16},
        "save": {"dtype": "float16", "save_every": 250, "max_step_saves_to_keep": 14, "push_to_hub": False},
        "datasets": [ds],
        "train": {"batch_size": 1, "steps": kroki, "gradient_accumulation_steps": 1, "train_unet": True, "train_text_encoder": False, "gradient_checkpointing": True,
                  "noise_scheduler": "flowmatch", "optimizer": "adamw8bit", "lr": 1e-4, "dtype": "bf16", "skip_first_sample": False, "cache_text_embeddings": True},
        "model": dict({"name_or_path": repo, "arch": arch, "quantize": False, "quantize_te": False, "low_vram": False}, **extra),
        "sample": sample}]}}
    with open(f"{D}/{name}.yaml", "w", encoding="utf-8") as f:
        f.write(f"# RunPod, budynki v3-final (88), 512, bf16 bez kwantyzacji, {kroki} krokow. Krok 0 = bez LoRA. Podglady co 250: 14 promptow testowych v3, seed 42+i.\n")
        yaml.safe_dump(cfg, f, allow_unicode=True, sort_keys=False, width=10000)
    shutil.copy(f"{R}/pakiet_v2_zimageturbo/na_podzie.sh", f"{D}/na_podzie.sh")
    plan.append((kod, gpus))
json.dump(plan, open(f"{R}/plan_v3.json", "w"), indent=1)
for k, g in plan: print(k, "->", g.split(",")[0], "| obrazow:", len(os.listdir(f"{R}/pakiet_v3_{k}/dataset/img")) // 2)
