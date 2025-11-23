
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