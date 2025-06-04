import torch
from transformers import AutoTokenizer, AutoConfig
import os
import sys
from tqdm import tqdm

# ======== USER CONFIGURATION ========
ROOT_DIR = "pop909_w_structure_label"  # Directory containing 001-909 folders
CLAMP_MODEL_NAME = "muzic/clamp/sander-wood/clamp-small-512"
TEXT_MODEL_NAME  = "distilroberta-base"
TEXT_LENGTH      = 128
UTILS_PATH = "muzic/clamp"
CONFIG_PATH = os.path.join(CLAMP_MODEL_NAME, "config.json")
# ====================================

sys.path.append(os.path.abspath(UTILS_PATH))
from utils import *  # Imports CLaMP and PATCH_LENGTH

# ----- Device -----
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# ----- Load Model -----
config = AutoConfig.from_pretrained(CONFIG_PATH)
model = CLaMP(config)
state_dict = torch.load(os.path.join(CLAMP_MODEL_NAME, "pytorch_model.bin"))
model.load_state_dict(state_dict, strict=False)
model = model.to(device).eval()

# ----- Tokenizer -----
tokenizer = AutoTokenizer.from_pretrained(TEXT_MODEL_NAME)

# ----- Batch Processing -----
for i in tqdm(range(1, 910)):  # Folders 001 to 909
    folder = f"{i:03d}"
    folder_path = os.path.join(ROOT_DIR, folder)
    text_file_path = os.path.join(folder_path, "midi_melody.txt")
    save_path = os.path.join(folder_path, "text_embedding.pt")

    # Skip if file doesn't exist
    if not os.path.exists(text_file_path):
        print(f"WARNING: {text_file_path} not found, skipping.")
        continue

# Read text
    with open(text_file_path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    # Tokenize
    encoded = tokenizer(text, return_tensors="pt", truncation=True, max_length=TEXT_LENGTH)
    input_ids = encoded["input_ids"].to(device)
    attention_mask = encoded["attention_mask"].to(device)

    # Encode
    with torch.no_grad():
        h = model.text_enc(input_ids, attention_mask=attention_mask)["last_hidden_state"]
        pooled = model.avg_pooling(h, attention_mask)
        embedding = model.text_proj(pooled)

    # Save
    torch.save(embedding[0].cpu(), save_path)

print("✅ Done embedding all melody.txt files!")
