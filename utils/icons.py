"""
Sistema de Iconos Profesionales para CoctelMatch
Desarrollado por: Álvaro Díaz Vallejos
"""

import streamlit as st
from typing import Optional, Dict, Any
import base64

class IconManager:
    """Gestor de iconos SVG profesionales"""
    
    def __init__(self):
        self.icons = {
            # Iconos de navegación
            'dashboard': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8.354 1.146a.5.5 0 0 0-.708 0l-6 6A.5.5 0 0 0 1.5 7.5v7a.5.5 0 0 0 .5.5h4.5a.5.5 0 0 0 .5-.5v-4h2v4a.5.5 0 0 0 .5.5H14a.5.5 0 0 0 .5-.5v-7a.5.5 0 0 0-.146-.354L13 5.793V2.5a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1.293L8.354 1.146zM2.5 14V7.707l5.5-5.5 5.5 5.5V14H10v-4a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5v4H2.5z"/></svg>',
            'cocktails': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M3 14.5A1.5 1.5 0 0 1 1.5 13V7A1.5 1.5 0 0 1 3 5.5h10a1.5 1.5 0 0 1 1.5 1.5v6a1.5 1.5 0 0 1-1.5 1.5H3zM1.5 7v6h13V7H1.5zM8 1.5A2.5 2.5 0 0 1 10.5 4h-5A2.5 2.5 0 0 1 8 1.5z"/></svg>',
            'inventory': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M1 2.5A1.5 1.5 0 0 1 2.5 1h3A1.5 1.5 0 0 1 7 2.5v3A1.5 1.5 0 0 1 5.5 7h-3A1.5 1.5 0 0 1 1 5.5v-3zM2.5 2a.5.5 0 0 0-.5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5h-3zm6.5.5A1.5 1.5 0 0 1 10.5 1h3A1.5 1.5 0 0 1 15 2.5v3A1.5 1.5 0 0 1 13.5 7h-3A1.5 1.5 0 0 1 9 5.5v-3zm1.5-.5a.5.5 0 0 0-.5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5h-3zM1 10.5A1.5 1.5 0 0 1 2.5 9h3A1.5 1.5 0 0 1 7 10.5v3A1.5 1.5 0 0 1 5.5 15h-3A1.5 1.5 0 0 1 1 13.5v-3zm1.5-.5a.5.5 0 0 0-.5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5h-3zm6.5.5A1.5 1.5 0 0 1 10.5 9h3a1.5 1.5 0 0 1 1.5 1.5v3a1.5 1.5 0 0 1-1.5 1.5h-3A1.5 1.5 0 0 1 9 13.5v-3zm1.5-.5a.5.5 0 0 0-.5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5h-3z"/></svg>',
            'users': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10z"/></svg>',
            'settings': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8 4.754a3.246 3.246 0 1 0 0 6.492 3.246 3.246 0 0 0 0-6.492zM5.754 8a2.246 2.246 0 1 1 4.492 0 2.246 2.246 0 0 1-4.492 0z"/><path d="M9.796 1.343c-.527-1.79-3.065-1.79-3.592 0l-.094.319a.873.873 0 0 1-1.255.52l-.292-.16c-1.64-.892-3.433.902-2.54 2.541l.159.292a.873.873 0 0 1-.52 1.255l-.319.094c-1.79.527-1.79 3.065 0 3.592l.319.094a.873.873 0 0 1 .52 1.255l-.16.292c-.892 1.64.901 3.434 2.541 2.54l.292-.159a.873.873 0 0 1 1.255.52l.094.319c.527 1.79 3.065 1.79 3.592 0l.094-.319a.873.873 0 0 1 1.255-.52l.292.16c1.64.893 3.434-.902 2.54-2.541l-.159-.292a.873.873 0 0 1 .52-1.255l.319-.094c1.79-.527 1.79-3.065 0-3.592l-.319-.094a.873.873 0 0 1-.52-1.255l.16-.292c.893-1.64-.902-3.433-2.541-2.54l-.292.159a.873.873 0 0 1-1.255-.52l-.094-.319zm-2.633.283c.246-.835 1.428-.835 1.674 0l.094.319a1.873 1.873 0 0 0 2.693 1.115l.292-.16c.764-.415 1.6.42 1.184 1.185l-.159.292a1.873 1.873 0 0 0 1.116 2.692l.318.094c.835.246.835 1.428 0 1.674l-.319.094a1.873 1.873 0 0 0-1.115 2.693l.16.292c.415.764-.42 1.6-1.185 1.184l-.292-.159a1.873 1.873 0 0 0-2.692 1.116l-.094.318c-.246.835-1.428.835-1.674 0l-.094-.319a1.873 1.873 0 0 0-2.693-1.115l-.292.16c-.764.415-1.6-.42-1.184-1.185l.159-.292A1.873 1.873 0 0 0 1.945 8.93l-.319-.094c-.835-.246-.835-1.428 0-1.674l.319-.094A1.873 1.873 0 0 0 3.06 4.377l-.16-.292c-.415-.764.42-1.6 1.185-1.184l.292.159a1.873 1.873 0 0 0 2.692-1.116l.094-.318z"/></svg>',
            
            # Iconos de acciones
            'add': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/></svg>',
            'edit': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168l10-10zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207 11.207 2.5zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293l6.5-6.5zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325z"/></svg>',
            'delete': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/><path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/></svg>',
            'view': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zM1.173 8a13.133 13.133 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.133 13.133 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5c-2.12 0-3.879-1.168-5.168-2.457A13.134 13.134 0 0 1 1.172 8z"/><path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z"/></svg>',
            'search': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/></svg>',
            'filter': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M6 10.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5zm-2-3a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5zm-2-3a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 0 1h-11a.5.5 0 0 1-.5-.5z"/></svg>',
            'export': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/><path d="M7.646 1.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 2.707V11.5a.5.5 0 0 1-1 0V2.707L5.354 4.854a.5.5 0 1 1-.708-.708l3-3z"/></svg>',
            'import': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/><path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/></svg>',
            'chart': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/><path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/></svg>',
            'logout': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path class="bi" d="M12 1a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H6.5A1.5 1.5 0 0 1 5 12.5V11a.5.5 0 0 1 1 0v1.5a.5.5 0 0 0 .5.5H12V3H6.5a.5.5 0 0 0-.5.5V5a.5.5 0 0 1-1 0V2.5A1.5 1.5 0 0 1 6.5 1H12z"/><path d="M8.5 5.5a.5.5 0 0 0-1 0V8H5a.5.5 0 0 0 0 1h2.5v2.5a.5.5 0 0 0 1 0V9H11a.5.5 0 0 0 0-1H8.5V5.5z"/></svg>',
            'login': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8.5 10.5a.5.5 0 0 1-1 0V8H5a.5.5 0 0 1 0-1h2.5V4.5a.5.5 0 0 1 1 0V7H11a.5.5 0 0 1 0 1H8.5v2.5z"/><path d="M3.5 2.5a.5.5 0 0 0-.5.5v9a.5.5 0 0 0 .5.5h7a.5.5 0 0 0 .5-.5v-2a.5.5 0 0 1 1 0v2A1.5 1.5 0 0 1 10.5 14h-7A1.5 1.5 0 0 1 2 12.5v-9A1.5 1.5 0 0 1 3.5 2h7A1.5 1.5 0 0 1 12 3.5v2a.5.5 0 0 1-1 0v-2a.5.5 0 0 0-.5-.5h-7z"/></svg>',
            'user': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10z"/></svg>',
            'password': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8 1a2 2 0 0 1 2 2v4H6V3a2 2 0 0 1 2-2zm3 6V3a3 3 0 0 0-6 0v4a2 2 0 0 0-2 2v5a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2zM5 8h6a1 1 0 0 1 1 1v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1z"/></svg>',
            'warning': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8.893 1.5c-.183-.31-.52-.5-.887-.5s-.703.19-.886.5L.074 13.499c-.18.31-.18.704 0 1.014.183.31.52.5.887.5h13.938c.367 0 .704-.19.887-.5.183-.31.183-.704 0-1.014L8.893 1.5zm.133 11.491H7.027v-2.026h1.999v2.026zm0-3.026H7.027V5.987h1.999v4.026z"/></svg>',
            'info': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/></svg>',
            'success': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/></svg>',
            'error': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z"/></svg>',
            
            # Iconos de categorías
            'alcohol': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M3 14.5A1.5 1.5 0 0 1 1.5 13V7A1.5 1.5 0 0 1 3 5.5h10a1.5 1.5 0 0 1 1.5 1.5v6a1.5 1.5 0 0 1-1.5 1.5H3zM1.5 7v6h13V7H1.5zM8 1.5A2.5 2.5 0 0 1 10.5 4h-5A2.5 2.5 0 0 1 8 1.5z"/></svg>',
            'juice': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M4 4a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v1.5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V4zM5 9a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v1.5a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V9zM6 14a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v1.5a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V14z"/></svg>',
            'fruit': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M11.5 8.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5zM7.5 3.5a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0zM1.5 12a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5zM14.5 12a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5zM8 13a3 3 0 1 1 0-6 3 3 0 0 1 0 6z"/></svg>',
            'herb': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8.5 1.5A1.5 1.5 0 0 0 7 0a1.5 1.5 0 0 0-1.5 1.5v1A1.5 1.5 0 0 0 7 4a1.5 1.5 0 0 0 1.5-1.5v1zM7 6.5a1.5 1.5 0 0 0-1.5 1.5v1A1.5 1.5 0 0 0 7 10.5a1.5 1.5 0 0 0 1.5-1.5v-1A1.5 1.5 0 0 0 7 6.5zM8.5 12a1.5 1.5 0 0 0-1.5 1.5v1A1.5 1.5 0 0 0 7 16a1.5 1.5 0 0 0 1.5-1.5v-1a1.5 1.5 0 0 0-1.5-1.5z"/></svg>',
            'spice': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8.5 1.5A1.5 1.5 0 0 0 7 0a1.5 1.5 0 0 0-1.5 1.5v1A1.5 1.5 0 0 0 7 4a1.5 1.5 0 0 0 1.5-1.5v1zM7 6.5a1.5 1.5 0 0 0-1.5 1.5v1A1.5 1.5 0 0 0 7 10.5a1.5 1.5 0 0 0 1.5-1.5v-1A1.5 1.5 0 0 0 7 6.5zM8.5 12a1.5 1.5 0 0 0-1.5 1.5v1A1.5 1.5 0 0 0 7 16a1.5 1.5 0 0 0 1.5-1.5v-1a1.5 1.5 0 0 0-1.5-1.5z"/></svg>',
            'syrup': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zM5.5 3A1.5 1.5 0 0 1 7 1.5h2A1.5 1.5 0 0 1 10.5 3v1.5a.5.5 0 0 1-1 0V3a.5.5 0 0 0-.5-.5H7a.5.5 0 0 0-.5.5v1.5a.5.5 0 0 1-1 0V3zM5 7.5a1.5 1.5 0 1 1 3 0 1.5 1.5 0 0 1-3 0zm4.5-.5a.5.5 0 0 0-.5.5v3a.5.5 0 0 0 1 0V7.5a.5.5 0 0 0-.5-.5z"/></svg>',
            'other': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/></svg>',
            
            # Iconos de estado
            'active': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/></svg>',
            'inactive': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z"/></svg>',
            'admin': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M7.854 4.854a.5.5 0 0 0-.708-.708L6.5 5.293 5.354 4.146a.5.5 0 1 0-.708.708L5.793 6l-1.147 1.146a.5.5 0 0 0 .708.708L6.5 6.707l1.146 1.147a.5.5 0 0 0 .708-.708L7.207 6l1.147-1.146a.5.5 0 0 0-.708-.708L6.5 5.293 5.354 4.146z"/><path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2zm5.5 10.854a.5.5 0 0 0 .707 0l3.5-3.5a.5.5 0 0 0-.707-.707L8 11.293V1.5a.5.5 0 0 0-1 0v9.793L4.854 9.146a.5.5 0 1 0-.708.708l3 3z"/></svg>',
            'bartender': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M3 14.5A1.5 1.5 0 0 1 1.5 13V7A1.5 1.5 0 0 1 3 5.5h10a1.5 1.5 0 0 1 1.5 1.5v6a1.5 1.5 0 0 1-1.5 1.5H3zM1.5 7v6h13V7H1.5zM8 1.5A2.5 2.5 0 0 1 10.5 4h-5A2.5 2.5 0 0 1 8 1.5z"/></svg>',
            'waiter': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/></svg>',
            
            # Iconos de navegación y UI
            'home': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8.354 1.146a.5.5 0 0 0-.708 0l-6 6A.5.5 0 0 0 1.5 7.5v7a.5.5 0 0 0 .5.5h4.5a.5.5 0 0 0 .5-.5v-4h2v4a.5.5 0 0 0 .5.5H14a.5.5 0 0 0 .5-.5v-7a.5.5 0 0 0-.146-.354L13 5.793V2.5a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1.293L8.354 1.146zM2.5 14V7.707l5.5-5.5 5.5 5.5V14H10v-4a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5v4H2.5z"/></svg>',
            'back': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M15 8a.5.5 0 0 0-.5-.5H2.707l3.147-3.146a.5.5 0 1 0-.708-.708l-4 4a.5.5 0 0 0 0 .708l4 4a.5.5 0 0 0 .708-.708L2.707 8.5H14.5A.5.5 0 0 0 15 8z"/></svg>',
            'next': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8z"/></svg>',
            'close': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 6.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 7l5.147 5.146a.5.5 0 0 1-.708.708L8 7.707 2.854 13.854a.5.5 0 1 1-.708-.708L7.293 7 2.146 1.854a.5.5 0 1 1 .708-.708L8 6.293 13.146 1.146a.5.5 0 1 1 .708.708L8.707 7l5.147 5.146a.5.5 0 0 1-.708.708L8 7.707 2.854 13.854a.5.5 0 1 1-.708-.708L7.293 7 2.146 1.854z"/></svg>',
            'save': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M2 1a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H9.5a1 1 0 0 0-1 1v1.5a.5.5 0 0 1-1 0V2a2 2 0 0 1 2-2H14a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2h2.5a.5.5 0 0 1 0 1H2z"/><path fill-rule="evenodd" d="M4.5 6.5A.5.5 0 0 1 5 6h6a.5.5 0 0 1 .5.5v4a.5.5 0 0 1-1 0V7H6v3.5a.5.5 0 0 1-1 0v-4a.5.5 0 0 1 .5-.5zM7 10h4v1H7v-1z"/></svg>',
            'cancel': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/><path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707 5.354 11.354a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/></svg>',
            
            # Iconos de medidas
            'ml': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/></svg>',
            'oz': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/></svg>',
            'dash': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M4 8a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7A.5.5 0 0 1 4 8z"/></svg>',
            'splash': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/></svg>',
            'cube': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8 1a1.5 1.5 0 0 1 1.5 1.5v1A1.5 1.5 0 0 1 8 5a1.5 1.5 0 0 1-1.5-1.5v-1A1.5 1.5 0 0 1 8 1zM3 5a1.5 1.5 0 0 1 1.5-1.5h1A1.5 1.5 0 0 1 7 5v1A1.5 1.5 0 0 1 5.5 7h-1A1.5 1.5 0 0 1 3 5.5V5zm9 0A1.5 1.5 0 0 1 10.5 3.5h1A1.5 1.5 0 0 1 13 5v1.5A1.5 1.5 0 0 1 11.5 8h-1A1.5 1.5 0 0 1 9 6.5V5zM3 11a1.5 1.5 0 0 1 1.5-1.5h1A1.5 1.5 0 0 1 7 11v1.5A1.5 1.5 0 0 1 5.5 14h-1A1.5 1.5 0 0 1 3 12.5V11zm9 0a1.5 1.5 0 0 1 1.5-1.5h1a1.5 1.5 0 0 1 1.5 1.5v1.5a1.5 1.5 0 0 1-1.5 1.5h-1a1.5 1.5 0 0 1-1.5-1.5V11z"/></svg>',
            'piece': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/></svg>',
            'slice': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/></svg>',
            'wedge': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/></svg>',
            'twist': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/></svg>',
            'wheel': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/></svg>',
            'whole': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/></svg>',
            'sprig': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/></svg>',
            'leaf': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/></svg>',
            'stem': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/></svg>',
            'top': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/></svg>',
            'flag': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M14.778.085A.5.5 0 0 1 15 .5V8a.5.5 0 0 1-.314.464L14.5 8l.186.464-.003.001-.006.003-.023.009a12.435 12.435 0 0 1-.397.15c-.21.065-.405.13-.602.194a13.57 13.57 0 0 1-1.404.267c-.385.049-.77.1-1.154.148A12.9 12.9 0 0 1 9.5 10c-.34.01-.68.025-1.02.04a12.35 12.35 0 0 1-1.01-.04c-.385-.049-.77-.1-1.154-.148a13.57 13.57 0 0 1-1.404-.267c-.197-.064-.392-.129-.602-.194a12.435 12.435 0 0 1-.397-.15l-.006-.003-.001-.001L.314 8.464.5 8l.186-.464.001-.001.006-.003.023-.009.397-.15c.21-.065.405-.13.602-.194.4-.129.804-.248 1.404-.267.385-.049.77-.1 1.154-.148A12.9 12.9 0 0 1 6.5 6c.34-.01.68-.025 1.02-.04a12.35 12.35 0 0 1 1.01.04c.385.049.77.1 1.154.148a13.57 13.57 0 0 1 1.404.267c.197.064.392.129.602.194a12.435 12.435 0 0 1 .397.15l.006.003.001.001L15.5 8l-.186.464-.001.001-.006.003-.023.009a12.435 12.435 0 0 1-.397.15c-.21.065-.405.13-.602.194a13.57 13.57 0 0 1-1.404.267c-.385.049-.77.1-1.154.148A12.9 12.9 0 0 1 9.5 10c-.34.01-.68.025-1.02.04a12.35 12.35 0 0 1-1.01-.04c-.385-.049-.77-.1-1.154-.148a13.57 13.57 0 0 1-1.404-.267c-.197-.064-.392-.129-.602-.194A12.435 12.435 0 0 1 .314 8.464.5.5 0 0 1 0 8V.5A.5.5 0 0 1 .5 0h.003a.5.5 0 0 1 .497.444L1 8.5A.5.5 0 0 1 .854 9z"/></svg>',
        }
    
    def get_icon(self, icon_name: str, size: int = 16, color: str = 'currentColor', custom_class: str = '') -> str:
        """
        Obtiene un icono SVG
        
        Args:
            icon_name: Nombre del icono
            size: Tamaño del icono
            color: Color del icono
            custom_class: Clases CSS adicionales
        
        Returns:
            str: SVG del icono
        """
        if icon_name in self.icons:
            svg = self.icons[icon_name]
            # Reemplazar tamaño y color
            svg = svg.replace('width="16"', f'width="{size}"')
            svg = svg.replace('height="16"', f'height="{size}"')
            svg = svg.replace('fill="currentColor"', f'fill="{color}"')
            
            # Agregar clases personalizadas
            if custom_class:
                svg = svg.replace('<svg ', f'<svg class="{custom_class}" ')
            
            return svg
        else:
            # Icono por defecto si no se encuentra
            return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" fill="{color}" viewBox="0 0 16 16"><circle cx="8" cy="8" r="7" stroke="currentColor" stroke-width="1" fill="none"/></svg>'
    
    def get_categorized_icons(self) -> Dict[str, Dict[str, str]]:
        """Retorna iconos organizados por categoría"""
        return {
            'navigation': {
                'dashboard': self.get_icon('dashboard'),
                'cocktails': self.get_icon('cocktails'),
                'inventory': self.get_icon('inventory'),
                'users': self.get_icon('users'),
                'settings': self.get_icon('settings'),
                'home': self.get_icon('home'),
                'logout': self.get_icon('logout'),
                'login': self.get_icon('login'),
            },
            'actions': {
                'add': self.get_icon('add'),
                'edit': self.get_icon('edit'),
                'delete': self.get_icon('delete'),
                'view': self.get_icon('view'),
                'search': self.get_icon('search'),
                'filter': self.get_icon('filter'),
                'export': self.get_icon('export'),
                'import': self.get_icon('import'),
                'save': self.get_icon('save'),
                'cancel': self.get_icon('cancel'),
                'chart': self.get_icon('chart'),
            },
            'status': {
                'active': self.get_icon('active'),
                'inactive': self.get_icon('inactive'),
                'warning': self.get_icon('warning'),
                'info': self.get_icon('info'),
                'success': self.get_icon('success'),
                'error': self.get_icon('error'),
            },
            'ingredients': {
                'alcohol': self.get_icon('alcohol'),
                'juice': self.get_icon('juice'),
                'fruit': self.get_icon('fruit'),
                'herb': self.get_icon('herb'),
                'spice': self.get_icon('spice'),
                'syrup': self.get_icon('syrup'),
                'other': self.get_icon('other'),
            },
            'user_roles': {
                'admin': self.get_icon('admin'),
                'bartender': self.get_icon('bartender'),
                'waiter': self.get_icon('waiter'),
                'user': self.get_icon('user'),
            },
            'measurements': {
                'ml': self.get_icon('ml'),
                'oz': self.get_icon('oz'),
                'dash': self.get_icon('dash'),
                'splash': self.get_icon('splash'),
                'cube': self.get_icon('cube'),
                'piece': self.get_icon('piece'),
                'slice': self.get_icon('slice'),
                'wedge': self.get_icon('wedge'),
                'twist': self.get_icon('twist'),
                'wheel': self.get_icon('wheel'),
                'whole': self.get_icon('whole'),
                'sprig': self.get_icon('sprig'),
                'leaf': self.get_icon('leaf'),
                'stem': self.get_icon('stem'),
                'top': self.get_icon('top'),
                'flag': self.get_icon('flag'),
            }
        }
    
    def render_icon(self, icon_name: str, size: int = 16, color: str = 'currentColor', 
                   custom_class: str = '', tooltip: str = '') -> None:
        """
        Renderiza un icono directamente en Streamlit
        
        Args:
            icon_name: Nombre del icono
            size: Tamaño del icono
            color: Color del icono
            custom_class: Clases CSS adicionales
            tooltip: Texto de ayuda
        """
        icon_svg = self.get_icon(icon_name, size, color, custom_class)
        
        if tooltip:
            st.markdown(f'<span title="{tooltip}">{icon_svg}</span>', unsafe_allow_html=True)
        else:
            st.markdown(icon_svg, unsafe_allow_html=True)
    
    def get_icon_html(self, icon_name: str, size: int = 16, color: str = 'currentColor', 
                     custom_class: str = '', tooltip: str = '') -> str:
        """
        Retorna HTML de un icono
        
        Args:
            icon_name: Nombre del icono
            size: Tamaño del icono
            color: Color del icono
            custom_class: Clases CSS adicionales
            tooltip: Texto de ayuda
        
        Returns:
            str: HTML del icono
        """
        icon_svg = self.get_icon(icon_name, size, color, custom_class)
        
        if tooltip:
            return f'<span title="{tooltip}">{icon_svg}</span>'
        else:
            return icon_svg

# Instancia global del gestor de iconos
icon_manager = IconManager()

# Funciones de conveniencia para uso rápido
def get_icon(icon_name: str, size: int = 16, color: str = 'currentColor', custom_class: str = '') -> str:
    """Obtiene un icono SVG"""
    return icon_manager.get_icon(icon_name, size, color, custom_class)

def render_icon(icon_name: str, size: int = 16, color: str = 'currentColor', 
               custom_class: str = '', tooltip: str = '') -> None:
    """Renderiza un icono en Streamlit"""
    icon_manager.render_icon(icon_name, size, color, custom_class, tooltip)

def get_menu_icons() -> Dict[str, str]:
    """Obtiene iconos para el menú principal"""
    return {
        'Dashboard': get_icon('dashboard', size=20),
        'Cócteles': get_icon('cocktails', size=20),
        'Inventario': get_icon('inventory', size=20),
        'Usuarios': get_icon('users', size=20),
        'Configuración': get_icon('settings', size=20),
    }

def get_action_icons() -> Dict[str, str]:
    """Obtiene iconos de acciones"""
    return {
        'Nuevo': get_icon('add', size=16),
        'Editar': get_icon('edit', size=16),
        'Eliminar': get_icon('delete', size=16),
        'Ver': get_icon('view', size=16),
        'Buscar': get_icon('search', size=16),
        'Filtrar': get_icon('filter', size=16),
        'Exportar': get_icon('export', size=16),
        'Importar': get_icon('import', size=16),
        'Guardar': get_icon('save', size=16),
        'Cancelar': get_icon('cancel', size=16),
        'Análisis': get_icon('chart', size=16),
    }