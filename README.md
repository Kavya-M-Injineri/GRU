# GRU Resume Analyzer & Job Predictor 

> An AI-powered resume analysis tool using a GRU (Gated Recurrent Unit) neural network to predict job roles from resume text with confidence scoring.

---

## Features

- **Multi-format Resume Parsing** — supports PDF, DOCX, TXT, and image files (PNG, JPG via OCR)
- **GRU Neural Inference** — 64-unit GRU with 64-dim embeddings predicts the most likely job role
- **Confidence Scoring** — softmax output gives ranked predictions with percentage confidence
- **Top-K Results** — returns up to 10 alternative role predictions, configurable at runtime
- **Skill Extraction** — identifies and highlights relevant keywords and technologies from the resume
- **Modern UI** — dark neural-aesthetic interface with animated pipeline visualization
- **Flask Backend** — lightweight REST API serving the model at `/predict`
- **CPU Optimized** — vocab limited to 5K, sequence length capped at 200 tokens for fast inference

---

## Project Structure

```
gru-resume-analyzer/
├── app.py                  # Flask server & /predict endpoint
├── train_model.py          # GRU training script
├── resume_parser.py        # Text extraction (PDF, DOCX, TXT, image)
├── requirements.txt        # Python dependencies
├── index.html              # Frontend UI
├── gru_resume_model.h5     # Trained model (generated after training)
├── tokenizer.pickle        # Keras tokenizer (generated after training)
└── label_encoder.pickle    # Sklearn LabelEncoder (generated after training)
```

---

## Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt** includes:

```
tensorflow
flask
pdfplumber
python-docx
pytesseract
pillow
nltk
scikit-learn
pandas
numpy
```

### 2. Install Tesseract OCR *(optional — required for image resumes)*

- **Windows**: Download from [github.com/UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki) and add to PATH
- **Linux**: `sudo apt install tesseract-ocr`
- **macOS**: `brew install tesseract`

If Tesseract is installed in a non-default location on Windows, update `resume_parser.py`:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

### 3. Download NLTK Data

Run once before training or inference:

```python
import nltk
nltk.download('stopwords')
nltk.download('punkt')
```

### 4. Train the Model

```bash
python train_model.py
```

This generates three files in the project root:

| File | Description |
|---|---|
| `gru_resume_model.h5` | Trained Keras GRU model weights |
| `tokenizer.pickle` | Fitted Keras tokenizer (vocab of 5000) |
| `label_encoder.pickle` | Sklearn label encoder for job role classes |

Training uses the **UpdatedResumeDataSet.csv** dataset by default. Place it in the project root or update the path inside `train_model.py`.

### 5. Run the Application

```bash
python app.py
```

Open your browser at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## API Reference

### `POST /predict`

Upload a resume file and receive job role predictions.

**Request** — `multipart/form-data`

| Field | Type | Description |
|---|---|---|
| `resume` | File | Resume file (PDF, DOCX, TXT, PNG, JPG) |

**Response** — `application/json`

```json
{
  "role": "Data Scientist",
  "confidence": 91.4,
  "alternatives": [
    { "role": "Machine Learning Engineer", "score": 5.2 },
    { "role": "Data Analyst", "score": 2.1 }
  ],
  "skills": ["Python", "TensorFlow", "Pandas", "SQL", "Scikit-learn"]
}
```

**Error Response**

```json
{
  "error": "Could not extract text from the uploaded file."
}
```

---

## Model Architecture

```
Input (sequence length: 200)
    │
    ▼
Embedding Layer (vocab: 5000, dim: 64)
    │
    ▼
SpatialDropout1D (rate: 0.3)
    │
    ▼
GRU Layer (units: 64, return_sequences: False)
    │
    ▼
Dense (units: num_classes, activation: softmax)
```

| Hyperparameter | Value |
|---|---|
| Vocabulary size | 5,000 |
| Embedding dimensions | 64 |
| GRU units | 64 |
| Max sequence length | 200 |
| Dropout rate | 0.3 (SpatialDropout) |
| Optimizer | Adam |
| Loss | Sparse Categorical Crossentropy |
| Batch size | 32 |

---

## Text Preprocessing Pipeline

Each resume goes through the following steps before inference:

1. **Extraction** — text pulled from PDF (pdfplumber), DOCX (python-docx), TXT (direct read), or image (pytesseract OCR)
2. **Cleaning** — lowercased, special characters removed, extra whitespace stripped
3. **Stopword removal** — NLTK English stopwords filtered out
4. **Tokenization** — Keras tokenizer converts words to integer sequences
5. **Padding** — sequences padded/truncated to max length of 200
6. **Inference** — padded sequence fed to GRU model, softmax output decoded via label encoder

---

## CPU Optimization Notes

This model is designed to run efficiently on CPU-only machines:

- Vocabulary capped at **5,000** tokens (reduces embedding lookup cost)
- Sequences truncated at **200 tokens** (reduces recurrent computation)
- GRU preferred over LSTM (fewer gate operations, faster on CPU)
- Batch size of **32** balances memory usage and throughput
- No GPU-specific ops — runs cleanly on standard laptops

---

## Supported Job Roles

The model is trained to classify resumes into categories including (but not limited to):

Data Science, Machine Learning, Web Development, Android, iOS, DevOps, Database, HR, Advocate, Arts, Health and Fitness, Civil Engineer, Java Developer, Business Analyst, SAP Developer, Automation Testing, ETL Developer, Operations Manager, Python Developer, Blockchain, Network Security Engineer

Exact classes depend on the training dataset used.

---

## Frontend Integration

The included `index.html` UI communicates with the Flask backend via a simple fetch call:

```javascript
const formData = new FormData();
formData.append('resume', file);

const res = await fetch('/predict', { method: 'POST', body: formData });
const data = await res.json();

console.log(data.role);       // "Data Scientist"
console.log(data.confidence); // 91.4
```

The UI supports drag-and-drop upload, configurable model parameters (sequence length, dropout, top-K), step-by-step loading animation, and animated confidence bars.

---

## Troubleshooting

**Model file not found**
Run `python train_model.py` first. The `.h5`, tokenizer, and label encoder files must exist before starting `app.py`.

**PDF text extraction returns empty**
Some PDFs are image-based. Install Tesseract OCR and ensure `pytesseract` is configured correctly in `resume_parser.py`.

**Low prediction confidence**
The resume may use uncommon formatting or domain-specific jargon not well represented in the training set. Try cleaning the resume to plain text first.

**TensorFlow import errors on Windows**
Ensure you are using Python 3.8–3.11. TensorFlow does not support Python 3.12+ on Windows as of TF 2.x.

---

## License

MIT License. Free to use, modify, and distribute.
