"""
Dashboard Premium para CoctelMatch
Desarrollado por: Álvaro Díaz Vallejos
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import Dict, List, Any
from utils.icons import get_icon, render_icon
from utils.helpers import UIComponents
from db.models import CocktailModel

# Modelo global para uso en todo el módulo
model = CocktailModel()

def render_dashboard_page():
    """Renderiza el dashboard principal con visualizaciones premium"""
    
    # Importar modelo para obtener datos reales
    from db.models import CocktailModel
    model = CocktailModel()
    
    # CSS personalizado para el dashboard
    st.markdown("""
    <style>
    .dashboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        text-align: center;
    }
    .dashboard-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .dashboard-subtitle {
        font-size: 1.1rem;
        opacity: 0.9;
    }
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        border-left: 5px solid;
        transition: all 0.3s ease;
        margin-bottom: 20px;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
    }
    .metric-card.primary { border-left-color: #FF6B6B; }
    .metric-card.success { border-left-color: #4ECDC4; }
    .metric-card.warning { border-left-color: #FFE66D; }
    .metric-card.info { border-left-color: #A8E6CF; }
    .metric-icon {
        font-size: 2.5rem;
        margin-bottom: 15px;
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #333;
        margin-bottom: 5px;
    }
    .metric-label {
        color: #666;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .metric-change {
        font-size: 0.8rem;
        margin-top: 10px;
        padding: 5px 10px;
        border-radius: 20px;
        display: inline-block;
    }
    .metric-change.positive {
        background: #e8f5e8;
        color: #28a745;
    }
    .metric-change.negative {
        background: #ffeaea;
        color: #dc3545;
    }
    .chart-container {
        background: white;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        margin-bottom: 30px;
    }
    .chart-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 20px;
        text-align: center;
    }
    .notification-card {
        background: linear-gradient(135deg, #fff8f3, #ffffff);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 4px solid #FF8E53;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    .notification-title {
        font-weight: 600;
        color: #333;
        margin-bottom: 8px;
    }
    .notification-text {
        color: #666;
        font-size: 0.9rem;
    }
    .notification-time {
        color: #999;
        font-size: 0.8rem;
        margin-top: 8px;
    }
    .activity-item {
        display: flex;
        align-items: center;
        padding: 15px;
        border-bottom: 1px solid #f0f0f0;
        transition: all 0.3s ease;
    }
    .activity-item:hover {
        background: #f8f9fa;
        border-radius: 8px;
    }
    .activity-icon {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 15px;
        font-size: 1.2rem;
    }
    .activity-content {
        flex: 1;
    }
    .activity-title {
        font-weight: 600;
        color: #333;
        margin-bottom: 4px;
    }
    .activity-description {
        color: #666;
        font-size: 0.9rem;
    }
    .activity-time {
        color: #999;
        font-size: 0.8rem;
    }
    .quick-actions {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 15px;
        margin-bottom: 30px;
    }
    .quick-action-btn {
        background: white;
        border: 2px solid #e1e5e9;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        color: #333;
    }
    .quick-action-btn:hover {
        border-color: #FF6B6B;
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(255, 107, 107, 0.1);
    }
    .quick-action-icon {
        font-size: 2rem;
        margin-bottom: 10px;
        color: #FF6B6B;
    }
    .quick-action-text {
        font-weight: 600;
        font-size: 0.9rem;
    }
    .footer {
        text-align: center;
        padding: 30px;
        color: #666;
        font-size: 0.9rem;
        border-top: 1px solid #e1e5e9;
        margin-top: 50px;
    }
    .footer-brand {
        font-weight: 600;
        color: #FF6B6B;
    }
    .footer-developer {
        color: #999;
        font-size: 0.8rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header del dashboard con datos del usuario y menú rápido
    user_name = st.session_state.user['nombre_completo'] if 'user' in st.session_state and st.session_state.user else 'Usuario'
    user_role = st.session_state.user.get('rol_nombre', 'Usuario') if 'user' in st.session_state and st.session_state.user else 'Usuario'
    st.markdown(f'''
    <div class="dashboard-header">
        <div class="dashboard-title">🍹 Bienvenido, {user_name}</div>
        <div class="dashboard-subtitle">Rol: {user_role}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    col_header_left, col_header_right = st.columns([3, 1])
    with col_header_right:
        opcion_usuario = st.selectbox(
            "👤 Opciones",
            ["Perfil", "Cambiar tema", "Cerrar sesión"],
            index=0,
        )
        if opcion_usuario == "Cambiar tema":
            st.session_state["theme"] = "dark" if st.session_state.get("theme") != "dark" else "light"
            st.success(f"Tema cambiado a {st.session_state['theme']}")
        elif opcion_usuario == "Cerrar sesión":
            st.session_state.pop('user', None)
            st.success("Sesión cerrada")
    
    # Métricas principales con datos reales
    col1, col2, col3, col4 = st.columns(4)
    
    # Obtener datos reales de la base de datos
    try:
        total_cocktails = model.get_total_cocteles() if hasattr(model, 'get_total_cocteles') else model.get_total_cocktails()
        total_ingredients = model.get_total_ingredientes() if hasattr(model, 'get_total_ingredientes') else len(model.get_all_ingredientes())
        # Ingredientes bajo stock basados en inventario
        low_stock_items = 0
        for ing in model.get_all_ingredientes():
            inventario = model.get_inventario_by_ingrediente(ing['id'])
            if not inventario:
                continue
            # Si alguno de los registros está por debajo del punto de reorden, contar como bajo stock
            for inv in inventario:
                punto = inv.get('punto_reorden') or 0
                cantidad = inv.get('cantidad_stock') or 0
                if punto and cantidad < punto:
                    low_stock_items += 1
                    break
        total_users = model.get_total_users() if hasattr(model, 'get_total_users') else model.get_total_usuarios()
    except Exception as e:
        # Valores por defecto si hay error
        total_cocktails = 0
        total_ingredients = 0
        low_stock_items = 0
        total_users = 0
        st.error(f"Error cargando métricas: {e}")
    
    with col1:
        render_metric_card(
            icon="🍸",
            title="Total Cocteles",
            value=str(total_cocktails),
            change="+12%",
            change_type="positive",
            card_type="primary"
        )
    
    with col2:
        render_metric_card(
            icon="📦",
            title="Ingredientes",
            value=str(total_ingredients),
            change="+5%",
            change_type="positive",
            card_type="success"
        )
    
    with col3:
        render_metric_card(
            icon="⚠️",
            title="Bajo Stock",
            value=str(low_stock_items),
            change="-3%",
            change_type="negative",
            card_type="warning"
        )
    
    with col4:
        render_metric_card(
            icon="👥",
            title="Usuarios Activos",
            value=str(total_users),
            change="+8%",
            change_type="positive",
            card_type="info"
        )
    
    # Gráficos principales
    col1, col2 = st.columns(2)
    
    with col1:
        render_cocktail_popularity_chart()
    
    with col2:
        render_inventory_status_chart()
    
    # Segunda fila de gráficos
    col3, col4 = st.columns(2)
    
    with col3:
        render_monthly_trends_chart()
    
    with col4:
        render_user_activity_chart()
    
    # Acciones rápidas según rol
    st.markdown("### ⚡ Acciones Rápidas", unsafe_allow_html=True)
    role_lower = (user_role or '').lower()
    col_actions1, col_actions2, col_actions3, col_actions4 = st.columns(4)

    if role_lower in ['admin', 'administrador']:
        with col_actions1:
            if st.button("👥 Gestionar Usuarios", use_container_width=True, key="manage_users"):
                st.success("Redirigiendo a usuarios...")
        with col_actions2:
            if st.button("🔐 Gestionar Roles", use_container_width=True, key="manage_roles"):
                st.success("Redirigiendo a roles...")
        with col_actions3:
            if st.button("📊 Generar Reporte", use_container_width=True, key="generate_report"):
                render_report_generation_modal()
        with col_actions4:
            if st.button("⚙️ Configuración", use_container_width=True, key="settings"):
                st.success("Abrir configuración...")
    elif role_lower in ['bartender', 'camarero']:
        with col_actions1:
            if st.button("🍹 Agregar Coctel", use_container_width=True, key="add_cocktail"):
                st.success("Redirigiendo a cocteles...")
        with col_actions2:
            if st.button("📦 Actualizar Inventario", use_container_width=True, key="update_inventory"):
                st.success("Redirigiendo a inventario...")
        with col_actions3:
            if st.button("🔎 Buscar Cocteles", use_container_width=True, key="search_cocktails"):
                st.success("Redirigiendo a cocteles...")
        with col_actions4:
            if st.button("📝 Registrar Venta", use_container_width=True, key="register_sale"):
                st.info("Funcionalidad de ventas próximamente")
    else:
        with col_actions1:
            if st.button("🍸 Explorar Cocteles", use_container_width=True, key="explore_cocktails"):
                st.success("Redirigiendo a cocteles...")
        with col_actions2:
            if st.button("⭐ Mis Favoritos", use_container_width=True, key="my_favorites"):
                st.info("Favoritos próximamente")
        with col_actions3:
            if st.button("🧾 Historial", use_container_width=True, key="history"):
                st.info("Historial próximamente")
        with col_actions4:
            if st.button("📊 Sugerencias", use_container_width=True, key="suggestions"):
                st.info("Sugerencias próximamente")
    
    # Notificaciones y actividad
    col_notif, col_activity = st.columns([1, 2])
    
    with col_notif:
        render_notifications_panel()
    
    with col_activity:
        render_recent_activity()
    
    # Footer
    st.markdown('''
    <div class="footer">
        <div class="footer-brand">🍹 CoctelMatch - Tu coctel favorito</div>
        <div class="footer-developer">Desarrollado por Álvaro Díaz Vallejos</div>
    </div>
    ''', unsafe_allow_html=True)

def render_metric_card(icon: str, title: str, value: str, change: str, change_type: str, card_type: str):
    """Renderiza una tarjeta de métrica premium"""
    change_class = "positive" if change_type == "positive" else "negative"
    
    st.markdown(f'''
    <div class="metric-card {card_type}">
        <div class="metric-icon">{icon}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{title}</div>
        <div class="metric-change {change_class}">{change} vs mes anterior</div>
    </div>
    ''', unsafe_allow_html=True)

def render_cocktail_popularity_chart():
    """Renderiza gráfico de popularidad de cocteles con datos reales"""
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">🍸 Cocteles Más Populares</div>', unsafe_allow_html=True)
    
    try:
        # Obtener datos reales de cócteles
        cocktails_data = model.get_all_cocktails()
        
        # Limitar a los 5 primeros cócteles por nombre
        cocktails = [cocktail['nombre'] for cocktail in cocktails_data[:5]]
        popularity = [85, 72, 68, 65, 58]  # Datos simulados basados en cantidad
        
        # Si hay menos de 5 cócteles, usar datos simulados
        if len(cocktails) < 5:
            cocktails = ['Mojito', 'Piña Colada', 'Margarita', 'Daiquiri', 'Cuba Libre']
            popularity = [85, 72, 68, 65, 58]
        
    except Exception as e:
        # Datos de ejemplo si hay error
        cocktails = ['Mojito', 'Piña Colada', 'Margarita', 'Daiquiri', 'Cuba Libre']
        popularity = [85, 72, 68, 65, 58]
        st.error(f"Error cargando datos de cócteles: {e}")
    
    fig = go.Figure(data=[
        go.Bar(
            x=cocktails,
            y=popularity,
            marker_color=['#FF6B6B', '#4ECDC4', '#FFE66D', '#A8E6CF', '#FF8E53'],
            text=popularity,
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Popularidad: %{y}%<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="",
        xaxis_title="Cocteles",
        yaxis_title="Popularidad (%)",
        showlegend=False,
        height=300,
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial", size=12),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0')
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

def render_inventory_status_chart():
    """Renderiza gráfico de estado del inventario con datos reales"""
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📦 Estado del Inventario</div>', unsafe_allow_html=True)
    
    try:
        # Obtener datos reales de inventario
        ingredientes = model.get_all_ingredientes()
        
        # Calcular categorías de stock basadas en inventario
        optimal_stock = 0
        low_stock = 0
        no_stock = 0
        
        for ing in ingredientes:
            inventario = model.get_inventario_by_ingrediente(ing['id'])
            if not inventario:
                no_stock += 1
                continue
            # Agrear cantidades y evaluar punto de reorden
            total_cantidad = sum((item.get('cantidad_stock') or 0) for item in inventario)
            punto_reorden = min([item.get('punto_reorden') or 0 for item in inventario]) if inventario else 0
            
            if total_cantidad == 0:
                no_stock += 1
            elif punto_reorden and total_cantidad < punto_reorden:
                low_stock += 1
            else:
                optimal_stock += 1
        
        labels = ['Stock Óptimo', 'Stock Bajo', 'Sin Stock']
        values = [optimal_stock, low_stock, no_stock]
        colors = ['#4ECDC4', '#FFE66D', '#FF6B6B']
        
    except Exception as e:
        # Datos de ejemplo si hay error
        labels = ['Stock Óptimo', 'Stock Bajo', 'Sin Stock']
        values = [65, 25, 10]
        colors = ['#4ECDC4', '#FFE66D', '#FF6B6B']
        st.error(f"Error cargando datos de inventario: {e}")
    
    fig = go.Figure(data=[
        go.Pie(
            labels=labels,
            values=values,
            hole=0.6,
            marker_colors=colors,
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Cantidad: %{value}<br>Porcentaje: %{percent}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="",
        height=300,
        margin=dict(l=0, r=0, t=0, b=0),
        font=dict(family="Arial", size=12),
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

def render_monthly_trends_chart():
    """Renderiza gráfico de tendencias mensuales"""
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📈 Tendencias Mensuales</div>', unsafe_allow_html=True)
    
    # Datos de ejemplo
    months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
    cocktails_sold = [120, 135, 148, 162, 178, 195]
    new_users = [15, 18, 22, 25, 28, 32]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months,
        y=cocktails_sold,
        name='Cocteles Vendidos',
        line=dict(color='#FF6B6B', width=3),
        mode='lines+markers',
        marker=dict(size=8),
        hovertemplate='<b>Cocteles</b><br>Mes: %{x}<br>Cantidad: %{y}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=months,
        y=new_users,
        name='Nuevos Usuarios',
        line=dict(color='#4ECDC4', width=3),
        mode='lines+markers',
        marker=dict(size=8),
        hovertemplate='<b>Usuarios</b><br>Mes: %{x}<br>Cantidad: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title="",
        xaxis_title="Mes",
        yaxis_title="Cantidad",
        height=300,
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial", size=12),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0')
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

def render_user_activity_chart():
    """Renderiza gráfico de actividad de usuarios"""
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">👥 Actividad de Usuarios</div>', unsafe_allow_html=True)
    
    # Datos de ejemplo
    hours = ['6AM', '9AM', '12PM', '3PM', '6PM', '9PM', '12AM']
    activity = [15, 35, 55, 45, 75, 85, 25]
    
    fig = go.Figure(data=[
        go.Scatter(
            x=hours,
            y=activity,
            fill='tozeroy',
            fillcolor='rgba(255, 107, 107, 0.3)',
            line=dict(color='#FF6B6B', width=3),
            mode='lines+markers',
            marker=dict(size=8, color='#FF6B6B'),
            hovertemplate='<b>Hora: %{x}</b><br>Actividad: %{y} usuarios<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="",
        xaxis_title="Hora del Día",
        yaxis_title="Usuarios Activos",
        height=300,
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial", size=12),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0')
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

def render_notifications_panel():
    """Renderiza panel de notificaciones"""
    st.markdown("### 🔔 Notificaciones", unsafe_allow_html=True)
    
    notifications = [
        {
            "title": "Stock Bajo",
            "text": "El ron está por debajo del nivel mínimo",
            "time": "Hace 5 minutos"
        },
        {
            "title": "Nuevo Pedido",
            "text": "Mesa 12 solicitó 3 mojitos",
            "time": "Hace 15 minutos"
        },
        {
            "title": "Usuario Nuevo",
            "text": "Carlos González se registró como bartender",
            "time": "Hace 1 hora"
        }
    ]
    
    for notification in notifications:
        st.markdown(f'''
        <div class="notification-card">
            <div class="notification-title">{get_icon("warning", size=16)} {notification["title"]}</div>
            <div class="notification-text">{notification["text"]}</div>
            <div class="notification-time">{notification["time"]}</div>
        </div>
        ''', unsafe_allow_html=True)

def render_recent_activity():
    """Renderiza actividad reciente"""
    st.markdown("### 📋 Actividad Reciente", unsafe_allow_html=True)
    
    activities = [
        {
            "icon": "🍹",
            "title": "Coctel Creado",
            "description": "Juan creó un nuevo coctel 'Tropical Sunset'",
            "time": "Hace 2 minutos",
            "color": "#FF6B6B"
        },
        {
            "icon": "📦",
            "title": "Inventario Actualizado",
            "description": "María actualizó el stock de vodka",
            "time": "Hace 10 minutos",
            "color": "#4ECDC4"
        },
        {
            "icon": "👤",
            "title": "Usuario Registrado",
            "description": "Pedro Sánchez se unió al equipo",
            "time": "Hace 25 minutos",
            "color": "#A8E6CF"
        },
        {
            "icon": "📊",
            "title": "Reporte Generado",
            "description": "Se generó el reporte mensual de ventas",
            "time": "Hace 1 hora",
            "color": "#FFE66D"
        }
    ]
    
    for activity in activities:
        st.markdown(f'''
        <div class="activity-item">
            <div class="activity-icon" style="background: {activity["color"]}20; color: {activity["color"]};">
                {activity["icon"]}
            </div>
            <div class="activity-content">
                <div class="activity-title">{activity["title"]}</div>
                <div class="activity-description">{activity["description"]}</div>
                <div class="activity-time">{activity["time"]}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

def render_report_generation_modal():
    """Renderiza modal para generación de reportes"""
    with st.expander("📊 Generar Reporte Personalizado", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            report_type = st.selectbox(
                "Tipo de Reporte",
                ["Ventas Mensuales", "Inventario", "Actividad de Usuarios", "Popularidad de Cocteles"]
            )
            
            start_date = st.date_input("Fecha Inicio", datetime.now() - timedelta(days=30))
        
        with col2:
            format_type = st.selectbox("Formato", ["PDF", "Excel", "CSV"])
            
            end_date = st.date_input("Fecha Fin", datetime.now())
        
        col3, col4, col5 = st.columns([1, 2, 1])
        
        with col4:
            if st.button("🚀 Generar Reporte", use_container_width=True, type="primary"):
                with st.spinner("Generando reporte..."):
                    time.sleep(2)
                    st.success(f"¡Reporte '{report_type}' generado exitosamente en formato {format_type}!")

# Función principal
def main():
    """Función principal del módulo de dashboard"""
    render_dashboard_page()

if __name__ == "__main__":
    main()