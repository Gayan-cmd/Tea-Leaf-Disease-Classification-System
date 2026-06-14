import torch
import torch.nn as nn
import torchvision.models as models

def build_resnet50(num_classes=3):
    """
    Builds the ResNet50 model with custom classifier head.
    """
    model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)

    # Replace final FC layer — fully customizable based on training
    in_features = model.fc.in_features  # 2048
    model.fc = nn.Sequential(
        nn.Linear(in_features, 512),
        nn.ReLU(),
        nn.Dropout(0.4),
        nn.Linear(512, 128),
        nn.ReLU(),
        nn.Dropout(0.3),
        nn.Linear(128, num_classes)
    )
    return model

def load_model(weights_path, device='cpu'):
    """
    Initializes the model and loads weights.
    """
    model = build_resnet50(num_classes=3)
    model.load_state_dict(torch.load(weights_path, map_location=device))
    model.to(device)
    model.eval()
    return model
