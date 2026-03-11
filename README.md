# 🛡️ Agentic AI Surveillance System

An enterprise-grade, intelligent video analytics system designed to showcase advanced AI capabilities. This platform processes video feeds using PyTorch-based detect-and-track architectures, identifies high-risk behavioral anomalies, and employs a multi-agent orchestrated reasoning engine to automate security operations.

## 🚀 Key Features

- **Advanced Computer Vision Pipeline:**
  - Real-time people detection using **Ultralytics YOLOv8**.
  - Multi-object continuity tracking with Centroid mapping logic.
- **Behavioral Event Engine:**
  - Spatial-temporal analysis for loitering detection.
  - Geo-fenced Restricted Zone entry detection.
- **Multi-Agent AI Architecture (LangGraph):**
  - **Vision Agent**: Parses spatial tracking logic.
  - **Context Agent**: Extracts RAG security policies.
  - **Investigation Agent**: Queries historical database patterns to identify recurring threats.
  - **Decision Agent**: Calculates threat thresholds based on synthesized intelligence.
  - **Reviewer Agent**: Acts as an AI safeguard filter, downgrading false positives and conditionally routing execution to optimize performance.
  - **Report & Alert Agents**: Automates IT ticket generation and email notifications.
- **Explainable RAG System:**
  - Connects system alerts to dynamic vector databases (FAISS) storing enterprise security policies.
- **Professional VMS Dashboard:**
  - Streamlit-powered dark-mode UI overlaying inference on video playback.
  - Real-time interactive AI Query interface to chat with the incident database.
- **Cloud-Ready Deployment:**
  - Fully containerized using `Dockerfile` and `docker-compose.yml`.

## 🛠 Tech Stack
- **Deep Learning**: PyTorch, Ultralytics (YOLO)
- **Computer Vision**: OpenCV, FilterPy, SciPy
- **AI Orchestration**: LangGraph, LangChain, FAISS, Sentence Transformers
- **Backend & Data**: FastAPI, SQLite, Pandas
- **Frontend**: Streamlit, Plotly
- **DevOps**: Docker, Docker Compose

## 📖 Getting Started
See the [RUNNING_STEPS.md](RUNNING_STEPS.md) file for instructions on installing dependencies, running the inference pipelines, loading the Streamlit Dashboards, and querying the API network!