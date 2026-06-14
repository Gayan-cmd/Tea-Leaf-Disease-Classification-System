import os
import sys
from fastapi import FastAPI, UploadFile, File, HTTPException
from contextlib import asynccontextmanager

# Add the parent directory to sys.path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.model import load_model
from src.inference import predict

# Global variable to hold the loaded model
app_context = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the model on startup
    print("Loading model...")
    weights_path = os.path.join("models", "best_ResNet50.pth")
    if not os.path.exists(weights_path):
        raise FileNotFoundError(f"Model weights not found at {weights_path}")
    
    try:
        app_context["model"] = load_model(weights_path, device='cpu')
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        raise e
    
    yield
    # Clean up on shutdown (if necessary)
    app_context.clear()

app = FastAPI(
    title="Tea Leaf Disease Classifier API",
    description="API for classifying tea leaf diseases using a custom ResNet50 model.",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Tea Leaf Disease Classifier API. Use the /predict endpoint to classify images."}

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    try:
        # Read the file bytes
        image_bytes = await file.read()
        
        # Ensure model is loaded
        if "model" not in app_context:
             raise HTTPException(status_code=503, detail="Model is not loaded.")

        # Pass bytes to the inference script
        result = predict(image_bytes, app_context["model"])
        
        return result
    
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error during prediction: {str(e)}")
