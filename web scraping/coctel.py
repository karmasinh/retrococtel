import json
import re

with open("apininjas_recetas.json", "r", encoding="utf-8") as f:
    data = json.load(f)

limpio = []

def parse_ingrediente(text):
    # Separa cantidad y unidad de ingrediente
    match = re.match(r"^([\d/\. ]+[a-zA-Z]*) (.+)$", text)
    if match:
        return {"cantidad": match.group(1).strip(), "ingrediente": match.group(2).strip()}
    return {"cantidad": "", "ingrediente": text.strip()}

for drink in data:
    coctel = {}
    coctel["nombre_en"] = drink.get("name")
    coctel["nombre_es"] = drink.get("name")  # placeholder para traducir
    coctel["sinst"] = drink.get("instructions", "").replace("\n", " ").replace("'", "''")
    coctel["ingredientes"] = [parse_ingrediente(i) for i in drink.get("ingredients", [])]
    coctel["imagen"] = None  # No hay imagen
    limpio.append(coctel)

with open("apininjas_recetas_limpio.json", "w", encoding="utf-8") as f:
    json.dump(limpio, f, indent=2, ensure_ascii=False)

print(f"Limpieza API Ninjas completada. {len(limpio)} recetas guardadas.")
