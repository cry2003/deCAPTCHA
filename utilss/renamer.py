import os
import numpy as np
from PIL import Image
import time
import hashlib

# Cartella radice da cui iniziare la ricerca
cartella_radice = r"Google_Recaptcha_V2\images"

# Dizionario per tenere traccia delle immagini duplicate e dei relativi hash
immagini_hash = {}

# Scorrere tutte le cartelle e i file nelle sottocartelle
for cartella_corrente, sottocartelle, file in os.walk(cartella_radice):
    for nome_file in file:
        percorso_completo = os.path.join(cartella_corrente, nome_file)

        # Verifica se il file è un'immagine supportata (puoi estendere questa lista se necessario)
        estensioni_immagini_supportate = [".jpg", ".jpeg", ".png", ".gif"]
        if any(
            nome_file.lower().endswith(est) for est in estensioni_immagini_supportate
        ):
            # Carica l'immagine utilizzando PIL
            try:
                img = Image.open(percorso_completo)
            except Exception as e:
                print(f"Error while opening: {percorso_completo}: {e}")
                continue

            # Converte l'immagine in un array NumPy
            img_array = np.array(img)

            # Genera un timestamp univoco (in questo caso, l'ora attuale in secondi)
            timestamp = int(time.time())

            # Combina l'array dell'immagine e il timestamp e calcola l'hash
            combined_data = img_array.tobytes() + str(timestamp).encode()
            img_hash = hashlib.md5(combined_data).hexdigest()

            # Rinomina il file con il nome della cartella, l'hash e l'estensione
            nome_cartella = os.path.basename(cartella_corrente)
            file_name, file_extension = os.path.splitext(nome_file)
            new_filename = f"{nome_cartella}${img_hash}{file_extension}"
            new_path = os.path.join(cartella_corrente, new_filename)

            try:
                if not file_name.find("$"):
                    os.rename(percorso_completo, new_path)
                    print(f"Renamed '{percorso_completo}' to '{new_path}'")
                else:
                    pass
            except Exception as e:
                print(f"Error renaming '{percorso_completo}': {str(e)}")

print("Operation completed.")
