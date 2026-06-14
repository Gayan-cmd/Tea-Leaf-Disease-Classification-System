# 🛠️ Development Process: Notebook to Production

This document outlines the step-by-step engineering process taken to transform an academic deep learning Jupyter Notebook into a production-ready, containerized microservices application deployed on Hugging Face Spaces.

The transition was executed in **5 distinct phases**.

---

## Phase 1: Code Extraction & Refactoring
**Goal:** Isolate the machine learning logic from the Jupyter Notebook environment to make it reusable for an API.

In a notebook, training, evaluation, and visualization are heavily coupled. For production, the API only needs the **architecture definition** and the **inference logic**.

1. **Directory Structure:** Established a modular project structure (`api/`, `app/`, `src/`, `models/`).
2. **Model Extraction (`src/model.py`):** 
   - Extracted the PyTorch `build_resnet50` function. 
   - Stripped out training-specific logic (like unfreezing layers for differential learning rates) since inference only requires the forward pass.
   - Created a robust `load_model()` utility to handle loading the `.pth` weights into memory.
3. **Inference Pipeline (`src/inference.py`):**
   - Extracted the validation `torchvision.transforms` (Resize, CenterCrop, Normalize).
   - Created a `predict()` function that accepts raw image bytes, converts them into a tensor, runs them through the model, applies a softmax activation, and returns a human-readable class name and confidence score.

---

## Phase 2: Building the FastAPI Backend
**Goal:** Expose the PyTorch model over a network using a high-performance REST API.

1. **FastAPI Setup (`api/main.py`):** Chosen for its speed and native async support.
2. **Memory Management (Lifespan Context):** 
   - A critical ML engineering best practice is to load the model into memory **only once** when the server starts, rather than loading it on every request. This was achieved using FastAPI's `@asynccontextmanager` lifespan hook.
3. **The `/predict` Endpoint:** 
   - Implemented an endpoint expecting a `multipart/form-data` image upload.
   - The endpoint validates the file type, reads the bytes, and passes them to the `predict()` function from Phase 1, returning a clean JSON response.

---

## Phase 3: Building the Streamlit Frontend
**Goal:** Create an interactive, user-friendly dashboard for non-technical users to interact with the API.

1. **Streamlit UI (`app/frontend.py`):** Chosen for its rapid prototyping capabilities in Python.
2. **Dashboard Design:**
   - Implemented a wide-screen, two-column layout.
   - **Left Column:** Handles file uploads and displays the image preview inside a bordered container.
   - **Right Column:** Contains the call-to-action button and displays the results using large, native `st.metric()` components and an `st.progress()` bar to visually represent model confidence.
3. **API Communication:** Utilized the `requests` library to send the uploaded image to the FastAPI backend. Implemented error handling to catch API disconnects or 500/400 status codes gracefully.

---

## Phase 4: Dockerization
**Goal:** Package the services to ensure they run identically across any environment (development, staging, production).

1. **Backend & Frontend Dockerfiles:** 
   - Created separate `Dockerfile`s for the `api` and `app` using `python:3.9-slim` to minimize image size.
   - Installed system-level dependencies (like `gcc`) required for compiling ML libraries.
2. **Docker Compose:** 
   - Authored a `docker-compose.yml` to orchestrate both containers locally.
   - Established an internal Docker network allowing the frontend to communicate securely with the backend via the `BACKEND_URL=http://backend:8000/predict` environment variable.

---

## Phase 5: Deployment & Hugging Face Adaptation
**Goal:** Deploy the application to the internet securely and reliably.

Hugging Face Spaces was chosen for hosting. However, Spaces traditionally support only **one container** and expose **one port** (7860). To maintain our microservice architecture, the deployment strategy was adapted:

1. **Unified Dockerfile:** 
   - Created a single `Dockerfile` at the project root that installs requirements for *both* FastAPI and Streamlit.
2. **Startup Script (`run.sh`):**
   - Written a bash script to start `uvicorn` (FastAPI) in the background on port 8000, wait 3 seconds, and then start `streamlit` on port 7860 (the port Hugging Face exposes to the public).
3. **Security Fixes (CORS & XSRF):**
   - Hugging Face runs Streamlit inside an iframe. This triggers Streamlit's Cross-Site Request Forgery (XSRF) protection, causing a `403 Forbidden` error on file upload. Fixed by adding `--server.enableCORS=false --server.enableXsrfProtection=false` to the startup command.
4. **Git LFS Integration:**
   - Standard Git cannot handle 100MB+ `.pth` model weights. Configured Git Large File Storage (LFS) (`.gitattributes`) to properly track and securely upload the ResNet50 model to the Hugging Face repository.
5. **Git History Cleanup:**
   - Bypassed Hugging Face's strict binary file limitations (Xet storage requirement) by using `git filter-branch` to forcefully rewrite the repository's history and permanently erase legacy `.png` files from the Jupyter notebook era.