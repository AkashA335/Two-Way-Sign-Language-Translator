import os
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Function to load pickled data
def load_pickled_data(pickle_folder):
    with open(os.path.join(pickle_folder, 'dataset_images.pkl'), 'rb') as f:
        images = pickle.load(f)
    
    with open(os.path.join(pickle_folder, 'dataset_labels.pkl'), 'rb') as f:
        labels = pickle.load(f)
    
    return images, labels

# Path to the pickle directory
pickle_folder = 'pickle'

# Load images and labels
images, labels = load_pickled_data(pickle_folder)

# Normalize images (assuming images are uint8)
images = images.astype('float32') / 255.0

# Convert labels from class names to integers
label_encoder = LabelEncoder()
labels = label_encoder.fit_transform(labels)

# Convert labels to categorical
num_classes = len(label_encoder.classes_)
labels = tf.keras.utils.to_categorical(labels, num_classes=num_classes)

# Split data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(images, labels, test_size=0.2, random_state=42)

# Define the model architecture
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(100, 100, 3))
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.5)(x)
predictions = Dense(num_classes, activation='softmax')(x)
model = Model(inputs=base_model.input, outputs=predictions)

# Freeze the base model layers
for layer in base_model.layers:
    layer.trainable = False

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Unfreeze some layers and fine-tune
for layer in base_model.layers[-20:]:
    layer.trainable = True

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5), loss='categorical_crossentropy', metrics=['accuracy'])

# Real-time data augmentation
datagen = ImageDataGenerator(
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Train the model with data augmentation
history = model.fit(datagen.flow(X_train, y_train, batch_size=32), 
                    epochs=20, 
                    validation_data=(X_val, y_val))

# Save the trained model
model.save('./model/sign_language_model.h5')

# Save the label encoder
with open(os.path.join(pickle_folder, 'label_encoder.pkl'), 'wb') as f:
    pickle.dump(label_encoder, f)

print("Model trained and saved as 'sign_language_model.h5'")
print("Label encoder saved as 'label_encoder.pkl'")
