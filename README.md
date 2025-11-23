# 🍸 Cocktail Management System

Un sistema completo de gestión de cócteles e inventario con interfaz moderna y visualizaciones premium, desarrollado con Streamlit y Python.

## ✨ Características Principales

### 🎯 Gestión Integral
- **CRUD Completo** de cócteles, ingredientes, usuarios e inventario
- **Autenticación** de usuarios con roles y permisos
- **Dashboard Premium** con visualizaciones interactivas
- **Exportación de datos** en múltiples formatos (CSV, Excel, JSON)

### 📊 Análisis y Reportes
- **Gráficos interactivos** con Plotly
- **Estadísticas en tiempo real** del inventario y ventas
- **Alertas automáticas** de stock bajo
- **Reportes personalizables** por período

### 🎨 Interfaz Moderna
- **Diseño responsive** y adaptativo
- **Temas personalizables** con CSS premium
- **Sistema de temas por usuario** - cada usuario puede tener su tema preferido
- **Temas disponibles**: Default, Dark, Blue, Green, Purple
- **Iconos y visualizaciones** profesionales
- **Navegación intuitiva** con menú lateral

### 🗄️ Base de Datos Robusta
- **MySQL** como sistema de gestión de base de datos
- **Modelo de datos optimizado** para rendimiento
- **Respaldo automático** de información crítica
- **Integración con APIs externas** para enriquecimiento de datos

## 🚀 Instalación Rápida

### Opción 1: Script de Despliegue Automatizado
```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/cocktail-management-system.git
cd cocktail-management-system

# Ejecutar el script de despliegue
python deploy.py
```

### Opción 2: Instalación Manual
```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/cocktail-management-system.git
cd cocktail-management-system

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# 5. Iniciar la aplicación
streamlit run app.py --server.port=8501
```

## 📋 Requisitos del Sistema

### Software Requerido
- **Python 3.8+**
- **MySQL 5.7+** o **MariaDB 10.2+**
- **Git** (para clonar el repositorio)

### Dependencias Principales
```
streamlit>=1.28.0
mysql-connector-python>=8.1.0
pandas>=2.0.0
plotly>=5.17.0
python-dotenv>=1.0.0
bcrypt>=4.0.0
Pillow>=10.0.0
```

## 🗄️ Configuración de Base de Datos

### 1. Crear Base de Datos
```sql
CREATE DATABASE IF NOT EXISTS cocktails_db;
USE cocktails_db;
```

### 2. Ejecutar Script de Inicialización
```bash
# El script de despliegue creará las tablas automáticamente
# O puedes ejecutar manualmente:
mysql -u root -p cocktails_db < database/schema.sql
```

### 3. Configurar Conexión
El script de despliegue te pedirá las credenciales de forma interactiva, o puedes editar manualmente el archivo `.env`:
```
DB_HOST=localhost
DB_USER=tu_usuario
DB_PASS=tu_contraseña
DB_NAME=cocktails_db
DB_PORT=3306
SECRET_KEY=tu_clave_secreta
JWT_SECRET=tu_jwt_secreto
```

## 🎮 Uso del Sistema

### 1. Inicio de Sesión
- Accede a `http://localhost:8501`
- Usa las credenciales por defecto (se crearán al inicializar)
- El sistema redirigirá al dashboard principal

### 2. Navegación Principal

#### 📊 Dashboard
- **Métricas generales** del sistema
- **Gráficos interactivos** de ventas e inventario
- **Alertas y notificaciones** en tiempo real
- **Accesos rápidos** a funciones principales

#### 🍹 Gestión de Cócteles
- **Catálogo completo** con búsqueda y filtros
- **Creación/edición** con formularios dinámicos
- **Gestión de ingredientes** por cóctel
- **Imágenes y descripciones** detalladas

#### 📦 Gestión de Inventario
- **Control de stock** con alertas automáticas
- **Movimientos de inventario** detallados
- **Importación/exportación** de datos
- **Reportes de inventario** personalizables

#### 👥 Gestión de Usuarios
- **Roles y permisos** diferenciados
- **Historial de actividad** de usuarios
- **Gestión de accesos** y sesiones
- **Configuración de perfiles**
- **Temas personalizados por usuario** - cada usuario puede tener su tema preferido

### 3. Funcionalidades Avanzadas

#### 📈 Análisis y Reportes
- **Estadísticas por período** (diario, semanal, mensual)
- **Análisis de tendencias** de ventas
- **Reportes exportables** en PDF y Excel
- **Dashboard personalizable** según rol

#### 🔧 Herramientas de Administración
- **Respaldo de base de datos**
- **Importación masiva** de datos
- **Configuración del sistema**
- **Gestión de APIs externas**

## 🛠️ Desarrollo

### Estructura del Proyecto
```
cocktail-management-system/
├── app.py                    # Aplicación principal
├── deploy.py                 # Script de despliegue
├── requirements.txt          # Dependencias
├── .env                      # Variables de entorno
├── README.md                 # Documentación
├── database/                 # Scripts SQL
│   ├── schema.sql           # Esquema de BD
│   └── seed.sql             # Datos iniciales
├── pages/                    # Páginas de Streamlit
│   ├── dashboard.py         # Dashboard principal
│   ├── cocktails.py         # Gestión de cócteles
│   ├── inventario.py        # Gestión de inventario
│   └── usuarios.py          # Gestión de usuarios
├── db/                       # Módulo de base de datos
│   ├── db.py               # Conexión a BD
│   └── models.py           # Modelos de datos
├── utils/                    # Utilidades
│   └── helpers.py          # Funciones auxiliares
├── static/                   # Archivos estáticos
│   ├── css/                # Estilos CSS
│   └── images/             # Imágenes
└── web_scraping/            # Scripts de web scraping
    ├── apininja.py         # API Ninja integration
    ├── apiverve.py         # API Verve integration
    └── boozed.py           # BoozeAPI integration
```

### Desarrollo Local
```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# Ejecutar en modo desarrollo
streamlit run app.py --server.port=8501 --server.runOnSave=true
```

### Contribuir al Proyecto
1. **Fork** el repositorio
2. **Crea una rama** para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. **Abre un Pull Request**

## 🐛 Solución de Problemas

### Problemas Comunes

#### Error de Conexión a BD
```
❌ Error: Can't connect to MySQL server
✅ Solución: Verifica que MySQL esté ejecutándose y las credenciales en .env sean correctas
```

#### Error de Dependencias
```
❌ Error: Module not found
✅ Solución: Ejecuta `pip install -r requirements.txt` nuevamente
```

#### Error de Puerto
```
❌ Error: Port 8501 is already in use
✅ Solución: Cambia el puerto con `--server.port=8502`
```

### Logs y Depuración
- Los logs se guardan en el directorio `logs/`
- Activa el modo debug en desarrollo
- Usa `st.write()` para debugging en Streamlit

## 🔐 Seguridad

### Mejores Prácticas
- **Cambia las contraseñas por defecto**
- **Usa HTTPS en producción**
- **Implementa rate limiting**
- **Valida todas las entradas**
- **Mantén las dependencias actualizadas**

### Configuración de Seguridad
```python
# En producción, usa variables de entorno
SECRET_KEY = os.getenv('SECRET_KEY')
JWT_SECRET = os.getenv('JWT_SECRET')
DB_PASS = os.getenv('DB_PASS')
```

## 📞 Soporte

### Documentación Adicional
- [Wiki del Proyecto](https://github.com/tu-usuario/cocktail-management-system/wiki)
- [Documentación de API](https://github.com/tu-usuario/cocktail-management-system/docs)
- [Guía de Usuario](https://github.com/tu-usuario/cocktail-management-system/guide)

### Comunidad
- **Issues**: Reporta bugs y solicita features
- **Discussions**: Participa en discusiones técnicas
- **Wiki**: Contribuye con documentación

### Contacto
- **Email**: soporte@cocktail-management.com
- **Issues**: [GitHub Issues](https://github.com/tu-usuario/cocktail-management-system/issues)

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🙏 Agradecimientos

- **Streamlit** por el framework increíble
- **Plotly** por las visualizaciones interactivas
- **MySQL** por el sistema de base de datos robusto
- **Comunidad Open Source** por las librerías y herramientas

---

## ⭐ Si te gustó este proyecto

¡No olvides dar una ⭐ si este proyecto te fue útil!

[![GitHub stars](https://img.shields.io/github/stars/tu-usuario/cocktail-management-system?style=social)](https://github.com/tu-usuario/cocktail-management-system/stargazers)

---

**Made with ❤️ and 🍸 by the Cocktail Management Team**