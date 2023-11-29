import numpy as np
from PIL import Image
import os
import pandas as pd
from keras.models import load_model


# Load the trained model
model = load_model("models/best_model.keras")

# Define the class labels (assuming they are in subdirectories)
class_labels = os.listdir("Google_Recaptcha_V2/images")

# Specify the root directory containing subdirectories with images
root_directory = r"/home/deCAPTCHA_2.0/payloads/300x300"

# Create an empty DataFrame to store the results
results_df = pd.DataFrame(columns=["Image Path", "Predicted Class", "Accuracy", "Reliability", "Recognized"])

# Function to recursively process images in subdirectories and append results to the DataFrame
def process_images_in_directory(directory):
    for subdir, _, files in os.walk(directory):
        for file in files:
            image_path = os.path.join(subdir, file)
            if image_path.endswith((".jpg", ".png", ".jpeg")):
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
                results_df.loc[len(results_df)] = [image_path, predicted_class, accuracy, reliability, recognized]

# Call the function to process images in the root directory and its subdirectories
process_images_in_directory(root_directory)

# Save the DataFrame to a CSV file
results_df.to_csv("results.csv", index=False)
