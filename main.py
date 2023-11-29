from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import undetected_chromedriver as uc
from fake_useragent import UserAgent
import pickle


from bs4 import BeautifulSoup
import time, os, requests, datetime, random
import packaging.version

import numpy as np
from PIL import Image
import os
import cv2
from keras.models import load_model
import shutil


def spoofing():
    random1 = random.uniform(0.1, 1.5)
    random2 = random.uniform(0.3, 1.8)
    time.sleep(random.uniform(random1, random2))

    while True:
        ua = UserAgent()
        random_user_agent = ua.chrome

        # Verifica se il numero di versione soddisfa il requisito minimo
        if "/" in random_user_agent:
            try:
                version_string = random_user_agent.split("Chrome/", 1)[1].split(" ")[0]
                if version_string:
                    if packaging.version.parse(
                        version_string
                    ) > packaging.version.parse("70.0.3538.77"):
                        break
            except packaging.version.InvalidVersion:
                print(f"Versione non valida: {version_string}")
        print(f"User-Agent {random_user_agent} non soddisfa la versione minima.")

    # proxy = get_random_proxy()

    # Crea un oggetto Service per ChromeDriver specificando il percorso
    chrome_driver_service = webdriver.chrome.service.Service(
        r"chromedriver-win64\chromedriver.exe"
    )

    chrome_options = uc.ChromeOptions()

    # Specifica il proxy
    # chrome_options.add_argument(f"--proxy-server={proxy}")
    # print(f"proxy in uso:{proxy}")

    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    )

    # Inizializza il WebDriver
    driver = webdriver.Chrome(options=chrome_options, service=chrome_driver_service)

    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
    cookies = pickle.load(open("cookies.pkl", "rb"))

    for cookie in cookies:
        driver.add_cookie(cookie)

    # Dimensioni casuali del browser
    width = random.randint(800, 1920)
    height = random.randint(600, 1080)
    driver.set_window_size(width, height)

    # Configura il WebDriver per evitare la rilevazione
    driver.execute_cdp_cmd(
        "Network.setUserAgentOverride", {"userAgent": random_user_agent}
    )
    print(f"UserAgent in uso:{random_user_agent}")

    driver.execute_cdp_cmd(
        "Emulation.setGeolocationOverride",
        {
            "latitude": random.uniform(-90, 90),
            "longitude": random.uniform(-180, 180),
        },
    )
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd(
        "Network.emulateNetworkConditions",
        {
            "offline": False,
            "downloadThroughput": random.randint(
                50 * 1024, 1024 * 1024
            ),  # Velocità di download casuale
            "uploadThroughput": random.randint(
                50 * 1024, 1024 * 1024
            ),  # Velocità di upload casuale
            "latency": random.randint(1, 200),  # Latenza casuale
        },
    )
    return driver


def custom_wait(driver):
    try:
        element_44 = EC.visibility_of_element_located(
            (By.CLASS_NAME, "rc-image-tile-44")
        )(driver)
        return element_44
    except Exception:
        print("rc-image-tile-44 Not Found")
        element_44 = False

    try:
        element_33 = EC.visibility_of_element_located(
            (By.CLASS_NAME, "rc-image-tile-33")
        )(driver)
        return element_33
    except Exception:
        print("rc-image-tile-33 Not Found")
        element_33 = False

    return element_44 or element_33


# def fake_mouse_moves(window_size):
#     # Numero di spostamenti del mouse
#     num_movements = random.randint(0, 10)

#     for _ in range(num_movements):
#         x = random.randint(0, window_size["width"] - 1)
#         y = random.randint(0, window_size["height"] - 1)

#         actions = ActionChains(driver)
#         actions.move_to_element_with_offset(
#             driver.find_element(By.TAG_NAME, "body"), x, y
#         ).perform()


def download_img(driver):
    def get_filename():
        def custom_wait(driver):
            try:
                element = EC.visibility_of_element_located(
                    (By.CLASS_NAME, "rc-imageselect-desc-no-canonical")
                )(driver)
            except Exception as e:
                print("Errore per rc-imageselect-desc-no-canonical:", e)
                element = False

            if not element:
                try:
                    element = EC.visibility_of_element_located(
                        (By.CLASS_NAME, "rc-imageselect-desc")
                    )(driver)
                except Exception as e:
                    print("Errore per rc-imageselect-desc:", e)
                    element = False

            return element

        timestrap = datetime.datetime.now().timestamp()
        WebDriverWait(driver, 5).until(custom_wait)

        try:
            element = driver.find_element(
                By.CLASS_NAME, "rc-imageselect-desc-no-canonical"
            )
        except NoSuchElementException:
            try:
                element = driver.find_element(By.CLASS_NAME, "rc-imageselect-desc")
            except NoSuchElementException as e:
                print("Elemento non trovato:", e)
                return None

        strong_element = element.find_element(By.TAG_NAME, "strong")
        filename = strong_element.text.strip() + f"-{timestrap}.jpg"

        return filename

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Trova l'elemento dell'immagine
    payload = soup.find("img")

    # Ottieni l'URL dell'immagine
    img_url = payload["src"]

    # Effettua la richiesta HTTP per scaricare l'immagine
    response = requests.get(img_url)

    if response.status_code == 200:
        # Crea la directory "payloads" se non esiste
        if not os.path.exists(r"Google_Recaptcha_V2\result"):
            os.makedirs(r"Google_Recaptcha_V2\result")

        # Crea il percorso completo per salvare l'immagine nella cartella "payloads"
        img_path = os.path.join(r"Google_Recaptcha_V2\result", get_filename())

        # Salva l'immagine nel percorso specificato
        with open(img_path, "wb") as img_file:
            img_file.write(response.content)
            print(f"Saved image: {img_path}")
    else:
        print(f"Error downloading image - Status code: {response.status_code}")

    return get_filename()


def split_img(debug=True):
    # Specifica il nome della cartella delle immagini
    cartella_immagini = r"Google_Recaptcha_V2\result"

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
                        nome_file = f"section_{i}_{j}.jpg"
                        percorso_file = os.path.join(cartella_output, nome_file)
                        cv2.imwrite(percorso_file, parte)

                # Rimuovi il file originale
                os.remove(percorso_file_immagine)
            else:
                # Verifica se il nome del file è diverso da "parte_*_*" prima di registrare il messaggio di errore nel log
                if not nome_file_immagine.startswith("section_"):
                    if debug:
                        print(f"Error processing image '{nome_file_immagine}'.")


# Load the trained model
model = load_model("models/best_model.keras")

# Define the class labels (assuming they are in subdirectories)
class_labels = os.listdir("Google_Recaptcha_V2/images")

buttons_predicted_classes = {}


# Function to recursively process images in subdirectories and append results to the DataFrame
def process_images_in_directory(directory, debug=True):
    time.sleep(0.5)
    split_img()

    for subdir, _, files in os.walk(directory):
        for i, file in enumerate(files, 4):
            image_path = os.path.join(subdir, file)
            if image_path.endswith((".jpg", ".png", ".jpeg")):
                img = Image.open(image_path)
                img = img.resize((100, 100))
                img_array = np.array(img) / 255.0

                if img_array.shape[-1] != 3:
                    img_array = img_array[:, :, :3]

                predictions = model.predict(np.expand_dims(img_array, axis=0))

                accuracy = predictions[0, np.argmax(predictions)]

                predicted_class_index = np.argmax(predictions)
                predicted_class = class_labels[predicted_class_index]

                buttons_predicted_classes[i] = predicted_class

                print(
                    f"File: {file}, Predicted class: {predicted_class}, Accuracy: {accuracy}"
                )

    # Rimuovi tutte le cartelle all'interno della cartella root
    if not debug:
        for subdir, _, _ in os.walk(directory):
            shutil.rmtree(subdir)


def selenium_actions(driver, strong_element: str):
    def get_deep_image_predicted(driver):
        random1 = random.uniform(2.1685, 3.59845)
        random2 = random.uniform(4.4759, 6.95896)
        time.sleep(random.uniform(random1, random2))

        # Trova il <td> con un attributo tabindex specifico
        tabindex = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f'//td[@tabindex="{keys[i]}"]'))
        )
        try:
            # All'interno del <td>, cerca l'elemento con la classe "rc-image-tile-11"
            element_tile_11 = WebDriverWait(tabindex, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "rc-image-tile-11"))
            )
        except:
            print("element_tile_11 not found.")
            return False

        src = element_tile_11.get_attribute("src")

        response = requests.get(src)

        if response.status_code == 200:
            if not os.path.exists(r"Google_Recaptcha_V2\result"):
                os.makedirs(r"Google_Recaptcha_V2\result")

            img_path = (
                r"Google_Recaptcha_V2\result\img-"
                + str(datetime.datetime.now().timestamp())
                + ".jpg"
            )

            # Salva l'immagine nel percorso specificato
            with open(img_path, "wb") as img_file:
                img_file.write(response.content)
                print(f"Saved deep image: {img_path}")

            if img_path.endswith((".jpg", ".png", ".jpeg")):
                img = Image.open(img_path)
                img = img.resize((100, 100))
                img_array = np.array(img) / 255.0

                if img_array.shape[-1] != 3:
                    img_array = img_array[:, :, :3]

                predictions = model.predict(np.expand_dims(img_array, axis=0))

                accuracy = predictions[0, np.argmax(predictions)]

                predicted_class_index = np.argmax(predictions)
                predicted_class = class_labels[predicted_class_index]

                print(
                    f"Deep File: {img_path}, Predicted class: {predicted_class}, Accuracy: {accuracy}"
                )

                os.remove(img_path)

        else:
            print(f"Error downloading image - Status code: {response.status_code}")

        deep_image_predicted = predicted_class

        return deep_image_predicted

    def clear_strong_element(strong_element: str):
        match strong_element:
            case "a fire hydrant":
                strong_element = strong_element.split()[2]
                return strong_element
            case "traffic lights":
                strong_element = strong_element[0] + strong_element[8:-1].capitalize()
                return strong_element
            case "cars":
                strong_element = strong_element[:-1]
                return strong_element
            case "crosswalks":
                strong_element = strong_element[:-1]
                return strong_element
            case "bridges":
                strong_element = strong_element[:-1]
                return strong_element
            case "bicycles":
                strong_element = strong_element[:-1]
                return strong_element
            case "chimneys":
                strong_element = strong_element[:-1]
                return strong_element
            case "stairs":
                strong_element = strong_element[:-1]
                return strong_element

        return strong_element

    strong_element = clear_strong_element(strong_element)
    print(buttons_predicted_classes, '\nStrong element: "' + strong_element + '"')
    predictions = list(buttons_predicted_classes.values())
    keys = list(buttons_predicted_classes.keys())

    for i in range(9):
        if predictions[i] == strong_element.capitalize():
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, f'td[tabindex="{keys[i]}"]')
                )
            ).click()
            print(str(keys[i]) + " Clicked.")

            while get_deep_image_predicted(driver) == strong_element.capitalize():
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, f'td[tabindex="{keys[i]}"]')
                    )
                ).click()
                print("Deep-Clicked.")
                time.sleep(1)

        random1 = random.uniform(0.1685, 1.59845)
        random2 = random.uniform(0.4759, 1.75896)
        time.sleep(random.uniform(random1, random2))

    bypassed = False
    if strong_element.capitalize() not in predictions:
        print("Bypassed.")
        bypassed = True

    return bypassed


if __name__ == "__main__":
    driver = spoofing()
    # window_size = driver.get_window_size()

    # fake_mouse_moves(window_size)

    driver.get("https://recaptcha-demo.appspot.com/recaptcha-v2-checkbox-explicit.php")

    # Aspetta fino a quando l'iframe di Google ReCaptcha è disponibile e passa ad esso
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it(
            (
                By.CSS_SELECTOR,
                "iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']",
            )
        )
    )

    # Clicca sulla casella di controllo ReCaptcha
    driver.find_element(
        By.CSS_SELECTOR,
        "div#rc-anchor-container div.recaptcha-checkbox-border",
    ).click()

    # Torna al contesto principale
    driver.switch_to.default_content()

    # Aspetta fino a quando l'iframe di Google ReCaptcha è disponibile e passa ad esso
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it(
            (
                By.CSS_SELECTOR,
                "iframe[name^='c-'][src^='https://www.google.com/recaptcha/api2/bframe?']",
            )
        )
    )

    while True:
        # Attendi che uno dei due elementi sia visibile
        element_44 = WebDriverWait(driver, 10).until(custom_wait)
        while element_44:
            time.sleep(0.3)
            try:
                element_44 = EC.visibility_of_element_located(
                    (By.CLASS_NAME, "rc-image-tile-44")
                )(driver)
                driver.find_element(
                    By.ID,
                    "recaptcha-reload-button",
                ).click()

            except Exception:
                print("rc-image-tile-44 Not Found")
                element_44 = False

        # Scarica le immagini
        file_name = download_img(driver)
        time.sleep(0.5)
        strong_element = file_name.split("-")[0]
        process_images_in_directory(r"Google_Recaptcha_V2\result", debug=False)
        selenium_actions(driver, strong_element)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "recaptcha-verify-button"))
        ).click()

        print("Done.")
        time.sleep(10)
