import requests
import os
import json
import re
import time

API_KEY = "xV7N9UNHq/8/YSlxmuLZLQ==oEt6TVCVnbkmtir4"
BASE_URL = "https://api.api-ninjas.com/v1/cocktail?name="
OUTPUT_JSON = "apininjas_recetas.json"
IMG_DIR = "imagenes_apininjas"

os.makedirs(IMG_DIR, exist_ok=True)
headers = {"X-Api-Key": API_KEY}

def sanitize_filename(name):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)

all_drinks = []
visited_names = set()

# Buscar por letra inicial a-z
for letra in "abcdefghijklmnopqrstuvwxyz":
    print(f"🔍 Buscando cócteles que comiencen con '{letra}' ...")
    try:
        resp = requests.get(BASE_URL + letra, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            for drink in data:
                nombre = drink.get("name", "").strip()
                if nombre and nombre not in visited_names:
                    visited_names.add(nombre)
                    all_drinks.append(drink)

                    # Descargar imagen si existe
                    img_url = drink.get("image")
                    if img_url:
                        nombre_archivo = sanitize_filename(nombre)
                        img_path = os.path.join(IMG_DIR, f"{nombre_archivo}.jpg")
                        try:
                            img_data = requests.get(img_url, timeout=10).content
                            with open(img_path, "wb") as f:
                                f.write(img_data)
                        except Exception as e:
                            print(f"❌ Error al descargar {img_url}: {e}")
        else:
            print(f"⚠️ Error {resp.status_code} con letra {letra}")
    except Exception as e:
        print(f"⚠️ Fallo con {letra}: {e}")
    time.sleep(1.5)  # evitar límites de tasa

# Guardar JSON estructurado
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(all_drinks, f, indent=2, ensure_ascii=False)

print(f"✅ Total de cócteles guardados: {len(all_drinks)}")
