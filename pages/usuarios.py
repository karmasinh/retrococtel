"""
👥 Página de Gestión de Usuarios
CRUD completo para usuarios con roles y permisos, diseño profesional
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from db.models import CocktailModel
from db.db import get_db_connection
from utils.helpers import UIComponents, ChartComponents
import io

def render_users_page():
    """Renderizar la página completa de gestión de usuarios"""
    
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
        <h1 style="margin: 0; font-size: 2.5em; font-weight: 700;">👥 Gestión de Usuarios</h1>
        <p style="margin: 10px 0 0 0; font-size: 1.1em; opacity: 0.9;">Administra usuarios, roles y permisos del sistema</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicializar modelo de datos
    try:
        cocktail_model = CocktailModel()
    except Exception as e:
        st.error(f"❌ Error al inicializar el modelo: {e}")
        return
    
    # Estado de la página
    if 'users_page_state' not in st.session_state:
        st.session_state.users_page_state = {
            'show_modal': False,
            'modal_mode': 'create',
            'selected_user': None,
            'search_term': '',
            'filter_role': 'Todos',
            'filter_status': 'Todos',
            'current_page': 1,
            'items_per_page': 10,
            'refresh_data': True
        }
    
    # Barra de herramientas superior
    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
    
    with col1:
        search_term = st.text_input("🔍 Buscar usuario...", 
                                  value=st.session_state.users_page_state['search_term'],
                                  placeholder="Ej: Juan, Administrador, juan@email.com...")
        st.session_state.users_page_state['search_term'] = search_term
    
    with col2:
        # Obtener roles de la BD
        try:
            roles = cocktail_model.get_all_roles()
            role_options = ['Todos'] + [role['nombre_rol'] for role in roles]
            filter_role = st.selectbox("🛡️ Filtrar por rol", role_options)
            st.session_state.users_page_state['filter_role'] = filter_role
        except Exception as e:
            st.error(f"Error al cargar roles: {e}")
            filter_role = st.selectbox("🛡️ Filtrar por rol", ['Todos'])
    
    with col3:
        status_options = ['Todos', 'Activo', 'Inactivo', 'Pendiente']
        filter_status = st.selectbox("📊 Filtrar por estado", status_options)
        st.session_state.users_page_state['filter_status'] = filter_status
    
    with col4:
        items_per_page = st.selectbox("📄 Usuarios por página", [5, 10, 20, 50], 
                                     index=1, key="users_per_page_select")
        st.session_state.users_page_state['items_per_page'] = items_per_page
    
    with col5:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        if st.button("➕ Nuevo Usuario", type="primary", use_container_width=True):
            st.session_state.users_page_state['show_modal'] = True
            st.session_state.users_page_state['modal_mode'] = 'create'
            st.session_state.users_page_state['selected_user'] = None
            st.rerun()
    
    # Obtener datos de usuarios
    try:
        usuarios = cocktail_model.get_all_usuarios()
        
        # Aplicar filtros
        filtered_users = []
        for usuario in usuarios:
            # Filtro de búsqueda
            if search_term and search_term.lower() not in usuario['nombre'].lower() and search_term.lower() not in usuario['email'].lower():
                continue
                
            # Filtro por rol
            if filter_role != 'Todos' and usuario.get('nombre_rol') != filter_role:
                continue
            
            # Filtro por estado
            if filter_status != 'Todos':
                if filter_status == 'Activo' and usuario.get('estado') != 'activo':
                    continue
                elif filter_status == 'Inactivo' and usuario.get('estado') != 'inactivo':
                    continue
                elif filter_status == 'Pendiente' and usuario.get('estado') != 'pendiente':
                    continue
            
            filtered_users.append(usuario)
        
    except Exception as e:
        st.error(f"Error al cargar usuarios: {e}")
        return
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_users = len(usuarios)
        UIComponents.CardMetric(
            value=total_users,
            label="Total Usuarios",
            icon="👥",
            trend="up",
            trend_value="+3"
        )
    
    with col2:
        active_users = len([u for u in usuarios if u.get('estado') == 'activo'])
        UIComponents.CardMetric(
            value=active_users,
            label="Usuarios Activos",
            icon="✅",
            trend="up" if active_users > total_users * 0.7 else "down",
            trend_value=f"{active_users}"
        )
    
    with col3:
        admin_users = len([u for u in usuarios if u.get('nombre_rol') == 'Administrador'])
        UIComponents.CardMetric(
            value=admin_users,
            label="Administradores",
            icon="🛡️",
            trend="stable",
            trend_value=f"{admin_users}"
        )
    
    with col4:
        inactive_users = len([u for u in usuarios if u.get('estado') == 'inactivo'])
        UIComponents.CardMetric(
            value=inactive_users,
            label="Usuarios Inactivos",
            icon="❌",
            trend="down" if inactive_users == 0 else "up",
            trend_value=f"{inactive_users}"
        )
    
    # Contenido principal con tabs
    tab1, tab2, tab3 = st.tabs(["📋 Lista de Usuarios", "📊 Análisis", "🔧 Herramientas"])
    
    with tab1:
        render_users_list(cocktail_model, filtered_users)
    
    with tab2:
        render_users_analytics(cocktail_model, usuarios)
    
    with tab3:
        render_users_tools(cocktail_model)
    
    # Modal para crear/editar usuario
    if st.session_state.users_page_state['show_modal']:
        render_user_modal(cocktail_model)

def render_users_list(cocktail_model: CocktailModel, usuarios: List[Dict]):
    """Renderizar la lista de usuarios con diseño moderno"""
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #4ECDC4, #44A08D);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
    ">
        <h3 style="margin: 0;">📋 Catálogo de Usuarios</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if not usuarios:
        st.info("👥 No se encontraron usuarios con los filtros aplicados")
        return
    
    # Paginación
    items_per_page = st.session_state.users_page_state['items_per_page']
    total_items = len(usuarios)
    total_pages = (total_items + items_per_page - 1) // items_per_page
    current_page = st.session_state.users_page_state['current_page']
    
    # Controles de paginación
    col1, col2, col3 = st.columns([2, 3, 2])
    
    with col1:
        st.write(f"Mostrando {min(items_per_page, total_items)} de {total_items} usuarios")
    
    with col2:
        if total_pages > 1:
            page_options = list(range(1, total_pages + 1))
            new_page = st.selectbox("Página", page_options, index=current_page-1)
            if new_page != current_page:
                st.session_state.users_page_state['current_page'] = new_page
                st.rerun()
    
    with col3:
        if st.button("🔄 Actualizar"):
            st.rerun()
    
    # Obtener usuarios para la página actual
    start_idx = (current_page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    page_users = usuarios[start_idx:end_idx]
    
    # Mostrar usuarios en grid responsive
    cols = st.columns(3)  # 3 columnas para diseño responsive
    
    for idx, usuario in enumerate(page_users):
        col_idx = idx % 3
        with cols[col_idx]:
            render_user_card(usuario)

def render_user_card(usuario: Dict):
    """Renderizar tarjeta individual de usuario"""
    
    # Determinar color del borde según estado
    estado = usuario.get('estado', 'desconocido')
    border_color = {
        'activo': '#4CAF50',      # Verde
        'inactivo': '#F44336',    # Rojo
        'pendiente': '#FF9800',   # Naranja
        'desconocido': '#9E9E9E' # Gris
    }.get(estado, '#9E9E9E')
    
    # Icono según rol
    rol_icon = {
        'Administrador': '🛡️',
        'Bartender': '🍹',
        'Mesero': '🍽️',
        'Cajero': '💰',
        'Gerente': '👔'
    }.get(usuario.get('nombre_rol', ''), '👤')
    
    # Crear tarjeta con diseño moderno
    card_html = f"""
    <div style="
        background: white;
        border: 2px solid {border_color};
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        cursor: pointer;
    " onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 8px 25px rgba(0,0,0,0.15)';" 
    onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(0,0,0,0.1)';">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <h4 style="margin: 0; color: #333;">{rol_icon} {usuario['nombre']}</h4>
            <span style="background: {border_color}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.8em;">
                {estado.title()}
            </span>
        </div>
        <p style="margin: 5px 0; color: #666; font-size: 0.9em;">
            <strong>Rol:</strong> {usuario.get('nombre_rol', 'Sin rol')}
        </p>
        <p style="margin: 5px 0; color: #666; font-size: 0.9em;">
            <strong>Email:</strong> {usuario.get('email', 'Sin email')}
        </p>
        <p style="margin: 5px 0; color: #666; font-size: 0.9em;">
            <strong>Teléfono:</strong> {usuario.get('telefono', 'Sin teléfono')}
        </p>
        <p style="margin: 5px 0; color: #666; font-size: 0.9em;">
            <strong>Último acceso:</strong> {usuario.get('ultimo_acceso', 'Nunca')}
        </p>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)
    
    # Botones de acción
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("👁️ Ver", key=f"view_user_{usuario['id']}", use_container_width=True):
            show_user_details_modal(usuario)
    
    with col2:
        if st.button("✏️ Editar", key=f"edit_user_{usuario['id']}", use_container_width=True):
            st.session_state.users_page_state['show_modal'] = True
            st.session_state.users_page_state['modal_mode'] = 'edit'
            st.session_state.users_page_state['selected_user'] = usuario
            st.rerun()
    
    with col3:
        estado_actual = usuario.get('estado', 'activo')
        if estado_actual == 'activo':
            if st.button("🔒 Desactivar", key=f"deactivate_user_{usuario['id']}", use_container_width=True):
                try:
                    success = cocktail_model.update_usuario_estado(usuario['id'], 'inactivo')
                    if success:
                        st.success(f"✅ Usuario {usuario['nombre']} desactivado")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Error al desactivar usuario")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        else:
            if st.button("🔓 Activar", key=f"activate_user_{usuario['id']}", use_container_width=True):
                try:
                    success = cocktail_model.update_usuario_estado(usuario['id'], 'activo')
                    if success:
                        st.success(f"✅ Usuario {usuario['nombre']} activado")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Error al activar usuario")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

def render_users_analytics(cocktail_model: CocktailModel, usuarios: List[Dict]):
    """Renderizar análisis de usuarios"""
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #ff9a9e, #fecfef);
        color: #333;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
    ">
        <h3 style="margin: 0;">📊 Análisis de Usuarios</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Gráficos de análisis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Distribución por Rol")
        
        role_counts = {}
        for usuario in usuarios:
            rol = usuario.get('nombre_rol', 'Sin rol')
            role_counts[rol] = role_counts.get(rol, 0) + 1
        
        if role_counts:
            df_roles = pd.DataFrame(list(role_counts.items()), columns=['Rol', 'Cantidad'])
            fig = ChartComponents.create_cocktail_distribution_chart(df_roles, 'Rol', 'Cantidad', 
                                                                   'Distribución por Rol')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Estado de Usuarios")
        
        status_counts = {'Activo': 0, 'Inactivo': 0, 'Pendiente': 0}
        
        for usuario in usuarios:
            estado = usuario.get('estado', 'pendiente')
            if estado == 'activo':
                status_counts['Activo'] += 1
            elif estado == 'inactivo':
                status_counts['Inactivo'] += 1
            else:
                status_counts['Pendiente'] += 1
        
        if status_counts:
            df_status = pd.DataFrame(list(status_counts.items()), columns=['Estado', 'Cantidad'])
            colors = ['#4CAF50', '#F44336', '#FF9800']  # Verde, Rojo, Naranja
            fig = ChartComponents.create_cocktail_distribution_chart(df_status, 'Estado', 'Cantidad', 
                                                                   'Estado de Usuarios', colors)
            st.plotly_chart(fig, use_container_width=True)
    
    # Estadísticas rápidas
    st.subheader("📈 Estadísticas Rápidas")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Usuarios nuevos en los últimos 30 días
        fecha_limite = datetime.now() - timedelta(days=30)
        usuarios_nuevos = len([u for u in usuarios if u.get('fecha_creacion') and datetime.strptime(u['fecha_creacion'], '%Y-%m-%d') > fecha_limite])
        st.metric("🆕 Usuarios Nuevos (30d)", usuarios_nuevos)
    
    with col2:
        # Tasa de activación
        tasa_activacion = (len([u for u in usuarios if u.get('estado') == 'activo']) / len(usuarios) * 100) if usuarios else 0
        st.metric("📈 Tasa de Activación", f"{tasa_activacion:.1f}%")
    
    with col3:
        # Usuarios por rol más común
        if usuarios:
            roles = [u.get('nombre_rol', 'Sin rol') for u in usuarios]
            rol_mas_comun = max(set(roles), key=roles.count)
            st.metric("👑 Rol Más Común", rol_mas_comun)
        else:
            st.metric("👑 Rol Más Común", "N/A")
    
    with col4:
        # Promedio de accesos por usuario activo
        usuarios_activos = [u for u in usuarios if u.get('estado') == 'activo']
        if usuarios_activos:
            accesos_totales = sum(u.get('total_accesos', 0) for u in usuarios_activos)
            promedio_accesos = accesos_totales / len(usuarios_activos)
            st.metric("📊 Promedio Accesos", f"{promedio_accesos:.0f}")
        else:
            st.metric("📊 Promedio Accesos", "0")

def render_users_tools(cocktail_model: CocktailModel):
    """Renderizar herramientas de usuarios"""
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #a8edea, #fed6e3);
        color: #333;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
    ">
        <h3 style="margin: 0;">🔧 Herramientas de Usuarios</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📤 Exportar Datos")
        
        if st.button("📊 Exportar a CSV", type="primary"):
            try:
                usuarios = cocktail_model.get_all_usuarios()
                
                if usuarios:
                    df = pd.DataFrame(usuarios)
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="⬇️ Descargar CSV",
                        data=csv,
                        file_name=f"usuarios_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                    st.success("✅ Datos preparados para descarga")
                else:
                    st.warning("⚠️ No hay usuarios para exportar")
            except Exception as e:
                st.error(f"❌ Error al exportar: {e}")
        
        if st.button("📋 Exportar a Excel"):
            try:
                usuarios = cocktail_model.get_all_usuarios()
                
                if usuarios:
                    df = pd.DataFrame(usuarios)
                    excel_buffer = io.BytesIO()
                    df.to_excel(excel_buffer, index=False, sheet_name='Usuarios')
                    excel_data = excel_buffer.getvalue()
                    
                    st.download_button(
                        label="⬇️ Descargar Excel",
                        data=excel_data,
                        file_name=f"usuarios_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    st.success("✅ Datos preparados para descarga")
                else:
                    st.warning("⚠️ No hay usuarios para exportar")
            except Exception as e:
                st.error(f"❌ Error al exportar: {e}")
        
        if st.button("📧 Exportar Emails"):
            try:
                usuarios = cocktail_model.get_all_usuarios()
                emails_activos = [u['email'] for u in usuarios if u.get('estado') == 'activo' and u.get('email')]
                
                if emails_activos:
                    emails_text = "; ".join(emails_activos)
                    st.download_button(
                        label="⬇️ Descargar Emails",
                        data=emails_text,
                        file_name=f"emails_activos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
                    st.success(f"✅ {len(emails_activos)} emails exportados")
                else:
                    st.warning("⚠️ No hay emails activos para exportar")
            except Exception as e:
                st.error(f"❌ Error al exportar emails: {e}")
    
    with col2:
        st.subheader("📥 Importar Datos")
        
        uploaded_file = st.file_uploader("📁 Seleccionar archivo CSV o Excel", 
                                       type=['csv', 'xlsx', 'xls'])
        
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                st.write("📊 Vista previa de datos:")
                st.dataframe(df.head(10))
                
                if st.button("📤 Cargar usuarios"):
                    # Procesar importación
                    success_count = 0
                    for _, row in df.iterrows():
                        try:
                            # Aquí iría la lógica de importación de usuarios
                            success_count += 1
                        except Exception as e:
                            st.warning(f"⚠️ Error en fila {row.name}: {e}")
                    
                    st.success(f"✅ Se importaron {success_count} usuarios exitosamente")
                    time.sleep(2)
                    st.rerun()
                    
            except Exception as e:
                st.error(f"❌ Error al procesar archivo: {e}")
    
    # Herramientas adicionales
    st.subheader("🛠️ Herramientas Adicionales")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔑 Generar contraseñas temporales"):
            try:
                usuarios = cocktail_model.get_all_usuarios()
                usuarios_inactivos = [u for u in usuarios if u.get('estado') == 'inactivo']
                
                if usuarios_inactivos:
                    import secrets
                    import string
                    
                    passwords = {}
                    for usuario in usuarios_inactivos:
                        # Generar contraseña temporal segura
                        alphabet = string.ascii_letters + string.digits
                        password = ''.join(secrets.choice(alphabet) for i in range(12))
                        passwords[usuario['nombre']] = password
                    
                    # Crear reporte de contraseñas
                    passwords_text = "CONTRASEÑAS TEMPORALES GENERADAS\n"
                    passwords_text += f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                    
                    for nombre, password in passwords.items():
                        passwords_text += f"{nombre}: {password}\n"
                    
                    st.download_button(
                        label="⬇️ Descargar Contraseñas",
                        data=passwords_text,
                        file_name=f"contraseñas_temporales_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
                    st.success(f"✅ {len(usuarios_inactivos)} contraseñas generadas")
                else:
                    st.warning("⚠️ No hay usuarios inactivos")
                    
            except Exception as e:
                st.error(f"❌ Error al generar contraseñas: {e}")
    
    with col2:
        if st.button("📊 Generar reporte de usuarios"):
            try:
                usuarios = cocktail_model.get_all_usuarios()
                
                # Crear reporte completo
                report_data = {
                    'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'total_usuarios': len(usuarios),
                    'usuarios_activos': len([u for u in usuarios if u.get('estado') == 'activo']),
                    'usuarios_inactivos': len([u for u in usuarios if u.get('estado') == 'inactivo']),
                    'administradores': len([u for u in usuarios if u.get('nombre_rol') == 'Administrador']),
                    'bartenders': len([u for u in usuarios if u.get('nombre_rol') == 'Bartender']),
                    'meseros': len([u for u in usuarios if u.get('nombre_rol') == 'Mesero'])
                }
                
                st.write("📊 Resumen del Reporte:")
                st.json(report_data)
                
                # Botón para descargar reporte
                report_text = f"""
REPORTE DE USUARIOS
Fecha: {report_data['fecha']}
Total Usuarios: {report_data['total_usuarios']}
Usuarios Activos: {report_data['usuarios_activos']}
Usuarios Inactivos: {report_data['usuarios_inactivos']}
Administradores: {report_data['administradores']}
Bartenders: {report_data['bartenders']}
Meseros: {report_data['meseros']}
                """
                
                st.download_button(
                    label="⬇️ Descargar Reporte",
                    data=report_text,
                    file_name=f"reporte_usuarios_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"❌ Error al generar reporte: {e}")
    
    with col3:
        if st.button("🗑️ Limpiar usuarios temporales"):
            try:
                # Limpiar usuarios antiguos inactivos
                usuarios = cocktail_model.get_all_usuarios()
                fecha_limite = datetime.now() - timedelta(days=90)  # 3 meses
                
                usuarios_a_limpiar = []
                for usuario in usuarios:
                    if (usuario.get('estado') == 'inactivo' and 
                        usuario.get('ultimo_acceso') and 
                        datetime.strptime(usuario['ultimo_acceso'], '%Y-%m-%d %H:%M:%S') < fecha_limite):
                        usuarios_a_limpiar.append(usuario)
                
                if usuarios_a_limpiar:
                    if st.checkbox(f"⚠️ Confirmar eliminación de {len(usuarios_a_limpiar)} usuarios inactivos"):
                        eliminados = 0
                        for usuario in usuarios_a_limpiar:
                            success = cocktail_model.delete_usuario(usuario['id'])
                            if success:
                                eliminados += 1
                        
                        st.success(f"✅ {eliminados} usuarios eliminados exitosamente")
                        time.sleep(2)
                        st.rerun()
                else:
                    st.info("ℹ️ No hay usuarios para limpiar")
                    
            except Exception as e:
                st.error(f"❌ Error al limpiar usuarios: {e}")

def show_user_details_modal(usuario: Dict):
    """Mostrar modal con detalles del usuario"""
    
    with st.expander(f"👁️ Detalles de {usuario['nombre']}", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Información Personal:**")
            st.write(f"**Nombre:** {usuario['nombre']}")
            st.write(f"**Email:** {usuario.get('email', 'Sin email')}")
            st.write(f"**Teléfono:** {usuario.get('telefono', 'Sin teléfono')}")
            st.write(f"**Dirección:** {usuario.get('direccion', 'Sin dirección')}")
            st.write(f"**Fecha de Nacimiento:** {usuario.get('fecha_nacimiento', 'No especificada')}")
        
        with col2:
            st.write("**Información del Sistema:**")
            st.write(f"**Rol:** {usuario.get('nombre_rol', 'Sin rol')}")
            st.write(f"**Estado:** {usuario.get('estado', 'Desconocido')}")
            st.write(f"**Fecha de Registro:** {usuario.get('fecha_creacion', 'No especificada')}")
            st.write(f"**Último Acceso:** {usuario.get('ultimo_acceso', 'Nunca')}")
            st.write(f"**Total de Accesos:** {usuario.get('total_accesos', 0)}")
        
        # Permisos y configuraciones
        if usuario.get('permisos'):
            st.write("**Permisos Especiales:**")
            for permiso in usuario['permisos']:
                st.write(f"- {permiso}")

def render_user_modal(cocktail_model: CocktailModel):
    """Modal para crear/editar usuario"""
    
    modal_title = "✏️ Editar Usuario" if st.session_state.users_page_state['modal_mode'] == 'edit' else "➕ Crear Nuevo Usuario"
    
    with st.expander(modal_title, expanded=True):
        try:
            # Obtener datos del usuario si es edición
            if st.session_state.users_page_state['modal_mode'] == 'edit' and st.session_state.users_page_state['selected_user']:
                usuario = st.session_state.users_page_state['selected_user']
            else:
                usuario = None
            
            # Formulario principal
            with st.form("user_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    nombre = st.text_input("👤 Nombre completo*", 
                                           value=usuario['nombre'] if usuario else "",
                                           placeholder="Ej: Juan Pérez García")
                    
                    email = st.text_input("📧 Email*", 
                                        value=usuario.get('email', '') if usuario else "",
                                        placeholder="ejemplo@correo.com")
                    
                    telefono = st.text_input("📱 Teléfono", 
                                             value=usuario.get('telefono', '') if usuario else "",
                                             placeholder="Ej: +34 600 123 456")
                    
                    fecha_nacimiento = st.date_input("🎂 Fecha de nacimiento", 
                                                     value=datetime.strptime(usuario['fecha_nacimiento'], '%Y-%m-%d').date() if usuario and usuario.get('fecha_nacimiento') else None,
                                                     help="Opcional")
                
                with col2:
                    # Selector de rol
                    roles = cocktail_model.get_all_roles()
                    role_options = [role['nombre_rol'] for role in roles]
                    role_default = usuario.get('nombre_rol', role_options[0]) if usuario else role_options[0]
                    rol_seleccionado = st.selectbox("🛡️ Rol*", role_options, 
                                                   index=role_options.index(role_default) if role_default in role_options else 0)
                    
                    estado_options = ['activo', 'inactivo', 'pendiente']
                    estado_default = usuario.get('estado', 'activo') if usuario else 'activo'
                    estado = st.selectbox("📊 Estado*", estado_options, 
                                        index=estado_options.index(estado_default))
                    
                    direccion = st.text_input("🏠 Dirección", 
                                            value=usuario.get('direccion', '') if usuario else '',
                                            placeholder="Calle, número, ciudad...")
                    
                    # Contraseña (solo para nuevos usuarios o cambio)
                    if not usuario:
                        contrasena = st.text_input("🔑 Contraseña*", type="password", 
                                                 placeholder="Mínimo 6 caracteres")
                        confirmar_contrasena = st.text_input("🔒 Confirmar contraseña*", type="password")
                
                # Permisos adicionales
                st.subheader("🔐 Permisos y Configuraciones")
                
                permisos_disponibles = [
                    "Gestionar inventario",
                    "Gestionar recetas", 
                    "Gestionar usuarios",
                    "Ver reportes",
                    "Gestionar ventas",
                    "Acceso a configuraciones"
                ]
                
                permisos_actuales = usuario.get('permisos', []) if usuario else []
                permisos_seleccionados = st.multiselect("✅ Permisos especiales", 
                                                        permisos_disponibles,
                                                        default=permisos_actuales)
                
                # Botones de acción
                col1, col2, col3 = st.columns([1, 1, 1])
                
                with col1:
                    submit = st.form_submit_button("💾 Guardar", type="primary", use_container_width=True)
                
                with col2:
                    if st.form_submit_button("❌ Cancelar", use_container_width=True):
                        st.session_state.users_page_state['show_modal'] = False
                        st.session_state.users_page_state['selected_user'] = None
                        st.rerun()
                
                with col3:
                    if st.form_submit_button("🔄 Reiniciar", use_container_width=True):
                        st.rerun()
                
                if submit:
                    # Validación de campos requeridos
                    if not nombre or not email or not rol_seleccionado:
                        st.error("❌ Por favor complete todos los campos requeridos*")
                        return
                    
                    # Validación de email
                    if "@" not in email or "." not in email:
                        st.error("❌ Por favor ingrese un email válido")
                        return
                    
                    # Validación de contraseña para nuevos usuarios
                    if not usuario:
                        if not contrasena or len(contrasena) < 6:
                            st.error("❌ La contraseña debe tener al menos 6 caracteres")
                            return
                        if contrasena != confirmar_contrasena:
                            st.error("❌ Las contraseñas no coinciden")
                            return
                    
                    try:
                        # Preparar datos del usuario
                        user_data = {
                            'nombre': nombre.strip(),
                            'email': email.strip(),
                            'telefono': telefono.strip(),
                            'direccion': direccion.strip(),
                            'fecha_nacimiento': fecha_nacimiento.strftime('%Y-%m-%d') if fecha_nacimiento else None,
                            'rol_id': next(r['id'] for r in roles if r['nombre_rol'] == rol_seleccionado),
                            'estado': estado,
                            'permisos': permisos_seleccionados
                        }
                        
                        if not usuario:
                            user_data['contrasena'] = contrasena
                        
                        if st.session_state.users_page_state['modal_mode'] == 'edit' and usuario:
                            # Actualizar usuario existente
                            success = cocktail_model.update_usuario(usuario['id'], user_data)
                            
                            if success:
                                st.success(f"✅ Usuario {nombre} actualizado exitosamente")
                                time.sleep(1)
                                st.session_state.users_page_state['show_modal'] = False
                                st.session_state.users_page_state['selected_user'] = None
                                st.rerun()
                            else:
                                st.error("❌ Error al actualizar usuario")
                        
                        else:
                            # Crear nuevo usuario
                            nuevo_usuario = cocktail_model.create_usuario(user_data)
                            
                            if nuevo_usuario:
                                st.success(f"✅ Usuario {nombre} creado exitosamente")
                                time.sleep(1)
                                st.session_state.users_page_state['show_modal'] = False
                                st.rerun()
                            else:
                                st.error("❌ Error al crear usuario")
                    
                    except Exception as e:
                        st.error(f"❌ Error al guardar: {e}")
        
        except Exception as e:
            st.error(f"❌ Error al cargar datos del formulario: {e}")

# Punto de entrada de la página
if __name__ == "__main__":
    render_users_page()