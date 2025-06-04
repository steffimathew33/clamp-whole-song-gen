import torch
from unidecode import unidecode
from transformers import AutoTokenizer
from transformers import AutoConfig
from tqdm import tqdm
import os
import sys

# ======== USER CONFIGURATION ========
CLAMP_MODEL_NAME = "muzic/clamp/sander-wood/clamp-small-512"
TEXT_MODEL_NAME  = "distilroberta-base"
TEXT_LENGTH      = 128
UTILS_PATH = "muzic/clamp"
CONFIG_PATH = "muzic/clamp/sander-wood/clamp-small-512/config.json"
# ====================================

sys.path.append(os.path.abspath(UTILS_PATH))

from utils import *

# ----- device -----
if torch.cuda.is_available():
    device = torch.device("cuda")
    print(f"There are {torch.cuda.device_count()} GPU(s) available.")
    print("Using GPU:", torch.cuda.get_device_name(0))
else:
    device = torch.device("cpu")
    print("No GPU available, using CPU.")

# ----- model -----
config = AutoConfig.from_pretrained(CONFIG_PATH)
model = CLaMP(config)
state_dict = torch.load(CLAMP_MODEL_NAME + "/pytorch_model.bin")
model.load_state_dict(state_dict, strict=False)  # Allow unexpected keys
music_length = model.config.max_length
model = model.to(device).eval()

# ----- helpers -----
patchilizer = MusicPatchilizer()
tokenizer   = AutoTokenizer.from_pretrained(TEXT_MODEL_NAME)

def abc_filter(lines):
    music = ""
    for line in lines:
        if line[:2] in ['A:', 'B:', 'C:', 'D:', 'F:', 'G', 'H:', 'N:', 'O:', 'R:', 'r:', 'S:', 'T:', 'W:', 'w:', 'X:', 'Z:'] \
        or line == '\n' \
        or (line.startswith('%') and not line.startswith('%%score')):
            continue
        else:
            if "%" in line and not line.startswith('%%score'):
                line = "%".join(line.split('%')[:-1])
                music += line.rstrip() + '\n'
            else:
                music += line
    return music

def encoding_data(data, modal):
    ids_list = []
    if modal == "music":
        for item in data:
            patches = patchilizer.encode(item,
                                         music_length=music_length,
                                         add_eos_patch=True)
            ids_list.append(torch.tensor(patches).reshape(-1))
    else:
        for item in data:
            enc = tokenizer(item,
                            return_tensors="pt",
                            truncation=True,
                            max_length=TEXT_LENGTH)
            ids_list.append(enc["input_ids"].squeeze(0))
    return ids_list

def get_features(ids_list, modal):
    feats = []
    print(f"Extracting {modal} features...")
    with torch.no_grad():
        for ids in tqdm(ids_list):
            ids = ids.unsqueeze(0).to(device)
            if modal == "text":
                masks = torch.tensor([1] * len(ids[0])).unsqueeze(0).to(device)
                h = model.text_enc(ids, attention_mask=masks)["last_hidden_state"]
                h = model.avg_pooling(h, masks)
                h = model.text_proj(h)
            else:
                masks = torch.tensor([1] * (len(ids[0]) // PATCH_LENGTH)).unsqueeze(0).to(device)
                h = model.music_enc(ids, masks)["last_hidden_state"]
                h = model.avg_pooling(h, masks)
                h = model.music_proj(h)
            feats.append(h[0])
    return torch.stack(feats).to(device)

# ----- main -----

if __name__ == "__main__":
    ABC_ROOT_DIR = "matched_pop909_acc"

    for i in tqdm(range(1, 910)):  # Loop from 001 to 909
        folder_name = f"{i:03d}"
        folder_path = os.path.join(ABC_ROOT_DIR, folder_name)
        abc_path = os.path.join(folder_path, "aligned_demo_melody.abc")
        save_path = os.path.join(folder_path, "melody_embedding.pt")

        if not os.path.exists(abc_path):
            print(f"WARNING: {abc_path} not found, skipping.")
            continue

        # Load and filter ABC
        with open(abc_path, "r", encoding="utf-8") as f:
            music_raw = f.read()
        music = abc_filter(unidecode(music_raw).split("\n"))

        # Encode and embed
        ids = encoding_data([music], modal="music")
        embedding = get_features(ids, modal="music")[0]

        # Save .pt file in the same folder
        torch.save(embedding.cpu(), save_path)

    print("Done embedding all ABC files into their respective folders.")

