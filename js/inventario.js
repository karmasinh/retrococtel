// Gestión de inventario - CRUD completo para ingredientes
class InventoryManager {
    constructor() {
        this.currentIngredient = null;
        this.ingredients = [];
        this.currentPage = 1;
        this.itemsPerPage = 10;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadIngredients();
    }

    setupEventListeners() {
        // Botón para agregar nuevo ingrediente
        const addIngredientBtn = document.getElementById('addIngredientBtn');
        if (addIngredientBtn) {
            addIngredientBtn.addEventListener('click', () => this.showIngredientModal());
        }

        // Botón para cargar datos de ejemplo
        const loadSeedDataBtn = document.getElementById('loadSeedDataBtn');
        if (loadSeedDataBtn) {
            loadSeedDataBtn.addEventListener('click', () => this.loadSeedData());
        }

        // Formulario de búsqueda
        const searchForm = document.getElementById('searchForm');
        if (searchForm) {
            searchForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.searchIngredients();
            });
        }

        // Filtros
        const filterSelects = document.querySelectorAll('.filter-select');
        filterSelects.forEach(select => {
            select.addEventListener('change', () => this.applyFilters());
        });

        // Búsqueda en tiempo real
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.addEventListener('input', () => {
                clearTimeout(this.searchTimeout);
                this.searchTimeout = setTimeout(() => this.searchIngredients(), 500);
            });
        }
    }

    async loadIngredients() {
        try {
            // Primero intentar cargar desde localStorage
            const savedIngredients = localStorage.getItem('cocktailIngredients');
            
            if (savedIngredients) {
                this.ingredients = JSON.parse(savedIngredients);
                this.updateMetrics();
                this.displayIngredients();
                return;
            }
            
            // Si no hay en localStorage, cargar desde el archivo JSON
            const response = await fetch('../data/seed_ingredients.json');
            if (!response.ok) {
                throw new Error('No se pudo cargar el archivo de ingredientes');
            }
            
            this.ingredients = await response.json();
            
            // Guardar en localStorage para uso futuro
            localStorage.setItem('cocktailIngredients', JSON.stringify(this.ingredients));
            
            this.updateMetrics();
            this.displayIngredients();
            
        } catch (error) {
            console.error('Error loading ingredients:', error);
            window.toastManager.show('Error al cargar los ingredientes', 'error');
            
            // Mostrar mensaje de que no hay ingredientes
            document.getElementById('ingredientsTable').querySelector('tbody').innerHTML = `
                <tr>
                    <td colspan="7" class="text-center py-4">
                        <i class="fas fa-carrot fa-3x text-muted mb-3"></i>
                        <h5 class="text-muted">No hay ingredientes en el inventario</h5>
                        <p class="text-muted">Agrega ingredientes manualmente o carga los datos de ejemplo.</p>
                        <button class="btn btn-primary mt-2" id="loadSeedDataBtn2">
                            <i class="fas fa-database me-2"></i> Cargar Datos de Ejemplo
                        </button>
                    </td>
                </tr>
            `;
            
            // Agregar event listener al botón dentro de la tabla
            const loadSeedDataBtn2 = document.getElementById('loadSeedDataBtn2');
            if (loadSeedDataBtn2) {
                loadSeedDataBtn2.addEventListener('click', () => this.loadSeedData());
            }
        }
    }

    async loadSeedData() {
        try {
            // Cargar datos de ejemplo desde el archivo JSON
            const response = await fetch('../data/seed_ingredients.json');
            if (!response.ok) {
                throw new Error('No se pudo cargar el archivo de datos de ejemplo');
            }
            
            this.ingredients = await response.json();
            
            // Guardar en localStorage para uso futuro
            localStorage.setItem('cocktailIngredients', JSON.stringify(this.ingredients));
            
            // Actualizar la UI
            this.updateMetrics();
            this.displayIngredients();
            
            window.toastManager.show('Datos de ejemplo cargados correctamente', 'success');
        } catch (error) {
            console.error('Error loading seed data:', error);
            window.toastManager.show('Error al cargar los datos de ejemplo: ' + error.message, 'error');
            
            // Datos de respaldo en caso de error
            this.ingredients = [
                { id: 1, name: "Ron blanco", category: "Alcohol", unit_default: "ml", calories_per_unit: 65, abv: 40, stock: 1500, reorder_threshold: 500 },
                { id: 2, name: "Jugo de lima", category: "Jugo", unit_default: "ml", calories_per_unit: 4, abv: 0, stock: 2000, reorder_threshold: 500 },
                { id: 3, name: "Azúcar moreno", category: "Endulzante", unit_default: "cucharadita", calories_per_unit: 16, abv: 0, stock: 500, reorder_threshold: 100 },
                { id: 4, name: "Hierbabuena", category: "Hierba", unit_default: "hojas", calories_per_unit: 1, abv: 0, stock: 200, reorder_threshold: 50 },
                { id: 5, name: "Soda", category: "Refresco", unit_default: "ml", calories_per_unit: 0, abv: 0, stock: 3000, reorder_threshold: 1000 }
            ];
            
            localStorage.setItem('cocktailIngredients', JSON.stringify(this.ingredients));
            this.updateMetrics();
            this.displayIngredients();
        }
    }

    updateMetrics() {
        const totalIngredients = this.ingredients.length;
        const lowStockIngredients = this.ingredients.filter(ing => 
            ing.stock !== null && ing.reorder_threshold !== null && ing.stock < ing.reorder_threshold && ing.stock > 0
        ).length;
        const outOfStockIngredients = this.ingredients.filter(ing => 
            ing.stock !== null && ing.stock === 0
        ).length;
        const goodStockIngredients = this.ingredients.filter(ing => 
            ing.stock === null || ing.reorder_threshold === null || ing.stock >= ing.reorder_threshold
        ).length;

        document.getElementById('totalIngredients').textContent = totalIngredients;
        document.getElementById('lowStockIngredients').textContent = lowStockIngredients;
        document.getElementById('outOfStockIngredients').textContent = outOfStockIngredients;
        document.getElementById('goodStockIngredients').textContent = goodStockIngredients;
    }

    displayIngredients(page = 1) {
        const tbody = document.getElementById('ingredientsTable').querySelector('tbody');
        if (!tbody) return;
        
        // Aplicar filtros y búsqueda
        const filteredIngredients = this.filterIngredients(this.ingredients);
        
        // Calcular paginación
        const totalPages = Math.ceil(filteredIngredients.length / this.itemsPerPage);
        this.currentPage = Math.min(Math.max(page, 1), totalPages);
        
        const startIndex = (this.currentPage - 1) * this.itemsPerPage;
        const endIndex = Math.min(startIndex + this.itemsPerPage, filteredIngredients.length);
        const paginatedIngredients = filteredIngredients.slice(startIndex, endIndex);
        
        // Actualizar información de la tabla
        document.getElementById('tableInfo').textContent = 
            `Mostrando ${startIndex + 1}-${endIndex} de ${filteredIngredients.length} ingredientes`;
        
        // Generar filas de la tabla
        tbody.innerHTML = '';
        
        if (paginatedIngredients.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" class="text-center py-4">
                        <i class="fas fa-search fa-2x text-muted mb-3"></i>
                        <h5 class="text-muted">No se encontraron ingredientes</h5>
                        <p class="text-muted">Intenta ajustar los filtros de búsqueda</p>
                    </td>
                </tr>
            `;
        } else {
            paginatedIngredients.forEach(ingredient => {
                const row = document.createElement('tr');
                
                // Determinar el estado del stock
                let stockStatus = '';
                let statusClass = '';
                
                if (ingredient.stock === null) {
                    stockStatus = 'No aplica';
                    statusClass = 'text-muted';
                } else if (ingredient.stock === 0) {
                    stockStatus = 'Sin stock';
                    statusClass = 'text-danger';
                } else if (ingredient.reorder_threshold !== null && ingredient.stock < ingredient.reorder_threshold) {
                    stockStatus = 'Stock bajo';
                    statusClass = 'text-warning';
                } else {
                    stockStatus = 'Stock bueno';
                    statusClass = 'text-success';
                }
                
                row.innerHTML = `
                    <td>${ingredient.name}</td>
                    <td><span class="badge bg-info">${ingredient.category}</span></td>
                    <td>${ingredient.stock !== null ? ingredient.stock : 'N/A'}</td>
                    <td>${ingredient.unit_default}</td>
                    <td>${ingredient.reorder_threshold !== null ? ingredient.reorder_threshold : 'N/A'}</td>
                    <td class="${statusClass}">${stockStatus}</td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary me-1" data-action="edit-ingredient" data-ingredient-id="${ingredient.id}">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" data-action="delete" data-item-type="ingredient" data-item-id="${ingredient.id}" data-item-name="${ingredient.name}">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                `;
                
                tbody.appendChild(row);
            });
        }
        
        // Generar paginación
        this.generatePagination(totalPages);
        
        // Añadir event listeners a los botones de edición
        const editButtons = tbody.querySelectorAll('[data-action="edit-ingredient"]');
        editButtons.forEach(button => {
            button.addEventListener('click', () => {
                const ingredientId = button.getAttribute('data-ingredient-id');
                this.editIngredient(ingredientId);
            });
        });
    }

    filterIngredients(ingredients) {
        const searchTerm = document.getElementById('searchInput').value.toLowerCase();
        const categoryFilter = document.getElementById('categoryFilter').value;
        const stockFilter = document.getElementById('stockFilter').value;
        const sortFilter = document.getElementById('sortFilter').value;
        
        let filtered = ingredients.filter(ingredient => {
            // Filtrar por término de búsqueda
            if (searchTerm && !ingredient.name.toLowerCase().includes(searchTerm) && 
                !ingredient.category.toLowerCase().includes(searchTerm)) {
                return false;
            }
            
            // Filtrar por categoría
            if (categoryFilter && ingredient.category !== categoryFilter) {
                return false;
            }
            
            // Filtrar por estado de stock
            if (stockFilter) {
                if (stockFilter === 'low' && 
                    (ingredient.stock === null || ingredient.reorder_threshold === null || 
                     ingredient.stock >= ingredient.reorder_threshold || ingredient.stock === 0)) {
                    return false;
                }
                
                if (stockFilter === 'out' && ingredient.stock !== 0) {
                    return false;
                }
                
                if (stockFilter === 'good' && 
                    (ingredient.stock !== null && ingredient.reorder_threshold !== null && 
                     ingredient.stock < ingredient.reorder_threshold)) {
                    return false;
                }
            }
            
            return true;
        });
        
        // Ordenar
        switch(sortFilter) {
            case 'name':
                filtered.sort((a, b) => a.name.localeCompare(b.name));
                break;
            case 'stock':
                filtered.sort((a, b) => {
                    // Los valores null van al final
                    if (a.stock === null) return 1;
                    if (b.stock === null) return -1;
                    return a.stock - b.stock;
                });
                break;
            case 'category':
                filtered.sort((a, b) => a.category.localeCompare(b.category));
                break;
        }
        
        return filtered;
    }

    generatePagination(totalPages) {
        const paginationContainer = document.getElementById('pagination');
        if (!paginationContainer) return;
        
        paginationContainer.innerHTML = '';
        
        if (totalPages <= 1) return;
        
        // Botón anterior
        const prevLi = document.createElement('li');
        prevLi.className = `page-item ${this.currentPage === 1 ? 'disabled' : ''}`;
        prevLi.innerHTML = `<a class="page-link" href="#" data-page="${this.currentPage - 1}">Anterior</a>`;
        paginationContainer.appendChild(prevLi);
        
        // Números de página
        for (let i = 1; i <= totalPages; i++) {
            const pageLi = document.createElement('li');
            pageLi.className = `page-item ${this.currentPage === i ? 'active' : ''}`;
            pageLi.innerHTML = `<a class="page-link" href="#" data-page="${i}">${i}</a>`;
            paginationContainer.appendChild(pageLi);
        }
        
        // Botón siguiente
        const nextLi = document.createElement('li');
        nextLi.className = `page-item ${this.currentPage === totalPages ? 'disabled' : ''}`;
        nextLi.innerHTML = `<a class="page-link" href="#" data-page="${this.currentPage + 1}">Siguiente</a>`;
        paginationContainer.appendChild(nextLi);
        
        // Event listeners para los botones de paginación
        const pageLinks = paginationContainer.querySelectorAll('.page-link');
        pageLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const page = parseInt(link.getAttribute('data-page'));
                this.displayIngredients(page);
            });
        });
    }

    searchIngredients() {
        this.displayIngredients(1);
    }

    applyFilters() {
        this.displayIngredients(1);
    }

    showIngredientModal(ingredientData = null) {
        this.currentIngredient = ingredientData;
        
        // Crear modal dinámicamente si no existe
        if (!document.getElementById('ingredientModal')) {
            this.createIngredientModal();
        }
        
        // Llenar el modal con datos si estamos editando
        if (this.currentIngredient) {
            this.populateIngredientForm(this.currentIngredient);
        } else {
            this.clearIngredientForm();
        }
        
        // Inicializar el modal de Bootstrap y mostrarlo
        const modal = new bootstrap.Modal(document.getElementById('ingredientModal'));
        modal.show();
    }

    createIngredientModal() {
        const modalHTML = `
        <div class="modal fade" id="ingredientModal" tabindex="-1" aria-labelledby="ingredientModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="ingredientModalLabel">${this.currentIngredient ? 'Editar' : 'Nuevo'} Ingrediente</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form id="ingredientForm">
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="ingredientName" class="form-label">Nombre del ingrediente *</label>
                                        <input type="text" class="form-control" id="ingredientName" required>
                                    </div>
                                    <div class="mb-3">
                                        <label for="ingredientCategory" class="form-label">Categoría *</label>
                                        <select class="form-select" id="ingredientCategory" required>
                                            <option value="">Seleccionar categoría...</option>
                                            <option value="Alcohol">Alcohol</option>
                                            <option value="Jugo">Jugo</option>
                                            <option value="Endulzante">Endulzante</option>
                                            <option value="Hierba">Hierba</option>
                                            <option value="Refresco">Refresco</option>
                                            <option value="Licor">Licor</option>
                                            <option value="Condimento">Condimento</option>
                                            <option value="Básico">Básico</option>
                                            <option value="Fruta">Fruta</option>
                                            <option value="Verdura">Verdura</option>
                                            <option value="Especia">Especia</option>
                                            <option value="Otro">Otro</option>
                                        </select>
                                    </div>
                                    <div class="mb-3">
                                        <label for="ingredientUnit" class="form-label">Unidad por defecto *</label>
                                        <select class="form-select" id="ingredientUnit" required>
                                            <option value="">Seleccionar unidad...</option>
                                            <option value="ml">ml</option>
                                            <option value="oz">oz</option>
                                            <option value="cucharadita">cucharadita</option>
                                            <option value="cucharada">cucharada</option>
                                            <option value="unidades">unidades</option>
                                            <option value="hojas">hojas</option>
                                            <option value="gotas">gotas</option>
                                            <option value="pizca">pizca</option>
                                            <option value="g">g</option>
                                            <option value="kg">kg</option>
                                            <option value="l">l</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="ingredientCalories" class="form-label">Calorías por unidad</label>
                                        <input type="number" class="form-control" id="ingredientCalories" min="0" step="0.1">
                                    </div>
                                    <div class="mb-3">
                                        <label for="ingredientABV" class="form-label">ABV (% alcohol)</label>
                                        <input type="number" class="form-control" id="ingredientABV" min="0" max="100" step="0.1">
                                    </div>
                                    <div class="mb-3">
                                        <label for="ingredientEffects" class="form-label">Efectos/sabores (separados por comas)</label>
                                        <input type="text" class="form-control" id="ingredientEffects" placeholder="ej: refrescante, dulce, ácido">
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="ingredientStock" class="form-label">Stock actual</label>
                                        <input type="number" class="form-control" id="ingredientStock" min="0" step="0.1">
                                        <div class="form-text">Dejar vacío si no aplica (ej: hielo, agua)</div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="ingredientThreshold" class="form-label">Umbral de reorden</label>
                                        <input type="number" class="form-control" id="ingredientThreshold" min="0" step="0.1">
                                        <div class="form-text">Stock mínimo antes de alertar (dejar vacío si no aplica)</div>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-primary" id="saveIngredientBtn">Guardar Ingrediente</button>
                    </div>
                </div>
            </div>
        </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Configurar event listeners del modal
        const saveIngredientBtn = document.getElementById('saveIngredientBtn');
        if (saveIngredientBtn) {
            saveIngredientBtn.addEventListener('click', () => this.saveIngredient());
        }
    }

    populateIngredientForm(ingredient) {
        document.getElementById('ingredientName').value = ingredient.name || '';
        document.getElementById('ingredientCategory').value = ingredient.category || '';
        document.getElementById('ingredientUnit').value = ingredient.unit_default || '';
        document.getElementById('ingredientCalories').value = ingredient.calories_per_unit || '';
        document.getElementById('ingredientABV').value = ingredient.abv || '';
        document.getElementById('ingredientEffects').value = ingredient.effects ? ingredient.effects.join(', ') : '';
        document.getElementById('ingredientStock').value = ingredient.stock !== null ? ingredient.stock : '';
        document.getElementById('ingredientThreshold').value = ingredient.reorder_threshold !== null ? ingredient.reorder_threshold : '';
    }

    clearIngredientForm() {
        const form = document.getElementById('ingredientForm');
        if (form) {
            form.reset();
        }
    }

    async saveIngredient() {
        // Validar formulario
        if (!this.validateIngredientForm()) {
            window.toastManager.show('Por favor, complete todos los campos requeridos', 'warning');
            return;
        }
        
        try {
            // Recopilar datos del formulario
            const formData = this.collectIngredientFormData();
            
            if (this.currentIngredient) {
                // Actualizar ingrediente existente
                const index = this.ingredients.findIndex(ing => ing.id == this.currentIngredient.id);
                if (index !== -1) {
                    this.ingredients[index] = { ...this.ingredients[index], ...formData };
                }
                window.toastManager.show('Ingrediente actualizado correctamente', 'success');
            } else {
                // Crear nuevo ingrediente
                const newId = Math.max(...this.ingredients.map(ing => ing.id), 0) + 1;
                formData.id = newId;
                this.ingredients.push(formData);
                window.toastManager.show('Ingrediente creado correctamente', 'success');
            }
            
            // Guardar en localStorage
            localStorage.setItem('cocktailIngredients', JSON.stringify(this.ingredients));
            
            // Cerrar modal y recargar la lista
            bootstrap.Modal.getInstance(document.getElementById('ingredientModal')).hide();
            this.updateMetrics();
            this.displayIngredients();
            
        } catch (error) {
            console.error('Error saving ingredient:', error);
            window.toastManager.show('Error al guardar el ingrediente: ' + error.message, 'error');
        }
    }

    validateIngredientForm() {
        // Validar campos requeridos
        const name = document.getElementById('ingredientName');
        const category = document.getElementById('ingredientCategory');
        const unit = document.getElementById('ingredientUnit');
        
        if (!name.value.trim()) {
            name.focus();
            return false;
        }
        
        if (!category.value) {
            category.focus();
            return false;
        }
        
        if (!unit.value) {
            unit.focus();
            return false;
        }
        
        return true;
    }

    collectIngredientFormData() {
        const formData = {
            name: document.getElementById('ingredientName').value,
            category: document.getElementById('ingredientCategory').value,
            unit_default: document.getElementById('ingredientUnit').value,
            calories_per_unit: document.getElementById('ingredientCalories').value ? parseFloat(document.getElementById('ingredientCalories').value) : null,
            abv: document.getElementById('ingredientABV').value ? parseFloat(document.getElementById('ingredientABV').value) : null,
            effects: document.getElementById('ingredientEffects').value.split(',').map(e => e.trim()).filter(e => e),
            stock: document.getElementById('ingredientStock').value ? parseFloat(document.getElementById('ingredientStock').value) : null,
            reorder_threshold: document.getElementById('ingredientThreshold').value ? parseFloat(document.getElementById('ingredientThreshold').value) : null
        };
        
        return formData;
    }

    editIngredient(id) {
        const ingredient = this.ingredients.find(ing => ing.id == id);
        if (ingredient) {
            this.showIngredientModal(ingredient);
        }
    }

    async deleteIngredient(id) {
        try {
            // Eliminar localmente
            this.ingredients = this.ingredients.filter(ing => ing.id != id);
            
            // Guardar en localStorage
            localStorage.setItem('cocktailIngredients', JSON.stringify(this.ingredients));
            
            // Actualizar la UI
            this.updateMetrics();
            this.displayIngredients();
            
            window.toastManager.show('Ingrediente eliminado correctamente', 'success');
        } catch (error) {
            console.error('Error deleting ingredient:', error);
            window.toastManager.show('Error al eliminar el ingrediente: ' + error.message, 'error');
        }
    }
}

// Inicializar el manager de inventario cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('ingredientsTable')) {
        window.inventoryManager = new InventoryManager();
    }
    
    // Manejar eliminación de ingredientes
    document.addEventListener('deleteItem', function(e) {
        if (e.detail.itemType === 'ingredient') {
            window.inventoryManager.deleteIngredient(e.detail.itemId);
        }
    });
});