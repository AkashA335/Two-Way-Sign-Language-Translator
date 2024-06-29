import whisper

# Load the model and specify to use GPU if available
model = whisper.load_model("base").to("cuda")

# Transcribe the audio file
result = model.transcribe("../RecordAudio/recordedAudio.wav")

# Write the transcription to a file
with open("speechToText.txt", "w") as f:
    f.write(result["text"])

# Define the translation table to replace specific characters with spaces
replace_chars = ",.!/\"\\{}()*&^%$#@!"
translation_table = str.maketrans(replace_chars, " " * len(replace_chars))

# Read the transcription, apply the translation table, and write it back
with open("speechToText.txt", "r") as f:
    text = f.read()

# Clean the text by applying the translation table
clean_text = text.translate(translation_table)

# Handle hyphens between words (e.g., step-sister -> stepsister)
clean_text = clean_text.replace("-", "")

# Write the cleaned text back to the file
with open("speechToText.txt", "w") as f:
    f.write(clean_text)

