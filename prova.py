import pandas as pd
import os
import uuid

# Specifica il percorso del tuo file CSV
csv_path = r"results.csv"


def count_true_values(csv_path):
    df = pd.read_csv(csv_path, sep=",")

    # Filtra il DataFrame per i valori "True" (case sensitive) nella colonna "Recognized"
    df_filtered = df[df["Recognized"] == True]

    # Calcola il numero di righe nel DataFrame filtrato
    true_count = df_filtered.shape[0]

    # Stampa il conteggio dei valori True trovati
    print("Numero di valori True trovati:", true_count)


def filter_and_save_true_values(csv_path, output_csv_path):
    df = pd.read_csv(csv_path)

    # Filtra il DataFrame per i valori "True" (case sensitive) nella colonna "Recognized"
    df_filtered = df[df["Recognized"] == True]

    # Salva il DataFrame filtrato in un nuovo file CSV
    df_filtered.to_csv(output_csv_path, index=False)


def move_img_from_csv(csv_path):
    df = pd.read_csv(csv_path)

    class_counts = (
        {}
    )

    for index, row in df.iterrows():
        image_path = row["Image Path"]
        predicted_class = row["Predicted Class"]

        # Crea la directory della classe se non esiste già
        class_directory = f"Google_Recaptcha_V2/images/{predicted_class}"
        if not os.path.exists(class_directory):
            os.makedirs(class_directory)

        # Genera un nome univoco per il file immagine
        unique_filename = str(uuid.uuid4()) + os.path.splitext(image_path)[-1]

        # Sposta il file immagine nella directory della classe con il nome univoco
        new_image_path = os.path.join(class_directory, unique_filename)
        os.rename(image_path, new_image_path)

        # Aggiorna il conteggio per la classe corrente
        class_counts[predicted_class] = class_counts.get(predicted_class, 0) + 1

    # Stampa il conteggio per ogni classe
    for class_name, count in class_counts.items():
        print(f"{class_name}: {count}")


# Esegui il conteggio dei valori True
count_true_values(csv_path)

# Filtra i dati e salvali in un nuovo file CSV
filter_and_save_true_values(csv_path, "recognized.csv")

#move_img_from_csv("recognized.csv")
