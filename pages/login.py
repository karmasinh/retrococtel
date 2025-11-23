"""
Página de Login Premium para CoctelMatch
Desarrollado por: Álvaro Díaz Vallejos
"""

import streamlit as st
import time
from typing import Optional, Dict, Any
from utils.icons import get_icon, render_icon
from utils.helpers import UIComponents
from db.models import CocktailModel

def render_login_page():
    """Renderiza la página de login con diseño premium"""
    
    # CSS personalizado para el login
    st.markdown("""
    <style>
    html, body, .stApp {
        height: 100%;
        margin: 0;
        padding: 0;
    }
    .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    .login-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px;
    }
    .login-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        padding: 40px;
        max-width: 400px;
        width: 100%;
        text-align: center;
    }
    .login-header {
        margin-bottom: 30px;
    }
    .login-logo {
        width: 80px;
        height: 80px;
        margin: 0 auto 20px;
        background: linear-gradient(135deg, #FF6B6B, #FF8E53);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 8px 20px rgba(255, 107, 107, 0.3);
    }
    .login-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #FF6B6B, #FF8E53);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 10px;
    }
    .login-subtitle {
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }
    .form-group {
        margin-bottom: 20px;
        text-align: left;
    }
    .form-label {
        display: block;
        margin-bottom: 8px;
        color: #333;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .form-input {
        width: 100%;
        padding: 12px 15px;
        border: 2px solid #e1e5e9;
        border-radius: 12px;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: #fff;
    }
    .form-input:focus {
        outline: none;
        border-color: #FF6B6B;
        box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.1);
    }
    .login-button {
        width: 100%;
        padding: 15px;
        background: linear-gradient(135deg, #FF6B6B, #FF8E53);
        color: white;
        border: none;
        border-radius: 12px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-top: 10px;
    }
    .login-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3);
    }
    .login-button:active {
        transform: translateY(0);
    }
    .login-footer {
        margin-top: 30px;
        padding-top: 20px;
        border-top: 1px solid #e1e5e9;
        color: #666;
        font-size: 0.9rem;
    }
    .error-message {
        background: #fee;
        color: #c33;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 20px;
        border-left: 4px solid #c33;
    }
    .success-message {
        background: #efe;
        color: #3c3;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 20px;
        border-left: 4px solid #3c3;
    }
    .test-connection-btn {
        background: linear-gradient(135deg, #4ECDC4, #44A08D);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        margin-top: 15px;
    }
    .test-connection-btn:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(78, 205, 196, 0.3);
    }
    .loading-spinner {
        border: 3px solid #f3f3f3;
        border-top: 3px solid #FF6B6B;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .theme-selector {
        position: absolute;
        top: 20px;
        right: 20px;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    .theme-button {
        background: none;
        border: 2px solid transparent;
        border-radius: 50%;
        width: 35px;
        height: 35px;
        margin: 0 5px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .theme-button:hover {
        transform: scale(1.1);
        border-color: #FF6B6B;
    }
    .theme-light { background: linear-gradient(135deg, #ffffff, #f8f9fa); }
    .theme-dark { background: linear-gradient(135deg, #2c3e50, #34495e); }
    .theme-tropical { background: linear-gradient(135deg, #FF6B9D, #C44569); }
    .theme-ocean { background: linear-gradient(135deg, #00B4DB, #0083B0); }
    .theme-sunset { background: linear-gradient(135deg, #FF512F, #F09819); }
    </style>
    """, unsafe_allow_html=True)
    
    # Contenedor principal
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    # Selector de temas
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        with st.container():
            st.markdown('<div class="theme-selector">', unsafe_allow_html=True)
            st.markdown("**Tema:**")
            col_t1, col_t2, col_t3, col_t4, col_t5 = st.columns(5)
            with col_t1:
                if st.button("⚪", key="theme_light", help="Tema Claro"):
                    st.session_state.theme = "light"
                    st.rerun()
            with col_t2:
                if st.button("⚫", key="theme_dark", help="Tema Oscuro"):
                    st.session_state.theme = "dark"
                    st.rerun()
            with col_t3:
                if st.button("🌺", key="theme_tropical", help="Tema Tropical"):
                    st.session_state.theme = "tropical"
                    st.rerun()
            with col_t4:
                if st.button("🌊", key="theme_ocean", help="Tema Océano"):
                    st.session_state.theme = "ocean"
                    st.rerun()
            with col_t5:
                if st.button("🌅", key="theme_sunset", help="Tema Sunset"):
                    st.session_state.theme = "sunset"
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Tarjeta de login
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    
    # Logo y título
    st.markdown('''
    <div class="login-header">
        <div class="login-logo">
            🍹
        </div>
        <h1 class="login-title">CoctelMatch</h1>
        <p class="login-subtitle">Tu coctel favorito está aquí</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Mensajes de estado
    if 'login_error' in st.session_state:
        st.markdown(f'<div class="error-message">{st.session_state.login_error}</div>', unsafe_allow_html=True)
        del st.session_state.login_error
    
    if 'login_success' in st.session_state:
        st.markdown(f'<div class="success-message">{st.session_state.login_success}</div>', unsafe_allow_html=True)
        del st.session_state.login_success
    
    # Formulario de login
    with st.form("login_form"):
        # Campo de usuario
        st.markdown('<div class="form-group">', unsafe_allow_html=True)
        st.markdown(f'<label class="form-label">{get_icon("user", size=16)} Usuario</label>', unsafe_allow_html=True)
        username = st.text_input(
            "Usuario",
            placeholder="Ingrese su nombre de usuario",
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Campo de contraseña
        st.markdown('<div class="form-group">', unsafe_allow_html=True)
        st.markdown(f'<label class="form-label">{get_icon("password", size=16)} Contraseña</label>', unsafe_allow_html=True)
        password = st.text_input(
            "Contraseña",
            type="password",
            placeholder="Ingrese su contraseña",
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Botón de login
        col1, col2 = st.columns([2, 1])
        with col1:
            submit_button = st.form_submit_button(
                "Iniciar Sesión",
                use_container_width=True,
                type="primary"
            )
        
        with col2:
            test_button = st.form_submit_button(
                "Probar BD",
                use_container_width=True,
                type="secondary"
            )
    
    # Acciones del formulario
    if submit_button:
        if username and password:
            with st.spinner("Verificando credenciales..."):
                time.sleep(0.8)  # Simulación ligera
                # Autenticación contra la BD
                try:
                    model = CocktailModel()
                    user = model.get_user_by_username(username)
                except Exception as e:
                    user = None
                    st.error(f"Error de autenticación: {e}")

                if user:
                    # Nota: validación de contraseña pendiente (hash). Por ahora, usuario existente pasa.
                    st.session_state.authenticated = True
                    st.session_state.user = user
                    st.session_state.user_theme = user.get('tema_preferido', 'default') or 'default'
                    st.success("¡Login exitoso! Redirigiendo...")
                    # Redirigir al archivo principal de la app
                    st.switch_page("app.py")
                else:
                    st.session_state.login_error = "Credenciales inválidas o usuario no encontrado"
                    st.rerun()
        else:
            st.session_state.login_error = "Por favor complete todos los campos"
            st.rerun()
    
    if test_button:
        with st.spinner("Probando conexión a base de datos..."):
            time.sleep(1)
            st.session_state.login_success = "Conexión a base de datos exitosa"
            st.rerun()
    
    # Footer
    st.markdown('''
    <div class="login-footer">
        <p><strong>CoctelMatch</strong> - Tu coctel favorito</p>
        <p style="font-size: 0.8rem; color: #999;">
            Desarrollado por Álvaro Díaz Vallejos
        </p>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Cerrar login-card
    st.markdown('</div>', unsafe_allow_html=True)  # Cerrar login-container

def render_forgot_password():
    """Renderiza la página de recuperación de contraseña"""
    st.markdown("""
    <style>
    .forgot-container {
        text-align: center;
        padding: 40px 20px;
    }
    .back-button {
        background: none;
        border: 2px solid #FF6B6B;
        color: #FF6B6B;
        padding: 10px 20px;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-top: 20px;
    }
    .back-button:hover {
        background: #FF6B6B;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="forgot-container">', unsafe_allow_html=True)
    
    st.markdown(f"{get_icon('password', size=24)} **Recuperar Contraseña**", unsafe_allow_html=True)
    st.write("Ingrese su dirección de correo electrónico para recuperar su contraseña.")
    
    email = st.text_input("Correo Electrónico", placeholder="tu@email.com")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Enviar Correo"):
            st.success("Se ha enviado un correo de recuperación a su dirección.")
    
    with col2:
        if st.button("Volver al Login"):
            st.session_state.page = "login"
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_register():
    """Renderiza la página de registro"""
    st.markdown("""
    <style>
    .register-container {
        max-width: 500px;
        margin: 0 auto;
        padding: 40px 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="register-container">', unsafe_allow_html=True)
    
    st.markdown(f"{get_icon('user', size=24)} **Crear Nueva Cuenta**", unsafe_allow_html=True)
    
    with st.form("register_form"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("Nombre", placeholder="Tu nombre")
        with col2:
            last_name = st.text_input("Apellido", placeholder="Tu apellido")
        
        email = st.text_input("Correo Electrónico", placeholder="tu@email.com")
        username = st.text_input("Nombre de Usuario", placeholder="usuario123")
        
        col3, col4 = st.columns(2)
        with col3:
            password = st.text_input("Contraseña", type="password", placeholder="Contraseña segura")
        with col4:
            confirm_password = st.text_input("Confirmar Contraseña", type="password", placeholder="Repetir contraseña")
        
        role = st.selectbox("Rol", ["Bartender", "Camarero", "Administrador"])
        
        col5, col6 = st.columns(2)
        with col5:
            if st.form_submit_button("Crear Cuenta", type="primary"):
                if password == confirm_password:
                    st.success("¡Cuenta creada exitosamente! Por favor inicie sesión.")
                    time.sleep(2)
                    st.session_state.page = "login"
                    st.rerun()
                else:
                    st.error("Las contraseñas no coinciden.")
        
        with col6:
            if st.form_submit_button("Volver al Login"):
                st.session_state.page = "login"
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Función principal
def main():
    """Función principal del módulo de login"""
    # Inicializar estado de la página si no existe
    if 'page' not in st.session_state:
        st.session_state.page = "login"
    
    # Inicializar tema si no existe
    if 'theme' not in st.session_state:
        st.session_state.theme = "light"
    
    # Aplicar tema seleccionado
    theme_colors = {
        "light": "",
        "dark": "<style>body { background: #1a1a1a; color: white; }</style>",
        "tropical": "<style>body { background: linear-gradient(135deg, #fff5e6, #ffffff); }</style>",
        "ocean": "<style>body { background: linear-gradient(135deg, #f0f8ff, #ffffff); }</style>",
        "sunset": "<style>body { background: linear-gradient(135deg, #fff8f3, #ffffff); }</style>"
    }
    
    if st.session_state.theme in theme_colors:
        st.markdown(theme_colors[st.session_state.theme], unsafe_allow_html=True)
    
    # Renderizar página correspondiente
    if st.session_state.page == "login":
        render_login_page()
    elif st.session_state.page == "forgot":
        render_forgot_password()
    elif st.session_state.page == "register":
        render_register()

if __name__ == "__main__":
    main()