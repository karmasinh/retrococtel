import requests
import json
import os
import time
import re

# === CONFIGURACIÓN ===
BASE_URL = "https://boozeapi.com/api/v1/cocktails"
OUTPUT_JSON = "boozeapi_cocktails.json"
IMAGES_DIR = "imagenes_boozeapi"

# Crear carpeta para imágenes
os.makedirs(IMAGES_DIR, exist_ok=True)

# Encabezados para evitar bloqueos
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; BoozeDataCollector/1.0; +https://boozeapi.com)",
    "Accept": "application/json"
}

def sanitize_filename(name):
    """Limpia el nombre del cóctel para usarlo como nombre de archivo."""
    return re.sub(r'[^a-zA-Z0-9_\- ]', '', name).strip().replace(" ", "_")

def download_image(url, cocktail_name):
    """Descarga y guarda una imagen localmente."""
    try:
        filename = sanitize_filename(cocktail_name) + os.path.splitext(url)[1]
        path = os.path.join(IMAGES_DIR, filename)
        if not os.path.exists(path):
            img = requests.get(url, timeout=20)
            if img.status_code == 200:
                with open(path, "wb") as f:
                    f.write(img.content)
        return path
    except Exception as e:
        print(f"⚠️ Error descargando imagen de {cocktail_name}: {e}")
        return None

def fetch_cocktails():
    """Descarga todas las páginas disponibles de la API Booze."""
    cocktails = []
    page = 1
    total_pages = 1  # inicial por defecto

    while page <= total_pages:
        print(f"📥 Página {page} de cócteles...")
        try:
            response = requests.get(BASE_URL, params={"page": page, "limit": 50},
                                    headers=HEADERS, timeout=20)
        except requests.exceptions.Timeout:
            print(f"⚠️ Timeout en página {page}, reintentando...")
            time.sleep(5)
            continue
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión: {e}")
            break

        if response.status_code != 200:
            print(f"⚠️ Código HTTP {response.status_code} en {response.url}")
            break

        data = response.json()
        results = data.get("data", [])

        if not results:
            print("⚠️ No se encontraron más resultados.")
            break

        for cocktail in results:
            img_path = None
            if cocktail.get("image"):
                img_path = download_image(cocktail["image"], cocktail["name"])
            cocktail["local_image"] = img_path
            cocktails.append(cocktail)

        pagination = data.get("pagination", {})
        total_pages = pagination.get("pages", total_pages)
        count = pagination.get("count", "?")

        print(f"✅ Página {page} completada ({len(results)} cócteles, total estimado: {count})")

        page += 1
        time.sleep(1)  # para respetar el límite de 60 requests/min

    return cocktails

if __name__ == "__main__":
    print("🚀 Iniciando descarga completa desde BoozeAPI...")
    cocktails = fetch_cocktails()

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(cocktails, f, indent=2, ensure_ascii=False)

    print(f"✅ Total de cócteles descargados: {len(cocktails)}")
    print(f"📁 Datos guardados en {OUTPUT_JSON}")
    print(f"🖼️ Imágenes en carpeta '{IMAGES_DIR}/'")
