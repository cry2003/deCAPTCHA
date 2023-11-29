import cv2
import os
import shutil
import zipfile
import logging
from tqdm import tqdm


def clust(debug=True):
    # Definisci una funzione per ottenere le dimensioni di un'immagine
    def get_image_dimensions(image_path):
        img = cv2.imread(image_path)
        height, width, _ = img.shape
        return (height, width)

    # Definisci una funzione per estrarre file ZIP in modo ricorsivo
    def extract_recursive_zip(zip_file, extract_path):
        with zipfile.ZipFile(zip_file, "r") as zip_ref:
            zip_ref.extractall(extract_path)
            for file_info in zip_ref.infolist():
                if file_info.is_dir():
                    extract_recursive_zip(
                        os.path.join(extract_path, file_info.filename), extract_path
                    )

    def remove_articles(text):
        articles = [
            "a",
            "an",
            "the",
            "this",
            "that",
            "these",
            "those",
            "my",
            "your",
            "his",
            "her",
            "its",
            "our",
            "their",
        ]
        words = text.split()
        cleaned_words = [word for word in words if word.lower() not in articles]
        return " ".join(cleaned_words)

    # Cartella contenente le tue immagini e file ZIP
    cartella_immagini = "payloads/scraps"

    # Cartella di destinazione per i gruppi di immagini
    cartella_destinazione = "payloads"

    # Creare un dizionario per raggruppare le immagini in base alle dimensioni e ai nomi
    dimensioni_e_nomi_immagini = {}

    # Continua a cercare e estrarre file ZIP in modo ricorsivo
    while True:
        found_zip = False
        for root, dirs, files in os.walk(cartella_immagini):
            for file in files:
                if file.endswith(".zip"):
                    zip_file_path = os.path.join(root, file)
                    extract_recursive_zip(zip_file_path, root)
                    os.remove(zip_file_path)  # Rimuovi il file ZIP dopo l'estrazione
                    found_zip = True

        if not found_zip:
            break  # Se non ci sono più file ZIP, esci dal ciclo

    # Ottieni la lista di immagini nella cartella
    immagini = [
        filename
        for filename in os.listdir(cartella_immagini)
        if filename.endswith((".jpg", ".png", ".jpeg"))
    ]

    # Crea una barra di avanzamento
    with tqdm(
        total=len(immagini), desc="Elaborazione immagini", disable=not debug
    ) as pbar:
        # Scansiona la cartella delle immagini
        for filename in immagini:
            cleaned_filename = remove_articles(
                os.path.splitext(os.path.basename(filename))[0]
            )
            image_path = os.path.join(cartella_immagini, filename)
            dimensions = get_image_dimensions(image_path)
            name = cleaned_filename.split("-")[0]

            # Utilizza le dimensioni e il nome come chiave nel dizionario
            key = (dimensions, name)
            if key in dimensioni_e_nomi_immagini:
                dimensioni_e_nomi_immagini[key].append(image_path)
            else:
                dimensioni_e_nomi_immagini[key] = [image_path]

            # Aggiorna la barra di avanzamento
            pbar.update(1)

    # Creare le cartelle di destinazione basate sulle dimensioni e nomi
    for dimensions, name in dimensioni_e_nomi_immagini.keys():
        folder_name = f"{dimensions[0]}x{dimensions[1]}/{name}"
        os.makedirs(os.path.join(cartella_destinazione, folder_name), exist_ok=True)

    # Sposta le immagini nei gruppi di cartelle corrispondenti
    for (dimensions, name), image_list in dimensioni_e_nomi_immagini.items():
        folder_name = f"{dimensions[0]}x{dimensions[1]}/{name}"
        for image_path in image_list:
            shutil.move(
                image_path,
                os.path.join(
                    cartella_destinazione, folder_name, os.path.basename(image_path)
                ),
            )
    if debug:
        print("Immagini suddivise nelle cartelle corrispondenti per dimensione e nome.")


if __name__ == "__main__":
    clust()
