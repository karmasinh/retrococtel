CREATE DATABASE IF NOT EXISTS retrococtel
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE retrococtel;

-- TABLA: roles
CREATE TABLE roles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    permissions JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- TABLA: users
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role_id INT NOT NULL,
    status ENUM('Activo', 'Inactivo') DEFAULT 'Activo',
    avatar_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (role_id) REFERENCES roles(id)
        ON DELETE RESTRICT
);

-- TABLA: ingredients
CREATE TABLE ingredients (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    category ENUM(
        'Alcohol','Jugo','Endulzante','Hierba','Refresco','Licor','Condimento',
        'Básico','Fruta','Verdura','Especia','Otro'
    ) NOT NULL,
    unit_default VARCHAR(20) NOT NULL,
    calories_per_unit DECIMAL(6,2),
    abv DECIMAL(5,2) DEFAULT 0,
    effects JSON,
    stock DECIMAL(10,2),
    reorder_threshold DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- TABLA: cocktails
CREATE TABLE cocktails (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    short_description TEXT,
    long_description TEXT,
    glass_type VARCHAR(50),
    method ENUM('Shaken','Stirred','Muddled','Blended','Built','Layered'),
    prep_time_minutes INT,
    servings INT DEFAULT 1,
    difficulty ENUM('Fácil','Moderado','Avanzado'),
    calories INT,
    is_published BOOLEAN DEFAULT FALSE,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (created_by) REFERENCES users(id)
        ON DELETE RESTRICT
);

-- TABLA: cocktail_ingredients (many-to-many)
CREATE TABLE cocktail_ingredients (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cocktail_id INT NOT NULL,
    ingredient_id INT NOT NULL,
    amount DECIMAL(8,2) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    note TEXT,
    order_index INT DEFAULT 0,

    FOREIGN KEY (cocktail_id) REFERENCES cocktails(id)
        ON DELETE CASCADE,
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)
);

-- TABLA: cocktail_steps
CREATE TABLE cocktail_steps (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cocktail_id INT NOT NULL,
    step_number INT NOT NULL,
    instruction TEXT NOT NULL,

    FOREIGN KEY (cocktail_id) REFERENCES cocktails(id)
        ON DELETE CASCADE
);

-- TABLA: cocktail_images
CREATE TABLE cocktail_images (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cocktail_id INT NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    order_index INT DEFAULT 0,
    is_primary BOOLEAN DEFAULT FALSE,

    FOREIGN KEY (cocktail_id) REFERENCES cocktails(id)
        ON DELETE CASCADE
);

-- TABLAS DE METADATA: categories, tags, bases, etc.
CREATE TABLE cocktail_categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cocktail_id INT NOT NULL,
    category VARCHAR(50) NOT NULL,
    FOREIGN KEY (cocktail_id) REFERENCES cocktails(id)
        ON DELETE CASCADE
);

CREATE TABLE cocktail_tags (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cocktail_id INT NOT NULL,
    tag VARCHAR(50) NOT NULL,
    FOREIGN KEY (cocktail_id) REFERENCES cocktails(id)
        ON DELETE CASCADE
);

CREATE TABLE cocktail_bases (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cocktail_id INT NOT NULL,
    base VARCHAR(50) NOT NULL,
    FOREIGN KEY (cocktail_id) REFERENCES cocktails(id)
        ON DELETE CASCADE
);

CREATE TABLE cocktail_aromatics (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cocktail_id INT NOT NULL,
    aromatic VARCHAR(50) NOT NULL,
    FOREIGN KEY (cocktail_id) REFERENCES cocktails(id)
        ON DELETE CASCADE
);

CREATE TABLE cocktail_garnish (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cocktail_id INT NOT NULL,
    garnish VARCHAR(50) NOT NULL,
    FOREIGN KEY (cocktail_id) REFERENCES cocktails(id)
        ON DELETE CASCADE
);

CREATE TABLE cocktail_effects (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cocktail_id INT NOT NULL,
    effect VARCHAR(50) NOT NULL,
    FOREIGN KEY (cocktail_id) REFERENCES cocktails(id)
        ON DELETE CASCADE
);

-- NUEVAS TABLAS PARA PERSONALIZACIÓN DE USUARIO
-- TABLA: user_preferences
CREATE TABLE user_preferences (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,

    -- preferencia por sabores
    prefers_sweet BOOLEAN DEFAULT NULL,
    prefers_bitter BOOLEAN DEFAULT NULL,
    prefers_citrus BOOLEAN DEFAULT NULL,
    prefers_strong BOOLEAN DEFAULT NULL,
    prefers_low_abv BOOLEAN DEFAULT NULL,

    -- preferencias avanzadas
    preferred_categories JSON,
    preferred_ingredients JSON,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
);

-- TABLA: user_favorites (favoritos del usuario)
CREATE TABLE user_favorites (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    cocktail_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE,
    FOREIGN KEY (cocktail_id) REFERENCES cocktails(id)
        ON DELETE CASCADE
);

-- TABLA: user_history

CREATE TABLE user_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    cocktail_id INT NOT NULL,
    action ENUM('view','create','prepare') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE,
    FOREIGN KEY (cocktail_id) REFERENCES cocktails(id)
        ON DELETE CASCADE
);
