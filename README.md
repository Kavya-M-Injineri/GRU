# GRU Resume Analyzer & Job Predictor

A powerful AI-powered Resume Analyzer using a GRU neural network to predict job roles from resumes.

## Features
- **Resume Parsing**: Supports PDF, DOCX, TXT, and Images.
- **AI Prediction**: Uses a GRU model trained on thousands of resumes.
- **Rich UI**: Modern, animated, and responsive interface.
- **Analysis**: Extracts text and predicts job role with confidence score.

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   (Note: `tensorflow`, `flask`, `pdfplumber`, `python-docx`, `pytesseract`, `pillow`, `nltk`, `scikit-learn`, `pandas`, `numpy`)

2. **Install Tesseract OCR (Optional for Images)**:
   - Download and install Tesseract-OCR for Windows.
   - Add it to your PATH or update `resume_parser.py` if needed.

3. **Train the Model**:
   ```bash
   python train_model.py
   ```
   This will create `gru_resume_model.h5`, `tokenizer.pickle`, and `label_encoder.pickle`.

4. **Run the Application**:
   ```bash
   python app.py
   ```
   Access at `http://127.0.0.1:5000`.

## Architecture
- **Model**: GRU (64 units) + Embedding (64 dim) + SpatialDropout.
- **Preprocessing**: Cleaning, Stopword removal, Tokenization (5000 vocab).
- **Backend**: Flask.

## Optimization for CPU
- Vocab size limited to 5000.
- Sequence length capped at 200.
- Batch size optimized.
