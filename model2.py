import logging
import signal
import os
import numpy as np

from preprocessing import train_generator, validation_generator, img_height, img_width
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Conv2D,
    MaxPooling2D,
    Flatten,
    Dense,
    BatchNormalization,
    Dropout,
    Activation,
)
from tensorflow.keras.callbacks import Callback, ModelCheckpoint, EarlyStopping
from tensorflow.keras.losses import CategoricalCrossentropy
from tensorflow.keras.optimizers import Adam

import tensorflow as tf


# Verify GPU availability
gpus = tf.config.experimental.list_physical_devices("GPU")
if gpus:
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)

# Configure logging
logging.basicConfig(
    filename="training.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Define the CNN model
model = Sequential(
    [
        Conv2D(
            32,
            kernel_size=(5, 5),
            activation="relu",
            input_shape=(img_height, img_width, 3),
            padding="same",
        ),
        Conv2D(
            32,
            kernel_size=(5, 5),
            activation="relu",
            padding="same",
        ),
        MaxPooling2D((3, 3), padding="same"),
        # Block 0
        Conv2D(
            64,
            kernel_size=(5, 5),
            activation="relu",
            padding="same",
        ),
        Conv2D(
            64,
            kernel_size=(5, 5),
            activation="relu",
            padding="same",
        ),
        BatchNormalization(),
        MaxPooling2D((3, 3), padding="same"),
        # Dropout(0.2),
        # Block 1
        Conv2D(
            128,
            kernel_size=(3, 3),
            activation="relu",
            padding="same",
        ),
        Conv2D(
            128,
            kernel_size=(3, 3),
            activation="relu",
            padding="same",
        ),
        BatchNormalization(),
        MaxPooling2D((3, 3), padding="same"),
        # Dropout(0.2),
        # Block 2
        Conv2D(
            256,
            kernel_size=(3, 3),
            activation="relu",
            padding="same",
        ),
        Conv2D(
            256,
            kernel_size=(3, 3),
            activation="relu",
            padding="same",
        ),
        BatchNormalization(),
        MaxPooling2D((3, 3), padding="same"),
        # Dropout(0.2),
        # Block 3
        Conv2D(
            512,
            kernel_size=(3, 3),
            activation="relu",
            padding="same",
        ),
        Conv2D(
            512,
            kernel_size=(3, 3),
            activation="relu",
            padding="same",
        ),
        BatchNormalization(),
        MaxPooling2D((3, 3), padding="same"),
        # Dropout(0.2),
        # Block 4
        Conv2D(
            1024,
            kernel_size=(3, 3),
            activation="relu",
            padding="same",
        ),
        Conv2D(
            1024,
            kernel_size=(3, 3),
            activation="relu",
            padding="same",
        ),
        BatchNormalization(),
        MaxPooling2D((3, 3), padding="same"),
        # Dropout(0.2),
        # Flatten
        Flatten(),
        Dense(2048, activation="relu"),
        # Dropout(0.2),
        Dense(2048, activation="relu"),
        # Dropout(0.2),
        Dense(13, activation="softmax"),
    ]
)

if os.path.exists(r"models/best_model.keras"):
    print("Loading model weights from checkpoint file...")
    model.load_weights(r"models/best_model.keras")
    print("Model weights loaded.")

# Compile the model
model.compile(optimizer=Adam(), loss=CategoricalCrossentropy(), metrics=["accuracy"])

model.summary()


# Define a callback to log training information
class TrainingLoggerCallback(Callback):
    def on_epoch_end(self, epoch, logs=None):
        logging.info(
            "Epoch %d - loss: %.4f - accuracy: %.4f - val_loss: %.4f - val_accuracy: %.4f"
            % (
                epoch + 1,
                logs["loss"],
                logs["accuracy"],
                logs["val_loss"],
                logs["val_accuracy"],
            )
        )


# Create an instance of the training logger callback
training_logger_callback = TrainingLoggerCallback()

# Define the callback for model checkpointing
checkpoint_callback = ModelCheckpoint(
    "models/best_model.keras",
    monitor="val_loss",
    save_best_only=True,
    mode="min",
    verbose=1,
)

# Define the callback for early stopping
early_stopping_callback = EarlyStopping(
    monitor="val_loss",
    patience=5,
    verbose=1,
    restore_best_weights=True,
)


# Define a function to handle interruption signals (e.g., Ctrl+C)
def handle_interrupt(signal, frame):
    print("\nInterruption signal received. Saving the model...")
    model.save("models/interrupted_model.keras")
    print("Model saved.")
    exit(0)


# Register the interrupt signal handler
signal.signal(signal.SIGINT, handle_interrupt)

# Train the model using data generators
history = model.fit(
    train_generator,
    epochs=100,
    validation_data=validation_generator,
    callbacks=[training_logger_callback, early_stopping_callback, checkpoint_callback],
    batch_size=128,
)
