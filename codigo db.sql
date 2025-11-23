CREATE DATABASE IF NOT EXISTS coctelmatchdb;
USE coctelmatchdb;

CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    estado TINYINT(1) DEFAULT 1
);

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(100) NOT NULL,
    nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    avatar_url VARCHAR(255),
    rol_id INT,
    estado ENUM('Activo','Inactivo') DEFAULT 'Activo',
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rol_id) REFERENCES roles(id)
);

CREATE TABLE unidades_medida (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    abreviatura VARCHAR(10),
    descripcion TEXT,
    estado TINYINT(1) DEFAULT 1
);


CREATE TABLE tipos_ingredientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_tipo VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT,
    estado TINYINT(1) DEFAULT 1
);


CREATE TABLE marcas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_marca VARCHAR(100) NOT NULL UNIQUE,
    pais_origen VARCHAR(50),
    descripcion TEXT,
    estado TINYINT(1) DEFAULT 1
);

CREATE TABLE ingredientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    tipo_id INT NOT NULL,
    unidad_predeterminada INT,
    abv DECIMAL(5,2),
    calorias_por_unidad DECIMAL(6,2),
    descripcion TEXT,
    estado TINYINT(1) DEFAULT 1,
    FOREIGN KEY (tipo_id) REFERENCES tipos_ingredientes(id),
    FOREIGN KEY (unidad_predeterminada) REFERENCES unidades_medida(id)
);

CREATE TABLE inventario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ingrediente_id INT NOT NULL,
    marca_id INT,
    cantidad_stock DECIMAL(10,2) DEFAULT 0,
    unidad_id INT NOT NULL,
    punto_reorden DECIMAL(10,2) DEFAULT 0,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    estado TINYINT(1) DEFAULT 1,
    FOREIGN KEY (ingrediente_id) REFERENCES ingredientes(id),
    FOREIGN KEY (marca_id) REFERENCES marcas(id),
    FOREIGN KEY (unidad_id) REFERENCES unidades_medida(id)
);

CREATE TABLE vasos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_vaso VARCHAR(50) NOT NULL UNIQUE,
    categoria VARCHAR(50),
    capacidad_ml DECIMAL(6,2),
    estado TINYINT(1) DEFAULT 1
);

CREATE TABLE metodos_preparacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_metodo VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT,
    estado TINYINT(1) DEFAULT 1
);


CREATE TABLE tipos_cocteles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_tipo VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT,
    estado TINYINT(1) DEFAULT 1
);

CREATE TABLE efectos_coctel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_efecto VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT,
    estado TINYINT(1) DEFAULT 1
);

CREATE TABLE categorias_cocteles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_categoria VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT,
    estado TINYINT(1) DEFAULT 1
);

CREATE TABLE cocteles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    slug VARCHAR(100) UNIQUE,
    descripcion_larga TEXT,
    vaso_id INT,
    metodo_id INT,
    tipo_id INT,
    porciones INT,
    calorias DECIMAL(6,2),
    tiempo_preparacion INT,
    dificultad ENUM('Fácil','Moderado','Difícil'),
    publicado BOOLEAN DEFAULT FALSE,
    creado_por INT,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado TINYINT(1) DEFAULT 1,
    FOREIGN KEY (vaso_id) REFERENCES vasos(id),
    FOREIGN KEY (metodo_id) REFERENCES metodos_preparacion(id),
    FOREIGN KEY (tipo_id) REFERENCES tipos_cocteles(id),
    FOREIGN KEY (creado_por) REFERENCES usuarios(id)
);

CREATE TABLE coctel_categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    coctel_id INT,
    categoria_id INT,
    FOREIGN KEY (coctel_id) REFERENCES cocteles(id),
    FOREIGN KEY (categoria_id) REFERENCES categorias_cocteles(id)
);

CREATE TABLE coctel_ingredientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    coctel_id INT,
    ingrediente_id INT,
    cantidad VARCHAR(50),
    unidad_id INT,
    nota_especial VARCHAR(255),
    estado TINYINT(1) DEFAULT 1,
    FOREIGN KEY (coctel_id) REFERENCES cocteles(id),
    FOREIGN KEY (ingrediente_id) REFERENCES ingredientes(id),
    FOREIGN KEY (unidad_id) REFERENCES unidades_medida(id)
);

CREATE TABLE coctel_efectos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    coctel_id INT,
    efecto_id INT,
    FOREIGN KEY (coctel_id) REFERENCES cocteles(id),
    FOREIGN KEY (efecto_id) REFERENCES efectos_coctel(id)
);

CREATE TABLE pasos_coctel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    coctel_id INT,
    orden_paso INT,
    descripcion TEXT,
    estado TINYINT(1) DEFAULT 1,
    FOREIGN KEY (coctel_id) REFERENCES cocteles(id)
);

CREATE TABLE garnish_coctel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    coctel_id INT,
    descripcion VARCHAR(255),
    estado TINYINT(1) DEFAULT 1,
    FOREIGN KEY (coctel_id) REFERENCES cocteles(id)
);

CREATE TABLE imagenes_coctel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    coctel_id INT,
    url VARCHAR(255),
    estado TINYINT(1) DEFAULT 1,
    FOREIGN KEY (coctel_id) REFERENCES cocteles(id)
);

CREATE TABLE preferencias_usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    tipo_coctel_id INT,
    efecto_id INT,
    nivel_preferencia ENUM('Bajo','Medio','Alto'),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (tipo_coctel_id) REFERENCES tipos_cocteles(id),
    FOREIGN KEY (efecto_id) REFERENCES efectos_coctel(id)
);

frontend/src/redux/recipeReducer/reducer.js → cocktailReducer/reducer.js


USE coctelmatchdb;

-- ========================
-- 🚀 ROLES
-- ========================
INSERT INTO roles (nombre, descripcion, estado) VALUES
('Administrador', 'Tiene acceso completo al sistema', 1),
('Bartender', 'Puede crear, editar y eliminar cócteles', 1),
('Cliente', 'Puede visualizar y valorar cócteles', 1);

-- ========================
-- 👤 USUARIOS
-- ========================
INSERT INTO usuarios (nombre_completo, nombre_usuario, email, password_hash, rol_id, estado)
VALUES
('Admin Principal', 'admin', 'admin@coctelmatch.com', '12345', 1, 'Activo'),
('Juan Bartender', 'bartender', 'bartender@coctelmatch.com', '12345', 2, 'Activo'),
('Carlos Cliente', 'cliente', 'cliente@coctelmatch.com', '12345', 3, 'Activo');

-- ========================
-- 📏 UNIDADES DE MEDIDA
-- ========================
INSERT INTO unidades_medida (nombre, abreviatura, descripcion, estado) VALUES
('Mililitro', 'ml', 'Unidad de volumen común para líquidos', 1),
('Centilitro', 'cl', 'Equivale a 10 mililitros', 1),
('Litro', 'L', 'Unidad de volumen estándar', 1),
('Gramo', 'g', 'Unidad de masa usada para sólidos', 1),
('Kilogramo', 'kg', '1000 gramos', 1),
('Onza líquida', 'oz', 'Medida estándar de bartending', 1),
('Pizca', 'pzc', 'Medida pequeña, usada para condimentos', 1),
('Unidad', 'u', 'Unidad individual de ingrediente', 1);

-- ========================
-- 🧪 TIPOS DE INGREDIENTES
-- ========================
INSERT INTO tipos_ingredientes (nombre_tipo, descripcion, estado) VALUES
('Destilado', 'Bebidas alcohólicas destiladas', 1),
('Licor', 'Bebidas alcohólicas con saborizantes', 1),
('Vino o Vermut', 'Vinos aromatizados o fortificados', 1),
('Cerveza', 'Bebida fermentada a base de cereales', 1),
('Espumante o Champagne', 'Vino espumoso con gas natural', 1),
('Jugo o Zumo', 'Extractos naturales de frutas', 1),
('Refresco o Soda', 'Bebidas gaseosas sin alcohol', 1),
('Jarabe o Endulzante', 'Azúcar líquida o saborizantes', 1),
('Esencia o Extracto', 'Concentrados aromáticos', 1),
('Decorativo o Garnish', 'Elementos visuales o aromáticos', 1);

-- ========================
-- 🏷️ MARCAS (Genéricas)
-- ========================
INSERT INTO marcas (nombre_marca, pais_origen, descripcion, estado) VALUES
('Genérico', 'Internacional', 'Marca genérica para ingredientes sin marca específica', 1);

-- ========================
-- 🍸 VASOS
-- ========================
INSERT INTO vasos (nombre_vaso, categoria, capacidad_ml, estado) VALUES
('Copa de Cóctel', 'Copa', 180.00, 1),
('Vaso Highball', 'Vaso alto', 300.00, 1),
('Vaso Old Fashioned', 'Vaso corto', 240.00, 1),
('Copa Martini', 'Copa', 150.00, 1),
('Copa de Vino', 'Copa', 250.00, 1),
('Copa Flute', 'Copa', 180.00, 1),
('Vaso Collins', 'Vaso alto', 350.00, 1),
('Copa Coupe', 'Copa', 180.00, 1);

-- ========================
-- 🌀 MÉTODOS DE PREPARACIÓN
-- ========================
INSERT INTO metodos_preparacion (nombre_metodo, descripcion, estado) VALUES
('Agitado', 'Se mezclan los ingredientes en coctelera con hielo y se agita vigorosamente', 1),
('Mezclado', 'Se remueven los ingredientes con una cuchara en un vaso mezclador', 1),
('Batido', 'Se mezclan los ingredientes en licuadora', 1),
('Directo', 'Se vierten los ingredientes directamente en el vaso de servicio', 1),
('Refrescado', 'Se remueve suavemente para enfriar sin agitar', 1);

-- ========================
-- 🍹 TIPOS DE CÓCTELES
-- ========================
INSERT INTO tipos_cocteles (nombre_tipo, descripcion, estado) VALUES
('Clásico', 'Recetas tradicionales reconocidas internacionalmente', 1),
('Moderno', 'Recetas innovadoras o adaptaciones contemporáneas', 1),
('Sin Alcohol', 'Cócteles no alcohólicos o mocktails', 1),
('Tropical', 'Cócteles frutales y refrescantes', 1),
('De Postre', 'Cócteles dulces o cremosos', 1),
('Aperitivo', 'Cócteles ligeros para antes de comer', 1),
('Digestivo', 'Cócteles fuertes o herbales para después de comer', 1);

-- ========================
-- 🌈 EFECTOS DE CÓCTEL
-- ========================
INSERT INTO efectos_coctel (nombre_efecto, descripcion, estado) VALUES
('Relajante', 'Provoca sensación de calma o relajación', 1),
('Energizante', 'Da sensación de energía o vitalidad', 1),
('Alegre', 'Aumenta el estado de ánimo o euforia leve', 1),
('Seductor', 'Aporta calidez o confianza social', 1),
('Refrescante', 'Causa sensación de frescura y ligereza', 1);

-- ========================
-- 🗂️ CATEGORÍAS DE CÓCTELES
-- ========================
INSERT INTO categorias_cocteles (nombre_categoria, descripcion, estado) VALUES
('Fuerte', 'Alta graduación alcohólica', 1),
('Dulce', 'Sabor predominante dulce', 1),
('Ácido', 'Sabor principal cítrico o ácido', 1),
('Suave', 'Equilibrado o ligero en alcohol', 1),
('Refrescante', 'Ideal para climas cálidos', 1),
('Cremoso', 'Textura espesa o láctea', 1),
('Amargo', 'Sabor amargo o especiado', 1);
