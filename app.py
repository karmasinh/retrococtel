import streamlit as st
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
from db.db import get_db_connection
from db.models import CocktailModel
from utils.helpers import UIComponents, ModalComponents, ChartComponents
import time

load_dotenv()

# Configuración de la página
st.set_page_config(
    page_title="🍸 Cocktail Management System",
    page_icon="🍸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar estilos CSS personalizados según tema del usuario
def load_theme_css(theme_name='default'):
    """Carga el CSS del tema especificado"""
    try:
        if theme_name == 'default':
            # Cargar tema por defecto
            with open('static/css/theme.css', 'r', encoding='utf-8') as f:
                css_content = f.read()
                st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)
        else:
            # Cargar tema específico
            theme_file = f'static/css/themes/{theme_name}.css'
            with open(theme_file, encoding='utf-8') as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f'Archivo de tema {theme_name} no encontrado, usando estilos por defecto')
        try:
            with open('static/css/theme.css', 'r', encoding='utf-8') as f:
                css_content = f.read()
                st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)
        except FileNotFoundError:
            # Estilos CSS de respaldo si no existe el archivo
            st.markdown("""
            <style>
            .stApp {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            .sidebar .sidebar-content {
                background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
            }
            .stButton>button {
                background: linear-gradient(135deg, #FF6B6B, #FF8E53);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 0.5rem 1rem;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            .stButton>button:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            .metric-card {
                background: white;
                padding: 1.5rem;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                margin: 0.5rem 0;
            }
            .cocktail-card {
                background: white;
                padding: 1rem;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                margin: 0.5rem 0;
                transition: all 0.3s ease;
            }
            .cocktail-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            }
            </style>
            """, unsafe_allow_html=True)

# Inicializar modelo
model = CocktailModel()

# Verificar autenticación - redirigir a login si no está autenticado
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.switch_page("pages/login.py")

else:
    # Cargar tema del usuario
    user_theme = st.session_state.user.get('tema_preferido', 'default')
    load_theme_css(user_theme)
    
    st.sidebar.markdown(f"**Usuario:** {st.session_state.user['nombre_completo']}")
    st.sidebar.markdown(f"**Rol:** {st.session_state.user['rol_nombre']}")

    # Perfil de usuario
    with st.sidebar.expander("👤 Perfil de Usuario", expanded=True):
        st.markdown(f"- Nombre: `{st.session_state.user['nombre_completo']}`")
        st.markdown(f"- Usuario: `{st.session_state.user.get('nombre_usuario', 'N/D')}`")
        st.markdown(f"- Rol: `{st.session_state.user['rol_nombre']}`")
        if st.session_state.user.get('email'):
            st.markdown(f"- Email: `{st.session_state.user['email']}`")
        st.markdown("- Preferencias: cambiar tema, cerrar sesión")
    
    # Selector de tema
    if 'user_theme' not in st.session_state:
        st.session_state.user_theme = st.session_state.user.get('tema_preferido', 'default')
    
    available_themes = ['default', 'dark', 'blue', 'green', 'purple']
    selected_theme = st.sidebar.selectbox(
        "🎨 Tema",
        available_themes,
        index=available_themes.index(st.session_state.user_theme)
    )
    
    if selected_theme != st.session_state.user_theme:
        st.session_state.user_theme = selected_theme
        # Actualizar tema en base de datos
        try:
            model.update_user_theme(st.session_state.user['id'], selected_theme)
            st.rerun()
        except Exception as e:
            st.error(f"Error actualizando tema: {e}")
    
    st.sidebar.divider()
    
    # Navegación principal
    st.sidebar.header("📋 Navegación")
    
    # Opciones de menú basadas en el rol del usuario
    menu_options = {
        "Dashboard": "📊",
        "Cócteles": "🍸",
        "Inventario": "📦",
        "Usuarios": "👥"
    }
    
    # Agregar opciones de administrador si el usuario es admin
    if st.session_state.user['rol_nombre'].lower() in ['admin', 'administrador']:
        menu_options["Roles"] = "🔐"
        menu_options["Configuración"] = "⚙️"
    
    # Crear radio buttons para navegación
    selected_page = st.sidebar.radio(
        "Seleccione una página:",
        list(menu_options.keys()),
        format_func=lambda x: f"{menu_options[x]} {x}"
    )
    
    st.sidebar.divider()
    
    # Botón de cerrar sesión
    if st.sidebar.button("🚪 Cerrar Sesión"):
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.user_theme = 'default'
        # Volver al login
        st.switch_page("pages/login.py")
        st.rerun()
    
    # Renderizar página seleccionada
    if selected_page == "Dashboard":
        # Importar y ejecutar el dashboard premium
        from pages.dashboard import render_dashboard_page
        render_dashboard_page()
    
    elif selected_page == "Cócteles":
        # Importar y ejecutar la página de cócteles
        from pages.cocktails import render_cocktails_page
        render_cocktails_page()
    
    elif selected_page == "Inventario":
        # Importar y ejecutar la página de inventario
        from pages.inventario import render_inventory_page
        render_inventory_page()
    
    elif selected_page == "Usuarios":
        # Importar y ejecutar la página de usuarios
        from pages.usuarios import render_usuarios_page
        render_usuarios_page()
    
    elif selected_page == "Roles":
        # Importar y ejecutar la página de roles
        from pages.roles import render_roles_page
        render_roles_page()
    
    elif selected_page == "Configuración":
        st.title("⚙️ Configuración")
        st.info("Panel de configuración del sistema (solo administradores)")
        
        # Test de conexión a BD
        if st.button("Probar Conexión a Base de Datos"):
            db = get_db_connection()
            result = db.test_connection()
            if "Conexión exitosa" in result:
                st.success(result)
            else:
                st.error(result)

# Footer
st.markdown("---")
st.markdown("Cocktail Dashboard v1.0.0 | Desarrollado con Streamlit 🍹")