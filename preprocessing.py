from keras.preprocessing.image import ImageDataGenerator
from utilss import duplicate
# Definisci il percorso della cartella con le immagini
data_dir = "Google_Recaptcha_V2/images"

# Specifica le dimensioni delle immagini e il batch size
img_height = 100
img_width = 100
batch_size = 128

print("Removing duplicates...\n")
duplicate.remove_duplicates(data_dir)

# Crea un generatore di dati per il training
train_datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    validation_split=0.2,
    horizontal_flip=True,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    fill_mode="nearest",
    
)

# Crea i generatori di dati per il training e la validation
train_generator = train_datagen.flow_from_directory(
    data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode="categorical",
    subset="training",
)

validation_generator = train_datagen.flow_from_directory(
    data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode="categorical",
    subset="validation",
)