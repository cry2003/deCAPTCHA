import csv
import ipaddress
from tqdm import tqdm


def normalize_proxy(proxy):
    try:
        parts = proxy.split(":")
        if len(parts) == 2:
            ip = ipaddress.ip_address(parts[0])
            port = int(parts[1])
            return f"{ip}:{port}"
    except ValueError:
        pass
    return None


def get_proxy_from_txt(txt_file):
    proxy_set = set()  # Utilizziamo un set per mantenere i proxy unici

    with open(txt_file, mode="r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in tqdm(lines, desc="Caricamento da TXT", unit=" line"):
            proxy = normalize_proxy(line.strip())
            if proxy:
                proxy_set.add(proxy)

    return list(proxy_set)


def get_proxy_from_csv(csv_file):
    proxy_set = set()  # Utilizziamo un set per mantenere i proxy unici

    with open(csv_file, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in tqdm(reader, desc="Caricamento da CSV", unit=" riga"):
            ip = row.get("ip")
            port = row.get("port")
            if ip and port:
                proxy = normalize_proxy(f"{ip}:{port}")
                if proxy:
                    proxy_set.add(proxy)

    return list(proxy_set)
