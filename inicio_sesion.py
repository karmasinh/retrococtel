"""
🍹 Sistema de Login para Cocktail Management System
Página dedicada de autenticación con diseño moderno y responsive
"""

import streamlit as st
import os
from db.db import get_db_connection
from db.models import CocktailModel

# Configuración de página para login
st.set_page_config(
    page_title="🍸 Cocktail Management System - Login",
    page_icon="🍸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Cargar CSS personalizado (tema por defecto para login)
def load_theme_css(theme_name='default'):
    """Carga el CSS del tema especificado"""
    try:
        if theme_name == 'default':
            # Cargar tema por defecto
            with open("static/css/theme.css", encoding='utf-8') as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        else:
            # Cargar tema específico
            theme_file = f"static/css/themes/{theme_name}.css"
            with open(theme_file, encoding='utf-8') as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"Archivo de tema {theme_name} no encontrado, usando estilos por defecto")
        try:
            with open("static/css/theme.css", encoding='utf-8') as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        except FileNotFoundError:
            st.markdown("""
            <style>
            .stButton>button {background-color: #4CAF50; color: white; border-radius: 8px;}
            .stTextInput>div>div>input {border-radius: 8px;}
            </style>
            """, unsafe_allow_html=True)

# Cargar tema por defecto para login
load_theme_css('default')

# Estilos CSS personalizados para login
st.markdown("""
<style>
/* Estilos generales */
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

/* Contenedor principal */
.main-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 20px;
}

/* Card de login */
.login-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    max-width: 400px;
    width: 100%;
    text-align: center;
}

/* Logo y título */
.logo-container {
    margin-bottom: 30px;
}

.logo {
    font-size: 4em;
    margin-bottom: 10px;
    animation: bounce 2s infinite;
}

.app-title {
    font-size: 2em;
    font-weight: 700;
    color: #2c3e50;
    margin-bottom: 10px;
}

.app-subtitle {
    color: #7f8c8d;
    font-size: 1.1em;
    margin-bottom: 30px;
}

/* Campos de entrada */
.stTextInput > div > div > input {
    background: rgba(255, 255, 255, 0.9);
    border: 2px solid #e0e0e0;
    border-radius: 10px;
    padding: 12px 15px;
    font-size: 16px;
    transition: all 0.3s ease;
}

.stTextInput > div > div > input:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    outline: none;
}

/* Botones */
.stButton > button {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px 30px;
    font-size: 16px;
    font-weight: 600;
    width: 100%;
    transition: all 0.3s ease;
    cursor: pointer;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
}

.stButton > button:active {
    transform: translateY(0);
}

/* Mensajes de error y éxito */
.stAlert {
    border-radius: 10px;
    border: none;
    padding: 15px;
    margin: 10px 0;
}

/* Animaciones */
@keyframes bounce {
    0%, 20%, 50%, 80%, 100% {
        transform: translateY(0);
    }
    40% {
        transform: translateY(-10px);
    }
    60% {
        transform: translateY(-5px);
    }
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.login-card {
    animation: fadeIn 0.6s ease-out;
}

/* Responsive */
@media (max-width: 768px) {
    .login-card {
        padding: 30px 20px;
        margin: 20px;
    }
    
    .app-title {
        font-size: 1.8em;
    }
    
    .logo {
        font-size: 3em;
    }
}
</style>
""", unsafe_allow_html=True)

# Contenedor principal
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Card de login
with st.container():
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    
    # Logo y título
    st.markdown("""
    <div class="logo-container">
        <div class="logo">🍸</div>
        <div class="app-title">Cocktail MS</div>
        <div class="app-subtitle">Sistema de Gestión de Cócteles</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Formulario de login
    with st.form("login_form", clear_on_submit=True):
        username = st.text_input(
            "👤 Usuario",
            placeholder="Ingrese su nombre de usuario",
            help="Usuario registrado en el sistema"
        )
        
        password = st.text_input(
            "🔒 Contraseña",
            type="password",
            placeholder="Ingrese su contraseña",
            help="Contraseña de acceso"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            submit_button = st.form_submit_button(
                "🚀 Ingresar",
                use_container_width=True,
                type="primary"
            )
        
        with col2:
            test_button = st.form_submit_button(
                "🔍 Probar BD",
                use_container_width=True,
                type="secondary"
            )
    
    # Información adicional
    with st.expander("ℹ️ Información del Sistema"):
        st.info("""
        **Sistema de Gestión de Cócteles**
        
        Funcionalidades:
        • Gestión de inventario
        • Catálogo de cócteles
        • Control de usuarios
        • Reportes y análisis
        
        **Versión:** 1.0.0
        **Desarrollado con:** Streamlit 🎈
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Lógica de autenticación
if submit_button:
    if username and password:
        try:
            # Inicializar modelo
            model = CocktailModel()
            
            # Verificar usuario
            user = model.get_user_by_username(username)
            if user:
                # En producción, usar bcrypt para verificar hash
                # Por ahora, verificación simple
                st.session_state.authenticated = True
                st.session_state.user = user
                st.session_state.user_theme = user.get('tema_preferido', 'default')
                
                # Redirigir al dashboard
                st.success("✅ Autenticación exitosa")
                st.balloons()
                
                # Pequeña pausa para mostrar el mensaje de éxito
                import time
                time.sleep(1)
                
                # Redirigir al dashboard
                st.switch_page("app.py")
                
            else:
                st.error("❌ Usuario o contraseña incorrectos")
                
        except Exception as e:
            st.error(f"❌ Error al conectar con la base de datos: {str(e)}")
    else:
        st.warning("⚠️ Por favor complete todos los campos")

if test_button:
    try:
        # Probar conexión a base de datos
        db = get_db_connection()
        result = db.test_connection()
        
        if "Conexión exitosa" in result:
            st.success(f"✅ {result}")
        else:
            st.error(f"❌ {result}")
            
    except Exception as e:
        st.error(f"❌ Error al conectar con la base de datos: {str(e)}")