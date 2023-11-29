import numpy as np
from PIL import Image
import os
import pandas as pd
from keras.models import load_model

# Load the trained model
model = load_model("models/best_model.keras")

# Define the class labels (assuming they are in subdirectories)
class_labels = os.listdir("Google_Recaptcha_V2/images")
class_labels.sort()

# Specify the root directory containing subdirectories with images
root_directory = r"/home/deCAPTCHA_2.0/payloads/300x300"

# Create an empty DataFrame to store the results
results_df = pd.DataFrame(
    columns=["Image Path", "Predicted Class", "Accuracy", "Reliability", "Recognized"]
)

# Function to process a chunk of images
def process_image_chunk(image_paths):
    for i, image_path in enumerate(image_paths, start=1):
        img = Image.open(image_path)
        img = img.resize((100, 100))
        img_array = np.array(img) / 255.0

        if img_array.shape[-1] != 3:
            img_array = img_array[:, :, :3]

        predictions = model.predict(np.expand_dims(img_array, axis=0))

        accuracy = predictions[0, np.argmax(predictions)]
        reliability = accuracy > 0.8
        recognized = accuracy == 1.0

        predicted_class_index = np.argmax(predictions)
        predicted_class = class_labels[predicted_class_index]

        # Append the results to the DataFrame
        results_df.loc[len(results_df)] = [
            image_path,
            predicted_class,
            accuracy,
            reliability,
            recognized,
        ]
        
        print(f"Chunk {chunk_number}/{total_images_count // chunk_size}, Images: {i}/{len(image_paths)}")

# Count the total number of images
total_images = []
for subdir, _, files in os.walk(root_directory):
    for file in files:
        image_path = os.path.join(subdir, file)
        if image_path.endswith((".jpg", ".png", ".jpeg")):
            total_images.append(image_path)

# Calculate the chunk size as a fraction of the total images
total_images_count = len(total_images)
chunk_fraction = 0.2
chunk_size = int(total_images_count * chunk_fraction)

# Process images in chunks
for i in range(0, total_images_count, chunk_size):
    image_chunk = total_images[i : i + chunk_size]
    chunk_number = i // chunk_size + 1  # Calculate the chunk number
    print(f"Processing chunk {chunk_number}/{total_images_count // chunk_size}")
    process_image_chunk(image_chunk)
    results_df.to_csv("results.csv", index=False)
    print(f"Processed {len(image_chunk)} images. Results saved to results.csv")

# Save any remaining results to the CSV file
results_df.to_csv("results.csv", index=False)