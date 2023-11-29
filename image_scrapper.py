from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc
from fake_useragent import UserAgent
import pickle


from bs4 import BeautifulSoup
import time, os, requests, datetime, random, threading
import packaging.version
from utils.FileLoader import get_proxy_from_txt
from utils import cluster, splitter, duplicate


def spoofing():
    time.sleep(random.uniform(0, 1.5))

    def get_random_proxy():
        def check_proxy(proxy):
            try:
                url = "https://www.google.com"
                response = requests.get(
                    url, proxies={"http": proxy, "https": proxy}, timeout=10
                )
                if response.status_code == 200:
                    return True
            except Exception as e:
                pass
            return False

        proxy_list = get_proxy_from_txt(r"utils\proxies\proxyList.txt")

        # Mescola la lista in modo casuale
        random.shuffle(proxy_list)

        for proxy in proxy_list:
            if check_proxy(proxy):
                return proxy

        return None  # Restituisce None se nessun proxy funziona

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
    except Exception as e:
        print("Errore per rc-image-tile-44", e)
        element_44 = False

    try:
        element_33 = EC.visibility_of_element_located(
            (By.CLASS_NAME, "rc-image-tile-33")
        )(driver)
    except Exception as e:
        print("Errore per rc-image-tile-33:", e)
        element_33 = False

    return element_44 or element_33


def fake_mouse_moves(window_size):
    # Numero di spostamenti del mouse
    num_movements = random.randint(0, 10)

    for _ in range(num_movements):
        x = random.randint(0, window_size["width"] - 1)
        y = random.randint(0, window_size["height"] - 1)

        actions = ActionChains(driver)
        actions.move_to_element_with_offset(
            driver.find_element(By.TAG_NAME, "body"), x, y
        ).perform()

        random1 = random.uniform(0.1, 1.5)
        random2 = random.uniform(0.3, 1.8)
        time.sleep(random.uniform(random1, random2))


def download_img():
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

        random1 = random.uniform(0.5, 5.3)
        random2 = random.uniform(0.6, 8)

        time.sleep(random.uniform(random1, random2))

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
        if not os.path.exists("payloads/scraps"):
            os.makedirs("payloads/scraps")

        # Crea il percorso completo per salvare l'immagine nella cartella "payloads"
        img_path = os.path.join("payloads/scraps", get_filename())

        # Salva l'immagine nel percorso specificato
        with open(img_path, "wb") as img_file:
            img_file.write(response.content)
            print(f"Immagine salvata: {img_path}")
    else:
        print(
            f"Errore nel download dell'immagine - Codice di stato: {response.status_code}"
        )


if __name__ == "__main__":

    def normalizing_image():
        cluster.clust(debug=False)
        splitter.split_img(debug=False)
        duplicate.remove_duplicates(r"C:\Users\ChristianVillani\Downloads\deCAPTCHA\payloads",debug=False)

    while True:
        try:
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

            random1 = random.uniform(1, 3)
            random2 = random.uniform(1.8, 5.8)

            time.sleep(random.uniform(random1, random2))

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
            # Attendi che uno dei due elementi sia visibile
            WebDriverWait(driver, 10).until(custom_wait)

            # Scarica le immagini
            download_img()

            # ritardo tra le iterazioni per evitare sovraccaricare il server
            random1 = random.uniform(1.9, 5)
            random2 = random.uniform(2.5, 9)

            time.sleep(random.uniform(random1, random2))

        except Exception as e:
            driver.quit()
            print(f"An error occurred: {e}")
            print("Restarting in 15 minutes...")
            sleep_timer = threading.Timer(random.randint(720,900), normalizing_image())
            sleep_timer.start()
            # Attendiamo che il timer termini prima di continuare con il ciclo
            sleep_timer.join()
