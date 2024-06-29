import os
import imageio
import numpy as np
from PIL import Image, ImageSequence

# Function to load a GIF
def load_gif(gif_path):
    return Image.open(gif_path)

# Function to convert text to sign GIFs
def text_to_sign_gifs(text, sign_folder='signs'):
    words = text.split()  # Split text into words
    gifs = []

    for word in words:
        gif_path = os.path.join(sign_folder, f"{word}.gif")
        if os.path.exists(gif_path):
            gifs.append(load_gif(gif_path))
        else:
            print(f"No sign GIF found for: {word}")

    return gifs

# Function to create an MP4 video from a list of GIFs
def create_mp4_video(gifs, output_path='output.mp4', fps=10):
    frames = []
    max_width = 0
    max_height = 0

    # Collect frames and determine maximum dimensions
    for gif in gifs:
        for frame in ImageSequence.Iterator(gif):
            frame_np = np.array(frame.convert("RGB"))
            frames.append(frame_np)
            max_width = max(max_width, frame_np.shape[1])
            max_height = max(max_height, frame_np.shape[0])

    # Resize frames to match maximum dimensions
    resized_frames = []
    for frame_np in frames:
        resized_frame = np.zeros((max_height, max_width, 3), dtype=np.uint8)
        resized_frame[:frame_np.shape[0], :frame_np.shape[1], :] = frame_np
        resized_frames.append(resized_frame)

    if resized_frames:
        # Use imageio to write frames to MP4 video
        writer = imageio.get_writer(output_path, fps=fps)
        for frame_np in resized_frames:
            writer.append_data(frame_np)
        writer.close()
        print(f"Combined MP4 video saved as {output_path}")
    else:
        print("No frames to create an MP4 video.")

# Main function
def main():
    text_file_path = '../speechToText/speechToText.txt'

    try:
        with open(text_file_path, 'r') as file:
            text = file.read().strip()
    except FileNotFoundError:
        print(f"File not found: {text_file_path}")
        return
    except IOError:
        print(f"Error reading file: {text_file_path}")
        return

    sign_gifs = text_to_sign_gifs(text)

    if sign_gifs:
        create_mp4_video(sign_gifs)
    else:
        print("No valid sign GIFs to create a combined MP4 video.")

if __name__ == "__main__":
    main()
