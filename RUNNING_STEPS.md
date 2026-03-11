# 🛡️ Multi-Agent AI Surveillance System - Running Guide

Welcome to the Agentic Surveillance AI project! This document outlines step-by-step instructions on how to set up, activate, and run the various components of the intelligence surveillance pipeline.

## 🛠 Prerequisites

Ensure you have Python 3.10+ installed on your system.

## 📦 Step 1: Clone & Setup the Environment

We strongly recommend using a virtual environment to manage project dependencies.

```powershell
# 1. Create a virtual environment
python -m venv venv

# 2. Activate the virtual environment
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# 3. Install the dependencies
pip install -r requirements.txt
```

---

## 🚀 Step 2: System Deployment (Docker Compose) - *Recommended*

The entire microservice architecture (Inference API + Streamlit Frontend + Database) is containerized for production deployment. 

```bash
# This will build and boot the entire platform simultaneously
docker-compose up --build
```
*Note: Ensure Docker Desktop is running on your machine.*

---

## 🧠 Step 3: Running the Core Engine Natively

If you want to bypass Docker and run the core reasoning pipeline locally to see the LangGraph agents spit out their logs in the terminal:

```powershell
# Make sure your virtual environment is active!
python main.py
```
### Pipeline Execution Flow:
1. Extracts frames to `data/frames/`.
2. Computes inference using `yolov8n.pt` and mathematical centroid object tracking.
3. `EventDetector` monitors behavioral zones (Loitering/Restricted Zones).
4. **LangGraph Workflow**: Vision Agent -> Context Agent (using RAG) -> Investigation Agent -> Decision Agent -> Reviewer Agent -> (Conditionally) Report & Alert Agents.
5. High-risk, reviewer-approved incidents trigger automated support tickets and log into the local SQLite `incidents.db`. Detailed incident explanations are written to `data/processed/reports/`.

---

## 📡 Step 4: Running the Backend FastAPI Server Natively

We expose an API representing the backend services where external dashboards and monitoring clients can query system health or incident records.

**Run the Server (using Uvicorn):**
```powershell
# Starts the server on localhost:8000
uvicorn backend.api:app --reload
```

**Testing the API:**
Open your browser and navigate to:
- Interactive API Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- System Status endpoint: [http://127.0.0.1:8000/status](http://127.0.0.1:8000/status)

---

## 🖥️ Step 5: Running the Streamlit VMS Dashboard Natively

Launch the custom Video Management System (VMS) frontend to visualize live inference tracking and chat with the RAG database.

```powershell
streamlit run dashboard/dashboard_server.py
```
Navigate to: [http://localhost:8501](http://localhost:8501)

### Dashboard Features:
- **Live Inference Engine**: See YOLO boundary boxes computing in real-time over the video feed.
- **RAG Query Interface**: Ask the AI questions like "What occurred today?" or "Why was the alert triggered?".
- **Dynamic Plotting**: Review operational metrics and incident timelines graphed via Plotly.

---

## 📈 Evaluate Performance

To observe the detection pipeline performance utilizing a mock ground-truth evaluation structure:

```powershell
python tests/evaluate.py
```
*Calculates Prediction Accuracy, Event Recall percentages, F1-Scores, and False-Positive frequencies.*
