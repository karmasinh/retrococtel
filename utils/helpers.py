"""
🍹 Cocktail Dashboard - Utilidades y Componentes UI
Módulo con funciones auxiliares y componentes reutilizables para la interfaz
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from typing import Dict, List, Any, Optional
import os

class UIComponents:
    """Clase con componentes UI reutilizables que reemplazan el JavaScript"""
    
    @staticmethod
    def CardMetric(icon: str, title: str, value: str, subtitle: str = "", color: str = "primary", key: str = None):
        """Card moderna para métricas (reemplaza CardMetric.js)"""
        
        colors = {
            "primary": "linear-gradient(135deg, #FF6B6B, #FF8E53)",
            "secondary": "linear-gradient(135deg, #4ECDC4, #44A08D)",
            "accent": "linear-gradient(135deg, #FFE66D, #FFA726)",
            "success": "linear-gradient(135deg, #56ab2f, #a8e6cf)",
            "warning": "linear-gradient(135deg, #ffb347, #ffcc33)",
            "danger": "linear-gradient(135deg, #ff416c, #ff4b2b)"
        }
        
        gradient = colors.get(color, colors["primary"])
        
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            cursor: pointer;
            border: 1px solid rgba(0,0,0,0.05);
            position: relative;
            overflow: hidden;
        " onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 15px 35px rgba(0,0,0,0.15)'" 
           onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 8px 25px rgba(0,0,0,0.1)'">
            
            <div style="
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: {gradient};
                border-radius: 20px 20px 0 0;
            "></div>
            
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <div style="
                    background: {gradient};
                    color: white;
                    width: 50px;
                    height: 50px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 24px;
                    margin-right: 15px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                ">{icon}</div>
                <div>
                    <h3 style="margin: 0; color: #2C3E50; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">{title}</h3>
                </div>
            </div>
            
            <div style="font-size: 32px; font-weight: 700; color: #2C3E50; margin-bottom: 5px;">{value}</div>
            {f'<div style="font-size: 14px; color: #7f8c8d;">{subtitle}</div>' if subtitle else ''}
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def CocktailCard(cocktail_data: Dict[str, Any], show_details: bool = True):
        """Card moderna para cócteles (reemplaza CocktailCard.js)"""
        
        nombre = cocktail_data.get('nombre', 'Cóctel sin nombre')
        tipo = cocktail_data.get('nombre_tipo', 'Sin categoría')
        dificultad = cocktail_data.get('dificultad', 'No especificada')
        tiempo = cocktail_data.get('tiempo_preparacion', 'N/A')
        imagen_url = cocktail_data.get('imagen_url', '')
        descripcion = cocktail_data.get('descripcion', '')
        
        # Colores según dificultad
        dificultad_colors = {
            'Fácil': '#56ab2f',
            'Media': '#ffb347',
            'Difícil': '#ff416c'
        }
        dificultad_color = dificultad_colors.get(dificultad, '#7f8c8d')
        
        with st.container():
            st.markdown(f"""
            <div style="
                background: white;
                border-radius: 20px;
                padding: 20px;
                box-shadow: 0 8px 25px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
                cursor: pointer;
                border: 1px solid rgba(0,0,0,0.05);
                margin-bottom: 20px;
                position: relative;
                overflow: hidden;
            " onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 15px 35px rgba(0,0,0,0.15)'" 
               onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 8px 25px rgba(0,0,0,0.1)'">
                
                <div style="
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    height: 4px;
                    background: linear-gradient(135deg, #FF6B6B, #FF8E53);
                    border-radius: 20px 20px 0 0;
                "></div>
                
                <div style="display: flex; align-items: center; margin-bottom: 15px;">
                    <div style="
                        background: linear-gradient(135deg, #FF6B6B, #FF8E53);
                        color: white;
                        width: 60px;
                        height: 60px;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 30px;
                        margin-right: 15px;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                    ">🍸</div>
                    <div style="flex: 1;">
                        <h3 style="margin: 0; color: #2C3E50; font-size: 20px; font-weight: 700;">{nombre}</h3>
                        <p style="margin: 5px 0; color: #7f8c8d; font-size: 14px;">{tipo}</p>
                    </div>
                    <div style="
                        background: {dificultad_color};
                        color: white;
                        padding: 5px 12px;
                        border-radius: 15px;
                        font-size: 12px;
                        font-weight: 600;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                    ">{dificultad}</div>
                </div>
                
                {f'<p style="color: #7f8c8d; font-size: 14px; margin-bottom: 15px;">{descripcion[:100]}...</p>' if descripcion else ''}
                
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px;">
                    <div style="display: flex; align-items: center;">
                        <span style="color: #4ECDC4; font-size: 14px; margin-right: 15px;">⏱️ {tiempo} min</span>
                    </div>
                    <div style="display: flex; gap: 10px;">
                        <button style="
                            background: linear-gradient(135deg, #4ECDC4, #44A08D);
                            color: white;
                            border: none;
                            padding: 8px 16px;
                            border-radius: 20px;
                            font-size: 12px;
                            font-weight: 600;
                            cursor: pointer;
                            transition: all 0.3s ease;
                        " onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                            Ver Receta
                        </button>
                        <button style="
                            background: linear-gradient(135deg, #FFE66D, #FFA726);
                            color: white;
                            border: none;
                            padding: 8px 16px;
                            border-radius: 20px;
                            font-size: 12px;
                            font-weight: 600;
                            cursor: pointer;
                            transition: all 0.3s ease;
                        " onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                            Editar
                        </button>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def RoleCard(role_data: Dict[str, Any]):
        """Card moderna para roles (reemplaza RoleCard.js)"""
        
        nombre = role_data.get('nombre', 'Rol sin nombre')
        descripcion = role_data.get('descripcion', 'Sin descripción')
        estado = role_data.get('estado', 1)
        creado_en = role_data.get('creado_en', 'N/A')
        
        # Estado color
        estado_colors = {
            1: '#56ab2f',  # Activo
            0: '#ff416c'   # Inactivo
        }
        estado_color = estado_colors.get(estado, '#7f8c8d')
        estado_texto = 'Activo' if estado == 1 else 'Inactivo'
        
        with st.container():
            st.markdown(f"""
            <div style="
                background: white;
                border-radius: 20px;
                padding: 20px;
                box-shadow: 0 8px 25px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
                cursor: pointer;
                border: 1px solid rgba(0,0,0,0.05);
                margin-bottom: 20px;
                position: relative;
                overflow: hidden;
            " onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 15px 35px rgba(0,0,0,0.15)'" 
               onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 8px 25px rgba(0,0,0,0.1)'">
                
                <div style="
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    height: 4px;
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    border-radius: 20px 20px 0 0;
                "></div>
                
                <div style="display: flex; align-items: center; margin-bottom: 15px;">
                    <div style="
                        background: linear-gradient(135deg, #667eea, #764ba2);
                        color: white;
                        width: 60px;
                        height: 60px;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 30px;
                        margin-right: 15px;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                    ">👥</div>
                    <div style="flex: 1;">
                        <h3 style="margin: 0; color: #2C3E50; font-size: 20px; font-weight: 700;">{nombre}</h3>
                        <p style="margin: 5px 0; color: #7f8c8d; font-size: 14px;">{descripcion[:50]}...</p>
                    </div>
                    <div style="
                        background: {estado_color};
                        color: white;
                        padding: 5px 12px;
                        border-radius: 15px;
                        font-size: 12px;
                        font-weight: 600;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                    ">{estado_texto}</div>
                </div>
                
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px;">
                    <div style="display: flex; align-items: center;">
                        <span style="color: #4ECDC4; font-size: 14px; margin-right: 15px;">📅 Creado: {creado_en}</span>
                    </div>
                    <div style="display: flex; gap: 10px;">
                        <button style="
                            background: linear-gradient(135deg, #4ECDC4, #44A08D);
                            color: white;
                            border: none;
                            padding: 8px 16px;
                            border-radius: 20px;
                            font-size: 12px;
                            font-weight: 600;
                            cursor: pointer;
                            transition: all 0.3s ease;
                        " onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                            Ver Detalles
                        </button>
                        <button style="
                            background: linear-gradient(135deg, #FFE66D, #FFA726);
                            color: white;
                            border: none;
                            padding: 8px 16px;
                            border-radius: 20px;
                            font-size: 12px;
                            font-weight: 600;
                            cursor: pointer;
                            transition: all 0.3s ease;
                        " onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                            Editar
                        </button>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def modal_cocktail_detalle(cocktail_details: Dict[str, Any]):
        """Modal para mostrar detalles completos del cóctel"""
        
        nombre = cocktail_details.get('nombre', 'Cóctel sin nombre')
        descripcion = cocktail_details.get('descripcion', 'Sin descripción')
        tipo = cocktail_details.get('nombre_tipo', 'Sin categoría')
        dificultad = cocktail_details.get('dificultad', 'No especificada')
        tiempo = cocktail_details.get('tiempo_preparacion', 'N/A')
        instrucciones = cocktail_details.get('instrucciones', 'Sin instrucciones')
        ingredientes = cocktail_details.get('ingredientes', [])
        
        with st.expander(f"👁️ Detalles de {nombre}", expanded=True):
            st.markdown(f"""
            <div style="
                background: white;
                border-radius: 15px;
                padding: 20px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                margin-bottom: 15px;
            ">
                <h3 style="color: #2C3E50; margin-bottom: 15px;">{nombre}</h3>
                <p style="color: #7f8c8d; margin-bottom: 10px;">{descripcion}</p>
                
                <div style="display: flex; gap: 20px; margin-bottom: 15px;">
                    <span style="background: #f8f9fa; padding: 5px 10px; border-radius: 8px; font-size: 14px;">
                        <strong>Tipo:</strong> {tipo}
                    </span>
                    <span style="background: #f8f9fa; padding: 5px 10px; border-radius: 8px; font-size: 14px;">
                        <strong>Dificultad:</strong> {dificultad}
                    </span>
                    <span style="background: #f8f9fa; padding: 5px 10px; border-radius: 8px; font-size: 14px;">
                        <strong>Tiempo:</strong> {tiempo} min
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🧪 Ingredientes:**")
                if ingredientes:
                    for ing in ingredientes:
                        cantidad = ing.get('cantidad', 'N/A')
                        unidad = ing.get('unidad', 'unidades')
                        nombre_ing = ing.get('nombre_ingrediente', 'Ingrediente desconocido')
                        st.write(f"• {cantidad} {unidad} de {nombre_ing}")
                else:
                    st.write("Sin ingredientes registrados")
            
            with col2:
                st.markdown("**📝 Instrucciones:**")
                st.write(instrucciones)
            
            st.markdown("---")
            st.caption("💡 Puedes cerrar este panel haciendo clic en el encabezado")

class ModalComponents:
    """Componentes de modales modernos"""
    
    @staticmethod
    def notification(message: str, type: str = "info", duration: int = 3):
        """Sistema de notificaciones moderno"""
        
        colors = {
            "success": "#56ab2f",
            "error": "#ff416c", 
            "warning": "#ffb347",
            "info": "#4ECDC4"
        }
        
        color = colors.get(type, colors["info"])
        
        placeholder = st.empty()
        
        placeholder.markdown(f"""
        <div style="
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            border-left: 5px solid {color};
            z-index: 1000;
            min-width: 300px;
            animation: slideInRight 0.3s ease-out;
        ">
            <div style="display: flex; align-items: center;">
                <div style="color: {color}; font-size: 24px; margin-right: 15px;">
                    {'✅' if type == 'success' else '❌' if type == 'error' else '⚠️' if type == 'warning' else 'ℹ️'}
                </div>
                <div style="flex: 1;">
                    <div style="font-weight: 600; color: #2C3E50;">{message}</div>
                </div>
            </div>
        </div>
        
        <style>
            @keyframes slideInRight {{
                from {{ transform: translateX(100%); opacity: 0; }}
                to {{ transform: translateX(0); opacity: 1; }}
            }}
        </style>
        """, unsafe_allow_html=True)
        
        time.sleep(duration)
        placeholder.empty()

class ChartComponents:
    """Componentes de gráficos modernos"""
    
    @staticmethod
    def create_cocktail_distribution_chart(cocktails_data: List[Dict[str, Any]]) -> go.Figure:
        """Crear gráfico de distribución de cócteles"""
        if not cocktails_data:
            return go.Figure()
        
        # Procesar datos para el gráfico
        tipo_counts = {}
        for cocktail in cocktails_data:
            tipo = cocktail.get('nombre_tipo', 'Sin categoría')
            tipo_counts[tipo] = tipo_counts.get(tipo, 0) + 1
        
        # Crear gráfico de pastel
        fig = go.Figure(data=[go.Pie(
            labels=list(tipo_counts.keys()),
            values=list(tipo_counts.values()),
            hole=0.3,
            marker_colors=['#FF6B6B', '#4ECDC4', '#FFE66D', '#FF8E53', '#667eea', '#764ba2'],
            textinfo='label+percent',
            textposition='outside',
            textfont=dict(size=12, color='#2C3E50')
        )])
        
        fig.update_layout(
            title=dict(
                text='Distribución de Cócteles por Tipo',
                font=dict(size=16, color='#2C3E50'),
                x=0.5
            ),
            showlegend=False,
            height=400,
            margin=dict(l=0, r=0, t=50, b=0)
        )
        
        return fig
    
    @staticmethod
    def create_roles_distribution_chart(roles_data: List[Dict[str, Any]]) -> go.Figure:
        """Crear gráfico de distribución de roles"""
        if not roles_data:
            return go.Figure()
        
        # Procesar datos para el gráfico
        estado_counts = {}
        for role in roles_data:
            estado = role.get('estado', 1)
            estado_texto = 'Activo' if estado == 1 else 'Inactivo'
            estado_counts[estado_texto] = estado_counts.get(estado_texto, 0) + 1
        
        # Crear gráfico de pastel
        fig = go.Figure(data=[go.Pie(
            labels=list(estado_counts.keys()),
            values=list(estado_counts.values()),
            hole=0.3,
            marker_colors=['#56ab2f', '#ff416c', '#4ECDC4', '#FFE66D', '#667eea', '#764ba2'],
            textinfo='label+percent',
            textposition='outside',
            textfont=dict(size=12, color='#2C3E50')
        )])
        
        fig.update_layout(
            title=dict(
                text='Distribución de Roles por Estado',
                font=dict(size=16, color='#2C3E50'),
                x=0.5
            ),
            showlegend=False,
            height=400,
            margin=dict(l=0, r=0, t=50, b=0)
        )
        
        return fig

# Funciones auxiliares
def format_currency(amount: float) -> str:
    """Formatear cantidad como moneda"""
    return f"${amount:,.2f}"

def get_status_color(status: str) -> str:
    """Obtener color según estado"""
    status_colors = {
        'activo': '#56ab2f',
        'inactivo': '#ff416c',
        'pendiente': '#ffb347',
        'completado': '#4ECDC4',
        'cancelado': '#ff416c'
    }
    return status_colors.get(status.lower(), '#7f8c8d')

def validate_email(email: str) -> bool:
    """Validar formato de email"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None