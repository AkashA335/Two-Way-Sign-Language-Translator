import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import queue
import threading
import sys
import time
import tkinter as tk

# Configuration
fs = 44100  # Sample rate
channels = 2  # Number of channels
volume_factor = 2.0  # Volume increase factor
output_filename = 'recordedAudio.wav'
blocksize = 2048  # Increased block size

# Queue to hold audio blocks
audio_queue = queue.Queue()
recording = threading.Event()
stop_event = threading.Event()

# Function to process audio blocks
def audio_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    # Put the audio block into the queue
    audio_queue.put(indata.copy())

# Function to write audio blocks to file
def audio_writer():
    all_data = []
    try:
        while not stop_event.is_set():
            try:
                block = audio_queue.get(timeout=1)
                # Increase volume
                block *= volume_factor
                # Clip the values to the range [-1.0, 1.0]
                block = np.clip(block, -1.0, 1.0)
                all_data.append(block)
            except queue.Empty:
                continue
    finally:
        if all_data:
            # Save all recorded data to a file
            all_data = np.concatenate(all_data, axis=0)
            write(output_filename, fs, (all_data * np.iinfo(np.int16).max).astype(np.int16))

def start_recording():
    if recording.is_set():
        return
    recording.set()
    stop_event.clear()
    start_time = time.time()

    def recording_thread():
        # Start the audio stream
        stream = sd.InputStream(samplerate=fs, channels=channels, callback=audio_callback, blocksize=blocksize, latency='high')
        with stream:
            writer_thread = threading.Thread(target=audio_writer)
            writer_thread.start()
            while not stop_event.is_set():
                elapsed_time = time.time() - start_time
                elapsed_time_var.set(f"Recording duration: {int(elapsed_time)} seconds")
                time.sleep(1)
            audio_queue.put(None)
            writer_thread.join()

    threading.Thread(target=recording_thread).start()

def stop_recording():
    if not recording.is_set():
        return
    recording.clear()
    stop_event.set()

# Create GUI
root = tk.Tk()
root.title("Audio Recorder")

start_button = tk.Button(root, text="Start Recording", command=start_recording)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Recording", command=stop_recording)
stop_button.pack(pady=10)

elapsed_time_var = tk.StringVar()
elapsed_time_label = tk.Label(root, textvariable=elapsed_time_var)
elapsed_time_label.pack(pady=10)

root.mainloop()