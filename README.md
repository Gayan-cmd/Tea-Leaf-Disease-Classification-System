
<div align="center">

# 🍃 Tea Leaf Disease Classification System

**An end-to-end deep learning system for automated tea leaf disease detection**

*From research notebook to a live, containerized microservices application*

![Python](https://img.shields.io/badge/Python-3.9-blue?logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0-EE4C2C?logo=pytorch&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-FF4B4B?logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)
![HuggingFace](https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-FFD21E)

</div>

---

## 📌 Overview

Tea leaf diseases cause significant economic losses in tea production worldwide. Early and accurate detection is critical for timely intervention and crop protection. This project applies **transfer learning** with state-of-the-art CNN architectures to automate disease classification from leaf images — eliminating the need for slow, costly manual expert inspection.

The project was built in two phases:

| Phase | Description |
|---|---|
| **Research** | Compared VGG16 and ResNet50 architectures using transfer learning in a Jupyter Notebook. ResNet50 achieved **91% test accuracy** and was selected for production. |
| **Production** | Refactored the notebook into a full-stack microservices application with a REST API, interactive web dashboard, Docker containerization, and live deployment on Hugging Face Spaces. |

---

## 🏆 Model Performance

Both models were fine-tuned on a dataset of **368 labelled tea leaf images** across 3 disease classes, using a **60/20/20 train/validation/test split**.

| Metric | VGG16 | ResNet50 |
|---|---|---|
| Test Accuracy | 80.00% | **91.00%** |
| Macro F1-Score | 0.79 | **0.91** |
| Best Val Accuracy | 82.43% | **86.49%** |
| Epochs to Converge | 16 | **10** |
| Overfitting | High | **Low** |

> **ResNet50** was selected for production deployment due to its superior accuracy, faster convergence, and better generalization on the small dataset — attributed to its residual (skip) connections.

---

## 🏗️ System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    Hugging Face Spaces                        │
│                                                              │
│   ┌─────────────────────────┐                               │
│   │   Streamlit Frontend    │  ← Port 7860 (Public)         │
│   │   app/frontend.py       │                               │
│   └────────────┬────────────┘                               │
│                │  HTTP POST /predict                         │
│                ▼                                             │
│   ┌─────────────────────────┐                               │
│   │   FastAPI Backend       │  ← Port 8000 (Internal)       │
│   │   api/main.py           │                               │
│   └────────────┬────────────┘                               │
│                │                                             │
│                ▼                                             │
│   ┌─────────────────────────┐                               │
│   │   ML Inference Engine   │                               │
│   │   src/inference.py      │                               │
│   │   src/model.py          │                               │
│   │   models/best_ResNet50  │                               │
│   └─────────────────────────┘                               │
└──────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Deep Learning** | PyTorch, torchvision |
| **Model Architectures** | ResNet50, VGG16 (ImageNet pretrained) |
| **Backend API** | FastAPI, Uvicorn |
| **Frontend UI** | Streamlit |
| **Containerization** | Docker, Docker Compose |
| **Deployment** | Hugging Face Spaces |
| **Evaluation** | scikit-learn, matplotlib, seaborn |
| **Large File Storage** | Git LFS |

---

## 📁 Project Structure

```
tea-leaf-disease-classifier/
│
├── api/                        # FastAPI backend service
│   ├── main.py                 # API endpoints and model lifespan management
│   ├── requirements.txt        # Backend dependencies
│   └── Dockerfile              # Backend container definition
│
├── app/                        # Streamlit frontend service
│   ├── frontend.py             # Web dashboard UI
│   ├── requirements.txt        # Frontend dependencies
│   └── Dockerfile              # Frontend container definition
│
├── src/                        # Core ML logic (shared)
│   ├── model.py                # ResNet50 architecture + weight loader
│   └── inference.py            # Prediction pipeline (transforms + softmax)
│
├── models/                     # Saved model weights (tracked via Git LFS)
│   ├── best_ResNet50.pth       # Production model (~98MB)
│   └── best_VGG16.pth          # Research comparison model (~163MB)
│
├── leaf_disease_classiflier.ipynb  # Original research notebook
├── model_comparison_report.md      # Detailed VGG16 vs ResNet50 analysis
├── docker-compose.yml              # Local multi-container orchestration
├── Dockerfile                      # Unified container for Hugging Face
├── run.sh                          # Startup script for HF Spaces deployment
├── .gitattributes                  # Git LFS tracking rules for .pth files
└── README.md
```

---

## 🌿 Disease Classes

The model classifies tea leaf images into **3 categories**:

| Class | Pathogen | Visual Symptom |
|---|---|---|
| **Algal Leaf** | *Cephaleuros virescens* | Orange-red circular spots on leaf surface |
| **Brown Blight** | Fungal infection | Brownish lesions spreading across the leaf |
| **White Spot** | Fungal infection | White circular spots on the leaf surface |

---

## 🚀 Getting Started

### Option 1 — Live Demo (No Setup Required)

Visit the live application on **Hugging Face Spaces** — upload any tea leaf image and get an instant disease prediction.

> 🤗 [**Launch Live Demo →**](https://huggingface.co/spaces/Neo-cmd/Tea-Leaf-Disease-Classifier)

---

### Option 2 — Run Locally with Docker Compose

The fastest way to run the full application stack locally.

**Prerequisites:** [Docker Desktop](https://docs.docker.com/desktop/) installed and running.

```bash
# 1. Clone the repository
git clone https://huggingface.co/spaces/<your-username>/tea-leaf-disease-classifier
cd tea-leaf-disease-classifier

# 2. Build and start both services
docker-compose up --build
```

| Service | URL | Description |
|---|---|---|
| **Web Dashboard** | http://localhost:8501 | Streamlit UI for image upload and prediction |
| **API Docs (Swagger)** | http://localhost:8000/docs | Interactive REST API documentation |
| **API Health Check** | http://localhost:8000/ | Confirms the API is running |

```bash
# Stop all containers
docker-compose down
```

---

### Option 3 — Run Locally without Docker

```bash
# 1. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# 2. Install dependencies
pip install -r api/requirements.txt
pip install -r app/requirements.txt

# 3. Start the FastAPI backend (in one terminal)
uvicorn api.main:app --host 0.0.0.0 --port 8000

# 4. Start the Streamlit frontend (in another terminal)
streamlit run app/frontend.py --server.port 8501
```

---

## 📡 API Reference

### `GET /`
Health check endpoint.

**Response:**
```json
{
  "message": "Welcome to the Tea Leaf Disease Classifier API. Use the /predict endpoint to classify images."
}
```

### `POST /predict`
Classifies an uploaded tea leaf image.

**Request:** `multipart/form-data` with an image file field named `file`.

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "accept: application/json" \
     -F "file=@your_leaf_image.jpg"
```

**Response:**
```json
{
  "class": "Brown Blight",
  "confidence": 0.9231
}
```

| Field | Type | Description |
|---|---|---|
| `class` | `string` | Predicted disease class name |
| `confidence` | `float` | Model confidence score (0.0 – 1.0) |

**Error Codes:**

| Code | Meaning |
|---|---|
| `400` | File is not a valid image |
| `503` | Model not yet loaded |
| `500` | Internal inference error |

---

## 🔬 Research Methodology

### Transfer Learning Strategy

Both models used **ImageNet pretrained weights** with a **differential learning rate** approach:

| Layer Group | Learning Rate | Strategy |
|---|---|---|
| Early backbone layers | Frozen (`0`) | Preserve low-level ImageNet features |
| Late backbone layers | `1e-5` (very slow) | Gently adapt to tea-specific visual patterns |
| Custom classifier head | `1e-3` (fast) | Learn the new 3-class task aggressively |

### Training Configuration

| Parameter | Value |
|---|---|
| Optimizer | Adam (differential LRs) |
| Loss Function | CrossEntropyLoss |
| LR Scheduler | ReduceLROnPlateau (factor=0.5, patience=3) |
| Batch Size | 16 |
| Max Epochs | 25 |
| Early Stopping | patience=5 |

### Data Augmentation (Training Only)

- Random horizontal flip (p=0.5)
- Random vertical flip (p=0.2)
- Random rotation (±20°)
- Color jitter (brightness, contrast, saturation)
- Resize to 224×224 + ImageNet normalization

---

## 🐳 Docker & Deployment Notes

### Local Development (Docker Compose)
Two isolated containers communicate over an internal Docker bridge network (`tea-leaf-net`). The frontend reaches the backend via the service name `http://backend:8000/predict` using Docker's internal DNS — no hardcoded IPs.

### Hugging Face Spaces Deployment
Hugging Face Spaces exposes only **port 7860**. To maintain the microservices architecture, both services run as parallel OS processes inside a single unified container:

- `run.sh` starts `uvicorn` (FastAPI) in the background on port 8000
- After a 3-second startup delay, `streamlit` starts on port 7860 (the public port)
- XSRF protection is disabled to allow file uploads through Hugging Face's iframe embedding

### Git LFS for Model Weights
Model weight files (`.pth`) are tracked with **Git LFS** via `.gitattributes` to handle files exceeding Git's 100MB limit.

---

## 📊 Detailed Results

For a full epoch-by-epoch training log, confusion matrices, classification reports, and an in-depth analysis of VGG16 vs ResNet50 on this dataset, see:

📄 [`model_comparison_report.md`](./model_comparison_report.md)

---

## 📝 License

This project was originally developed for academic purposes as part of a Deep Learning assignment at the **University of Peradeniya**, and subsequently upgraded to a production-grade, deployed application.