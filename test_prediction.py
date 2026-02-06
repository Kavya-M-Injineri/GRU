import os
import numpy as np
import tensorflow as tf
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences
from resume_parser import parse_resume

def test_prediction(resume_path):
    print(f"Testing prediction for: {resume_path}")
    
    # Load artifacts
    try:
        model = tf.keras.models.load_model('gru_resume_model.h5')
        with open('tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)
        with open('label_encoder.pickle', 'rb') as handle:
            label_encoder = pickle.load(handle)
        print("Model and artifacts loaded.")
    except Exception as e:
        print(f"Error loading model or artifacts: {e}")
        return

    # Parse resume
    parsed_data = parse_resume(resume_path)
    cleaned_text = parsed_data['cleaned_text']
    print(f"Parsed text (first 100 chars): {cleaned_text[:100]}...")

    # Predict
    MAX_SEQUENCE_LENGTH = 200
    seq = tokenizer.texts_to_sequences([cleaned_text])
    padded = pad_sequences(seq, maxlen=MAX_SEQUENCE_LENGTH, padding='post', truncating='post')
    
    pred_prob = model.predict(padded)
    pred_class_idx = np.argmax(pred_prob)
    predicted_role = label_encoder.inverse_transform([pred_class_idx])[0]
    confidence = np.max(pred_prob)

    print(f"\n--- Prediction Results ---")
    print(f"Predicted Role: {predicted_role}")
    print(f"Confidence: {confidence*100:.2f}%")
    
    # Top 3
    top_3_indices = np.argsort(pred_prob[0])[-3:][::-1]
    print("\nTop 3 Suggestions:")
    for i in top_3_indices:
        role = label_encoder.inverse_transform([i])[0]
        prob = pred_prob[0][i]
        print(f"- {role}: {prob*100:.2f}%")

if __name__ == "__main__":
    resume_path = os.path.join('uploads', 'Raghav_Resume_1_1.pdf')
    if os.path.exists(resume_path):
        test_prediction(resume_path)
    else:
        print(f"Resume not found at {resume_path}")
