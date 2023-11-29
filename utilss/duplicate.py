import os
import numpy as np
from PIL import Image
import logging
from tqdm import tqdm
from datetime import datetime, timedelta


def get_last_log_time(log_filename):
    last_log_time = None
    if os.path.isfile(log_filename):
        with open(log_filename, "r") as log_file:
            for line in log_file:
                parts = line.split(" - ")
                if len(parts) >= 2:
                    timestamp = parts[0]
                    log_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S,%f")
                    if last_log_time is None or log_time > last_log_time:
                        last_log_time = log_time
    return last_log_time


def remove_duplicates(root_folder, debug=True, date_threshold=3600):
    log_filename = "duplicates.log"

    last_log_time = get_last_log_time(log_filename)
    min_allowed_date = datetime.now() - timedelta(seconds=date_threshold)

    if last_log_time is not None and last_log_time < min_allowed_date:
        print("Skipping duplicate removal due to recent log entries.")
        return

    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    total_files = sum([len(files) for _, _, files in os.walk(root_folder)])

    file_progress_bar = tqdm(
        total=total_files, desc=f"Scanning files for duplicates", disable=not debug
    )

    for cartella_corrente, _, files in os.walk(root_folder):
        hash_set = set()

        for nome_file in files:
            percorso_completo = os.path.join(cartella_corrente, nome_file)

            estensioni_immagini_supportate = (".jpg", ".jpeg", ".png", ".gif")
            if nome_file.lower().endswith(estensioni_immagini_supportate):
                try:
                    img = Image.open(percorso_completo)
                except Exception as e:
                    logging.error(f"Error while opening: {percorso_completo}: {e}")
                    continue

                img_hash = hash(img.tobytes())

                if img_hash in hash_set:
                    logging.info(
                        f"Duplicate image found (hash: {img_hash}): {percorso_completo}"
                    )
                    try:
                        os.remove(percorso_completo)
                        if debug:
                            print(
                                f"\033[1;31mDuplicate file removed: {percorso_completo}\033[0m"
                            )
                    except Exception as e:
                        logging.error(f"Error while deleting {percorso_completo}: {e}")
                else:
                    hash_set.add(img_hash)

                if debug:
                    file_progress_bar.update(1)

    file_progress_bar.close()
    logging.info(f"Operation completed.")
    if debug:
        print("Operation completed. Check the log file for details: 'duplicates.log'")


if __name__ == "__main__":
    cartella_radice = r"Google_Recaptcha_V2\images"
    remove_duplicates(cartella_radice)
