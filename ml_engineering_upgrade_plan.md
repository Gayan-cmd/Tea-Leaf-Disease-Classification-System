# 🚀 1-Day ML Engineering Upgrade Plan: Tea Leaf Disease Classifier

**Goal:** Transform the academic Jupyter Notebook assignment into a production-ready, deployable machine learning application.
**Outcome:** A REST API (FastAPI), a Web Frontend (Streamlit), containerized with Docker, and ready for deployment (Hugging Face Spaces or Render).

---

## 🕒 Schedule Overview

| Time | Phase | Focus |
|---|---|---|
| 09:00 - 10:30 | Phase 1 | Code Extraction & Refactoring |
| 10:30 - 12:30 | Phase 2 | Building the FastAPI Backend |
| 12:30 - 13:30 | *Lunch Break* | |
| 13:30 - 15:30 | Phase 3 | Building the Streamlit Frontend |
| 15:30 - 17:00 | Phase 4 | Dockerization |
| 17:00 - 18:00 | Phase 5 | Deployment & Documentation Update |

---

## 🛠️ Detailed Execution Plan

### Phase 1: Code Extraction & Refactoring (09:00 - 10:30)
**Objective:** Move inference logic out of the Jupyter Notebook into reusable Python scripts.

1. **Setup Project Structure:**
   Create the following new directories and files:
   ```text
   DL_assigment02/
   ├── api/
   │   ├── main.py         # FastAPI app
   │   └── requirements.txt
   ├── app/
   │   ├── frontend.py     # Streamlit app
   │   └── requirements.txt
   ├── src/
   │   ├── model.py        # Model architecture & loading logic
   │   └── inference.py    # Image preprocessing & prediction logic
   ├── models/             # Move best_ResNet50.pth here
   ```
2. **Write `src/model.py`:**
   - Extract the PyTorch `ResNet50` architecture definition from the notebook.
   - Write a function `load_model(weights_path)` that initializes the model, loads the state dict, and sets it to `eval()` mode.
3. **Write `src/inference.py`:**
   - Extract the `torchvision.transforms` used for the test set (Resize, CenterCrop, ToTensor, Normalize).
   - Write a `predict(image_bytes, model)` function that takes raw image bytes, applies transforms, passes it through the model, and returns the predicted class name and confidence score.

### Phase 2: Building the FastAPI Backend (10:30 - 12:30)
**Objective:** Create a REST API that accepts an image and returns JSON predictions.

1. **Install Dependencies:** `pip install fastapi uvicorn python-multipart`
2. **Develop `api/main.py`:**
   - Initialize the FastAPI app.
   - Use the `@app.on_event("startup")` hook to load the ResNet50 model into memory *once* when the server starts.
   - Create a `POST /predict` endpoint that accepts an `UploadFile`.
   - Read the file bytes, pass them to `src.inference.predict`, and return a JSON response (e.g., `{"class": "White Spot", "confidence": 0.98}`).
3. **Test Locally:**
   - Run the server: `uvicorn api.main:app --reload`
   - Test using the built-in Swagger UI at `http://localhost:8000/docs` by uploading a sample leaf image.

### Phase 3: Building the Streamlit Frontend (13:30 - 15:30)
**Objective:** Build a user-friendly web UI for non-technical users to interact with the model.

1. **Install Dependencies:** `pip install streamlit requests pillow`
2. **Develop `app/frontend.py`:**
   - Set up the page layout (Title, description of the 3 diseases).
   - Add a `st.file_uploader` for users to upload `.jpg` or `.png` images.
   - When an image is uploaded, display it on the screen.
   - Add a "Predict" button.
   - When clicked, use the `requests` library to send the image to your FastAPI endpoint (`http://localhost:8000/predict`).
   - Parse the JSON response and display the predicted class and confidence using Streamlit metrics or success messages.
3. **Test Locally:**
   - Run the app: `streamlit run app/frontend.py`
   - Ensure the Streamlit app correctly communicates with the FastAPI backend running in a separate terminal.

### Phase 4: Dockerization (15:30 - 17:00)
**Objective:** Package the API and Frontend into containers for consistent deployment.
*(Note: For simplicity on a 1-day build, we will use a Docker Compose setup, or combine them if deploying to a single container platform).*

1. **Write `api/Dockerfile`:**
   - Base image: `python:3.9-slim`
   - Copy `api/requirements.txt`, `src/`, and `models/`.
   - Expose port 8000.
   - Command: `uvicorn main:app --host 0.0.0.0 --port 8000`
2. **Write `app/Dockerfile`:**
   - Base image: `python:3.9-slim`
   - Copy `app/requirements.txt`.
   - Expose port 8501.
   - Command: `streamlit run frontend.py --server.port=8501 --server.address=0.0.0.0`
3. **Write `docker-compose.yml` (Root directory):**
   - Define two services: `backend` (FastAPI) and `frontend` (Streamlit).
   - Ensure the `frontend` service points its API requests to `http://backend:8000/predict` instead of `localhost`.
4. **Build and Test:** `docker-compose up --build`

### Phase 5: Deployment & Documentation Update (17:00 - 18:00)
**Objective:** Put the project live on the internet and update the CV/README.

1. **Deployment Choice (Hugging Face Spaces - Easiest for Portfolio):**
   - *Alternative to Docker phase if time is short:* Hugging Face Spaces supports Gradio/Streamlit natively.
   - If deploying via Docker, push to a platform like Render or Railway.
2. **Update `README.md`:**
   - Add screenshots of the new web interface.
   - Add an "Architecture" section explaining the API and UI separation.
   - Provide instructions on how to run the Docker containers.
   - Include the live link to the deployed application.
3. **Draft CV Bullet Points:** Write the final bullet points highlighting the transition from notebook to deployed microservices.

---

## 🎯 Next Steps

If you are ready to begin, we can start with **Phase 1** right now. I can help write the `model.py` and `inference.py` scripts to extract your PyTorch logic from the notebook.