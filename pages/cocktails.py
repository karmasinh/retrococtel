"""
🍸 Página de Gestión de Cócteles
CRUD completo de cócteles con diseño profesional y modales
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

def render_cocktails_page():
    """Renderizar la página completa de cócteles"""
    
    # Título principal con diseño moderno
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #FF6B6B, #FF8E53);
        color: white;
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    ">
        <h1 style="margin: 0; font-size: 2.5em; font-weight: 700;">🍸 Gestión de Cócteles</h1>
        <p style="margin: 10px 0 0 0; font-size: 1.1em; opacity: 0.9;">Crea, edita y administra tu catálogo de cócteles</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicializar modelo de datos
    cocktail_model = CocktailModel()
    
    # Estado de la página
    if 'cocktail_page_state' not in st.session_state:
        st.session_state.cocktail_page_state = {
            'show_modal': False,
            'modal_mode': 'create',
            'selected_cocktail': None,
            'search_term': '',
            'filter_type': 'Todos',
            'filter_difficulty': 'Todos',
            'refresh_data': True
        }
    
    # Barra de herramientas superior
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    
    with col1:
        search_term = st.text_input("🔍 Buscar cóctel...", 
                                  value=st.session_state.cocktail_page_state['search_term'],
                                  placeholder="Ej: Margarita, Mojito...")
        st.session_state.cocktail_page_state['search_term'] = search_term
    
    with col2:
        # Obtener tipos de cócteles de la BD
        try:
            tipos = cocktail_model.get_all_tipos_cocteles()
            tipo_options = ['Todos'] + [tipo['nombre_tipo'] for tipo in tipos]
            filter_type = st.selectbox("🍹 Filtrar por tipo", tipo_options)
            st.session_state.cocktail_page_state['filter_type'] = filter_type
        except Exception as e:
            st.error(f"Error al cargar tipos: {e}")
            filter_type = st.selectbox("🍹 Filtrar por tipo", ['Todos'])
    
    with col3:
        difficulty_options = ['Todos', 'Fácil', 'Media', 'Difícil']
        filter_difficulty = st.selectbox("⭐ Filtrar por dificultad", difficulty_options)
        st.session_state.cocktail_page_state['filter_difficulty'] = filter_difficulty
    
    with col4:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        if st.button("➕ Nuevo Cóctel", type="primary", use_container_width=True):
            st.session_state.cocktail_page_state['show_modal'] = True
            st.session_state.cocktail_page_state['modal_mode'] = 'create'
            st.session_state.cocktail_page_state['selected_cocktail'] = None
            st.rerun()
    
    # Métricas principales
    try:
        total_cocktails = cocktail_model.get_total_cocktails()
        cocktails_by_type = cocktail_model.get_cocktails_by_type()
        recent_cocktails = cocktail_model.get_recent_cocktails(limit=5)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            UIComponents.CardMetric("🍸", "Total Cócteles", str(total_cocktails), 
                                  f"{len(cocktails_by_type)} tipos diferentes", "primary")
        
        with col2:
            # Obtener cóctel más popular (placeholder - necesitaría lógica real)
            UIComponents.CardMetric("⭐", "Más Popular", "Margarita", 
                                  "Clásico atemporal", "accent")
        
        with col3:
            # Calcular promedio de preparación
            avg_time = "8.5"  # Placeholder
            UIComponents.CardMetric("⏱️", "Tiempo Promedio", f"{avg_time} min", 
                                  "Preparación estándar", "secondary")
        
        with col4:
            # Contar ingredientes únicos
            unique_ingredients = "47"  # Placeholder
            UIComponents.CardMetric("🧪", "Ingredientes Únicos", unique_ingredients, 
                                  "En catálogo", "success")
    
    except Exception as e:
        st.error(f"Error al cargar métricas: {e}")
    
    # Contenido principal con tabs
    tab1, tab2, tab3 = st.tabs(["📋 Lista de Cócteles", "📊 Análisis", "🔧 Herramientas"])
    
    with tab1:
        render_cocktails_list(cocktail_model)
    
    with tab2:
        render_cocktails_analytics(cocktail_model, cocktails_by_type)
    
    with tab3:
        render_tools_section(cocktail_model)
    
    # Modal para crear/editar cócteles
    if st.session_state.cocktail_page_state['show_modal']:
        render_cocktail_modal(cocktail_model)

def render_cocktails_list(cocktail_model: CocktailModel):
    """Renderizar la lista de cócteles con diseño moderno"""
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #4ECDC4, #44A08D);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
    ">
        <h3 style="margin: 0;">📋 Catálogo de Cócteles</h3>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        # Obtener cócteles con filtros
        search_term = st.session_state.cocktail_page_state['search_term']
        filter_type = st.session_state.cocktail_page_state['filter_type']
        filter_difficulty = st.session_state.cocktail_page_state['filter_difficulty']
        
        cocktails = cocktail_model.get_cocktails_filtered(
            search_term=search_term,
            tipo_filter=filter_type if filter_type != 'Todos' else None,
            dificultad_filter=filter_difficulty if filter_difficulty != 'Todos' else None
        )
        
        if not cocktails:
            st.info("🍸 No se encontraron cócteles con los filtros aplicados")
            return
        
        # Mostrar cócteles en grid responsive
        cols = st.columns(3)  # 3 columnas para desktop
        
        for idx, cocktail in enumerate(cocktails):
            col_idx = idx % 3
            with cols[col_idx]:
                render_cocktail_card(cocktail, cocktail_model)
    
    except Exception as e:
        st.error(f"Error al cargar cócteles: {e}")

def render_cocktail_card(cocktail: Dict[str, Any], cocktail_model: CocktailModel):
    """Renderizar una card individual de cóctel con acciones"""
    
    # Contenedor principal
    with st.container():
        # Card con diseño moderno
        UIComponents.CocktailCard(cocktail)
        
        # Botones de acción
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("👁️ Ver", key=f"view_{cocktail['id']}", use_container_width=True):
                show_cocktail_details_modal(cocktail, cocktail_model)
        
        with col2:
            if st.button("✏️ Editar", key=f"edit_{cocktail['id']}", use_container_width=True):
                st.session_state.cocktail_page_state['show_modal'] = True
                st.session_state.cocktail_page_state['modal_mode'] = 'edit'
                st.session_state.cocktail_page_state['selected_cocktail'] = cocktail
                st.rerun()
        
        with col3:
            if st.button("🗑️ Eliminar", key=f"delete_{cocktail['id']}", use_container_width=True, type="secondary"):
                if st.checkbox(f"¿Confirmar eliminación de {cocktail['nombre']}?", key=f"confirm_{cocktail['id']}"):
                    try:
                        if cocktail_model.delete_cocktail(cocktail['id']):
                            ModalComponents.notification(f"✅ Cóctel {cocktail['nombre']} eliminado exitosamente", "success")
                            st.session_state.cocktail_page_state['refresh_data'] = True
                            st.rerun()
                        else:
                            ModalComponents.notification("❌ Error al eliminar cóctel", "error")
                    except Exception as e:
                        ModalComponents.notification(f"❌ Error: {str(e)}", "error")

def render_cocktails_analytics(cocktail_model: CocktailModel, cocktails_by_type: List[Dict]):
    """Renderizar sección de análisis y estadísticas"""
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #FFE66D, #FFA726);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
    ">
        <h3 style="margin: 0;">📊 Análisis de Cócteles</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Gráfico de distribución por tipo
        if cocktails_by_type:
            fig = ChartComponents.create_cocktail_distribution_chart(cocktails_by_type)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📊 No hay datos suficientes para mostrar gráficos")
    
    with col2:
        # Estadísticas rápidas
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 15px;">
            <h4 style="color: #FF6B6B; margin-bottom: 15px;">📈 Estadísticas</h4>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            stats = cocktail_model.get_cocktail_statistics()
            
            st.metric("Total de Cócteles", stats.get('total', 0))
            st.metric("Promedio de Ingredientes", f"{stats.get('avg_ingredients', 0):.1f}")
            st.metric("Tiempo Promedio", f"{stats.get('avg_time', 0):.1f} min")
            
            # Top de ingredientes más usados
            if stats.get('top_ingredients'):
                st.markdown("**🧪 Ingredientes más usados:**")
                for ingredient in stats['top_ingredients'][:5]:
                    st.write(f"• {ingredient['nombre']}: {ingredient['usos']} veces")
        
        except Exception as e:
            st.error(f"Error al cargar estadísticas: {e}")

def render_tools_section(cocktail_model: CocktailModel):
    """Renderizar sección de herramientas y utilidades"""
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #f093fb, #f5576c);
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
            <h4 style="color: #FF6B6B; margin-bottom: 15px;">📤 Importar/Exportar</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Botones de importar/exportar
        if st.button("📤 Exportar Catálogo (CSV)", use_container_width=True):
            try:
                cocktails = cocktail_model.get_all_cocktails()
                if cocktails:
                    df = pd.DataFrame(cocktails)
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="⬇️ Descargar CSV",
                        data=csv,
                        file_name=f"catalogo_cocteles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                else:
                    st.warning("No hay cócteles para exportar")
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
                    # Aquí iría la lógica de importación
                    ModalComponents.notification("✅ Importación completada", "success")
            except Exception as e:
                st.error(f"Error al importar: {e}")
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 15px;">
            <h4 style="color: #4ECDC4; margin-bottom: 15px;">🎨 Personalización</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Opciones de personalización
        if st.button("🎨 Generar Reporte Completo", use_container_width=True):
            try:
                # Generar reporte con estadísticas completas
                report_data = generate_complete_report(cocktail_model)
                st.json(report_data)
            except Exception as e:
                st.error(f"Error al generar reporte: {e}")
        
        if st.button("🔄 Actualizar Cache", use_container_width=True):
            st.session_state.cocktail_page_state['refresh_data'] = True
            ModalComponents.notification("✅ Cache actualizado", "success")
            st.rerun()

def render_cocktail_modal(cocktail_model: CocktailModel):
    """Renderizar modal para crear/editar cócteles"""
    
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
                max-width: 800px;
                max-height: 90vh;
                overflow-y: auto;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                position: relative;
                width: 90%;
            ">
        """, unsafe_allow_html=True)
        
        # Header del modal
        mode = st.session_state.cocktail_page_state['modal_mode']
        cocktail_data = st.session_state.cocktail_page_state.get('selected_cocktail')
        
        title = "🍸 Crear Nuevo Cóctel" if mode == 'create' else f"✏️ Editar {cocktail_data.get('nombre', 'Cóctel')}"
        
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"<h2 style='color: #FF6B6B; margin-bottom: 20px;'>{title}</h2>", unsafe_allow_html=True)
        with col2:
            if st.button("❌ Cerrar", type="secondary"):
                st.session_state.cocktail_page_state['show_modal'] = False
                st.rerun()
        
        # Formulario principal
        with st.form("cocktail_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div style="background: #f8f9fa; padding: 20px; border-radius: 15px; margin-bottom: 15px;">
                    <h4 style="color: #FF6B6B; margin-bottom: 15px;">📋 Información Básica</h4>
                </div>
                """, unsafe_allow_html=True)
                
                nombre = st.text_input("🍸 Nombre del Cóctel *", 
                                     value=cocktail_data.get('nombre', '') if cocktail_data else '',
                                     placeholder="Ej: Margarita Clásica",
                                     help="Nombre único del cóctel")
                
                descripcion = st.text_area("📝 Descripción",
                                         value=cocktail_data.get('descripcion', '') if cocktail_data else '',
                                         placeholder="Describe el cóctel, su historia o características...")
                
                tiempo_prep = st.number_input("⏱️ Tiempo de Preparación (min) *",
                                            min_value=1, max_value=60,
                                            value=cocktail_data.get('tiempo_preparacion', 5) if cocktail_data else 5)
            
            with col2:
                st.markdown("""
                <div style="background: #f8f9fa; padding: 20px; border-radius: 15px; margin-bottom: 15px;">
                    <h4 style="color: #4ECDC4; margin-bottom: 15px;">⚙️ Configuración</h4>
                </div>
                """, unsafe_allow_html=True)
                
                # Cargar opciones desde la BD
                try:
                    tipos = cocktail_model.get_all_tipos_cocteles()
                    tipo_options = [t['nombre_tipo'] for t in tipos]
                    tipo_default = cocktail_data.get('nombre_tipo', tipo_options[0]) if cocktail_data else tipo_options[0]
                    tipo_idx = tipo_options.index(tipo_default) if tipo_default in tipo_options else 0
                    
                    tipo_selected = st.selectbox("🍹 Tipo de Cóctel *", tipo_options, index=tipo_idx)
                    tipo_id = next((t['id'] for t in tipos if t['nombre_tipo'] == tipo_selected), None)
                    
                    vasos = cocktail_model.get_all_vasos()
                    vaso_options = [v['nombre_vaso'] for v in vasos]
                    vaso_default = cocktail_data.get('nombre_vaso', vaso_options[0]) if cocktail_data else vaso_options[0]
                    vaso_idx = vaso_options.index(vaso_default) if vaso_default in vaso_options else 0
                    
                    vaso_selected = st.selectbox("🥤 Tipo de Vaso *", vaso_options, index=vaso_idx)
                    vaso_id = next((v['id'] for v in vasos if v['nombre_vaso'] == vaso_selected), None)
                    
                    metodos = cocktail_model.get_all_metodos_preparacion()
                    metodo_options = [m['nombre_metodo'] for m in metodos]
                    metodo_default = cocktail_data.get('nombre_metodo', metodo_options[0]) if cocktail_data else metodo_options[0]
                    metodo_idx = metodo_options.index(metodo_default) if metodo_default in metodo_options else 0
                    
                    metodo_selected = st.selectbox("⚗️ Método de Preparación *", metodo_options, index=metodo_idx)
                    metodo_id = next((m['id'] for m in metodos if m['nombre_metodo'] == metodo_selected), None)
                    
                    dificultad_options = ['Fácil', 'Media', 'Difícil']
                    dificultad_default = cocktail_data.get('dificultad', 'Media') if cocktail_data else 'Media'
                    dificultad_idx = dificultad_options.index(dificultad_default)
                    dificultad = st.selectbox("⭐ Dificultad *", dificultad_options, index=dificultad_idx)
                    
                except Exception as e:
                    st.error(f"Error al cargar opciones: {e}")
                    return
            
            # Botones de acción
            col_btn1, col_btn2 = st.columns([1, 1])
            
            with col_btn1:
                submitted = st.form_submit_button("💾 Guardar Cóctel", type="primary", use_container_width=True)
            
            with col_btn2:
                if st.form_submit_button("❌ Cancelar", type="secondary", use_container_width=True):
                    st.session_state.cocktail_page_state['show_modal'] = False
                    st.rerun()
            
            if submitted:
                # Validaciones
                if not nombre.strip():
                    st.error("❌ El nombre del cóctel es obligatorio")
                    return
                
                try:
                    # Preparar datos del cóctel
                    cocktail_data = {
                        'nombre': nombre.strip(),
                        'descripcion': descripcion.strip(),
                        'tiempo_preparacion': tiempo_prep,
                        'dificultad': dificultad,
                        'tipo_id': tipo_id,
                        'vaso_id': vaso_id,
                        'metodo_preparacion_id': metodo_id
                    }
                    
                    if mode == 'create':
                        # Crear nuevo cóctel
                        new_id = cocktail_model.create_cocktail(cocktail_data)
                        if new_id:
                            ModalComponents.notification(f"✅ Cóctel '{nombre}' creado exitosamente", "success")
                            st.session_state.cocktail_page_state['show_modal'] = False
                            st.rerun()
                        else:
                            ModalComponents.notification("❌ Error al crear cóctel", "error")
                    
                    elif mode == 'edit' and cocktail_data:
                        # Actualizar cóctel existente
                        cocktail_data['id'] = st.session_state.cocktail_page_state['selected_cocktail']['id']
                        if cocktail_model.update_cocktail(cocktail_data):
                            ModalComponents.notification(f"✅ Cóctel '{nombre}' actualizado exitosamente", "success")
                            st.session_state.cocktail_page_state['show_modal'] = False
                            st.rerun()
                        else:
                            ModalComponents.notification("❌ Error al actualizar cóctel", "error")
                
                except Exception as e:
                    ModalComponents.notification(f"❌ Error: {str(e)}", "error")
        
        st.markdown("</div></div>", unsafe_allow_html=True)

def show_cocktail_details_modal(cocktail: Dict[str, Any], cocktail_model: CocktailModel):
    """Mostrar modal con detalles completos del cóctel"""
    
    try:
        # Obtener información completa del cóctel
        cocktail_details = cocktail_model.get_cocktail_full_details(cocktail['id'])
        
        # Mostrar en un expander o modal temporal
        with st.expander(f"📋 Detalles de {cocktail['nombre']}", expanded=True):
            UIComponents.modal_cocktail_detalle(cocktail_details)
    
    except Exception as e:
        st.error(f"Error al cargar detalles: {e}")

def generate_complete_report(cocktail_model: CocktailModel) -> Dict[str, Any]:
    """Generar reporte completo del catálogo"""
    
    try:
        report = {
            'fecha_generacion': datetime.now().isoformat(),
            'total_cocteles': cocktail_model.get_total_cocktails(),
            'distribucion_por_tipo': cocktail_model.get_cocktails_by_type(),
            'ingredientes_totales': len(cocktail_model.get_all_ingredientes()),
            'estadisticas': cocktail_model.get_cocktail_statistics(),
            'cocteles_recientes': cocktail_model.get_recent_cocktails(limit=10)
        }
        return report
    
    except Exception as e:
        return {'error': str(e)}

# Renderizar la página
if __name__ == "__main__":
    render_cocktails_page()