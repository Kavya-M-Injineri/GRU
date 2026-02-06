import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, GRU, Dense, Dropout, SpatialDropout1D
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle
import os
from utils import clean_text

# Architecture Config
VOCAB_SIZE = 10000  # Increased for better coverage
EMBEDDING_DIM = 128
MAX_SEQUENCE_LENGTH = 300 # Longer context
GRU_UNITS = 128
BATCH_SIZE = 32 # Smaller batch for more updates per epoch
EPOCHS = 20

def load_and_preprocess_data(csv_path):
    print("Loading dataset...")
    df = pd.read_csv(csv_path)
    
    # Drop NAs
    df.dropna(subset=['Resume_str', 'Category'], inplace=True)
    
    print(f"Dataset size: {len(df)}")
    
    # Clean text
    print("Cleaning text...")
    df['Cleaned_Resume'] = df['Resume_str'].apply(clean_text)
    
    return df

def train_model():
    csv_path = os.path.join('archive', 'Resume', 'Resume.csv')
    if not os.path.exists(csv_path):
        # Fallback to current dir if not in archive/Resume
        csv_path = 'Resume.csv'
        if not os.path.exists(csv_path):
            print(f"Error: Dataset not found. Checked default locations.")
            return

    df = load_and_preprocess_data(csv_path)

    # Encode Labels
    le = LabelEncoder()
    df['Category_Label'] = le.fit_transform(df['Category'])
    num_classes = len(le.classes_)
    
    # Save LabelEncoder
    with open('label_encoder.pickle', 'wb') as handle:
        pickle.dump(le, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # Tokenizer
    print("Tokenizing...")
    tokenizer = Tokenizer(num_words=VOCAB_SIZE, oov_token='<OOV>')
    tokenizer.fit_on_texts(df['Cleaned_Resume'])
    
    sequences = tokenizer.texts_to_sequences(df['Cleaned_Resume'])
    padded_sequences = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH, padding='post', truncating='post')
    
    # Save Tokenizer
    with open('tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # Split Data
    X_train, X_test, y_train, y_test = train_test_split(padded_sequences, df['Category_Label'], test_size=0.2, random_state=42)

    # Build Model
    print("Building Optimized GRU Model...")
    model = Sequential([
        Embedding(VOCAB_SIZE, EMBEDDING_DIM, input_length=MAX_SEQUENCE_LENGTH),
        SpatialDropout1D(0.3),
        tf.keras.layers.Bidirectional(GRU(GRU_UNITS, dropout=0.2)),
        Dense(128, activation='relu'),
        Dropout(0.3),
        Dense(num_classes, activation='softmax')
    ])

    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.summary()

    # Early Stopping
    early_stop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

    # Train
    print("Starting Training...")
    history = model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=[early_stop]
    )

    # Evaluate
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"Test Accuracy: {accuracy*100:.2f}%")

    # Save Model
    model.save('gru_resume_model.h5')
    print("Model saved as gru_resume_model.h5")

if __name__ == "__main__":
    train_model()
