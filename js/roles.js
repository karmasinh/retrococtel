// Gestión de roles - CRUD completo
class RoleManager {
    constructor() {
        this.currentRole = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadRoles();
    }

    setupEventListeners() {
        // Botón para agregar nuevo rol
        const addRoleBtn = document.getElementById('addRoleBtn');
        if (addRoleBtn) {
            addRoleBtn.addEventListener('click', () => this.showRoleModal());
        }

        // Formulario de búsqueda
        const searchForm = document.getElementById('searchForm');
        if (searchForm) {
            searchForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.searchRoles();
            });
        }

        // Búsqueda en tiempo real
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.addEventListener('input', () => {
                clearTimeout(this.searchTimeout);
                this.searchTimeout = setTimeout(() => this.searchRoles(), 500);
            });
        }
    }

    async loadRoles() {
        try {
            // En una implementación real, se obtendrían de la API
            // const roles = await window.apiClient.getRoles();
            
            // Usar datos de ejemplo por ahora
            const roles = [
                {
                    id: 1,
                    name: "Administrador",
                    description: "Acceso completo a todas las funcionalidades del sistema",
                    permissions: ["all"],
                    user_count: 1
                },
                {
                    id: 2,
                    name: "Editor",
                    description: "Puede ver, crear y editar contenido pero no gestionar usuarios",
                    permissions: ["read", "create", "update"],
                    user_count: 2
                },
                {
                    id: 3,
                    name: "Lector",
                    description: "Solo puede ver el contenido existente",
                    permissions: ["read"],
                    user_count: 1
                }
            ];
            
            this.displayRoles(roles);
        } catch (error) {
            console.error('Error loading roles:', error);
            window.toastManager.show('Error al cargar los roles', 'error');
        }
    }

    displayRoles(roles) {
        const container = document.getElementById('rolesContainer');
        if (!container) return;
        
        container.innerHTML = '';
        
        if (roles.length === 0) {
            container.innerHTML = `
                <div class="col-12 text-center py-5">
                    <i class="fas fa-user-shield fa-3x text-muted mb-3"></i>
                    <h4 class="text-muted">No se encontraron roles</h4>
                    <p class="text-muted">Intenta ajustar los filtros de búsqueda</p>
                </div>
            `;
            return;
        }
        
        roles.forEach(role => {
            const col = document.createElement('div');
            col.className = 'col-md-6 col-lg-4 mb-4';
            col.innerHTML = this.createRoleCard(role);
            container.appendChild(col);
        });
    }

    createRoleCard(role) {
        return `
            <div class="card role-card h-100">
                <div class="card-body">
                    <h5 class="card-title">${role.name}</h5>
                    <p class="card-text">${role.description}</p>
                    <div class="mb-3">
                        <span class="badge bg-primary">${role.user_count} usuarios</span>
                    </div>
                    <div class="permissions-list">
                        <h6 class="text-muted">Permisos:</h6>
                        <ul class="list-unstyled">
                            ${role.permissions.map(perm => `
                                <li><i class="fas fa-check-circle text-success me-2"></i>${this.getPermissionLabel(perm)}</li>
                            `).join('')}
                        </ul>
                    </div>
                </div>
                <div class="card-footer bg-transparent d-flex justify-content-between">
                    <button class="btn btn-sm btn-outline-primary" data-action="edit-role" data-role-id="${role.id}">
                        <i class="fas fa-edit me-1"></i> Editar
                    </button>
                    <button class="btn btn-sm btn-outline-danger" data-action="delete" data-item-type="role" data-item-id="${role.id}" data-item-name="${role.name}">
                        <i class="fas fa-trash me-1"></i> Eliminar
                    </button>
                </div>
            </div>
        `;
    }

    getPermissionLabel(permission) {
        const labels = {
            'all': 'Todos los permisos',
            'read': 'Ver contenido',
            'create': 'Crear contenido',
            'update': 'Editar contenido',
            'delete': 'Eliminar contenido',
            'manage_users': 'Gestionar usuarios',
            'manage_roles': 'Gestionar roles'
        };
        
        return labels[permission] || permission;
    }

    showRoleModal(roleData = null) {
        this.currentRole = roleData;
        
        // Crear modal dinámicamente si no existe
        if (!document.getElementById('roleModal')) {
            this.createRoleModal();
        }
        
        // Llenar el modal con datos si estamos editando
        if (this.currentRole) {
            this.populateRoleForm(this.currentRole);
        } else {
            this.clearRoleForm();
        }
        
        // Inicializar el modal de Bootstrap y mostrarlo
        const modal = new bootstrap.Modal(document.getElementById('roleModal'));
        modal.show();
    }

    createRoleModal() {
        const modalHTML = `
        <div class="modal fade" id="roleModal" tabindex="-1" aria-labelledby="roleModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="roleModalLabel">${this.currentRole ? 'Editar' : 'Nuevo'} Rol</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form id="roleForm">
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="roleName" class="form-label">Nombre del rol *</label>
                                        <input type="text" class="form-control" id="roleName" required>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="roleDescription" class="form-label">Descripción</label>
                                        <input type="text" class="form-control" id="roleDescription">
                                    </div>
                                </div>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Permisos *</label>
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="form-check">
                                            <input class="form-check-input" type="checkbox" id="permRead" value="read">
                                            <label class="form-check-label" for="permRead">Ver contenido</label>
                                        </div>
                                        <div class="form-check">
                                            <input class="form-check-input" type="checkbox" id="permCreate" value="create">
                                            <label class="form-check-label" for="permCreate">Crear contenido</label>
                                        </div>
                                        <div class="form-check">
                                            <input class="form-check-input" type="checkbox" id="permUpdate" value="update">
                                            <label class="form-check-label" for="permUpdate">Editar contenido</label>
                                        </div>
                                        <div class="form-check">
                                            <input class="form-check-input" type="checkbox" id="permDelete" value="delete">
                                            <label class="form-check-label" for="permDelete">Eliminar contenido</label>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="form-check">
                                            <input class="form-check-input" type="checkbox" id="permManageUsers" value="manage_users">
                                            <label class="form-check-label" for="permManageUsers">Gestionar usuarios</label>
                                        </div>
                                        <div class="form-check">
                                            <input class="form-check-input" type="checkbox" id="permManageRoles" value="manage_roles">
                                            <label class="form-check-label" for="permManageRoles">Gestionar roles</label>
                                        </div>
                                        <div class="form-check">
                                            <input class="form-check-input" type="checkbox" id="permAll" value="all">
                                            <label class="form-check-label" for="permAll">Todos los permisos</label>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-primary" id="saveRoleBtn">Guardar Rol</button>
                    </div>
                </div>
            </div>
        </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Configurar event listeners del modal
        this.setupRoleModalEventListeners();
    }

    setupRoleModalEventListeners() {
        // Checkbox "Todos los permisos" debe seleccionar/deseleccionar todos
        const permAll = document.getElementById('permAll');
        if (permAll) {
            permAll.addEventListener('change', function() {
                const checkboxes = document.querySelectorAll('input[type="checkbox"]:not(#permAll)');
                checkboxes.forEach(checkbox => {
                    checkbox.checked = this.checked;
                    checkbox.disabled = this.checked;
                });
            });
        }
        
        // Si se deselecciona algún permiso individual, deseleccionar "Todos"
        const permissionCheckboxes = document.querySelectorAll('input[type="checkbox"]:not(#permAll)');
        permissionCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', function() {
                if (!this.checked && document.getElementById('permAll').checked) {
                    document.getElementById('permAll').checked = false;
                    
                    // Habilitar todos los checkboxes
                    permissionCheckboxes.forEach(cb => cb.disabled = false);
                }
            });
        });
        
        // Guardar rol
        const saveRoleBtn = document.getElementById('saveRoleBtn');
        if (saveRoleBtn) {
            saveRoleBtn.addEventListener('click', () => this.saveRole());
        }
    }

    populateRoleForm(role) {
        document.getElementById('roleName').value = role.name || '';
        document.getElementById('roleDescription').value = role.description || '';
        
        // Seleccionar los permisos
        if (role.permissions) {
            if (role.permissions.includes('all')) {
                document.getElementById('permAll').checked = true;
                
                // Deshabilitar los demás checkboxes
                const checkboxes = document.querySelectorAll('input[type="checkbox"]:not(#permAll)');
                checkboxes.forEach(checkbox => {
                    checkbox.checked = true;
                    checkbox.disabled = true;
                });
            } else {
                role.permissions.forEach(perm => {
                    const checkbox = document.getElementById(`perm${this.capitalizeFirst(perm)}`);
                    if (checkbox) {
                        checkbox.checked = true;
                    }
                });
            }
        }
    }

    capitalizeFirst(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    clearRoleForm() {
        const form = document.getElementById('roleForm');
        if (form) {
            form.reset();
            
            // Habilitar todos los checkboxes
            const checkboxes = document.querySelectorAll('input[type="checkbox"]:not(#permAll)');
            checkboxes.forEach(checkbox => {
                checkbox.disabled = false;
            });
        }
    }

    async saveRole() {
        // Validar formulario
        if (!this.validateRoleForm()) {
            window.toastManager.show('Por favor, complete todos los campos requeridos', 'warning');
            return;
        }
        
        try {
            // Recopilar datos del formulario
            const formData = this.collectRoleFormData();
            
            // En una implementación real, se enviaría a la API
            if (this.currentRole) {
                // await window.apiClient.updateRole(this.currentRole.id, formData);
                window.toastManager.show('Rol actualizado correctamente', 'success');
            } else {
                // await window.apiClient.createRole(formData);
                window.toastManager.show('Rol creado correctamente', 'success');
            }
            
            // Cerrar modal y recargar la lista
            bootstrap.Modal.getInstance(document.getElementById('roleModal')).hide();
            this.loadRoles();
            
        } catch (error) {
            console.error('Error saving role:', error);
            window.toastManager.show('Error al guardar el rol: ' + error.message, 'error');
        }
    }

    validateRoleForm() {
        // Validar campos requeridos
        const roleName = document.getElementById('roleName');
        
        if (!roleName.value.trim()) {
            roleName.focus();
            return false;
        }
        
        // Validar que haya al menos un permiso seleccionado
        const hasAll = document.getElementById('permAll').checked;
        const hasOther = Array.from(document.querySelectorAll('input[type="checkbox"]:not(#permAll)'))
            .some(checkbox => checkbox.checked);
        
        if (!hasAll && !hasOther) {
            window.toastManager.show('Debe seleccionar al menos un permiso', 'warning');
            return false;
        }
        
        return true;
    }

    collectRoleFormData() {
        const formData = {
            name: document.getElementById('roleName').value,
            description: document.getElementById('roleDescription').value,
            permissions: []
        };
        
        // Recopilar permisos seleccionados
        if (document.getElementById('permAll').checked) {
            formData.permissions.push('all');
        } else {
            const checkboxes = document.querySelectorAll('input[type="checkbox"]:not(#permAll):checked');
            checkboxes.forEach(checkbox => {
                formData.permissions.push(checkbox.value);
            });
        }
        
        return formData;
    }

    searchRoles() {
        const searchTerm = document.getElementById('searchInput').value.toLowerCase();
        
        // En una implementación real, se enviarían estos filtros a la API
        // Por ahora, filtramos localmente los roles de ejemplo
        
        const filteredRoles = [
            {
                id: 1,
                name: "Administrador",
                description: "Acceso completo a todas las funcionalidades del sistema",
                permissions: ["all"],
                user_count: 1
            },
            {
                id: 2,
                name: "Editor",
                description: "Puede ver, crear y editar contenido pero no gestionar usuarios",
                permissions: ["read", "create", "update"],
                user_count: 2
            },
            {
                id: 3,
                name: "Lector",
                description: "Solo puede ver el contenido existente",
                permissions: ["read"],
                user_count: 1
            }
        ].filter(role => {
            // Filtrar por término de búsqueda
            if (searchTerm && 
                !role.name.toLowerCase().includes(searchTerm) && 
                !role.description.toLowerCase().includes(searchTerm)) {
                return false;
            }
            
            return true;
        });
        
        this.displayRoles(filteredRoles);
    }
}

// Inicializar el manager de roles cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('rolesContainer')) {
        window.roleManager = new RoleManager();
    }
});