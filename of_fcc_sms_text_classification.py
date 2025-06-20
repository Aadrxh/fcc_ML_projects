# -*- coding: utf-8 -*-
"""of fcc_sms_text_classification.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Y7U-i_DrLNYkF1obvD4BfFvAvk6dRd91
"""

# import libraries

import tensorflow as tf
import pandas as pd
from tensorflow import keras
!pip install tensorflow-datasets
import tensorflow_datasets as tfds
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Embedding, Dense,Dropout,GlobalAveragePooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# get data files
!wget https://cdn.freecodecamp.org/project-data/sms/train-data.tsv
!wget https://cdn.freecodecamp.org/project-data/sms/valid-data.tsv

train_file_path = "train-data.tsv"
test_file_path = "valid-data.tsv"

test_data = pd.read_csv(test_file_path, sep="\t", names=["class", "text"])
train_data = pd.read_csv(train_file_path, sep="\t", names=["class", "text"])

print(train_data)

train_text = train_data["text"].values.tolist()
train_label = np.array([0 if x=="ham" else 1 for x in train_data['class'].values.tolist()])
test_text = test_data["text"].values.tolist()
test_label = np.array([0 if x=="ham" else 1 for x in test_data['class'].values.tolist()])
print(train_text)
print(train_label)

vocabulary_dict = {}
for messgae in train_text:
  for vocabulary in messgae.split():
    if vocabulary not in vocabulary_dict:
      vocabulary_dict[vocabulary] = 1
    else:
      vocabulary_dict[vocabulary] += 1

print(vocabulary_dict)
VOCAB_SIZE = len(vocabulary_dict)
MAX_LENGTH = max(len(msg.split()) for msg in train_text)

tokenizer = Tokenizer(num_words=VOCAB_SIZE, oov_token="<OOV>")
tokenizer.fit_on_texts(train_text)
encoded_train = tokenizer.texts_to_sequences(train_text)
padded_train = pad_sequences(encoded_train, padding='post', truncating='post')
encoded_test = tokenizer.texts_to_sequences(test_text)
padded_test = pad_sequences(encoded_test, padding='post',truncating='post')

model = Sequential([
    Embedding(VOCAB_SIZE, 16, input_length=MAX_LENGTH),
    GlobalAveragePooling1D(),
    Dense(16, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.fit(padded_train, train_label,batch_size=32,validation_data=(padded_test, test_label),epochs=10, verbose=1)

# function to predict messages based on model
# (should return list containing prediction and label, ex. [0.008318834938108921, 'ham'])
def predict_message(pred_text):
    class_dict = {
        0: "ham",
        1: "spam",
    }

    encoded_pred = tokenizer.texts_to_sequences([pred_text])
    padded_pred = pad_sequences(encoded_pred, padding='post',truncating='post')

    prediction = model.predict(padded_pred)[0][0]

    return [prediction, class_dict[np.round(prediction)]]

# Run this cell to test your function and model. Do not modify contents.
def test_predictions():
  test_messages = ["how are you doing today",
                   "sale today! to stop texts call 98912460324",
                   "i dont want to go. can we try it a different day? available sat",
                   "our new mobile video service is live. just install on your phone to start watching.",
                   "you have won £1000 cash! call to claim your prize.",
                   "i'll bring it tomorrow. don't forget the milk.",
                   "wow, is your arm alright. that happened to me one time too"
                  ]

  test_answers = ["ham", "spam", "ham", "spam", "spam", "ham", "ham"]
  passed = True

  for msg, ans in zip(test_messages, test_answers):
    prediction = predict_message(msg)
    if prediction[1] != ans:
      passed = False

  if passed:
    print("You passed the challenge. Great job!")
  else:
    print("You haven't passed yet. Keep trying.")

test_predictions()