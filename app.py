from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk import WordNetLemmatizer
import string
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)

model = load_model("spam.h5")
tokenizer = pickle.load(open("tokenizer.pkl", "rb"))

stop_words = set(stopwords.words("english"))
maxlen = 411

def clean(text):
    text = re.sub(r"[^\w\s]", "", text)
    text = text.lower()
    text = re.sub(r"\d+", "", text)
    text = " ".join([word for word in text.split() if word not in stop_words])
    lemmatizer = WordNetLemmatizer()
    text = " ".join([lemmatizer.lemmatize(word) for word in text.split()])
    text = text.strip()
    return text

@app.route("/check-spam", methods=["POST"])
def check_spam():
    content = request.json["content"]

    context_clean = clean(content)
    test = tokenizer.texts_to_sequences([context_clean])
    test = pad_sequences(test, maxlen=maxlen)
    is_spam = model.predict(test)
    is_spam = np.round(is_spam)[0][0]

    if is_spam == 1.0:
        result = {"spam": True}
    else:
        result = {"spam": False}

    print(result)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)