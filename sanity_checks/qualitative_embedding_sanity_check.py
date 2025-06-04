import os
import random
import numpy as np
import torch
import torch.nn.functional as F
from tqdm import tqdm

# ======= CONFIG =======
NUM_SONGS = 909
MUSIC_ROOT = "matched_pop909_acc"
TEXT_ROOT = "pop909_w_structure_label"
EMBEDDING_FILENAME = {
    "music": "melody_embedding.pt",
    "text": "text_embedding.pt"
}
NUM_NEGATIVES = 9  # Updated to 9 negative samples
SEED = 42
# ======================

random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)

def load_embedding(folder_id, modality):
    root = MUSIC_ROOT if modality == "music" else TEXT_ROOT
    path = os.path.join(root, f"{folder_id:03d}", EMBEDDING_FILENAME[modality])
    if not os.path.exists(path):
        raise FileNotFoundError(f"{modality} embedding missing: {path}")
    return torch.load(path)

def inner_product(a, b):
    return torch.dot(a, b).item()

# Store similarities
similarities = []
ranks = []
top1_matches = 0
top5_matches = 0

print("🔍 Running sanity check...")
for song_id in tqdm(range(1, NUM_SONGS + 1)):
    try:
        music_emb = load_embedding(song_id, "music")
        text_emb  = load_embedding(song_id, "text")
    except FileNotFoundError:
        continue

    # Compute correct similarity (inner product)
    pos_sim = inner_product(music_emb, text_emb)

    # Pick negatives
    neg_ids = random.sample([i for i in range(1, NUM_SONGS + 1) if i != song_id], NUM_NEGATIVES)
    neg_texts = [load_embedding(neg_id, "text") for neg_id in neg_ids]

    # Similarities
    all_sims = [pos_sim] + [inner_product(music_emb, neg) for neg in neg_texts]
    sorted_indices = np.argsort(all_sims)[::-1]  # descending

    rank = np.where(sorted_indices == 0)[0][0] + 1  # 1-based rank of correct match
    ranks.append(rank)

    if rank == 1:
        top1_matches += 1
    if rank <= 5:
        top5_matches += 1

    similarities.append(pos_sim)

# Report results
print("\n🔍 Sanity Check Report")
print("----------------------")
print(f"Top-1 Accuracy:  {100 * top1_matches / NUM_SONGS:.2f}%")
print(f"Top-5 Accuracy:  {100 * top5_matches / NUM_SONGS:.2f}%")
print(f"Median Rank:     {np.median(ranks):.2f}")
# print(f"Mean Similarity (match): {np.mean(similarities):.4f}")

