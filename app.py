import os
import numpy as np
import tensorflow as tf
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences
from resume_parser import parse_resume

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global variables for model
model = None
tokenizer = None
label_encoder = None
MAX_SEQUENCE_LENGTH = 200

def load_artifacts():
    global model, tokenizer, label_encoder
    try:
        model = tf.keras.models.load_model('gru_resume_model.h5')
        print("Model loaded.")
        
        with open('tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)
        print("Tokenizer loaded.")
        
        with open('label_encoder.pickle', 'rb') as handle:
            label_encoder = pickle.load(handle)
        print("Label Encoder loaded.")
        
    except Exception as e:
        print(f"Error loading artifacts: {e}. Ensure model is trained first.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Parse Resume
        parsed_data = parse_resume(filepath)
        cleaned_text = parsed_data['cleaned_text']
        
        if not tokenizer or not model:
            # Try loading again if not loaded (e.g., restart or first run)
            load_artifacts()
            if not tokenizer or not model:
                flash("Model not loaded. Please train the model first.")
                return redirect(url_for('index'))

        # Prepare for prediction
        seq = tokenizer.texts_to_sequences([cleaned_text])
        padded = pad_sequences(seq, maxlen=MAX_SEQUENCE_LENGTH, padding='post', truncating='post')
        
        # Predict
        pred_prob = model.predict(padded)
        pred_class_idx = np.argmax(pred_prob)
        confidence = np.max(pred_prob)
        base_role = label_encoder.inverse_transform([pred_class_idx])[0]
        
        # Refinement & Skill Gap Logic (Delegated to resume_parser)
        from resume_parser import get_sub_role, get_missing_skills
        
        refined_role = get_sub_role(cleaned_text, base_role)
        
        # Check for tags
        tags = []
        text_lower = cleaned_text.lower()
        if 'intern' in text_lower:
            tags.append('Intern')
        if 'freelancer' in text_lower or 'freelance' in text_lower:
            tags.append('Freelancer')
        
        display_role = refined_role
        if tags:
            display_role += f" ({', '.join(tags)})"

        # Skill Gap Analysis
        missing_skills = get_missing_skills(cleaned_text, refined_role)
        
        # Get top 3 predictions
        top_3_indices = np.argsort(pred_prob[0])[-3:][::-1]
        top_3_roles = [
            (label_encoder.inverse_transform([i])[0], float(pred_prob[0][i])) 
            for i in top_3_indices
        ]
        
        return render_template('result.html', 
                               role=display_role, 
                               confidence=f"{confidence*100:.2f}%", 
                               top_roles=top_3_roles,
                               missing_skills=missing_skills,
                               analysis=parsed_data.get('analysis', {}),
                               text_snippet=cleaned_text[:500] + "...")

    return redirect(url_for('index'))

if __name__ == '__main__':
    load_artifacts()
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False) # use_reloader=False to avoid loading model twice
