import re

# Orden de tablas según FK para no romper constraints
orden_tablas = [
    "roles",
    "usuarios",
    "unidades_medida",
    "tipos_ingredientes",
    "marcas",
    "vasos",
    "metodos_preparacion",
    "tipos_cocteles",
    "efectos_coctel",
    "categorias_cocteles",
    "ingredientes",
    "cocteles",
    "coctel_categorias",
    "coctel_ingredientes",
    "coctel_efectos",
    "pasos_coctel",
    "garnish_coctel",
    "imagenes_coctel"
]

columnas_por_tabla = {
    "roles": ["nombre", "descripcion", "estado"],
    "usuarios": ["nombre_completo", "nombre_usuario", "email", "password_hash", "rol_id", "estado"],
    "unidades_medida": ["nombre", "abreviatura", "descripcion", "estado"],
    "tipos_ingredientes": ["nombre_tipo", "descripcion", "estado"],
    "marcas": ["nombre_marca", "pais_origen", "descripcion", "estado"],
    "vasos": ["nombre_vaso", "categoria", "capacidad_ml", "estado"],
    "metodos_preparacion": ["nombre_metodo", "descripcion", "estado"],
    "tipos_cocteles": ["nombre_tipo", "descripcion", "estado"],
    "efectos_coctel": ["nombre_efecto", "descripcion", "estado"],
    "categorias_cocteles": ["nombre_categoria", "descripcion", "estado"],
    "ingredientes": ["nombre", "tipo_id", "unidad_predeterminada", "abv", "calorias_por_unidad", "descripcion", "estado"],
    "cocteles": ["nombre", "slug", "descripcion_larga", "vaso_id", "metodo_id", "tipo_id",
                 "porciones", "calorias", "tiempo_preparacion", "dificultad", "publicado", "creado_por", "estado"],
    "coctel_categorias": ["coctel_id", "categoria_id"],
    "coctel_ingredientes": ["coctel_id", "ingrediente_id", "cantidad", "unidad_id", "nota_especial", "estado"],
    "coctel_efectos": ["coctel_id", "efecto_id"],
    "pasos_coctel": ["coctel_id", "orden_paso", "descripcion", "estado"],
    "garnish_coctel": ["coctel_id", "descripcion", "estado"],
    "imagenes_coctel": ["coctel_id", "url", "estado"]
}

def limpiar_valor(valor, columna=None):
    valor = valor.strip()
    if valor.upper() == "NULL" or valor == "":
        # Si es columna estado, default 1
        if columna == "estado":
            return "1"
        return "NULL"
    # Detecta booleanos
    if valor.upper() in ["TRUE", "FALSE"]:
        return valor.upper()
    # Detecta números
    if re.match(r"^-?\d+(\.\d+)?$", valor):
        return valor
    # Escapa comillas simples
    valor = valor.strip("'").replace("\\", "")
    valor = valor.replace("'", "''")
    return f"'{valor}'"

def generar_insert(tabla, filas):
    columnas = columnas_por_tabla.get(tabla)
    columnas_sql = f"({', '.join(columnas)})" if columnas else ""
    valores_sql = []

    for fila in filas:
        valores = re.findall(r"\((.*)\)", fila, re.DOTALL)[0]
        # Separar por comas que no estén dentro de paréntesis
        partes = re.split(r",(?![^\(\)]*\))", valores)
        partes = [limpiar_valor(x.strip(), columnas[i] if columnas and i < len(columnas) else None)
                  for i, x in enumerate(partes)]
        # Rellenar con NULL o 1 si hay columnas faltantes
        if columnas and len(partes) < len(columnas):
            for i in range(len(partes), len(columnas)):
                if columnas[i] == "estado":
                    partes.append("1")
                else:
                    partes.append("NULL")
        # Truncar si hay columnas de más
        if columnas:
            partes = partes[:len(columnas)]
        valores_sql.append(f"({', '.join(partes)})")

    return f"INSERT INTO {tabla} {columnas_sql} VALUES\n" + ",\n".join(valores_sql) + ";\n"

def generar_inserts_mysql(archivo_txt, salida_sql):
    with open(archivo_txt, "r", encoding="utf-8") as f:
        contenido = f.read()

    # Separar bloques por -- tabla
    bloques = re.split(r"--\s*(\w+)", contenido)
    bloques_dict = {}
    for i in range(1, len(bloques), 2):
        tabla = bloques[i].strip()
        datos = bloques[i + 1].strip().rstrip(";")
        filas = re.findall(r"\([^\)]*\)", datos, re.DOTALL)
        if filas:
            bloques_dict[tabla] = filas

    resultado_sql = []
    for tabla in orden_tablas:
        if tabla in bloques_dict:
            resultado_sql.append(generar_insert(tabla, bloques_dict[tabla]))

    with open(salida_sql, "w", encoding="utf-8") as f_out:
        f_out.write("\n\n".join(resultado_sql))

    print(f"✅ Archivo SQL generado correctamente: {salida_sql}")

if __name__ == "__main__":
    generar_inserts_mysql("datos.txt", "salida_mysql.sql")
