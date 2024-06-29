import os
import cv2
import numpy as np
import pickle
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Function to load images from directory
def load_images_from_folder(folder):
    images = []
    labels = []
    class_names = sorted(os.listdir(folder))  # Get sorted list of subdirectories
    for class_name in class_names:
        class_path = os.path.join(folder, class_name)
        if os.path.isdir(class_path):  # Ensure it's a directory
            for filename in os.listdir(class_path):
                img_path = os.path.join(class_path, filename)
                img = cv2.imread(img_path)
                if img is not None:
                    img = cv2.resize(img, (100, 100))  # Resize image to 100x100 pixels
                    images.append(img)
                    labels.append(class_name)  # Assign label as class name
    return np.array(images), np.array(labels), class_names

# Function to augment and save images
def augment_and_save_images(images, labels, path, class_names):
    datagen = ImageDataGenerator(
        rotation_range=10,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    for idx, (image, label) in enumerate(zip(images, labels)):
        save_dir = os.path.join(path, label)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        image = np.expand_dims(image, 0)
        i = 0
        for batch in datagen.flow(image, batch_size=1, save_to_dir=save_dir, save_prefix=label, save_format='jpg'):
            i += 1
            if i >= 10:  # Save 10 augmented images per original image
                break

# Path to your dataset directory
dataset_path = 'data'

# Load images and labels
images, labels, class_names = load_images_from_folder(dataset_path)

# Augment and save images
augment_and_save_images(images, labels, dataset_path, class_names)

# Create a directory named 'pickle' if it doesn't exist
pickle_folder = 'pickle'
if not os.path.exists(pickle_folder):
    os.makedirs(pickle_folder)

# Save images and labels using pickle in the 'pickle' folder
with open(os.path.join(pickle_folder, 'dataset_images.pkl'), 'wb') as f:
    pickle.dump(images, f)

with open(os.path.join(pickle_folder, 'dataset_labels.pkl'), 'wb') as f:
    pickle.dump(labels, f)

# Save the class names using pickle
with open(os.path.join(pickle_folder, 'class_names.pkl'), 'wb') as f:
    pickle.dump(class_names, f)

print("Dataset images, labels, and class names saved successfully in the 'pickle' folder.")
