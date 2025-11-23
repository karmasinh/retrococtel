from .db import get_db_connection
import streamlit as st
from typing import List, Dict, Optional, Any

class CocktailModel:
    def __init__(self):
        self.db = get_db_connection()
    
    # ===== COCTELES =====
    def get_all_cocteles(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Obtiene todos los cócteles con paginación"""
        query = """
            SELECT c.*, v.nombre_vaso, mp.nombre_metodo, tc.nombre_tipo,
                   u.nombre_usuario as creado_por_nombre
            FROM cocteles c
            LEFT JOIN vasos v ON c.vaso_id = v.id
            LEFT JOIN metodos_preparacion mp ON c.metodo_id = mp.id
            LEFT JOIN tipos_cocteles tc ON c.tipo_id = tc.id
            LEFT JOIN usuarios u ON c.creado_por = u.id
            WHERE c.estado = 1
            ORDER BY c.creado_en DESC
            LIMIT %s OFFSET %s
        """
        return self.db.execute_query(query, (limit, offset))
    
    def get_coctel_by_id(self, coctel_id: int) -> Optional[Dict]:
        """Obtiene un cóctel por ID"""
        query = """
            SELECT c.*, v.nombre_vaso, mp.nombre_metodo, tc.nombre_tipo,
                   u.nombre_usuario as creado_por_nombre
            FROM cocteles c
            LEFT JOIN vasos v ON c.vaso_id = v.id
            LEFT JOIN metodos_preparacion mp ON c.metodo_id = mp.id
            LEFT JOIN tipos_cocteles tc ON c.tipo_id = tc.id
            LEFT JOIN usuarios u ON c.creado_por = u.id
            WHERE c.id = %s AND c.estado = 1
        """
        result = self.db.execute_query(query, (coctel_id,))
        return result[0] if result else None
    
    def create_coctel(self, coctel_data: Dict) -> Optional[int]:
        """Crea un nuevo cóctel"""
        query = """
            INSERT INTO cocteles (nombre, slug, descripcion_larga, vaso_id, 
                                metodo_id, tipo_id, porciones, calorias, 
                                tiempo_preparacion, dificultad, creado_por)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            coctel_data['nombre'],
            coctel_data['slug'],
            coctel_data.get('descripcion_larga'),
            coctel_data.get('vaso_id'),
            coctel_data.get('metodo_id'),
            coctel_data.get('tipo_id'),
            coctel_data.get('porciones', 1),
            coctel_data.get('calorias'),
            coctel_data.get('tiempo_preparacion'),
            coctel_data.get('dificultad', 'Fácil'),
            coctel_data.get('creado_por', 1)
        )
        return self.db.execute_query(query, params, fetch=False)
    
    def update_coctel(self, coctel_id: int, coctel_data: Dict) -> bool:
        """Actualiza un cóctel existente"""
        query = """
            UPDATE cocteles 
            SET nombre = %s, slug = %s, descripcion_larga = %s, 
                vaso_id = %s, metodo_id = %s, tipo_id = %s, 
                porciones = %s, calorias = %s, tiempo_preparacion = %s, 
                dificultad = %s
            WHERE id = %s
        """
        params = (
            coctel_data['nombre'],
            coctel_data['slug'],
            coctel_data.get('descripcion_larga'),
            coctel_data.get('vaso_id'),
            coctel_data.get('metodo_id'),
            coctel_data.get('tipo_id'),
            coctel_data.get('porciones', 1),
            coctel_data.get('calorias'),
            coctel_data.get('tiempo_preparacion'),
            coctel_data.get('dificultad', 'Fácil'),
            coctel_id
        )
        result = self.db.execute_query(query, params, fetch=False)
        return bool(result)
    
    def delete_coctel(self, coctel_id: int) -> bool:
        """Elimina un cóctel (borrado lógico)"""
        query = "UPDATE cocteles SET estado = 0 WHERE id = %s"
        result = self.db.execute_query(query, (coctel_id,), fetch=False)
        return bool(result)
    
    # ===== INGREDIENTES E INVENTARIO =====
    def get_all_ingredientes(self) -> List[Dict]:
        """Obtiene todos los ingredientes activos"""
        query = """
            SELECT i.*, ti.nombre_tipo, um.nombre as unidad_predeterminada
            FROM ingredientes i
            LEFT JOIN tipos_ingredientes ti ON i.tipo_id = ti.id
            LEFT JOIN unidades_medida um ON i.unidad_predeterminada = um.id
            WHERE i.estado = 1
            ORDER BY i.nombre
        """
        return self.db.execute_query(query)
    
    def get_inventario_by_ingrediente(self, ingrediente_id: int) -> List[Dict]:
        """Obtiene el inventario de un ingrediente específico"""
        query = """
            SELECT inv.*, i.nombre as ingrediente_nombre, m.nombre_marca, um.nombre as unidad_nombre
            FROM inventario inv
            JOIN ingredientes i ON inv.ingrediente_id = i.id
            LEFT JOIN marcas m ON inv.marca_id = m.id
            LEFT JOIN unidades_medida um ON inv.unidad_id = um.id
            WHERE inv.ingrediente_id = %s AND inv.estado = 1
        """
        return self.db.execute_query(query, (ingrediente_id,))
    
    def update_inventario_stock(self, inventario_id: int, nueva_cantidad: float) -> bool:
        """Actualiza el stock de un item del inventario"""
        query = "UPDATE inventario SET cantidad_stock = %s WHERE id = %s"
        result = self.db.execute_query(query, (nueva_cantidad, inventario_id), fetch=False)
        return bool(result)
    
    # ===== USUARIOS Y ROLES =====
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Obtiene un usuario por nombre de usuario"""
        query = """
            SELECT u.*, r.nombre as rol_nombre, r.tema_preferido
            FROM usuarios u
            LEFT JOIN roles r ON u.rol_id = r.id
            WHERE u.nombre_usuario = %s AND u.estado = 'Activo'
        """
        result = self.db.execute_query(query, (username,))
        return result[0] if result else None
    
    def get_all_roles(self) -> List[Dict]:
        """Obtiene todos los roles"""
        query = "SELECT * FROM roles WHERE estado = 1 ORDER BY nombre"
        return self.db.execute_query(query)
    
    def create_user(self, user_data: Dict) -> Optional[int]:
        """Crea un nuevo usuario"""
        query = """
            INSERT INTO usuarios (nombre_completo, nombre_usuario, email, 
                                password_hash, rol_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            user_data['nombre_completo'],
            user_data['nombre_usuario'],
            user_data['email'],
            user_data['password_hash'],
            user_data.get('rol_id', 2)  # Rol por defecto: usuario normal
        )
        return self.db.execute_query(query, params, fetch=False)
    
    # ===== CATALOGOS =====
    def get_vasos(self) -> List[Dict]:
        """Obtiene todos los vasos"""
        query = "SELECT * FROM vasos WHERE estado = 1 ORDER BY nombre_vaso"
        return self.db.execute_query(query)
    
    def get_metodos_preparacion(self) -> List[Dict]:
        """Obtiene todos los métodos de preparación"""
        query = "SELECT * FROM metodos_preparacion WHERE estado = 1 ORDER BY nombre_metodo"
        return self.db.execute_query(query)
    
    def get_tipos_cocteles(self) -> List[Dict]:
        """Obtiene todos los tipos de cócteles"""
        query = "SELECT * FROM tipos_cocteles WHERE estado = 1 ORDER BY nombre_tipo"
        return self.db.execute_query(query)
    
    def get_categorias_cocteles(self) -> List[Dict]:
        """Obtiene todas las categorías de cócteles"""
        query = "SELECT * FROM categorias_cocteles WHERE estado = 1 ORDER BY nombre_categoria"
        return self.db.execute_query(query)
    
    def get_unidades_medida(self) -> List[Dict]:
        """Obtiene todas las unidades de medida"""
        query = "SELECT * FROM unidades_medida WHERE estado = 1 ORDER BY nombre"
        return self.db.execute_query(query)
    
    def get_tipos_ingredientes(self) -> List[Dict]:
        """Obtiene todos los tipos de ingredientes"""
        query = "SELECT * FROM tipos_ingredientes WHERE estado = 1 ORDER BY nombre_tipo"
        return self.db.execute_query(query)
    
    def get_marcas(self) -> List[Dict]:
        """Obtiene todas las marcas"""
        query = "SELECT * FROM marcas WHERE estado = 1 ORDER BY nombre_marca"
        return self.db.execute_query(query)
    
    # ===== MÉTODOS ADICIONALES PARA STREAMLIT =====
    def get_all_cocktails(self) -> List[Dict]:
        """Obtiene todos los cócteles (alias para compatibilidad)"""
        return self.get_all_cocteles()
    
    # ===== MÉTODOS ADICIONALES PARA CÓCTELES =====
    def get_total_cocktails(self) -> int:
        """Obtiene el total de cócteles activos"""
        query = "SELECT COUNT(*) as total FROM cocteles WHERE estado = 1"
        result = self.db.execute_query(query)
        return result[0]['total'] if result else 0
    
    def get_cocktails_by_type(self) -> List[Dict]:
        """Obtiene cócteles agrupados por tipo"""
        query = """
            SELECT tc.nombre_tipo as tipo, COUNT(c.id) as cantidad
            FROM cocteles c
            JOIN tipos_cocteles tc ON c.tipo_id = tc.id
            WHERE c.estado = 1
            GROUP BY tc.nombre_tipo
            ORDER BY cantidad DESC
        """
        return self.db.execute_query(query)
    
    def get_recent_cocktails(self, limit: int = 5) -> List[Dict]:
        """Obtiene los cócteles más recientes"""
        query = f"""
            SELECT c.*, tc.nombre_tipo, v.nombre_vaso, mp.nombre_metodo
            FROM cocteles c
            LEFT JOIN tipos_cocteles tc ON c.tipo_id = tc.id
            LEFT JOIN vasos v ON c.vaso_id = v.id
            LEFT JOIN metodos_preparacion mp ON c.metodo_id = mp.id
            WHERE c.estado = 1
            ORDER BY c.creado_en DESC
            LIMIT {limit}
        """
        return self.db.execute_query(query)
    
    def get_cocktails_filtered(self, search_term: str = "", tipo_filter: str = None, dificultad_filter: str = None) -> List[Dict]:
        """Obtiene cócteles con filtros"""
        conditions = ["c.estado = 1"]
        params = []
        
        if search_term:
            conditions.append("(c.nombre LIKE %s OR c.descripcion_larga LIKE %s)")
            search_pattern = f"%{search_term}%"
            params.extend([search_pattern, search_pattern])
        
        if tipo_filter and tipo_filter != 'Todos':
            conditions.append("tc.nombre_tipo = %s")
            params.append(tipo_filter)
        
        if dificultad_filter and dificultad_filter != 'Todos':
            conditions.append("c.dificultad = %s")
            params.append(dificultad_filter)
        
        where_clause = " AND ".join(conditions)
        
        query = f"""
            SELECT c.*, tc.nombre_tipo, v.nombre_vaso, mp.nombre_metodo
            FROM cocteles c
            LEFT JOIN tipos_cocteles tc ON c.tipo_id = tc.id
            LEFT JOIN vasos v ON c.vaso_id = v.id
            LEFT JOIN metodos_preparacion mp ON c.metodo_id = mp.id
            WHERE {where_clause}
            ORDER BY c.nombre
        """
        
        return self.db.execute_query(query, params if params else None)
    
    # ===== MÉTODOS PARA GESTIÓN DE ROLES (ADICIONALES) =====
    def get_total_roles(self) -> int:
        """Obtiene el total de roles"""
        query = "SELECT COUNT(*) as total FROM roles WHERE estado = 1"
        result = self.db.execute_query(query)
        return result[0]['total'] if result else 0
    
    def get_active_roles_count(self) -> int:
        """Obtiene el número de roles activos"""
        return self.get_total_roles()  # Mismo que total_roles ya que solo traemos activos
    
    def get_roles_by_permission_level(self) -> List[Dict]:
        """Obtiene roles agrupados por nivel de permisos (versión simplificada)"""
        # Como no tenemos columnas de permisos, retornamos un agregado simple de roles activos
        query = """
            SELECT 
                'Roles activos' AS nivel_permiso,
                COUNT(*) AS cantidad
            FROM roles 
            WHERE estado = 1
        """
        return self.db.execute_query(query)
    
    def get_most_common_role(self) -> Optional[Dict]:
        """Obtiene el rol más común"""
        query = """
            SELECT r.*, COUNT(u.id) as usuarios_count
            FROM roles r
            LEFT JOIN usuarios u ON r.id = u.rol_id AND u.estado = 'Activo'
            WHERE r.estado = 1
            GROUP BY r.id
            ORDER BY usuarios_count DESC
            LIMIT 1
        """
        result = self.db.execute_query(query)
        return result[0] if result else None
    
    def get_recent_roles(self, limit: int = 5) -> List[Dict]:
        """Obtiene los roles más recientes"""
        query = f"SELECT * FROM roles WHERE estado = 1 ORDER BY id DESC LIMIT {limit}"
        return self.db.execute_query(query)
    
    def get_roles_filtered(self, search_term: str = "") -> List[Dict]:
        """Obtiene roles filtrados por búsqueda"""
        if search_term:
            query = """
                SELECT * FROM roles 
                WHERE estado = 1 AND (nombre LIKE %s OR descripcion LIKE %s)
                ORDER BY nombre
            """
            search_pattern = f"%{search_term}%"
            return self.db.execute_query(query, (search_pattern, search_pattern))
        else:
            return self.get_all_roles()
    
    def delete_role(self, role_id: int) -> bool:
        """Elimina un rol (borrado lógico)"""
        query = "UPDATE roles SET estado = 0 WHERE id = %s"
        result = self.db.execute_query(query, (role_id,), fetch=False)
        return bool(result)
    
    def get_roles_distribution(self) -> List[Dict]:
        """Obtiene la distribución de roles"""
        query = """
            SELECT r.nombre, COUNT(u.id) as usuarios_count
            FROM roles r
            LEFT JOIN usuarios u ON r.id = u.rol_id AND u.estado = 'Activo'
            WHERE r.estado = 1
            GROUP BY r.id, r.nombre
            ORDER BY usuarios_count DESC
        """
        return self.db.execute_query(query)
    
    def get_role_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas de roles (versión simplificada)"""
        total_roles = self.get_total_roles()
        active_roles = self.get_active_roles_count()
        
        # Como no tenemos columnas de permisos, retornamos estadísticas básicas
        return {
            'total_roles': total_roles,
            'active_roles': active_roles,
            'admin_roles': 0,  # No hay datos de permisos
            'user_roles': 0,   # No hay datos de permisos
            'inventory_roles': 0,  # No hay datos de permisos
            'cocktail_roles': 0    # No hay datos de permisos
        }
    
    def create_role(self, role_data: Dict) -> Optional[int]:
        """Crea un nuevo rol (versión simplificada sin permisos)"""
        query = """
            INSERT INTO roles (nombre, descripcion, estado)
            VALUES (%s, %s, %s)
        """
        params = (
            role_data['nombre'],
            role_data.get('descripcion', ''),
            role_data.get('estado', 1)
        )
        return self.db.execute_query(query, params, fetch=False)
    
    def update_role(self, role_data: Dict) -> bool:
        """Actualiza un rol existente (versión simplificada sin permisos)"""
        query = """
            UPDATE roles 
            SET nombre = %s, descripcion = %s, estado = %s
            WHERE id = %s
        """
        params = (
            role_data['nombre'],
            role_data.get('descripcion', ''),
            role_data.get('estado', 1),
            role_data['id']
        )
        result = self.db.execute_query(query, params, fetch=False)
        return bool(result)
    
    def get_users_by_role(self, role_id: int) -> List[Dict]:
        """Obtiene usuarios por rol"""
        query = """
            SELECT u.id, u.nombre_completo, u.nombre_usuario, u.email
            FROM usuarios u
            WHERE u.rol_id = %s AND u.estado = 'Activo'
        """
        return self.db.execute_query(query, (role_id,))
    
    def get_total_users(self) -> int:
        """Obtiene el total de usuarios activos"""
        query = "SELECT COUNT(*) as total FROM usuarios WHERE estado = 'Activo'"
        result = self.db.execute_query(query)
        return result[0]['total'] if result else 0
    
    def update_user_theme(self, user_id: int, theme: str) -> bool:
        """Actualiza el tema preferido del usuario"""
        query = """
            UPDATE usuarios SET tema_preferido = %s WHERE id = %s
        """
        result = self.db.execute_query(query, (theme, user_id), fetch=False)
        return bool(result)
    
    def get_user_theme(self, user_id: int) -> str:
        """Obtiene el tema preferido del usuario"""
        query = "SELECT tema_preferido FROM usuarios WHERE id = %s"
        result = self.db.execute_query(query, (user_id,))
        if result and result[0].get('tema_preferido'):
            return result[0]['tema_preferido']
        return 'default'
    
    # ===== MÉTODOS ADICIONALES PARA INVENTARIO =====
    def get_all_tipos_ingredientes(self) -> List[Dict]:
        """Obtiene todos los tipos de ingredientes"""
        query = "SELECT * FROM tipos_ingredientes WHERE estado = 1 ORDER BY nombre_tipo"
        return self.db.execute_query(query)
    
    def create_cocktail(self, cocktail_data: Dict) -> Optional[int]:
        """Crea un nuevo cóctel (alias para compatibilidad)"""
        return self.create_coctel(cocktail_data)
    
    def update_cocktail(self, cocktail_id: int, cocktail_data: Dict) -> bool:
        """Actualiza un cóctel (alias para compatibilidad)"""
        return self.update_coctel(cocktail_id, cocktail_data)
    
    def delete_cocktail(self, cocktail_id: int) -> bool:
        """Elimina un cóctel (alias para compatibilidad)"""
        return self.delete_coctel(cocktail_id)
    
    def get_cocktail_by_id(self, cocktail_id: int) -> Optional[Dict]:
        """Obtiene un cóctel por ID (alias para compatibilidad)"""
        return self.get_coctel_by_id(cocktail_id)
    
    def get_cocktails_filtered(self, search_term: str = '', tipo_filter: str = None, 
                              dificultad_filter: str = None) -> List[Dict]:
        """Obtiene cócteles con filtros avanzados"""
        query = """
            SELECT c.*, v.nombre_vaso, mp.nombre_metodo, tc.nombre_tipo,
                   u.nombre_usuario as creado_por_nombre
            FROM cocteles c
            LEFT JOIN vasos v ON c.vaso_id = v.id
            LEFT JOIN metodos_preparacion mp ON c.metodo_id = mp.id
            LEFT JOIN tipos_cocteles tc ON c.tipo_id = tc.id
            LEFT JOIN usuarios u ON c.creado_por = u.id
            WHERE c.estado = 1
        """
        
        params = []
        
        if search_term:
            query += " AND (c.nombre LIKE %s OR c.descripcion_larga LIKE %s)"
            search_pattern = f"%{search_term}%"
            params.extend([search_pattern, search_pattern])
        
        if tipo_filter:
            query += " AND tc.nombre_tipo = %s"
            params.append(tipo_filter)
        
        if dificultad_filter:
            query += " AND c.dificultad = %s"
            params.append(dificultad_filter)
        
        query += " ORDER BY c.creado_en DESC"
        
        return self.db.execute_query(query, tuple(params))
    
    def get_cocktails_by_type(self) -> List[Dict]:
        """Obtiene la distribución de cócteles por tipo"""
        query = """
            SELECT tc.nombre_tipo, COUNT(c.id) as cantidad
            FROM tipos_cocteles tc
            LEFT JOIN cocteles c ON tc.id = c.tipo_id AND c.estado = 1
            WHERE tc.estado = 1
            GROUP BY tc.id, tc.nombre_tipo
            ORDER BY cantidad DESC
        """
        return self.db.execute_query(query)
    
    def get_recent_cocktails(self, limit: int = 5) -> List[Dict]:
        """Obtiene los cócteles más recientes"""
        query = """
            SELECT c.*, v.nombre_vaso, mp.nombre_metodo, tc.nombre_tipo,
                   u.nombre_usuario as creado_por_nombre
            FROM cocteles c
            LEFT JOIN vasos v ON c.vaso_id = v.id
            LEFT JOIN metodos_preparacion mp ON c.metodo_id = mp.id
            LEFT JOIN tipos_cocteles tc ON c.tipo_id = tc.id
            LEFT JOIN usuarios u ON c.creado_por = u.id
            WHERE c.estado = 1
            ORDER BY c.creado_en DESC
            LIMIT %s
        """
        return self.db.execute_query(query, (limit,))
    
    def get_cocktail_full_details(self, cocktail_id: int) -> Optional[Dict]:
        """Obtiene todos los detalles de un cóctel"""
        # Información básica del cóctel
        cocktail = self.get_coctel_by_id(cocktail_id)
        if not cocktail:
            return None
        
        # Ingredientes del cóctel
        ingredientes_query = """
            SELECT ci.*, i.nombre AS ingrediente_nombre, i.descripcion,
                   um.nombre AS unidad_nombre, ti.nombre_tipo
            FROM coctel_ingredientes ci
            JOIN ingredientes i ON ci.ingrediente_id = i.id
            LEFT JOIN unidades_medida um ON ci.unidad_id = um.id
            LEFT JOIN tipos_ingredientes ti ON i.tipo_id = ti.id
            WHERE ci.coctel_id = %s AND ci.estado = 1
            ORDER BY i.nombre
        """
        ingredientes = self.db.execute_query(ingredientes_query, (cocktail_id,))
        
        # Instrucciones de preparación
        instrucciones_query = """
            SELECT *
            FROM pasos_coctel
            WHERE coctel_id = %s AND estado = 1
            ORDER BY orden
        """
        instrucciones = self.db.execute_query(instrucciones_query, (cocktail_id,))
        
        # Notas y variaciones
        notas = []
        
        return {
            'cocktail': cocktail,
            'ingredientes': ingredientes,
            'instrucciones': instrucciones,
            'notas': notas
        }
    
    def get_cocktail_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas del catálogo de cócteles"""
        stats = {}
        
        # Total de cócteles
        stats['total'] = self.get_total_cocteles()
        
        # Promedio de ingredientes por cóctel
        query = """
            SELECT AVG(ingredientes_count) as avg_ingredients
            FROM (
                SELECT c.id, COUNT(ci.id) as ingredientes_count
                FROM cocteles c
                LEFT JOIN coctel_ingredientes ci ON c.id = ci.coctel_id AND ci.estado = 1
                WHERE c.estado = 1
                GROUP BY c.id
            ) as subquery
        """
        result = self.db.execute_query(query)
        stats['avg_ingredients'] = result[0]['avg_ingredients'] if result and result[0]['avg_ingredients'] else 0
        
        # Tiempo promedio de preparación
        query = "SELECT AVG(tiempo_preparacion) as avg_time FROM cocteles WHERE estado = 1"
        result = self.db.execute_query(query)
        stats['avg_time'] = result[0]['avg_time'] if result and result[0]['avg_time'] else 0
        
        # Ingredientes más usados
        query = """
            SELECT i.nombre, COUNT(ci.id) as usos
            FROM ingredientes i
            JOIN coctel_ingredientes ci ON i.id = ci.ingrediente_id
            WHERE i.estado = 1 AND ci.estado = 1
            GROUP BY i.id, i.nombre
            ORDER BY usos DESC
            LIMIT 10
        """
        stats['top_ingredients'] = self.db.execute_query(query)
        
        return stats
    
    # ===== MÉTODOS ADICIONALES DE CATÁLOGOS =====
    def get_all_tipos_cocteles(self) -> List[Dict]:
        """Obtiene todos los tipos de cócteles (alias)"""
        return self.get_tipos_cocteles()
    
    def get_all_vasos(self) -> List[Dict]:
        """Obtiene todos los vasos (alias)"""
        return self.get_vasos()
    
    def get_all_metodos_preparacion(self) -> List[Dict]:
        """Obtiene todos los métodos de preparación (alias)"""
        return self.get_metodos_preparacion()
    
    def get_ingredientes(self) -> List[Dict]:
        """Alias: Obtiene todos los ingredientes"""
        return self.get_all_ingredientes()
    
    # ===== MÉTRICAS PARA DASHBOARD =====
    def get_total_cocteles(self) -> int:
        """Obtiene el total de cócteles activos"""
        query = "SELECT COUNT(*) as total FROM cocteles WHERE estado = 1"
        result = self.db.execute_query(query)
        return result[0]['total'] if result else 0
    
    def get_total_ingredientes(self) -> int:
        """Obtiene el total de ingredientes activos"""
        query = "SELECT COUNT(*) as total FROM ingredientes WHERE estado = 1"
        result = self.db.execute_query(query)
        return result[0]['total'] if result else 0
    
    def get_total_usuarios(self) -> int:
        """Obtiene el total de usuarios activos"""
        query = "SELECT COUNT(*) as total FROM usuarios WHERE estado = 'Activo'"
        result = self.db.execute_query(query)
        return result[0]['total'] if result else 0
    
    def get_cocteles_por_tipo(self) -> List[Dict]:
        """Obtiene cantidad de cócteles por tipo"""
        query = """
            SELECT tc.nombre_tipo, COUNT(c.id) as cantidad
            FROM tipos_cocteles tc
            LEFT JOIN cocteles c ON tc.id = c.tipo_id AND c.estado = 1
            WHERE tc.estado = 1
            GROUP BY tc.id, tc.nombre_tipo
            ORDER BY cantidad DESC
        """
        return self.db.execute_query(query)
    
    def get_ingredientes_bajo_stock(self) -> List[Dict]:
        """Obtiene ingredientes con bajo stock"""
        query = """
            SELECT i.nombre, inv.cantidad_stock, inv.punto_reorden, um.nombre as unidad
            FROM inventario inv
            JOIN ingredientes i ON inv.ingrediente_id = i.id
            LEFT JOIN unidades_medida um ON inv.unidad_id = um.id
            WHERE inv.cantidad_stock <= inv.punto_reorden AND inv.estado = 1
            ORDER BY inv.cantidad_stock ASC
        """
        return self.db.execute_query(query)
    
    def create_inventario(self, inventario_data: Dict) -> Optional[int]:
        """Crea un nuevo registro de inventario (alineado al esquema actual)"""
        query = """
            INSERT INTO inventario (ingrediente_id, marca_id, cantidad_stock, unidad_id, punto_reorden, estado)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            inventario_data['ingrediente_id'],
            inventario_data.get('marca_id'),
            inventario_data['cantidad_stock'],
            inventario_data['unidad_id'],
            inventario_data.get('punto_reorden', 0),
            inventario_data.get('estado', 1)
        )
        return self.db.execute_query(query, params, fetch=False)
    
    def update_inventario(self, inventario_data: Dict) -> bool:
        """Actualiza un registro de inventario existente (alineado al esquema actual)"""
        query = """
            UPDATE inventario 
            SET cantidad_stock = %s,
                unidad_id = COALESCE(%s, unidad_id),
                punto_reorden = %s,
                estado = %s
            WHERE id = %s
        """
        params = (
            inventario_data['cantidad_stock'],
            inventario_data.get('unidad_id'),
            inventario_data.get('punto_reorden', 0),
            inventario_data.get('estado', 1),
            inventario_data['id']
        )
        result = self.db.execute_query(query, params, fetch=False)
        return bool(result)
    
    def delete_ingrediente(self, ingrediente_id: int) -> bool:
        """Elimina un ingrediente (borrado lógico)"""
        query = "UPDATE ingredientes SET estado = 0 WHERE id = %s"
        result = self.db.execute_query(query, (ingrediente_id,), fetch=False)
        return bool(result)
