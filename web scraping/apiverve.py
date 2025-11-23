import requests
import os
import json
import re
import time

API_KEY = "d543d42b-7ccf-47b5-89c6-fd6a43862e43"
BASE_URL = "https://api.apiverve.com/v1/cocktail"
OUTPUT_JSON = "apiverve_recetas.json"
IMG_DIR = "imagenes_apiverve"

os.makedirs(IMG_DIR, exist_ok=True)
headers = {"x-api-key": API_KEY}

def sanitize_filename(name):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)

all_drinks = []
visited_names = set()

# Búsqueda automática a-z
for letra in "abcdefghijklmnopqrstuvwxyz":
    print(f"🔍 Buscando cócteles con '{letra}' en APIVerve...")
    try:
        resp = requests.get(f"{BASE_URL}?name={letra}", headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            # Dependiendo del formato de respuesta de APIVerve
            results = data.get("data")
            if isinstance(results, list):
                drinks = results
            elif isinstance(results, dict):
                drinks = [results]
            else:
                drinks = []

            for drink in drinks:
                nombre = drink.get("name", "").strip()
                if nombre and nombre not in visited_names:
                    visited_names.add(nombre)
                    all_drinks.append(drink)

                    # Descargar imagen
                    img_url = drink.get("image")
                    if img_url:
                        nombre_archivo = sanitize_filename(nombre)
                        img_path = os.path.join(IMG_DIR, f"{nombre_archivo}.jpg")
                        try:
                            img_data = requests.get(img_url, timeout=10).content
                            with open(img_path, "wb") as f:
                                f.write(img_data)
                        except Exception as e:
                            print(f"❌ Error con {img_url}: {e}")
        else:
            print(f"⚠️ Código HTTP {resp.status_code} para letra {letra}")
    except Exception as e:
        print(f"⚠️ Fallo con letra {letra}: {e}")
    time.sleep(1.5)

# Guardar JSON
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(all_drinks, f, indent=2, ensure_ascii=False)

print(f"✅ Total de cócteles guardados: {len(all_drinks)}")
