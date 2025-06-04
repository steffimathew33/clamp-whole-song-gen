# note: should work for any kind of embedding (.pt file) - music OR text

import torch

# Load the file
embeddings = torch.load("matched_pop909_acc/001/melody_embedding.pt")

# Print the type
print("Type:", type(embeddings))

# If it's a tensor
if isinstance(embeddings, torch.Tensor):
    print("Shape:", embeddings.shape)
    print("Sample values:", embeddings[:5])  # Print the first 5 vectors

# If it's a dictionary
elif isinstance(embeddings, dict):
    for key, value in embeddings.items():
        print(f"Key: {key}, Shape: {value.shape if isinstance(value, torch.Tensor) else type(value)}")
        print(f"Sample from '{key}':", value[0] if isinstance(value, torch.Tensor) else value)

# If it's a list of tensors
elif isinstance(embeddings, list):
    print(f"List of {len(embeddings)} items")
    print("First item shape:", embeddings[0].shape)
    print("First item values:", embeddings[0][:5])

