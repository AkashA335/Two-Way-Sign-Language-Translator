# Real-Time Two-Way Sign Language Translator 🤟🔊

- Develops a system using MediaPipe, CannyEdge, and OpenCV for real-time gesture recognition.
- Translates sign language gestures into text and vice versa, enhancing communication between hearing and deaf individuals.

## Speech To Sign 🎤🗣️📜

- Records audio with PyAudio.
- Converts audio to text using Whisper AI.
- Translates text into sign language gestures using a dataset of GIFs converted to MP4 format.

## Sign To Speech 📹🧠🔊

- Uses a webcam to capture sign language gestures.
- Processes gestures with MediaPipe and Canny edge detection to interpret them into text.
- Converts interpreted text into speech using gTTS for real-time translation from sign language to spoken language.

### Enhanced Communication Accessibility 🌐

- Focuses on enhancing accessibility through real-time translation across audio, text, and sign language.

### Neural Network for Gesture Prediction 🤖

- Leverages a trained neural network for accurate gesture prediction in sign language interpretation.

### Bridging Communication Gap 🌍

- Aims to bridge the communication gap between sign language users and non-sign language speakers.

### Facilitating Seamless Communication 🔄

- Enables seamless communication by providing real-time translation capabilities for improved accessibility.


# Installation Process 🛠️

## Global 🌐

### Step 1: Create an environment named `.env` 📝

This will be the Global environment used for:
- Recording Audio 🎤
- Speech To Text 🗣️
- Text To Speech 📢

## Speech To Sign 🤟

### Step 2: Install Requirements of "Record Audio" and Run it 🎧

### Step 3: Install Requirements of "Speech To Text" and Run it 🔊

### Step 4: Install Requirements of "Text To Sign" and Run it 📜

## Sign To Speech 📝➡️🔊

There are Two models in Sign To Text, one is using MediaPipe (for Action/Gestures) another is CannyEdge (for Alphabets and numbers).

### Step 5: Create an environment named `.venv` inside "Action To Text" 🖼️

### Step 6: Install Requirements of "Action To Text" and Run it in the following Order:
1. `collectImages.py` 📸
2. `modelTrain.py` 🚂
3. `realTimeTest.py` 🕒

### Step 7: Create an environment named `.venv` inside "Alnum Sign To Text" 🏷️

### Step 8: Install Requirements of "Alnum Sign To Text" and Run it in the following Order:
1. `imageCollection.py` 📷
2. `createDataset.py` 📊
3. `modelTraining.py` 🏋️‍♂️
4. `modelInference.py` 🧠

These two will have a common `output.txt` which we will use later.

### Step 9: Install Requirements of "Text To Speech" and Run it 🔊
