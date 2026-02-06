# Implementation Plan - GRU Resume Analyzer & Job Role Predictor

This plan outlines the steps to build a GRU-based Resume Analyzer and Job Role Prediction System, optimized for CPU and deployed via Flask with a premium UI.

## Phase 1: Environment Setup & Data Preparation
- [ ] **Dependencies**: Install `tensorflow`, `flask`, `pdfplumber`, `python-docx`, `pytesseract`, `Pillow`, `nltk`, `scikit-learn`, `pandas`, `numpy`.
- [ ] **Data Analysis**: Load `archive/Resume/Resume.csv`. Analyze class distribution (Categories).
- [ ] **Data Preprocessing**:
    - Clean text (remove special characters, lowercase, remove stopwords).
    - Tokenization (limit vocab size ~5000-10000 for CPU speed).
    - Padding sequences (limit max_len ~200-300).
    - Encode labels (`Category` column).

## Phase 2: Model Development (CPU Optimized)
- [ ] **Architecture**:
    - Embedding Layer (dim=50-100).
    - GRU Layer (units=64, return_sequences=False). *Keep it light.*
    - Dropout (0.3).
    - Dense Output Layer (softmax).
- [ ] **Training**:
    - Batch size: 64 or 128 (balance speed/memory).
    - Epochs: 10-15 with EarlyStopping.
    - Optimizer: Adam.
    - Application of Class Weights (if data unbalanced).
- [ ] **Save Model**: Save as `gru_resume_model.h5` and tokenizer as `tokenizer.pickle`.

## Phase 3: Resume Parsing & Inference Logic
- [ ] **Parser Module** (`resume_parser.py`):
    - `extract_text_from_pdf`: use `pdfplumber`.
    - `extract_text_from_docx`: use `python-docx`.
    - `extract_text_from_image`: use `pytesseract`.
    - `clean_text`: matching training preprocessing.
- [ ] **Extraction Components**:
    - Skills extraction (keyword matching vs predefined list).
    - Education/Experience extraction (regex/pattern based for this scope).

## Phase 4: Flask Application
- [ ] **Backend** (`app.py`):
    - Routes: `/` (home), `/upload` (POST), `/predict` (result).
    - Load model and tokenizer on startup.
- [ ] **Frontend**:
    - `templates/index.html`: Drag & drop upload, animated interface.
    - `templates/result.html`: Dashboard showing prediction, confidence, skills, and recommendations.
    - `static/style.css`: Glassmorphism, modern typography, animations.

## Phase 5: Testing & Deployment
- [ ] **Test**: Run with sample resumes (PDF/DOCX/IMG).
- [ ] **Optimization Check**: Measure inference time on CPU.
- [ ] **Documentation**: `README.md` with usage instructions.

