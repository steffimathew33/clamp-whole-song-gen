import torch
import os
from pathlib import Path
import random

# === Configuration ===
ORIGINAL_SONG_NUMBER = "001"  # <-- Change this to a string like "001" to "909"

EMBEDDING_ROOT = Path("matched_pop909_acc")
NUM_SONGS = 909

def load_embedding(song_number_str):
    folder = EMBEDDING_ROOT / song_number_str
    path = folder / "melody_embedding.pt"
    return torch.load(path)

def inner_product(a, b):
    return torch.dot(a.view(-1), b.view(-1)).item()

def main():
    original_song_str = ORIGINAL_SONG_NUMBER
    original_song_int = int(original_song_str)
    print(f"Original song number selected: {original_song_str}")

    original_embedding = load_embedding(original_song_str)

    similarities = []
    for i in range(1, NUM_SONGS + 1):
        if i == original_song_int:
            continue
        song_str = f"{i:03d}"
        try:
            other_embedding = load_embedding(song_str)
            similarity = inner_product(original_embedding, other_embedding)
            similarities.append((song_str, similarity))
        except Exception as e:
            print(f"Skipping song {song_str} due to error: {e}")

    similarities.sort(key=lambda x: x[1])  # ascending order

    least_similar_song = similarities[0][0]
    most_similar_song = similarities[-1][0]

    # Shuffle so you don't know which is which
    blind_list = [most_similar_song, least_similar_song]
    random.shuffle(blind_list)

    print(f"\n🎵 Original Song Number: {original_song_str}")
    print(f"🔍 Here are two other song numbers for blind listening:")
    print(f" - Blind Song A: {blind_list[0]}")
    print(f" - Blind Song B: {blind_list[1]}")

    input("\nPress Enter to reveal which was most similar and least similar...")

    print(f"\n✅ Most Similar Song (highest inner product): {most_similar_song}")
    print(f"❌ Least Similar Song (lowest inner product): {least_similar_song}")

if __name__ == "__main__":
    main()

