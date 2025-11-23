// Gestión de usuarios - CRUD completo
class UserManager {
    constructor() {
        this.currentUser = null;
        this.roles = [];
        this.init();
    }

    init() {
        this.loadRoles();
        this.setupEventListeners();
        this.loadUsers();
    }

    setupEventListeners() {
        // Botón para agregar nuevo usuario
        const addUserBtn = document.getElementById('addUserBtn');
        if (addUserBtn) {
            addUserBtn.addEventListener('click', () => this.showUserModal());
        }

        // Formulario de búsqueda
        const searchForm = document.getElementById('searchForm');
        if (searchForm) {
            searchForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.searchUsers();
            });
        }

        // Búsqueda en tiempo real
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.addEventListener('input', () => {
                clearTimeout(this.searchTimeout);
                this.searchTimeout = setTimeout(() => this.searchUsers(), 500);
            });
        }
    }

    async loadRoles() {
        try { this.roles = await window.apiClient.getRoles(); }
        catch (error) { console.error('Error loading roles:', error); window.toastManager.show('Error al cargar los roles', 'error'); }
    }

    async loadUsers() { try { const users = await window.apiClient.getUsers(); this.users = users; this.displayUsers(users) } catch (error) { console.error('Error loading users:', error); window.toastManager.show('Error al cargar los usuarios', 'error') } }

    displayUsers(users) {
        const container = document.getElementById('usersContainer');
        if (!container) return;
        
        container.innerHTML = '';
        
        if (users.length === 0) {
            container.innerHTML = `
                <div class="col-12 text-center py-5">
                    <i class="fas fa-users fa-3x text-muted mb-3"></i>
                    <h4 class="text-muted">No se encontraron usuarios</h4>
                    <p class="text-muted">Intenta ajustar los filtros de búsqueda</p>
                </div>
            `;
            return;
        }
        
        users.forEach(user => {
            const col = document.createElement('div');
            col.className = 'col-md-6 col-lg-4 mb-4';
            col.innerHTML = this.createUserCard(user);
            container.appendChild(col);
        });
    }

    createUserCard(user) {
        const statusClass = user.status === 'Activo' ? 'bg-success' : 'bg-secondary';
        
        return `
            <div class="card user-card h-100">
                <div class="card-body text-center">
                    <img src="${user.avatar_url}" class="rounded-circle mb-3" alt="${user.full_name}" width="80" height="80">
                    <h5 class="card-title">${user.full_name}</h5>
                    <p class="card-text text-muted">${user.email}</p>
                    <div class="d-flex justify-content-center mb-3">
                        <span class="badge ${statusClass} me-2">${user.status}</span>
                        <span class="badge bg-info">${user.role}</span>
                    </div>
                    <p class="card-text">
                        <small class="text-muted">@${user.username}</small>
                    </p>
                </div>
                <div class="card-footer bg-transparent d-flex justify-content-between">
                    <button class="btn btn-sm btn-outline-primary" data-action="edit-user" data-user-id="${user.id}">
                        <i class="fas fa-edit me-1"></i> Editar
                    </button>
                    <button class="btn btn-sm btn-outline-danger" data-action="delete" data-item-type="user" data-item-id="${user.id}" data-item-name="${user.full_name}">
                        <i class="fas fa-trash me-1"></i> Eliminar
                    </button>
                </div>
            </div>
        `;
    }

    showUserModal(userData = null) {
        this.currentUser = userData;
        
        // Crear modal dinámicamente si no existe
        if (!document.getElementById('userModal')) {
            this.createUserModal();
        }
        
        // Llenar el modal con datos si estamos editando
        if (this.currentUser) {
            this.populateUserForm(this.currentUser);
        } else {
            this.clearUserForm();
        }
        
        // Inicializar el modal de Bootstrap y mostrarlo
        const modal = new bootstrap.Modal(document.getElementById('userModal'));
        modal.show();
    }

    createUserModal() {
        const modalHTML = `
        <div class="modal fade" id="userModal" tabindex="-1" aria-labelledby="userModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="userModalLabel">${this.currentUser ? 'Editar' : 'Nuevo'} Usuario</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form id="userForm">
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="userFullName" class="form-label">Nombre completo *</label>
                                        <input type="text" class="form-control" id="userFullName" required>
                                    </div>
                                    <div class="mb-3">
                                        <label for="userUsername" class="form-label">Nombre de usuario *</label>
                                        <input type="text" class="form-control" id="userUsername" required>
                                    </div>
                                    <div class="mb-3">
                                        <label for="userEmail" class="form-label">Email *</label>
                                        <input type="email" class="form-control" id="userEmail" required>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="userRole" class="form-label">Rol *</label>
                                        <select class="form-select" id="userRole" required>
                                            <option value="">Seleccionar rol...</option>
                                            ${this.roles.map(role => `<option value="${role.id}">${role.name}</option>`).join('')}
                                        </select>
                                    </div>
                                    <div class="mb-3">
                                        <label for="userStatus" class="form-label">Estado</label>
                                        <select class="form-select" id="userStatus">
                                            <option value="Activo">Activo</option>
                                            <option value="Inactivo">Inactivo</option>
                                        </select>
                                    </div>
                                    <div class="mb-3">
                                        <label for="userAvatar" class="form-label">Avatar URL</label>
                                        <input type="url" class="form-control" id="userAvatar" placeholder="https://...">
                                    </div>
                                </div>
                            </div>
                            ${!this.currentUser ? `
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="userPassword" class="form-label">Contraseña *</label>
                                        <input type="password" class="form-control" id="userPassword" required>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="userConfirmPassword" class="form-label">Confirmar contraseña *</label>
                                        <input type="password" class="form-control" id="userConfirmPassword" required>
                                    </div>
                                </div>
                            </div>
                            ` : ''}
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-primary" id="saveUserBtn">Guardar Usuario</button>
                    </div>
                </div>
            </div>
        </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Configurar event listeners del modal
        const saveUserBtn = document.getElementById('saveUserBtn');
        if (saveUserBtn) {
            saveUserBtn.addEventListener('click', () => this.saveUser());
        }
    }

    populateUserForm(user) {
        document.getElementById('userFullName').value = user.full_name || '';
        document.getElementById('userUsername').value = user.username || '';
        document.getElementById('userEmail').value = user.email || '';
        document.getElementById('userRole').value = this.roles.find(r => r.name === user.role)?.id || '';
        document.getElementById('userStatus').value = user.status || 'Activo';
        document.getElementById('userAvatar').value = user.avatar_url || '';
    }

    clearUserForm() {
        const form = document.getElementById('userForm');
        if (form) {
            form.reset();
        }
    }

    async saveUser() {
        // Validar formulario
        if (!this.validateUserForm()) {
            window.toastManager.show('Por favor, complete todos los campos requeridos', 'warning');
            return;
        }
        
        try {
            // Recopilar datos del formulario
            const formData = this.collectUserFormData();
            
            if (this.currentUser) {
                await window.apiClient.updateUser(this.currentUser.id, formData);
                window.toastManager.show('Usuario actualizado correctamente', 'success');
            } else {
                await window.apiClient.createUser(formData);
                window.toastManager.show('Usuario creado correctamente', 'success');
            }
            
            // Cerrar modal y recargar la lista
            bootstrap.Modal.getInstance(document.getElementById('userModal')).hide();
            this.loadUsers();
            
        } catch (error) {
            console.error('Error saving user:', error);
            window.toastManager.show('Error al guardar el usuario: ' + error.message, 'error');
        }
    }

    validateUserForm() {
        // Validar campos requeridos
        const fullName = document.getElementById('userFullName');
        const username = document.getElementById('userUsername');
        const email = document.getElementById('userEmail');
        const role = document.getElementById('userRole');
        
        if (!fullName.value.trim()) {
            fullName.focus();
            return false;
        }
        
        if (!username.value.trim()) {
            username.focus();
            return false;
        }
        
        if (!email.value.trim() || !this.isValidEmail(email.value)) {
            email.focus();
            return false;
        }
        
        if (!role.value) {
            role.focus();
            return false;
        }
        
        // Validar contraseña si es un nuevo usuario
        if (!this.currentUser) {
            const password = document.getElementById('userPassword');
            const confirmPassword = document.getElementById('userConfirmPassword');
            
            if (!password.value) {
                password.focus();
                return false;
            }
            
            if (password.value !== confirmPassword.value) {
                confirmPassword.focus();
                window.toastManager.show('Las contraseñas no coinciden', 'warning');
                return false;
            }
        }
        
        return true;
    }

    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    collectUserFormData() {
        const formData = {
            full_name: document.getElementById('userFullName').value,
            username: document.getElementById('userUsername').value,
            email: document.getElementById('userEmail').value,
            role_id: parseInt(document.getElementById('userRole').value),
            status: document.getElementById('userStatus').value,
            avatar_url: document.getElementById('userAvatar').value || null
        };
        
        // Añadir contraseña solo si es un nuevo usuario
        if (!this.currentUser) {
            formData.password = document.getElementById('userPassword').value;
        }
        
        return formData;
    }

    async searchUsers() { const q = document.getElementById('searchInput').value || ''; const roleName = document.getElementById('roleFilter').value || ''; const status = document.getElementById('statusFilter').value || ''; let role_id = ''; if (roleName) { const r = this.roles.find(x=> x.name===roleName); role_id = r? r.id : '' } const users = await window.apiClient.getUsers({ q, role_id, status }); this.users = users; this.displayUsers(users) }
}

// Inicializar el manager de usuarios cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('usersContainer')) {
        window.userManager = new UserManager();
    }
});
