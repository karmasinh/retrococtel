import requests
import os
import json
import re

def sanitize_filename(name):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)

BASE_URL = "https://www.thecocktaildb.com/api/json/v1/1/"
OUTPUT_JSON = "thecocktaildb_recetas.json"
IMG_DIR = "imagenes_cocktaildb"

os.makedirs(IMG_DIR, exist_ok=True)

all_drinks = []

# Buscar por letras (a-z)
for letra in "abcdefghijklmnopqrstuvwxyz":
    url = f"{BASE_URL}search.php?f={letra}"
    resp = requests.get(url)
    data = resp.json()
    if data["drinks"]:
        for drink in data["drinks"]:
            all_drinks.append(drink)
            # Descargar imagen
            img_url = drink.get("strDrinkThumb")
            if img_url:
                nombre = sanitize_filename(drink["strDrink"])
                img_path = os.path.join(IMG_DIR, f"{nombre}.jpg")
                try:
                    img_data = requests.get(img_url).content
                    with open(img_path, "wb") as f:
                        f.write(img_data)
                except Exception as e:
                    print(f"Error descargando {img_url}: {e}")

# Guardar JSON estructurado
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(all_drinks, f, indent=2, ensure_ascii=False)

print(f"Descargadas {len(all_drinks)} recetas y sus imágenes.")
