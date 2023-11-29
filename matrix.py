import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
from itertools import product
from keras.models import load_model
from preprocessing import train_generator, validation_generator

# Load the saved model
saved_model_path = r"C:\Users\ChristianVillani\Downloads\deCAPTCHA_2.0\models\best_model.keras"
loaded_model = load_model(saved_model_path)

# Generate predictions for the validation set
validation_predictions = loaded_model.predict(validation_generator)

# Get true labels for the validation set
true_labels = validation_generator.labels

# Convert predictions and true labels to class labels
predicted_labels = np.argmax(validation_predictions, axis=1)

# Calculate the confusion matrix
conf_matrix = confusion_matrix(true_labels, predicted_labels)

# Display the confusion matrix
plt.figure(figsize=(10, 8))
plt.imshow(conf_matrix, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('Confusion Matrix')
plt.colorbar()

# Add class labels to axes
classes = list(validation_generator.class_indices.keys())
tick_marks = np.arange(len(classes))
plt.xticks(tick_marks, classes, rotation=45)
plt.yticks(tick_marks, classes)

# Add text annotations
for i, j in product(range(conf_matrix.shape[0]), range(conf_matrix.shape[1])):
    plt.text(j, i, format(conf_matrix[i, j], 'd'),
             horizontalalignment="center",
             color="white" if conf_matrix[i, j] > conf_matrix.max() / 2. else "black")

plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.tight_layout()
plt.show()

# Display classification report
print("Classification Report:")
print(classification_report(true_labels, predicted_labels, target_names=classes))
