import torch
import transformers

print(f"Torch version: {torch.__version__}")
print(f"Transformers version: {transformers.__version__}")

# Simple check to ensure CUDA is available if possible, or just CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")
