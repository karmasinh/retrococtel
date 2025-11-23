// Configuración inicial y manejo del tema
class ThemeManager {
  constructor() {
    this.theme = localStorage.getItem('theme') || 'light';
    this.init();
  }
  
  init() {
    this.applyTheme(this.theme);
    this.setupThemeToggle();
  }
  
  applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    
    // Actualizar el icono del toggle
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
      const icon = theme === 'dark' ? 'fa-sun' : 'fa-moon';
      themeToggle.innerHTML = `<i class="fas ${icon}"></i>`;
    }
  }
  
  toggleTheme() {
    this.theme = this.theme === 'light' ? 'dark' : 'light';
    this.applyTheme(this.theme);
  }
  
  setupThemeToggle() {
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
      themeToggle.addEventListener('click', () => this.toggleTheme());
    }
  }
}

// Gestor de navegación y sidebar
class NavigationManager {
  constructor() {
    this.sidebarVisible = window.innerWidth >= 992;
    this.init();
  }
  
  init() {
    this.setupSidebarToggle();
    this.setupActiveLinks();
    this.handleResize();
  }
  
  setupSidebarToggle() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    if (sidebarToggle) {
      sidebarToggle.addEventListener('click', () => this.toggleSidebar());
    }
  }
  
  toggleSidebar() {
    this.sidebarVisible = !this.sidebarVisible;
    const sidebar = document.getElementById('sidebar');
    
    if (sidebar) {
      if (this.sidebarVisible) {
        sidebar.classList.add('show');
      } else {
        sidebar.classList.remove('show');
      }
    }
  }
  
  setupActiveLinks() {
    const currentPage = window.location.pathname.split('/').pop();
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
      const href = link.getAttribute('href');
      if (href === currentPage) {
        link.classList.add('active');
      }
    });
  }
  
  handleResize() {
    window.addEventListener('resize', () => {
      const sidebar = document.getElementById('sidebar');
      if (window.innerWidth >= 992) {
        this.sidebarVisible = true;
        if (sidebar) sidebar.classList.add('show');
      } else {
        this.sidebarVisible = false;
        if (sidebar) sidebar.classList.remove('show');
      }
    });
  }
}

// Sistema de notificaciones Toast
class ToastManager {
  constructor() {
    this.container = document.createElement('div');
    this.container.className = 'toast-container';
    document.body.appendChild(this.container);
  }
  
  show(message, type = 'info', title = null, duration = 5000) {
    const toast = document.createElement('div');
    toast.className = `toast fade-in toast-${type}`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    // Icono según el tipo
    let icon = 'fa-info-circle';
    if (type === 'success') icon = 'fa-check-circle';
    if (type === 'error') icon = 'fa-exclamation-circle';
    if (type === 'warning') icon = 'fa-exclamation-triangle';
    
    // Título por defecto según tipo
    if (!title) {
      if (type === 'success') title = 'Éxito';
      if (type === 'error') title = 'Error';
      if (type === 'warning') title = 'Advertencia';
      if (type === 'info') title = 'Información';
    }
    
    toast.innerHTML = `
      <div class="toast-header">
        <i class="fas ${icon} me-2"></i>
        <strong class="me-auto">${title}</strong>
        <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Cerrar"></button>
      </div>
      <div class="toast-body">
        ${message}
      </div>
    `;
    
    this.container.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast, {
      delay: duration
    });
    
    bsToast.show();
    
    // Eliminar el toast del DOM cuando se oculte
    toast.addEventListener('hidden.bs.toast', () => {
      toast.remove();
    });
    
    return toast;
  }
}

// API Client para comunicarse con el backend
class APIClient {
  constructor(baseURL = 'http://localhost:3000/api') {
    this.baseURL = baseURL;
  }
  
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    };
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    
    if (config.body && typeof config.body === 'object') {
      config.body = JSON.stringify(config.body);
    }
    
    try {
      const response = await fetch(url, config);
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.message || 'Error en la solicitud');
      }
      
      return data;
    } catch (error) {
      console.error('API Request Error:', error);
      throw error;
    }
  }
  async login(credentials) {
    const res = await this.request('/auth/login', { method: 'POST', body: credentials })
    if (res && res.token) localStorage.setItem('authToken', res.token)
    return res
  }
  
  // Métodos para Cocktails
  async getCocktails(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/cocktails${queryString ? `?${queryString}` : ''}`);
  }
  
  async getCocktail(id) {
    return this.request(`/cocktails/${id}`);
  }
  
  async createCocktail(cocktail) {
    return this.request('/cocktails', {
      method: 'POST',
      body: cocktail
    });
  }
  
  async updateCocktail(id, cocktail) {
    return this.request(`/cocktails/${id}`, {
      method: 'PUT',
      body: cocktail
    });
  }
  
  async deleteCocktail(id) {
    return this.request(`/cocktails/${id}`, {
      method: 'DELETE'
    });
  }
  
  // Métodos para Ingredientes
  async getIngredients(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/ingredients${queryString ? `?${queryString}` : ''}`);
  }
  
  // Métodos para Usuarios
  async getUsers(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/users${queryString ? `?${queryString}` : ''}`);
  }
  
  // Métodos para Roles
  async getRoles(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/roles${queryString ? `?${queryString}` : ''}`);
  }
}

// Inicialización de la aplicación
document.addEventListener('DOMContentLoaded', function() {
  // Inicializar managers
  window.themeManager = new ThemeManager();
  window.navigationManager = new NavigationManager();
  window.toastManager = new ToastManager();
  
  // Configurar API Client (cambiar la URL base según el entorno)
  const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:3000/api';
  window.apiClient = new APIClient(API_BASE_URL);
  
  // Inicializar tooltips de Bootstrap
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
  
  // Manejar formularios de login
  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', handleLogin);
  }
  
  // Configurar event listeners globales
  setupGlobalEventListeners();
});

// Manejador de login
async function handleLogin(e) {
  e.preventDefault();
  
  const formData = new FormData(e.target);
  const credentials = {
    username: formData.get('username'),
    password: formData.get('password')
  };
  
  try {
    await window.apiClient.login(credentials)
    window.toastManager.show('Inicio de sesión exitoso', 'success');
    setTimeout(() => {
      window.location.href = 'index.html';
    }, 1500);
  } catch (error) {
    window.toastManager.show('Error en el inicio de sesión: ' + error.message, 'error');
  }
}

// Configurar event listeners globales
function setupGlobalEventListeners() {
  // Manejar enlaces de logout
  const logoutLinks = document.querySelectorAll('[data-action="logout"]');
  logoutLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      // Aquí se limpiarían las credenciales de autenticación
      window.toastManager.show('Sesión cerrada correctamente', 'success');
      setTimeout(() => {
        window.location.href = 'login.html';
      }, 1000);
    });
  });
  
  // Manejar confirmaciones de eliminación
  const deleteButtons = document.querySelectorAll('[data-action="delete"]');
  deleteButtons.forEach(button => {
    button.addEventListener('click', function(e) {
      e.preventDefault();
      const itemName = this.getAttribute('data-item-name') || 'este elemento';
      if (confirm(`¿Estás seguro de que deseas eliminar ${itemName}? Esta acción no se puede deshacer.`)) {
        // Aquí se ejecutaría la eliminación
        const itemId = this.getAttribute('data-item-id');
        const itemType = this.getAttribute('data-item-type');
        
        if (itemType && itemId) {
          // Eliminar el elemento mediante API
          deleteItem(itemType, itemId);
        } else {
          // Si no hay tipo e ID, simular eliminación exitosa
          window.toastManager.show('Elemento eliminado correctamente', 'success');
          // Recargar la página después de un breve delay
          setTimeout(() => {
            window.location.reload();
          }, 1500);
        }
      }
    });
  });
}

// Función para eliminar elementos
async function deleteItem(type, id) {
  try {
    let endpoint;
    switch(type) {
      case 'cocktail':
        endpoint = `/cocktails/${id}`;
        break;
      case 'user':
        endpoint = `/users/${id}`;
        break;
      case 'role':
        endpoint = `/roles/${id}`;
        break;
      default:
        throw new Error('Tipo de elemento no válido');
    }
    
    // await window.apiClient.request(endpoint, { method: 'DELETE' });
    
    // Simular eliminación exitosa
    window.toastManager.show('Elemento eliminado correctamente', 'success');
    
    // Recargar la página después de un breve delay
    setTimeout(() => {
      window.location.reload();
    }, 1500);
  } catch (error) {
    window.toastManager.show('Error al eliminar: ' + error.message, 'error');
  }
}
