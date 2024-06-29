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
