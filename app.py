from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import numpy as np
import joblib
import re
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = FastAPI(title="Cyberbullying Detection API")

model = tf.keras.models.load_model('models/lstm_model.h5')
tokenizer = joblib.load('models/lstm_tokenizer.pkl')
le = joblib.load('models/label_encoder.pkl')

MAX_LEN = 100

# Peta karakter leetspeak & simbol ke huruf asli
LEET_MAP = {
    "0": "o",
    "1": "i",
    "!": "i",
    "3": "e",
    "€": "e",
    "4": "a",
    "@": "a",
    "^": "a",
    "5": "s",
    "$": "s",
    "ß": "s",
    "7": "t",
    "+": "t",
    "†": "t",
    "8": "b",
    "6": "g",
    "9": "g",
    "q": "g",  # q sering dipakai sebagai g
    "2": "z",
    "z": "z",
    "(": "c",
    "<": "c",
    "{": "c",
    "[": "c",
    ")": "d",
    "}": "d",
    "ø": "o",
    "°": "o",
    "*": "",   # hapus asterisk (f*ck -> fck)
    "_": "",   # hapus underscore
    "-": "",   # hapus dash antar huruf
    ".": "",   # hapus titik antar huruf
    ",": "",   # hapus koma antar huruf
}

def normalize_leetspeak(text: str) -> str:
    result = []
    for char in text.lower():
        result.append(LEET_MAP.get(char, char))
    return ''.join(result)

def remove_repeated_chars(text: str) -> str:
    # niiiggger -> nigger (max 2 karakter berulang)
    return re.sub(r'(.)\1{2,}', r'\1\1', text)

def clean_text(text: str) -> str:
    text = str(text).lower()
    text = normalize_leetspeak(text)         # n1gg3r -> nigger
    text = remove_repeated_chars(text)       # niiiigger -> niigger
    text = re.sub(r'http\S+', '', text)      # hapus URL
    text = re.sub(r'@\w+', '', text)         # hapus mention
    text = re.sub(r'#\w+', '', text)         # hapus hashtag
    text = re.sub(r'[^a-z0-9\s]', '', text) # hapus karakter aneh sisa
    text = re.sub(r'\s+', ' ', text).strip() # rapikan spasi
    return text

class TextInput(BaseModel):
    text: str

@app.get("/")
def root():
    return FileResponse("index.html")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(input: TextInput):
    cleaned = clean_text(input.text)
    seq = tokenizer.texts_to_sequences([cleaned])
    padded = pad_sequences(seq, maxlen=MAX_LEN, padding='post', truncating='post')

    proba_all = model.predict(padded)[0]
    pred = np.argmax(proba_all)
    confidence = float(np.max(proba_all))
    label = le.inverse_transform([pred])[0]

    # Threshold: kalau model tidak yakin & prediksi not_cyberbullying, flag sebagai cyberbullying
    if confidence < 0.60 and label == "not_cyberbullying":
        label = "other_cyberbullying"
        is_cyber = True
    else:
        is_cyber = label != "not_cyberbullying"

    return {
        "input_text": input.text,
        "cleaned_text": cleaned,       # tampilkan teks setelah normalisasi
        "prediction": label,
        "confidence": f"{round(confidence * 100, 2)}%",
        "is_cyberbullying": is_cyber
    }