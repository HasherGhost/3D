"""
model.py -- loads the ResNet-50 checkpoint at startup.
Architecture and weights are never modified.
"""
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

# Preprocessing must match training exactly
TRANSFORM = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])


def load_model(weights_path: str) -> torch.nn.Module:
    """Build the exact training architecture and load saved weights (CPU only)."""
    model = models.resnet50(weights=None)
    model.fc = nn.Sequential(
        nn.Dropout(0.3),
        nn.Linear(model.fc.in_features, 1),
        nn.Sigmoid(),
    )
    state_dict = torch.load(weights_path, map_location="cpu")
    model.load_state_dict(state_dict)
    model.eval()
    return model


def predict(model: torch.nn.Module, image: Image.Image) -> dict:
    """
    Run inference on a PIL image.
    Returns {p_real, p_ai, label} where label is 'real' or 'ai'.
    """
    tensor = TRANSFORM(image.convert("RGB")).unsqueeze(0)   # (1,3,224,224)
    with torch.no_grad():
        p_real = float(model(tensor).item())   # sigmoid output = P(real)
    p_ai  = 1.0 - p_real
    label = "ai" if p_real < 0.5 else "real"
    return {"p_real": p_real, "p_ai": p_ai, "label": label}
