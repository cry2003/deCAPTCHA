import os
import requests
from concurrent.futures import ThreadPoolExecutor
from FileLoader import get_proxy_from_txt


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


def main():
    proxy_list = get_proxy_from_txt(r"utils\proxies\proxyList.txt")
    valid_proxies = []

    # Ottieni il numero di processori disponibili sul sistema
    num_processors = os.cpu_count()

    # Imposta il numero di workers in base al numero di processori
    max_workers = min(
        num_processors * 2, len(proxy_list)
    )  # Puoi regolare il moltiplicatore in base alle prestazioni

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(check_proxy, proxy) for proxy in proxy_list]

        for future, proxy in zip(futures, proxy_list):
            if future.result():
                valid_proxies.append(proxy)
                print(f"\033[1;32mProxy {proxy} funziona.\033[0m")
            else:
                print(f"\033[1;31mProxy {proxy} NON funziona.\033[0m")

    print("\nProxy funzionanti:")
    for proxy in valid_proxies:
        print(proxy)


if __name__ == "__main__":
    main()
