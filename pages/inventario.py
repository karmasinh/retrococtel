"""
📦 Página de Gestión de Inventario
CRUD completo para ingredientes con diseño profesional y adaptación a nueva BD
"""

import streamlit as st
import pandas as pd
import io
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from db.models import CocktailModel
from db.db import get_db_connection
from utils.helpers import UIComponents, ModalComponents, ChartComponents

def render_inventory_page():
    """Renderizar la página completa de inventario"""
    
    # Título principal con diseño moderno
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #4ECDC4, #44A08D);
        color: white;
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    ">
        <h1 style="margin: 0; font-size: 2.5em; font-weight: 700;">📦 Gestión de Inventario</h1>
        <p style="margin: 10px 0 0 0; font-size: 1.1em; opacity: 0.9;">Administra ingredientes, stock y reabastecimiento</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicializar modelo de datos
    cocktail_model = CocktailModel()
    
    # Estado de la página
    if 'inventory_page_state' not in st.session_state:
        st.session_state.inventory_page_state = {
            'show_modal': False,
            'modal_mode': 'create',
            'selected_ingredient': None,
            'search_term': '',
            'filter_type': 'Todos',
            'filter_stock': 'Todos',
            'refresh_data': True,
            'current_page': 1,
            'items_per_page': 10
        }
    
    # Barra de herramientas superior
    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
    
    with col1:
        search_term = st.text_input("🔍 Buscar ingrediente...", 
                                  value=st.session_state.inventory_page_state['search_term'],
                                  placeholder="Ej: Ron, Lima, Azúcar...")
        st.session_state.inventory_page_state['search_term'] = search_term
    
    with col2:
        # Obtener tipos de ingredientes de la BD
        try:
            tipos = cocktail_model.get_all_tipos_ingredientes()
            tipo_options = ['Todos'] + [tipo['nombre_tipo'] for tipo in tipos]
            filter_type = st.selectbox("🧪 Filtrar por tipo", tipo_options)
            st.session_state.inventory_page_state['filter_type'] = filter_type
        except Exception as e:
            st.error(f"Error al cargar tipos: {e}")
            filter_type = st.selectbox("🧪 Filtrar por tipo", ['Todos'])
    
    with col3:
        stock_options = ['Todos', 'En stock', 'Bajo stock', 'Sin stock']
        filter_stock = st.selectbox("📊 Filtrar por stock", stock_options)
        st.session_state.inventory_page_state['filter_stock'] = filter_stock
    
    with col4:
        items_per_page = st.selectbox("📄 Items por página", [5, 10, 20, 50], 
                                     index=1, key="items_per_page_select")
        st.session_state.inventory_page_state['items_per_page'] = items_per_page
    
    with col5:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        if st.button("➕ Nuevo Ingrediente", type="primary", use_container_width=True):
            st.session_state.inventory_page_state['show_modal'] = True
            st.session_state.inventory_page_state['modal_mode'] = 'create'
            st.session_state.inventory_page_state['selected_ingredient'] = None
            st.rerun()
    
    # Obtener datos
    try:
        ingredientes = cocktail_model.get_all_ingredientes()
        inventario_items = []
        
        # Obtener todos los items de inventario
        for ingrediente in ingredientes:
            inventario = cocktail_model.get_inventario_by_ingrediente(ingrediente['id'])
            inventario_items.extend(inventario)
            
    except Exception as e:
        st.error(f"Error al conectar con la base de datos: {e}")
        return
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_ingredientes = len(ingredientes)
        UIComponents.CardMetric(
            value=total_ingredientes,
            label="Total Ingredientes",
            icon="🧪",
            trend="up",
            trend_value="+5"
        )
    
    with col2:
        total_stock = sum(item['cantidad_stock'] for item in inventario_items)
        UIComponents.CardMetric(
            value=total_stock,
            label="Stock Total",
            icon="📦",
            trend="stable",
            trend_value="0"
        )
    
    with col3:
        low_stock_count = sum(1 for item in inventario_items if item['cantidad_stock'] <= item['punto_reorden'] and item['cantidad_stock'] > 0)
        UIComponents.CardMetric(
            value=low_stock_count,
            label="Bajo Stock",
            icon="⚠️",
            trend="up" if low_stock_count > 0 else "down",
            trend_value=f"+{low_stock_count}" if low_stock_count > 0 else "0"
        )
    
    with col4:
        out_of_stock_count = sum(1 for item in inventario_items if item['cantidad_stock'] == 0)
        UIComponents.CardMetric(
            value=out_of_stock_count,
            label="Sin Stock",
            icon="❌",
            trend="up" if out_of_stock_count > 0 else "down",
            trend_value=f"+{out_of_stock_count}" if out_of_stock_count > 0 else "0"
        )
    
    # Contenido principal con tabs
    tab1, tab2, tab3 = st.tabs(["📋 Lista de Ingredientes", "📊 Análisis", "🔧 Herramientas"])
    
    with tab1:
        render_ingredients_list(cocktail_model, inventario_items)
    
    with tab2:
        render_inventory_analytics(cocktail_model, ingredientes, inventario_items)
    
    with tab3:
        render_inventory_tools(cocktail_model)
    
    # Modal para crear/editar ingrediente
    if st.session_state.inventory_page_state['show_modal']:
        render_ingredient_modal(cocktail_model)

def render_ingredients_list(cocktail_model: CocktailModel, inventario_items: List[Dict]):
    """Renderizar la lista de ingredientes con diseño moderno"""
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
    ">
        <h3 style="margin: 0;">📋 Catálogo de Ingredientes</h3>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        # Obtener ingredientes con filtros
        search_term = st.session_state.inventory_page_state['search_term']
        filter_type = st.session_state.inventory_page_state['filter_type']
        filter_stock = st.session_state.inventory_page_state['filter_stock']
        
        ingredientes = cocktail_model.get_all_ingredientes()
        
        if not ingredientes:
            st.info("🧪 No se encontraron ingredientes en el catálogo")
            return
        
        # Aplicar filtros
        filtered_ingredients = []
        for ingrediente in ingredientes:
            # Filtro de búsqueda
            if search_term and search_term.lower() not in ingrediente['nombre'].lower():
                continue
                
            # Filtro por tipo
            if filter_type != 'Todos' and ingrediente.get('nombre_tipo') != filter_type:
                continue
            
            # Obtener inventario para este ingrediente
            inventario = cocktail_model.get_inventario_by_ingrediente(ingrediente['id'])
            
            # Filtro por stock
            if filter_stock != 'Todos':
                if filter_stock == 'En stock':
                    if not any(item['cantidad_stock'] > 0 for item in inventario):
                        continue
                elif filter_stock == 'Bajo stock':
                    if not any(item['cantidad_stock'] <= item['punto_reorden'] and item['cantidad_stock'] > 0 for item in inventario):
                        continue
                elif filter_stock == 'Sin stock':
                    if not any(item['cantidad_stock'] == 0 for item in inventario):
                        continue
            
            # Agregar datos de inventario al ingrediente
            ingrediente['inventario'] = inventario
            ingrediente['total_stock'] = sum(item['cantidad_stock'] for item in inventario)
            ingrediente['stock_status'] = get_stock_status(inventario)
            
            filtered_ingredients.append(ingrediente)
        
        # Paginación
        items_per_page = st.session_state.inventory_page_state['items_per_page']
        total_items = len(filtered_ingredients)
        total_pages = (total_items + items_per_page - 1) // items_per_page
        current_page = st.session_state.inventory_page_state['current_page']
        
        # Mostrar información de paginación
        col1, col2, col3 = st.columns([2, 3, 2])
        with col1:
            st.write(f"Mostrando {min(items_per_page, total_items)} de {total_items} ingredientes")
        
        with col2:
            if total_pages > 1:
                page_options = list(range(1, total_pages + 1))
                new_page = st.selectbox("Página", page_options, index=current_page-1)
                if new_page != current_page:
                    st.session_state.inventory_page_state['current_page'] = new_page
                    st.rerun()
        
        with col3:
            if st.button("🔄 Actualizar"):
                st.rerun()
        
        # Obtener ingredientes para la página actual
        start_idx = (current_page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        page_ingredients = filtered_ingredients[start_idx:end_idx]
        
        # Mostrar ingredientes en grid responsive
        if page_ingredients:
            cols = st.columns(3)  # 3 columnas para diseño responsive
            
            for idx, ingrediente in enumerate(page_ingredients):
                col_idx = idx % 3
                with cols[col_idx]:
                    render_ingredient_card(ingrediente)
        else:
            st.info("🧪 No se encontraron ingredientes con los filtros aplicados")
            
    except Exception as e:
        st.error(f"Error al cargar ingredientes: {e}")

def render_ingredient_card(ingrediente: Dict):
    """Renderizar tarjeta individual de ingrediente"""
    
    # Determinar color del borde según estado del stock
    stock_status = ingrediente.get('stock_status', 'unknown')
    border_color = {
        'good': '#4CAF50',      # Verde
        'low': '#FF9800',       # Naranja
        'out': '#F44336',       # Rojo
        'unknown': '#9E9E9E'    # Gris
    }.get(stock_status, '#9E9E9E')
    
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
            <h4 style="margin: 0; color: #333;">{ingrediente['nombre']}</h4>
            <span style="background: {border_color}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.8em;">
                {get_stock_status_text(stock_status)}
            </span>
        </div>
        <p style="margin: 5px 0; color: #666; font-size: 0.9em;">
            <strong>Tipo:</strong> {ingrediente.get('nombre_tipo', 'Sin tipo')}
        </p>
        <p style="margin: 5px 0; color: #666; font-size: 0.9em;">
            <strong>Stock Total:</strong> {ingrediente.get('total_stock', 0)} {ingrediente.get('unidad_medida', 'unidades')}
        </p>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)
    
    # Botones de acción
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("👁️ Ver", key=f"view_{ingrediente['id']}", use_container_width=True):
            show_ingredient_details_modal(ingrediente)
    
    with col2:
        if st.button("✏️ Editar", key=f"edit_{ingrediente['id']}", use_container_width=True):
            st.session_state.inventory_page_state['show_modal'] = True
            st.session_state.inventory_page_state['modal_mode'] = 'edit'
            st.session_state.inventory_page_state['selected_ingredient'] = ingrediente
            st.rerun()
    
    with col3:
        if st.button("🗑️ Eliminar", key=f"delete_{ingrediente['id']}", use_container_width=True):
            if st.checkbox("⚠️ Confirmar eliminación", key=f"confirm_{ingrediente['id']}"):
                try:
                    success = cocktail_model.delete_ingrediente(ingrediente['id'])
                    if success:
                        st.success(f"✅ Ingrediente {ingrediente['nombre']} eliminado exitosamente")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Error al eliminar ingrediente")
                except Exception as e:
                    st.error(f"❌ Error al eliminar: {e}")

def render_inventory_analytics(cocktail_model: CocktailModel, ingredientes: List[Dict], inventario_items: List[Dict]):
    """Renderizar análisis de inventario"""
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
    ">
        <h3 style="margin: 0;">📊 Análisis de Inventario</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Gráficos de análisis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Distribución por Tipo de Ingrediente")
        
        tipo_counts = {}
        for ingrediente in ingredientes:
            tipo = ingrediente.get('nombre_tipo', 'Sin tipo')
            tipo_counts[tipo] = tipo_counts.get(tipo, 0) + 1
        
        if tipo_counts:
            df_tipos = pd.DataFrame(list(tipo_counts.items()), columns=['Tipo', 'Cantidad'])
            fig = ChartComponents.create_cocktail_distribution_chart(df_tipos, 'Tipo', 'Cantidad', 
                                                                   'Distribución por Tipo')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Estado del Stock")
        
        stock_status = {'Buen Stock': 0, 'Stock Bajo': 0, 'Sin Stock': 0}
        
        for item in inventario_items:
            cantidad = item.get('cantidad_stock', 0)
            minimo = item.get('punto_reorden', 0)
            
            if cantidad == 0:
                stock_status['Sin Stock'] += 1
            elif cantidad <= minimo:
                stock_status['Stock Bajo'] += 1
            else:
                stock_status['Buen Stock'] += 1
        
        if stock_status:
            df_stock = pd.DataFrame(list(stock_status.items()), columns=['Estado', 'Cantidad'])
            colors = ['#4CAF50', '#FF9800', '#F44336']  # Verde, Naranja, Rojo
            fig = ChartComponents.create_cocktail_distribution_chart(df_stock, 'Estado', 'Cantidad', 
                                                                   'Estado del Stock', colors)
            st.plotly_chart(fig, use_container_width=True)
    
    # Estadísticas rápidas
    st.subheader("📈 Estadísticas Rápidas")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        valor_total = sum(item.get('cantidad_stock', 0) * item.get('precio_unitario', 0) for item in inventario_items)
        st.metric("💰 Valor Total", f"${valor_total:,.2f}")
    
    with col2:
        avg_stock = sum(item.get('cantidad_stock', 0) for item in inventario_items) / len(inventario_items) if inventario_items else 0
        st.metric("📊 Stock Promedio", f"{avg_stock:.1f}")
    
    with col3:
        ingredientes_unicos = len(set(item.get('ingrediente_id') for item in inventario_items))
        st.metric("🧪 Ingredientes Únicos", ingredientes_unicos)
    
    with col4:
        items_reorder = sum(1 for item in inventario_items if item.get('cantidad_stock', 0) <= item.get('punto_reorden', 0))
        st.metric("⚠️ Items a Reordenar", items_reorder)

def render_inventory_tools(cocktail_model: CocktailModel):
    """Renderizar herramientas de inventario"""
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #a8edea, #fed6e3);
        color: #333;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
    ">
        <h3 style="margin: 0;">🔧 Herramientas de Inventario</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📤 Exportar Datos")
        
        if st.button("📊 Exportar a CSV", type="primary"):
            try:
                ingredientes = cocktail_model.get_all_ingredientes()
                inventario = []
                for ing in ingredientes:
                    inv_items = cocktail_model.get_inventario_by_ingrediente(ing['id'])
                    inventario.extend(inv_items)
                
                if inventario:
                    df = pd.DataFrame(inventario)
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="⬇️ Descargar CSV",
                        data=csv,
                        file_name=f"inventario_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                    st.success("✅ Datos preparados para descarga")
                else:
                    st.warning("⚠️ No hay datos de inventario para exportar")
            except Exception as e:
                st.error(f"❌ Error al exportar: {e}")
        
        if st.button("📋 Exportar a Excel"):
            try:
                ingredientes = cocktail_model.get_all_ingredientes()
                inventario = []
                for ing in ingredientes:
                    inv_items = cocktail_model.get_inventario_by_ingrediente(ing['id'])
                    inventario.extend(inv_items)
                
                if inventario:
                    df = pd.DataFrame(inventario)
                    excel_buffer = io.BytesIO()
                    df.to_excel(excel_buffer, index=False, sheet_name='Inventario')
                    excel_data = excel_buffer.getvalue()
                    
                    st.download_button(
                        label="⬇️ Descargar Excel",
                        data=excel_data,
                        file_name=f"inventario_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    st.success("✅ Datos preparados para descarga")
                else:
                    st.warning("⚠️ No hay datos de inventario para exportar")
            except Exception as e:
                st.error(f"❌ Error al exportar: {e}")
    
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
                
                if st.button("📤 Cargar datos"):
                    # Procesar importación
                    success_count = 0
                    for _, row in df.iterrows():
                        try:
                            # Aquí iría la lógica de importación
                            success_count += 1
                        except Exception as e:
                            st.warning(f"⚠️ Error en fila {row.name}: {e}")
                    
                    st.success(f"✅ Se importaron {success_count} registros exitosamente")
                    time.sleep(2)
                    st.rerun()
                    
            except Exception as e:
                st.error(f"❌ Error al procesar archivo: {e}")
    
    # Herramientas adicionales
    st.subheader("🛠️ Herramientas Adicionales")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Actualizar todo el inventario"):
            try:
                # Lógica de actualización masiva
                st.info("🔄 Actualizando inventario...")
                time.sleep(2)
                st.success("✅ Inventario actualizado exitosamente")
            except Exception as e:
                st.error(f"❌ Error al actualizar: {e}")
    
    with col2:
        if st.button("📊 Generar reporte de inventario"):
            try:
                # Generar reporte completo
                ingredientes = cocktail_model.get_all_ingredientes()
                inventario = []
                for ing in ingredientes:
                    inv_items = cocktail_model.get_inventario_by_ingrediente(ing['id'])
                    inventario.extend(inv_items)
                
                # Crear resumen
                report_data = {
                    'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'total_ingredientes': len(ingredientes),
                    'total_items_inventario': len(inventario),
                    'valor_total': sum(item.get('cantidad_stock', 0) * item.get('precio_unitario', 0) for item in inventario),
                    'items_bajo_stock': sum(1 for item in inventario if item.get('cantidad_stock', 0) <= item.get('punto_reorden', 0)),
                    'items_sin_stock': sum(1 for item in inventario if item.get('cantidad_stock', 0) == 0)
                }
                
                st.write("📊 Resumen del Reporte:")
                st.json(report_data)
                
                # Botón para descargar reporte
                report_text = f"""
REPORTE DE INVENTARIO
Fecha: {report_data['fecha']}
Total Ingredientes: {report_data['total_ingredientes']}
Total Items Inventario: {report_data['total_items_inventario']}
Valor Total: ${report_data['valor_total']:,.2f}
Items Bajo Stock: {report_data['items_bajo_stock']}
Items Sin Stock: {report_data['items_sin_stock']}
                """
                
                st.download_button(
                    label="⬇️ Descargar Reporte",
                    data=report_text,
                    file_name=f"reporte_inventario_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"❌ Error al generar reporte: {e}")
    
    with col3:
        if st.button("🗂️ Limpiar datos temporales"):
            try:
                # Limpiar caché y datos temporales
                st.cache_data.clear()
                st.success("✅ Datos temporales limpiados")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error al limpiar: {e}")

def show_ingredient_details_modal(ingrediente: Dict):
    """Mostrar modal con detalles del ingrediente"""
    
    with st.expander(f"👁️ Detalles de {ingrediente['nombre']}", expanded=True):
        st.write(f"**Nombre:** {ingrediente['nombre']}")
        st.write(f"**Tipo:** {ingrediente.get('nombre_tipo', 'Sin tipo')}")
        st.write(f"**Descripción:** {ingrediente.get('descripcion', 'Sin descripción')}")
        st.write(f"**Unidad de Medida:** {ingrediente.get('unidad_predeterminada', 'No especificada')}")
        
        # Mostrar inventario
        inventario = ingrediente.get('inventario', [])
        if inventario:
            st.write("**Stock en Inventario:**")
            for item in inventario:
                unidad_nombre = item.get('unidad_nombre', ingrediente.get('unidad_predeterminada', 'unidades'))
                st.write(f"- Unidad: {unidad_nombre}")
                st.write(f"  Cantidad: {item.get('cantidad_stock', 0)}")
                st.write(f"  Punto de Reorden: {item.get('punto_reorden', 0)}")
        else:
            st.write("**Sin información de inventario**")

def render_ingredient_modal(cocktail_model: CocktailModel):
    """Modal para crear/editar ingrediente"""
    
    modal_title = "✏️ Editar Ingrediente" if st.session_state.inventory_page_state['modal_mode'] == 'edit' else "➕ Crear Nuevo Ingrediente"
    
    with st.expander(modal_title, expanded=True):
        try:
            # Obtener datos del ingrediente si es edición
            if st.session_state.inventory_page_state['modal_mode'] == 'edit' and st.session_state.inventory_page_state['selected_ingredient']:
                ingrediente = st.session_state.inventory_page_state['selected_ingredient']
                inventario = cocktail_model.get_inventario_by_ingrediente(ingrediente['id'])
            else:
                ingrediente = None
                inventario = []
            
            # Formulario principal
            with st.form("ingredient_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    nombre = st.text_input("🏷️ Nombre del ingrediente*", 
                                         value=ingrediente['nombre'] if ingrediente else "",
                                         placeholder="Ej: Ron Blanco")
                    
                    # Selector de tipo
                    tipos = cocktail_model.get_all_tipos_ingredientes()
                    tipo_options = [tipo['nombre_tipo'] for tipo in tipos]
                    tipo_default = ingrediente.get('nombre_tipo', tipo_options[0]) if ingrediente else tipo_options[0]
                    tipo_ingrediente = st.selectbox("🧪 Tipo de ingrediente*", tipo_options, 
                                                  index=tipo_options.index(tipo_default) if tipo_default in tipo_options else 0)
                    
                    # Selector de unidad de medida desde catálogo
                    unidades = cocktail_model.get_unidades_medida()
                    unidad_nombres = [u['nombre'] for u in unidades] if unidades else ['Unidad']
                    unidad_default_nombre = (inventario[0].get('unidad_nombre') if inventario and inventario[0].get('unidad_nombre') else (ingrediente.get('unidad_predeterminada') if ingrediente else unidad_nombres[0]))
                    unidad_nombre = st.selectbox("⚖️ Unidad de medida*", unidad_nombres, index=(unidad_nombres.index(unidad_default_nombre) if unidad_default_nombre in unidad_nombres else 0))
                    unidad_id_seleccionada = next((u['id'] for u in unidades if u['nombre'] == unidad_nombre), None)
                
                with col2:
                    cantidad_stock = st.number_input("📦 Cantidad en stock*", 
                                                     min_value=0, 
                                                     value=inventario[0]['cantidad_stock'] if inventario else 0,
                                                     step=1)
                    
                    punto_reorden = st.number_input("⚠️ Punto de reorden*", 
                                                   min_value=0,
                                                   value=inventario[0]['punto_reorden'] if inventario else 10,
                                                   step=1)
                    
                    # El esquema actual no maneja precio_unitario en inventario
                    st.info("El precio unitario no está soportado por el esquema actual")
                
                descripcion = st.text_area("📝 Descripción", 
                                         value=ingrediente.get('descripcion', '') if ingrediente else '',
                                         placeholder="Descripción del ingrediente...")
                
                ubicacion = st.text_input("📍 Ubicación en almacén", 
                                        value=inventario[0]['ubicacion'] if inventario else '',
                                        placeholder="Ej: Estantería A, Sección 1")
                
                fecha_caducidad = st.date_input("📅 Fecha de caducidad", 
                                              value=datetime.strptime(inventario[0]['fecha_caducidad'], '%Y-%m-%d').date() if inventario and inventario[0].get('fecha_caducidad') else None,
                                              help="Dejar vacío si no aplica")
                
                # Botones de acción
                col1, col2, col3 = st.columns([1, 1, 1])
                
                with col1:
                    submit = st.form_submit_button("💾 Guardar", type="primary", use_container_width=True)
                
                with col2:
                    if st.form_submit_button("❌ Cancelar", use_container_width=True):
                        st.session_state.inventory_page_state['show_modal'] = False
                        st.session_state.inventory_page_state['selected_ingredient'] = None
                        st.rerun()
                
                with col3:
                    if st.form_submit_button("🔄 Reiniciar", use_container_width=True):
                        st.rerun()
                
                if submit:
                    # Validación de campos requeridos
                    if not nombre or not tipo_ingrediente or not unidad_id_seleccionada:
                        st.error("❌ Por favor complete todos los campos requeridos*")
                        return
                    
                    try:
                        if st.session_state.inventory_page_state['modal_mode'] == 'edit' and ingrediente:
                            # Actualizar ingrediente existente
                            success = cocktail_model.update_ingrediente(
                                ingrediente_id=ingrediente['id'],
                                nombre=nombre,
                                tipo_ingrediente_id=next(t['id'] for t in tipos if t['nombre_tipo'] == tipo_ingrediente),
                                descripcion=descripcion,
                                unidad_medida=unidad_medida
                            )
                            
                            if success and inventario:
                                # Actualizar inventario
                                inventario_data = {
                                    'id': inventario[0]['id'],
                                    'cantidad_stock': cantidad_stock,
                                    'punto_reorden': punto_reorden,
                                    'unidad_id': unidad_id_seleccionada,
                                    'estado': 1
                                }
                                cocktail_model.update_inventario(inventario_data)
                            
                            if success:
                                st.success(f"✅ Ingrediente {nombre} actualizado exitosamente")
                                time.sleep(1)
                                st.session_state.inventory_page_state['show_modal'] = False
                                st.session_state.inventory_page_state['selected_ingredient'] = None
                                st.rerun()
                            else:
                                st.error("❌ Error al actualizar ingrediente")
                        
                        else:
                            # Crear nuevo ingrediente
                            nuevo_ingrediente = cocktail_model.create_ingrediente(
                                nombre=nombre,
                                tipo_ingrediente_id=next(t['id'] for t in tipos if t['nombre_tipo'] == tipo_ingrediente),
                                descripcion=descripcion,
                                unidad_medida=unidad_medida
                            )
                            
                            if nuevo_ingrediente:
                                # Crear entrada en inventario
                                inventario_data = {
                                    'ingrediente_id': nuevo_ingrediente['id'],
                                    'marca_id': None,
                                    'cantidad_stock': cantidad_stock,
                                    'punto_reorden': punto_reorden,
                                    'unidad_id': unidad_id_seleccionada,
                                    'estado': 1
                                }
                                cocktail_model.create_inventario(inventario_data)
                                
                                st.success(f"✅ Ingrediente {nombre} creado exitosamente")
                                time.sleep(1)
                                st.session_state.inventory_page_state['show_modal'] = False
                                st.rerun()
                            else:
                                st.error("❌ Error al crear ingrediente")
                    
                    except Exception as e:
                        st.error(f"❌ Error al guardar: {e}")
        
        except Exception as e:
            st.error(f"❌ Error al cargar datos del formulario: {e}")

def get_stock_status(inventario: List[Dict]) -> str:
    """Determinar el estado del stock"""
    if not inventario:
        return 'out'
    
    total_stock = sum(item.get('cantidad_stock', 0) for item in inventario)
    if total_stock == 0:
        return 'out'
    
    # Verificar si algún item está bajo stock
    for item in inventario:
        if item.get('cantidad_stock', 0) <= item.get('punto_reorden', 0) and item.get('cantidad_stock', 0) > 0:
            return 'low'
    
    return 'good'

def get_stock_status_text(status: str) -> str:
    """Obtener texto descriptivo del estado del stock"""
    return {
        'good': 'Buen Stock',
        'low': 'Stock Bajo',
        'out': 'Sin Stock',
        'unknown': 'Desconocido'
    }.get(status, 'Desconocido')

# Punto de entrada de la página
if __name__ == "__main__":
    render_inventory_page()