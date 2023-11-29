import cv2
import os
import logging
from tqdm import tqdm  # Importa la libreria tqdm per la progress bar


def split_img(debug=True):
    # Configura il logger per registrare i messaggi in un file
    logging.basicConfig(
        filename="splitter.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s: %(message)s",
    )

    # Specifica il nome della cartella delle immagini
    cartella_immagini = "payloads/300x300"

    # Conta il numero totale di file immagine
    num_files = sum([len(files) for _, _, files in os.walk(cartella_immagini)])

    # Inizializza la barra di avanzamento
    with tqdm(total=num_files, disable=not debug) as pbar:
        # Itera attraverso la cartella delle immagini e le subcartelle
        for root, _, files in os.walk(cartella_immagini):
            for nome_file_immagine in files:
                # Estrai il nome del file senza estensione
                nome_cartella = os.path.splitext(nome_file_immagine)[0]

                # Crea il percorso completo del file immagine
                percorso_file_immagine = os.path.join(root, nome_file_immagine)

                # Carica l'immagine
                immagine = cv2.imread(percorso_file_immagine)

                # Assicurati che l'immagine sia 300x300 pixel
                if immagine is not None and immagine.shape[:2] == (300, 300):
                    # Crea una cartella con il nome dell'immagine originale nella cartella corrente
                    cartella_corrente = os.path.dirname(percorso_file_immagine)
                    cartella_output = os.path.join(cartella_corrente, nome_cartella)
                    os.makedirs(cartella_output, exist_ok=True)

                    # Definisci le dimensioni delle immagini di output (100x100)
                    righe, colonne = 3, 3
                    altezza, larghezza = 100, 100

                    # Suddividi l'immagine in 9 parti da 100x100 pixel e salva ciascuna parte nella cartella
                    for i in range(righe):
                        for j in range(colonne):
                            y1 = i * altezza
                            y2 = (i + 1) * altezza
                            x1 = j * larghezza
                            x2 = (j + 1) * larghezza
                            parte = immagine[y1:y2, x1:x2]

                            # Salva ogni parte nella cartella con un nome unico
                            nome_file = f"parte_{i}_{j}.jpg"
                            percorso_file = os.path.join(cartella_output, nome_file)
                            cv2.imwrite(percorso_file, parte)

                    # Rimuovi il file originale
                    os.remove(percorso_file_immagine)

                    # Aggiorna la barra di avanzamento
                    if debug:
                        pbar.update(1)
                else:
                    # Verifica se il nome del file è diverso da "parte_*_*" prima di registrare il messaggio di errore nel log
                    if not nome_file_immagine.startswith("parte_"):
                        # Registra un messaggio di errore nel file di log
                        logging.error(f"Error processing image '{nome_file_immagine}'")
                    if debug:
                        print(f"Error processing image '{nome_file_immagine}'.")

                    # Aggiorna la barra di avanzamento anche per le immagini non valide
                    if debug:
                        pbar.update(1)


if __name__ == "__main__":
    split_img()
