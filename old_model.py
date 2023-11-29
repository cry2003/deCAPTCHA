import logging
import signal

from preprocessing import train_generator, validation_generator, img_height, img_width
from keras.models import Sequential
from keras.layers import (
    Conv2D,
    MaxPooling2D,
    Flatten,
    Dense,
    ConvLSTM2D,
    Reshape,
    BatchNormalizationV2,
    UnitNormalization,
    Dropout,
)
from keras.callbacks import Callback, ModelCheckpoint, EarlyStopping
from keras.losses import CategoricalCrossentropy
from keras.optimizers import Adam
import tensorflow as tf

# Verifica le GPU disponibili
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)

# Configure the logging
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
            kernel_size=(3, 3),
            activation="relu",
            input_shape=(img_height, img_width, 3),
            padding="same",
        ),
        MaxPooling2D((3, 3), padding="same"),
        BatchNormalizationV2(),
        Conv2D(64, kernel_size=(5, 5), activation="relu", padding="same"),
        MaxPooling2D((5, 5), padding="same"),
        BatchNormalizationV2(),
        Conv2D(128, kernel_size=(5, 5), activation="relu", padding="same"),
        MaxPooling2D((5, 5), padding="same"),
        BatchNormalizationV2(),
        Reshape((1, 6, 6, 64)),
        ConvLSTM2D(
            128,
            kernel_size=(5, 5),
            activation="relu",
            return_sequences=True,
            padding="same",
            dropout=0.2,
        ),
        UnitNormalization(),
        Flatten(),
        Dropout(0.2),
        Dense(256, activation="relu"),
        Dropout(0.2),
        Dense(256, activation="relu"),
        Dense(13, activation="softmax"),
    ]
)

# Compile the model
model.compile(optimizer=Adam(), loss=CategoricalCrossentropy(), metrics=["accuracy"])


# Define a callback to log training information
class TrainingLoggerCallback(Callback):
    def on_epoch_end(self, epoch, logs=None):
        logging.info(
            "Epoch %d - loss: %.4f - accuracy: %.4f - val_loss: %.4f - val_accuracy: %.4f"
            % (
                epoch,
                logs["loss"],
                logs["accuracy"],
                logs["val_loss"],
                logs["val_accuracy"],
            )
        )


# Create an instance of the callback
training_logger_callback = TrainingLoggerCallback()

# Definizione del callback per il checkpoint
checkpoint_callback = ModelCheckpoint(
    "models/best_model.keras",
    monitor="val_loss",
    save_best_only=True,
    mode="min",
    verbose=1,
)

# Definizione del callback per l'early stopping
early_stopping_callback = EarlyStopping(
    monitor="val_loss",
    patience=10,
    verbose=1,
    restore_best_weights=True,
)


def handle_interrupt(signal, frame):
    print("\nInterruption signal received. Saving the model...")
    model.save("models/interrupted_model.keras")
    print("Model saved.")
    exit(0)


signal.signal(signal.SIGINT, handle_interrupt)


# Train the model using data generators
history = model.fit(
    train_generator,
    epochs=200,
    validation_data=validation_generator,
    callbacks=[training_logger_callback, early_stopping_callback, checkpoint_callback],
    batch_size=64,
)
