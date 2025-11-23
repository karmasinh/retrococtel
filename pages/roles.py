"""
👥 Página de Gestión de Roles
CRUD completo de roles con diseño profesional y permisos
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Any, Optional
import time
from datetime import datetime

# Importar componentes personalizados
from utils.helpers import UIComponents, ModalComponents, ChartComponents
from db.models import CocktailModel
from db.db import get_db_connection

def render_roles_page():
    """Renderizar la página completa de roles"""
    
    # Título principal con diseño moderno
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    ">
        <h1 style="margin: 0; font-size: 2.5em; font-weight: 700;">👥 Gestión de Roles</h1>
        <p style="margin: 10px 0 0 0; font-size: 1.1em; opacity: 0.9;">Administra roles y permisos del sistema</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicializar modelo de datos
    db_connection = get_db_connection()
    if not db_connection:
        st.error("❌ Error al conectar con la base de datos")
        return
    
    cocktail_model = CocktailModel()
    
    # Estado de la página
    if 'roles_page_state' not in st.session_state:
        st.session_state.roles_page_state = {
            'show_modal': False,
            'modal_mode': 'create',
            'selected_role': None,
            'search_term': '',
            'refresh_data': True
        }
    
    # Barra de herramientas superior
    col1, col2, col3 = st.columns([3, 2, 1])
    
    with col1:
        search_term = st.text_input("🔍 Buscar rol...", 
                                  value=st.session_state.roles_page_state['search_term'],
                                  placeholder="Ej: Administrador, Usuario...")
        st.session_state.roles_page_state['search_term'] = search_term
    
    with col2:
        # Filtros adicionales
        filter_options = ['Todos', 'Activos', 'Inactivos']
        filter_status = st.selectbox("📊 Filtrar por estado", filter_options)
    
    with col3:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        if st.button("➕ Nuevo Rol", type="primary", use_container_width=True):
            st.session_state.roles_page_state['show_modal'] = True
            st.session_state.roles_page_state['modal_mode'] = 'create'
            st.session_state.roles_page_state['selected_role'] = None
            st.rerun()
    
    # Métricas principales
    try:
        total_roles = cocktail_model.get_total_roles()
        active_roles = cocktail_model.get_active_roles_count()
        roles_by_permissions = cocktail_model.get_roles_by_permission_level()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            UIComponents.CardMetric("👥", "Total Roles", str(total_roles), 
                                  f"{active_roles} activos", "primary")
        
        with col2:
            avg_permissions = f"{len(roles_by_permissions)}" if roles_by_permissions else "0"
            UIComponents.CardMetric("🔐", "Niveles de Permiso", avg_permissions, 
                                  "Diferentes niveles", "accent")
        
        with col3:
            most_common_role = cocktail_model.get_most_common_role()
            role_name = most_common_role['nombre'] if most_common_role else "Ninguno"
            UIComponents.CardMetric("⭐", "Rol Más Común", role_name, 
                                  "Más asignado", "secondary")
        
        with col4:
            recent_roles = cocktail_model.get_recent_roles(limit=5)
            UIComponents.CardMetric("🆕", "Roles Recientes", str(len(recent_roles)), 
                                  "Últimos creados", "success")
    
    except Exception as e:
        st.error(f"Error al cargar métricas: {e}")
    
    # Contenido principal con tabs
    tab1, tab2, tab3 = st.tabs(["📋 Lista de Roles", "📊 Análisis", "🔧 Herramientas"])
    
    with tab1:
        render_roles_list(cocktail_model)
    
    with tab2:
        render_roles_analytics(cocktail_model)
    
    with tab3:
        render_tools_section(cocktail_model)
    
    # Modal para crear/editar roles
    if st.session_state.roles_page_state['show_modal']:
        render_role_modal(cocktail_model)

def render_roles_list(cocktail_model: CocktailModel):
    """Renderizar la lista de roles con diseño moderno"""
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
    ">
        <h3 style="margin: 0;">📋 Catálogo de Roles</h3>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        # Obtener roles con filtros
        search_term = st.session_state.roles_page_state['search_term']
        roles = cocktail_model.get_roles_filtered(search_term=search_term)
        
        if not roles:
            st.info("👥 No se encontraron roles con los filtros aplicados")
            return
        
        # Mostrar roles en grid responsive
        cols = st.columns(2)  # 2 columnas para desktop
        
        for idx, role in enumerate(roles):
            col_idx = idx % 2
            with cols[col_idx]:
                render_role_card(role, cocktail_model)
    
    except Exception as e:
        st.error(f"Error al cargar roles: {e}")

def render_role_card(role: Dict[str, Any], cocktail_model: CocktailModel):
    """Renderizar una card individual de rol con acciones"""
    
    # Contenedor principal
    with st.container():
        # Card con diseño moderno
        UIComponents.RoleCard(role)
        
        # Botones de acción
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("👁️ Ver", key=f"view_{role['id']}", use_container_width=True):
                show_role_details_modal(role, cocktail_model)
        
        with col2:
            if st.button("✏️ Editar", key=f"edit_{role['id']}", use_container_width=True):
                st.session_state.roles_page_state['show_modal'] = True
                st.session_state.roles_page_state['modal_mode'] = 'edit'
                st.session_state.roles_page_state['selected_role'] = role
                st.rerun()
        
        with col3:
            if role.get('nombre') != 'Administrador':  # No permitir eliminar el rol admin
                if st.button("🗑️ Eliminar", key=f"delete_{role['id']}", use_container_width=True, type="secondary"):
                    if st.checkbox(f"¿Confirmar eliminación de {role['nombre']}?", key=f"confirm_{role['id']}"):
                        try:
                            if cocktail_model.delete_role(role['id']):
                                ModalComponents.notification(f"✅ Rol {role['nombre']} eliminado exitosamente", "success")
                                st.session_state.roles_page_state['refresh_data'] = True
                                st.rerun()
                            else:
                                ModalComponents.notification("❌ Error al eliminar rol", "error")
                        except Exception as e:
                            ModalComponents.notification(f"❌ Error: {str(e)}", "error")

def render_roles_analytics(cocktail_model: CocktailModel):
    """Renderizar sección de análisis y estadísticas de roles"""
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #f093fb, #f5576c);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
    ">
        <h3 style="margin: 0;">📊 Análisis de Roles</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Gráfico de distribución de roles
        try:
            roles_distribution = cocktail_model.get_roles_distribution()
            if roles_distribution:
                fig = ChartComponents.create_roles_distribution_chart(roles_distribution)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("📊 No hay datos suficientes para mostrar gráficos")
        except Exception as e:
            st.error(f"Error al cargar distribución: {e}")
    
    with col2:
        # Estadísticas rápidas
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 15px;">
            <h4 style="color: #667eea; margin-bottom: 15px;">📈 Estadísticas</h4>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            stats = cocktail_model.get_role_statistics()
            
            st.metric("Total de Roles", stats.get('total_roles', 0))
            st.metric("Roles Activos", stats.get('active_roles', 0))
            st.metric("Usuarios Totales", stats.get('total_users', 0))
            
            # Top de roles más asignados
            if stats.get('top_roles'):
                st.markdown("**⭐ Roles más asignados:**")
                for role in stats['top_roles'][:5]:
                    st.write(f"• {role['nombre']}: {role['user_count']} usuarios")
        
        except Exception as e:
            st.error(f"Error al cargar estadísticas: {e}")

def render_tools_section(cocktail_model: CocktailModel):
    """Renderizar sección de herramientas y utilidades para roles"""
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #4facfe, #00f2fe);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
    ">
        <h3 style="margin: 0;">🔧 Herramientas</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 15px;">
            <h4 style="color: #667eea; margin-bottom: 15px;">📤 Importar/Exportar</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Botones de importar/exportar
        if st.button("📤 Exportar Roles (CSV)", use_container_width=True):
            try:
                roles = cocktail_model.get_all_roles()
                if roles:
                    df = pd.DataFrame(roles)
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="⬇️ Descargar CSV",
                        data=csv,
                        file_name=f"roles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                else:
                    st.warning("No hay roles para exportar")
            except Exception as e:
                st.error(f"Error al exportar: {e}")
        
        # Importar (placeholder)
        uploaded_file = st.file_uploader("📥 Importar desde CSV", type=['csv'])
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.write("📋 Vista previa del archivo:")
                st.dataframe(df.head())
                
                if st.button("✅ Confirmar Importación"):
                    ModalComponents.notification("✅ Importación completada", "success")
            except Exception as e:
                st.error(f"Error al importar: {e}")
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 15px;">
            <h4 style="color: #4facfe; margin-bottom: 15px;">🎨 Personalización</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Opciones de personalización
        if st.button("🎨 Generar Reporte de Permisos", use_container_width=True):
            try:
                report_data = generate_permissions_report(cocktail_model)
                st.json(report_data)
            except Exception as e:
                st.error(f"Error al generar reporte: {e}")
        
        if st.button("🔄 Actualizar Cache", use_container_width=True):
            st.session_state.roles_page_state['refresh_data'] = True
            ModalComponents.notification("✅ Cache actualizado", "success")
            st.rerun()

def render_role_modal(cocktail_model: CocktailModel):
    """Renderizar modal para crear/editar roles"""
    
    # Crear overlay para el modal
    modal_container = st.container()
    
    with modal_container:
        # Fondo semi-transparente
        st.markdown("""
        <div style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 999;
            display: flex;
            align-items: center;
            justify-content: center;
        ">
            <div style="
                background: white;
                border-radius: 20px;
                padding: 30px;
                max-width: 600px;
                max-height: 90vh;
                overflow-y: auto;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                position: relative;
                width: 90%;
            ">
        """, unsafe_allow_html=True)
        
        # Header del modal
        mode = st.session_state.roles_page_state['modal_mode']
        role_data = st.session_state.roles_page_state.get('selected_role')
        
        title = "👥 Crear Nuevo Rol" if mode == 'create' else f"✏️ Editar {role_data.get('nombre', 'Rol')}"
        
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"<h2 style='color: #667eea; margin-bottom: 20px;'>{title}</h2>", unsafe_allow_html=True)
        with col2:
            if st.button("❌ Cerrar", type="secondary"):
                st.session_state.roles_page_state['show_modal'] = False
                st.rerun()
        
        # Formulario principal
        with st.form("role_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div style="background: #f8f9fa; padding: 20px; border-radius: 15px; margin-bottom: 15px;">
                    <h4 style="color: #667eea; margin-bottom: 15px;">📋 Información Básica</h4>
                </div>
                """, unsafe_allow_html=True)
                
                nombre = st.text_input("👥 Nombre del Rol *", 
                                     value=role_data.get('nombre', '') if role_data else '',
                                     placeholder="Ej: Administrador, Bartender...",
                                     help="Nombre único del rol")
                
                descripcion = st.text_area("📝 Descripción",
                                         value=role_data.get('descripcion', '') if role_data else '',
                                         placeholder="Describe el propósito y responsabilidades del rol...")
                
                nivel_permiso = st.number_input("🔐 Nivel de Permiso *",
                                              min_value=1, max_value=10, 
                                              value=role_data.get('nivel_permiso', 1) if role_data else 1,
                                              help="1 = Mínimo, 10 = Máximo")
            
            with col2:
                st.markdown("""
                <div style="background: #f8f9fa; padding: 20px; border-radius: 15px; margin-bottom: 15px;">
                    <h4 style="color: #764ba2; margin-bottom: 15px;">⚙️ Configuración</h4>
                </div>
                """, unsafe_allow_html=True)
                
                estado = st.selectbox("📊 Estado *", 
                                    ['Activo', 'Inactivo'],
                                    index=0 if not role_data or int(role_data.get('estado', 1)) == 1 else 1)
                
                # Configuración adicional
                st.markdown("**⚙️ Configuración del Rol:**")
                
                # Información adicional que puede ser útil
                st.info("💡 El nivel de permiso determina el acceso a funciones del sistema")
            
            # Botones de acción
            col_btn1, col_btn2 = st.columns([1, 1])
            
            with col_btn1:
                submit_button = st.form_submit_button("💾 Guardar Rol", type="primary", use_container_width=True)
            
            with col_btn2:
                cancel_button = st.form_submit_button("❌ Cancelar", type="secondary", use_container_width=True)
            
            if submit_button:
                try:
                    # Validar datos
                    if not nombre.strip():
                        st.error("❌ El nombre del rol es obligatorio")
                        return
                    
                    # Preparar datos del rol (versión simplificada)
                    estado_val = 1 if estado == 'Activo' else 0
                    role_data_dict = {
                        'nombre': nombre.strip(),
                        'descripcion': descripcion.strip(),
                        'nivel_permiso': nivel_permiso,
                        'estado': estado_val
                    }
                    
                    # Guardar en la base de datos
                    if mode == 'create':
                        success = cocktail_model.create_role(role_data_dict)
                        message = "✅ Rol creado exitosamente"
                    else:
                        role_data_dict['id'] = role_data['id']
                        success = cocktail_model.update_role(role_data_dict)
                        message = "✅ Rol actualizado exitosamente"
                    
                    if success:
                        ModalComponents.notification(message, "success")
                        st.session_state.roles_page_state['show_modal'] = False
                        st.session_state.roles_page_state['refresh_data'] = True
                        st.rerun()
                    else:
                        ModalComponents.notification("❌ Error al guardar rol", "error")
                
                except Exception as e:
                    ModalComponents.notification(f"❌ Error: {str(e)}", "error")
            
            if cancel_button:
                st.session_state.roles_page_state['show_modal'] = False
                st.rerun()
        
        st.markdown("</div></div>", unsafe_allow_html=True)

def show_role_details_modal(role: Dict[str, Any], cocktail_model: CocktailModel):
    """Mostrar modal con detalles completos del rol"""
    
    with st.container():
        st.markdown("""
        <div style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 999;
            display: flex;
            align-items: center;
            justify-content: center;
        ">
            <div style="
                background: white;
                border-radius: 20px;
                padding: 30px;
                max-width: 500px;
                max-height: 80vh;
                overflow-y: auto;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                position: relative;
                width: 90%;
            ">
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"<h2 style='color: #667eea; margin-bottom: 20px;'>👥 Detalles del Rol</h2>", unsafe_allow_html=True)
        with col2:
            if st.button("❌ Cerrar", type="secondary"):
                st.rerun()
        
        # Información del rol
        display_estado = 'Activo' if int(role.get('estado', 1)) == 1 else 'Inactivo'
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 15px; margin-bottom: 15px;">
            <h4 style="color: #667eea; margin-bottom: 15px;">{role['nombre']}</h4>
            <p><strong>📝 Descripción:</strong> {role.get('descripcion', 'Sin descripción')}</p>
            <p><strong>🔐 Nivel de Permiso:</strong> {role.get('nivel_permiso', 'N/A')}</p>
            <p><strong>📊 Estado:</strong> {display_estado}</p>
            <p><strong>📅 Fecha de Creación:</strong> {role.get('fecha_creacion', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Información del sistema
        st.markdown("**⚙️ Información del Sistema:**")
        st.write(f"📊 **Nivel de Permiso:** {role.get('nivel_permiso', 'N/A')}")
        st.write(f"📅 **Estado:** {role.get('estado', 'Activo')}")
        
        # Información adicional
        st.info("💡 Los permisos y accesos están determinados por el nivel de permiso del rol")
        
        # Usuarios con este rol
        try:
            users_with_role = cocktail_model.get_users_by_role(role['id'])
            if users_with_role:
                st.markdown(f"**👥 Usuarios con este rol ({len(users_with_role)}):**")
                for user in users_with_role[:5]:  # Mostrar máximo 5
                    st.write(f"• {user['nombre_completo']} ({user['email']})")
                if len(users_with_role) > 5:
                    st.write(f"... y {len(users_with_role) - 5} más")
            else:
                st.info("No hay usuarios asignados a este rol")
        except Exception as e:
            st.error(f"Error al cargar usuarios: {e}")
        
        st.markdown("</div></div>", unsafe_allow_html=True)

def generate_permissions_report(cocktail_model: CocktailModel) -> Dict[str, Any]:
    """Generar reporte completo de permisos y roles"""
    
    try:
        roles = cocktail_model.get_all_roles()
        total_users = cocktail_model.get_total_users()
        
        report = {
            'fecha_generacion': datetime.now().isoformat(),
            'total_roles': len(roles),
            'total_usuarios': total_users,
            'roles_detalle': []
        }
        
        for role in roles:
            role_detail = {
                'nombre': role['nombre'],
                'nivel_permiso': role.get('nivel_permiso', 1),
                'estado': role.get('estado', 'Activo'),
                'usuarios_asignados': len(cocktail_model.get_users_by_role(role['id']))
            }
            report['roles_detalle'].append(role_detail)
        
        return report
    
    except Exception as e:
        return {'error': str(e)}

if __name__ == "__main__":
    render_roles_page()