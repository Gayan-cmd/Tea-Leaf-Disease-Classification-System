import torch
import torchvision.transforms as transforms
from PIL import Image
import io

# ImageNet mean and std since we use pretrained weights
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD  = [0.229, 0.224, 0.225]

# Define the transforms used for validation/testing
val_test_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD)
])

# Define the class names matching the order from the notebook (alphabetical from ImageFolder)
CLASS_NAMES = ['algal leaf', 'brown blight', 'white spot']

def predict(image_bytes, model, device='cpu'):
    """
    Takes raw image bytes, applies transforms, passes it through the model, 
    and returns the predicted class name and confidence score.
    """
    try:
        # Load image from bytes
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception as e:
        raise ValueError(f"Invalid image format: {e}")

    # Apply transformations and add batch dimension
    input_tensor = val_test_transforms(image).unsqueeze(0).to(device)

    # Perform inference
    with torch.no_grad():
        outputs = model(input_tensor)
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
        
        # Get the highest probability class
        confidence, predicted_idx = torch.max(probabilities, 0)
        
        predicted_class = CLASS_NAMES[predicted_idx.item()]
        confidence_score = confidence.item()

    return {
        "class": predicted_class.title(), # Title case for better display
        "confidence": round(confidence_score, 4)
    }
