// Gestión de cócteles - CRUD completo
class CocktailManager {
    constructor() {
        this.currentCocktail = null;
        this.ingredients = [];
        this.cocktails = [];
        this.init();
    }

    init() {
        this.loadIngredients();
        this.loadCocktails();
        this.setupEventListeners();
        
        // Verificar si estamos editando un cóctel desde la URL
        const urlParams = new URLSearchParams(window.location.search);
        const editId = urlParams.get('edit');
        if (editId) {
            this.loadCocktailForEditing(editId);
        }
    }

    setupEventListeners() {
        // Botón para agregar nuevo cóctel
        const addCocktailBtn = document.getElementById('addCocktailBtn');
        if (addCocktailBtn) {
            addCocktailBtn.addEventListener('click', () => this.showCocktailModal());
        }

        // Formulario de búsqueda
        const searchForm = document.getElementById('searchForm');
        if (searchForm) {
            searchForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.searchCocktails();
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
                this.searchTimeout = setTimeout(() => this.searchCocktails(), 500);
            });
        }
    }

    async loadIngredients() {
        try {
            // Primero intentar cargar desde localStorage
            const savedIngredients = localStorage.getItem('cocktailIngredients');
            
            if (savedIngredients) {
                this.ingredients = JSON.parse(savedIngredients);
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
            
        } catch (error) {
            console.error('Error loading ingredients:', error);
            window.toastManager.show('Error al cargar los ingredientes', 'error');
            
            // Datos de respaldo en caso de error
            this.ingredients = [
                { id: 1, name: "Ron blanco", category: "Alcohol", unit_default: "ml", calories_per_unit: 65, abv: 40 },
                { id: 2, name: "Jugo de lima", category: "Jugo", unit_default: "ml", calories_per_unit: 4, abv: 0 },
                { id: 3, name: "Azúcar moreno", category: "Endulzante", unit_default: "cucharadita", calories_per_unit: 16, abv: 0 },
                { id: 4, name: "Hierbabuena", category: "Hierba", unit_default: "hojas", calories_per_unit: 1, abv: 0 },
                { id: 5, name: "Soda", category: "Refresco", unit_default: "ml", calories_per_unit: 0, abv: 0 }
            ];
        }
    }

    async loadCocktails() {
        try {
            // Primero intentar cargar desde localStorage
            const savedCocktails = localStorage.getItem('cocktailRecipes');
            
            if (savedCocktails) {
                this.cocktails = JSON.parse(savedCocktails);
                this.displayCocktails(this.cocktails);
                return;
            }
            
            // Si no hay en localStorage, cargar desde el archivo JSON
            const response = await fetch('../data/seed_cocktails.json');
            if (!response.ok) {
                throw new Error('No se pudo cargar el archivo de cócteles');
            }
            
            this.cocktails = await response.json();
            
            // Guardar en localStorage para uso futuro
            localStorage.setItem('cocktailRecipes', JSON.stringify(this.cocktails));
            
            this.displayCocktails(this.cocktails);
            
        } catch (error) {
            console.error('Error loading cocktails:', error);
            window.toastManager.show('Error al cargar los cócteles', 'error');
            
            // Datos de respaldo en caso de error
            const backupCocktails = [
                {
                    id: 1,
                    name: "Mojito Clásico",
                    short_description: "Refrescante cóctel cubano con hierbabuena y lima",
                    image_urls: ["https://via.placeholder.com/300x200/3D8FC2/FFFFFF?text=Mojito"],
                    categories: ["Refrescante", "Tropical"],
                    bases: ["Ron blanco"],
                    prep_time_minutes: 5,
                    difficulty: "Fácil",
                    calories: 180,
                    is_published: true
                },
                {
                    id: 2,
                    name: "Margarita",
                    short_description: "Cóctel de tequila con triple sec y lima",
                    image_urls: ["https://via.placeholder.com/300x200/3D8FC2/FFFFFF?text=Margarita"],
                    categories: ["Clásico", "Ácido"],
                    bases: ["Tequila"],
                    prep_time_minutes: 7,
                    difficulty: "Moderado",
                    calories: 200,
                    is_published: true
                }
            ];
            
            this.displayCocktails(backupCocktails);
        }
    }

    displayCocktails(cocktails) {
        const container = document.getElementById('cocktailsContainer');
        if (!container) return;
        
        container.innerHTML = '';
        
        if (cocktails.length === 0) {
            container.innerHTML = `
                <div class="col-12 text-center py-5">
                    <i class="fas fa-glass-martini-alt fa-3x text-muted mb-3"></i>
                    <h4 class="text-muted">No se encontraron cócteles</h4>
                    <p class="text-muted">Intenta ajustar los filtros de búsqueda</p>
                </div>
            `;
            return;
        }
        
        cocktails.forEach(cocktail => {
            const col = document.createElement('div');
            col.className = 'col-md-6 col-lg-4 mb-4';
            col.innerHTML = this.createCocktailCard(cocktail);
            container.appendChild(col);
            
            // Añadir event listeners a los botones
            const editBtn = col.querySelector('[data-action="edit"]');
            if (editBtn) {
                editBtn.addEventListener('click', () => {
                    this.loadCocktailForEditing(cocktail.id);
                });
            }
        });
    }

    createCocktailCard(cocktail) {
        const publishedStatus = cocktail.is_published ? 
            '<span class="badge bg-success">Publicado</span>' : 
            '<span class="badge bg-secondary">Borrador</span>';
            
        const baseSpirit = cocktail.bases && cocktail.bases.length > 0 ? 
            `<span class="badge bg-info">${cocktail.bases[0]}</span>` : '';
            
        return `
            <div class="cocktail-card card h-100">
                <img src="${cocktail.image_urls && cocktail.image_urls[0] ? cocktail.image_urls[0] : 'https://via.placeholder.com/300x200/3D8FC2/FFFFFF?text=Cóctel'}" 
                     class="cocktail-image card-img-top" alt="${cocktail.name}">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <h5 class="cocktail-title">${cocktail.name}</h5>
                        ${publishedStatus}
                    </div>
                    <p class="cocktail-description">${cocktail.short_description || 'Descripción no disponible'}</p>
                    <div class="cocktail-meta">
                        <div>
                            ${baseSpirit}
                            <span class="badge bg-primary">${cocktail.prep_time_minutes || '?'} min</span>
                            <span class="badge bg-secondary">${cocktail.difficulty || 'N/A'}</span>
                        </div>
                        <div class="mt-2">
                            <span class="text-muted">${cocktail.calories || '?'} cal</span>
                        </div>
                    </div>
                </div>
                <div class="card-footer bg-transparent d-flex justify-content-between">
                    <button class="btn btn-sm btn-outline-primary" data-action="edit" data-cocktail-id="${cocktail.id}">
                        <i class="fas fa-edit me-1"></i> Editar
                    </button>
                    <button class="btn btn-sm btn-outline-danger" data-action="delete" data-item-type="cocktail" data-item-id="${cocktail.id}" data-item-name="${cocktail.name}">
                        <i class="fas fa-trash me-1"></i> Eliminar
                    </button>
                </div>
            </div>
        `;
    }

    async loadCocktailForEditing(id) {
        try {
            // Buscar el cóctel en la lista cargada
            this.currentCocktail = this.cocktails.find(c => c.id == id) || null;
            
            if (this.currentCocktail) {
                this.showCocktailModal();
            } else {
                window.toastManager.show('No se encontró el cóctel solicitado', 'error');
            }
        } catch (error) {
            console.error('Error loading cocktail for editing:', error);
            window.toastManager.show('Error al cargar el cóctel para edición', 'error');
        }
    }

    showCocktailModal() {
        // Crear modal dinámicamente si no existe
        if (!document.getElementById('cocktailModal')) {
            this.createCocktailModal();
        }
        
        // Llenar el modal con datos si estamos editando
        if (this.currentCocktail) {
            this.populateCocktailForm(this.currentCocktail);
        } else {
            this.clearCocktailForm();
        }
        
        // Mostrar el modal
        const modalElement = document.getElementById('cocktailModal');
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
    }

    createCocktailModal() {
        const modalHTML = `
        <div class="modal fade" id="cocktailModal" tabindex="-1" aria-labelledby="cocktailModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-xl">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="cocktailModalLabel">${this.currentCocktail ? 'Editar' : 'Nuevo'} Cóctel</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <ul class="nav nav-tabs modal-tabs" id="cocktailTabs" role="tablist">
                            <li class="nav-item" role="presentation">
                                <button class="nav-link active" id="general-tab" data-bs-toggle="tab" data-bs-target="#general" type="button" role="tab" aria-controls="general" aria-selected="true">General</button>
                            </li>
                            <li class="nav-item" role="presentation">
                                <button class="nav-link" id="ingredients-tab" data-bs-toggle="tab" data-bs-target="#ingredients" type="button" role="tab" aria-controls="ingredients" aria-selected="false">Ingredientes</button>
                            </li>
                            <li class="nav-item" role="presentation">
                                <button class="nav-link" id="preparation-tab" data-bs-toggle="tab" data-bs-target="#preparation" type="button" role="tab" aria-controls="preparation" aria-selected="false">Preparación</button>
                            </li>
                            <li class="nav-item" role="presentation">
                                <button class="nav-link" id="media-tab" data-bs-toggle="tab" data-bs-target="#media" type="button" role="tab" aria-controls="media" aria-selected="false">Multimedia</button>
                            </li>
                            <li class="nav-item" role="presentation">
                                <button class="nav-link" id="metadata-tab" data-bs-toggle="tab" data-bs-target="#metadata" type="button" role="tab" aria-controls="metadata" aria-selected="false">Metadatos</button>
                            </li>
                        </ul>
                        <div class="tab-content p-3" id="cocktailTabContent">
                            <!-- General Tab -->
                            <div class="tab-pane fade show active" id="general" role="tabpanel" aria-labelledby="general-tab">
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <label for="cocktailName" class="form-label">Nombre del cóctel *</label>
                                            <input type="text" class="form-control" id="cocktailName" required>
                                        </div>
                                        <div class="mb-3">
                                            <label for="cocktailSlug" class="form-label">Slug (URL)</label>
                                            <input type="text" class="form-control" id="cocktailSlug">
                                        </div>
                                        <div class="mb-3">
                                            <label for="shortDescription" class="form-label">Descripción corta *</label>
                                            <textarea class="form-control" id="shortDescription" rows="2" required></textarea>
                                        </div>
                                        <div class="mb-3">
                                            <label for="longDescription" class="form-label">Descripción larga</label>
                                            <textarea class="form-control" id="longDescription" rows="4"></textarea>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <label for="glassType" class="form-label">Tipo de vaso</label>
                                            <select class="form-select" id="glassType">
                                                <option value="">Seleccionar...</option>
                                                <option value="Highball">Highball</option>
                                                <option value="Old Fashioned">Old Fashioned</option>
                                                <option value="Martini">Martini</option>
                                                <option value="Margarita">Margarita</option>
                                                <option value="Hurricane">Hurricane</option>
                                                <option value="Shot">Shot</option>
                                                <option value="Coupe">Coupe</option>
                                                <option value="Flute">Flute</option>
                                            </select>
                                        </div>
                                        <div class="mb-3">
                                            <label for="method" class="form-label">Método de preparación</label>
                                            <select class="form-select" id="method">
                                                <option value="">Seleccionar...</option>
                                                <option value="Shaken">Agitado (Shaken)</option>
                                                <option value="Stirred">Mezclado (Stirred)</option>
                                                <option value="Muddled">Macerado (Muddled)</option>
                                                <option value="Blended">Licuado (Blended)</option>
                                                <option value="Built">Construido en vaso (Built)</option>
                                                <option value="Layered">En capas (Layered)</option>
                                            </select>
                                        </div>
                                        <div class="row">
                                            <div class="col-md-6">
                                                <div class="mb-3">
                                                    <label for="prepTime" class="form-label">Tiempo preparación (min)</label>
                                                    <input type="number" class="form-control" id="prepTime" min="1">
                                                </div>
                                            </div>
                                            <div class="col-md-6">
                                                <div class="mb-3">
                                                    <label for="servings" class="form-label">Porciones</label>
                                                    <input type="number" class="form-control" id="servings" min="1" value="1">
                                                </div>
                                            </div>
                                        </div>
                                        <div class="mb-3">
                                            <label for="difficulty" class="form-label">Dificultad</label>
                                            <select class="form-select" id="difficulty">
                                                <option value="Fácil">Fácil</option>
                                                <option value="Moderado">Moderado</option>
                                                <option value="Avanzado">Avanzado</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Ingredients Tab -->
                            <div class="tab-pane fade" id="ingredients" role="tabpanel" aria-labelledby="ingredients-tab">
                                <div id="ingredientsContainer">
                                    <!-- Los ingredientes se añadirán dinámicamente aquí -->
                                </div>
                                <button type="button" class="btn btn-sm btn-outline-primary mt-3" id="addIngredientBtn">
                                    <i class="fas fa-plus me-1"></i> Añadir ingrediente
                                </button>
                            </div>
                            
                            <!-- Preparation Tab -->
                            <div class="tab-pane fade" id="preparation" role="tabpanel" aria-labelledby="preparation-tab">
                                <div class="mb-3">
                                    <label class="form-label">Pasos de preparación *</label>
                                    <div id="stepsContainer">
                                        <!-- Los pasos se añadirán dinámicamente aquí -->
                                    </div>
                                    <button type="button" class="btn btn-sm btn-outline-primary mt-3" id="addStepBtn">
                                        <i class="fas fa-plus me-1"></i> Añadir paso
                                    </button>
                                </div>
                            </div>
                            
                            <!-- Media Tab -->
                            <div class="tab-pane fade" id="media" role="tabpanel" aria-labelledby="media-tab">
                                <div class="mb-3">
                                    <label class="form-label">Imágenes del cóctel</label>
                                    <div class="image-uploader" id="imageUploader">
                                        <i class="fas fa-cloud-upload-alt upload-icon"></i>
                                        <p class="upload-text">Arrastra imágenes aquí o haz clic para seleccionar</p>
                                        <input type="file" multiple accept="image/*" style="display: none;" id="imageInput">
                                    </div>
                                    <div class="image-preview mt-3" id="imagePreview">
                                        <!-- Las previsualizaciones de imágenes se mostrarán aquí -->
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Metadata Tab -->
                            <div class="tab-pane fade" id="metadata" role="tabpanel" aria-labelledby="metadata-tab">
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <label for="categories" class="form-label">Categorías</label>
                                            <select class="form-select" id="categories" multiple>
                                                <option value="Refrescante">Refrescante</option>
                                                <option value="Tropical">Tropical</option>
                                                <option value="Clásico">Clásico</option>
                                                <option value="Ácido">Ácido</option>
                                                <option value="Cremoso">Cremoso</option>
                                                <option value="Fuerte">Fuerte</option>
                                                <option value="Dulce">Dulce</option>
                                                <option value="Amargo">Amargo</option>
                                                <option value="Festivo">Festivo</option>
                                                <option value="Digestivo">Digestivo</option>
                                            </select>
                                            <div class="form-text">Mantén presionada la tecla Ctrl para seleccionar múltiples opciones</div>
                                        </div>
                                        <div class="mb-3">
                                            <label for="bases" class="form-label">Bases alcohólicas</label>
                                            <select class="form-select" id="bases" multiple>
                                                <option value="Ron blanco">Ron blanco</option>
                                                <option value="Ron oscuro">Ron oscuro</option>
                                                <option value="Tequila">Tequila</option>
                                                <option value="Vodka">Vodka</option>
                                                <option value="Ginebra">Ginebra</option>
                                                <option value="Whisky">Whisky</option>
                                                <option value="Brandy">Brandy</option>
                                                <option value="Champagne">Champagne</option>
                                                <option value="Vino">Vino</option>
                                                <option value="Cerveza">Cerveza</option>
                                            </select>
                                        </div>
                                        <div class="mb-3">
                                            <label for="effects" class="form-label">Efectos/sabores</label>
                                            <select class="form-select" id="effects" multiple>
                                                <option value="Refrescante">Refrescante</option>
                                                <option value="Energizante">Energizante</option>
                                                <option value="Relajante">Relajante</option>
                                                <option value="Cítrico">Cítrico</option>
                                                <option value="Dulce">Dulce</option>
                                                <option value="Amargo">Amargo</option>
                                                <option value="Picante">Picante</option>
                                                <option value="Herbal">Herbal</option>
                                                <option value="Afrutado">Afrutado</option>
                                                <option value="Cremoso">Cremoso</option>
                                            </select>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <label for="tags" class="form-label">Etiquetas (separadas por comas)</label>
                                            <input type="text" class="form-control" id="tags" placeholder="ej: verano, fiesta, cubano">
                                        </div>
                                        <div class="mb-3">
                                            <label for="aromatics" class="form-label">Aromáticos</label>
                                            <input type="text" class="form-control" id="aromatics" placeholder="ej: hierbabuena, jengibre, canela">
                                        </div>
                                        <div class="mb-3">
                                            <label for="garnish" class="form-label">Guarnición</label>
                                            <input type="text" class="form-control" id="garnish" placeholder="ej: rodaja de lima, rama de hierbabuena">
                                        </div>
                                        <div class="mb-3">
                                            <label for="calories" class="form-label">Calorías (aprox.)</label>
                                            <input type="number" class="form-control" id="calories" min="0">
                                        </div>
                                        <div class="form-check form-switch mb-3">
                                            <input class="form-check-input" type="checkbox" id="isPublished">
                                            <label class="form-check-label" for="isPublished">Publicado</label>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-primary" id="saveCocktailBtn">Guardar Cóctel</button>
                    </div>
                </div>
            </div>
        </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Configurar event listeners del modal
        this.setupModalEventListeners();
    }

    setupModalEventListeners() {
        // Auto-generar slug a partir del nombre
        const cocktailName = document.getElementById('cocktailName');
        const cocktailSlug = document.getElementById('cocktailSlug');
        
        if (cocktailName && cocktailSlug) {
            cocktailName.addEventListener('blur', function() {
                if (!cocktailSlug.value) {
                    const slug = this.value.toLowerCase()
                        .replace(/[^\w\s]/gi, '')
                        .replace(/\s+/g, '-');
                    cocktailSlug.value = slug;
                }
            });
        }
        
        // Botón para añadir ingredientes
        const addIngredientBtn = document.getElementById('addIngredientBtn');
        if (addIngredientBtn) {
            addIngredientBtn.addEventListener('click', () => this.addIngredientRow());
        }
        
        // Botón para añadir pasos
        const addStepBtn = document.getElementById('addStepBtn');
        if (addStepBtn) {
            addStepBtn.addEventListener('click', () => this.addStepField());
        }
        
        // Upload de imágenes
        const imageUploader = document.getElementById('imageUploader');
        const imageInput = document.getElementById('imageInput');
        
        if (imageUploader && imageInput) {
            imageUploader.addEventListener('click', () => imageInput.click());
            
            imageUploader.addEventListener('dragover', (e) => {
                e.preventDefault();
                imageUploader.classList.add('bg-light');
            });
            
            imageUploader.addEventListener('dragleave', () => {
                imageUploader.classList.remove('bg-light');
            });
            
            imageUploader.addEventListener('drop', (e) => {
                e.preventDefault();
                imageUploader.classList.remove('bg-light');
                
                if (e.dataTransfer.files.length > 0) {
                    imageInput.files = e.dataTransfer.files;
                    this.handleImageUpload(e.dataTransfer.files);
                }
            });
            
            imageInput.addEventListener('change', () => {
                if (imageInput.files.length > 0) {
                    this.handleImageUpload(imageInput.files);
                }
            });
        }
        
        // Guardar cóctel
        const saveCocktailBtn = document.getElementById('saveCocktailBtn');
        if (saveCocktailBtn) {
            saveCocktailBtn.addEventListener('click', () => this.saveCocktail());
        }
        
        // Inicializar ingredientes y pasos si estamos en modo edición
        if (this.currentCocktail) {
            // Añadir filas de ingredientes
            if (this.currentCocktail.ingredients && this.currentCocktail.ingredients.length > 0) {
                this.currentCocktail.ingredients.forEach(ing => this.addIngredientRow(ing));
            } else {
                this.addIngredientRow(); // Añadir una fila vacía por defecto
            }
            
            // Añadir campos de pasos
            if (this.currentCocktail.steps && this.currentCocktail.steps.length > 0) {
                this.currentCocktail.steps.forEach(step => this.addStepField(step));
            } else {
                this.addStepField(); // Añadir un campo vacío por defecto
            }
            
            // Cargar imágenes si existen
            if (this.currentCocktail.image_urls && this.currentCocktail.image_urls.length > 0) {
                // Simular la visualización de imágenes existentes
                this.currentCocktail.image_urls.forEach(url => {
                    this.showImagePreview(url);
                });
            }
        } else {
            // Modo nuevo: añadir una fila de ingrediente y un paso vacíos
            this.addIngredientRow();
            this.addStepField();
        }
    }

    addIngredientRow(ingredientData = null) {
        const container = document.getElementById('ingredientsContainer');
        if (!container) return;
        
        const rowId = `ingredient-${Date.now()}`;
        const row = document.createElement('div');
        row.className = 'ingredient-row';
        row.id = rowId;
        
        // Obtener opciones de ingredientes
        const ingredientOptions = this.ingredients.map(ing => 
            `<option value="${ing.id}" ${ingredientData && ingredientData.ingredient_id == ing.id ? 'selected' : ''}>${ing.name}</option>`
        ).join('');
        
        // Unidades de medida comunes
        const unitOptions = `
            <option value="ml" ${ingredientData && ingredientData.unit === 'ml' ? 'selected' : ''}>ml</option>
            <option value="oz" ${ingredientData && ingredientData.unit === 'oz' ? 'selected' : ''}>oz</option>
            <option value="cucharadita" ${ingredientData && ingredientData.unit === 'cucharadita' ? 'selected' : ''}>cucharadita</option>
            <option value="cucharada" ${ingredientData && ingredientData.unit === 'cucharada' ? 'selected' : ''}>cucharada</option>
            <option value="unidades" ${ingredientData && ingredientData.unit === 'unidades' ? 'selected' : ''}>unidades</option>
            <option value="hojas" ${ingredientData && ingredientData.unit === 'hojas' ? 'selected' : ''}>hojas</option>
            <option value="gotas" ${ingredientData && ingredientData.unit === 'gotas' ? 'selected' : ''}>gotas</option>
            <option value="pizca" ${ingredientData && ingredientData.unit === 'pizca' ? 'selected' : ''}>pizca</option>
        `;
        
        row.innerHTML = `
            <div class="ingredient-field">
                <label class="form-label">Ingrediente</label>
                <select class="form-select ingredient-select" name="ingredient">
                    <option value="">Seleccionar ingrediente...</option>
                    ${ingredientOptions}
                </select>
            </div>
            <div class="amount-field">
                <label class="form-label">Cantidad</label>
                <input type="number" class="form-control" name="amount" step="0.5" min="0" value="${ingredientData ? ingredientData.amount : ''}">
            </div>
            <div class="unit-field">
                <label class="form-label">Unidad</label>
                <select class="form-select" name="unit">
                    <option value="">Seleccionar...</option>
                    ${unitOptions}
                </select>
            </div>
            <div class="ingredient-field">
                <label class="form-label">Nota (opcional)</label>
                <input type="text" class="form-control" name="note" value="${ingredientData ? ingredientData.note : ''}">
            </div>
            <button type="button" class="btn btn-sm btn-outline-danger remove-btn" data-remove-row="${rowId}">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        container.appendChild(row);
        
        // Event listener para eliminar fila
        const removeBtn = row.querySelector(`[data-remove-row="${rowId}"]`);
        if (removeBtn) {
            removeBtn.addEventListener('click', () => row.remove());
        }
    }

    addStepField(stepText = '') {
        const container = document.getElementById('stepsContainer');
        if (!container) return;
        
        const stepId = `step-${Date.now()}`;
        const stepCount = container.children.length + 1;
        
        const stepDiv = document.createElement('div');
        stepDiv.className = 'mb-2 step-row';
        stepDiv.innerHTML = `
            <label class="form-label">Paso ${stepCount}</label>
            <div class="input-group">
                <textarea class="form-control" name="step" rows="2">${stepText}</textarea>
                <button class="btn btn-outline-danger" type="button" data-remove-step>
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        container.appendChild(stepDiv);
        
        // Event listener para eliminar paso
        const removeBtn = stepDiv.querySelector('[data-remove-step]');
        if (removeBtn) {
            removeBtn.addEventListener('click', () => {
                stepDiv.remove();
                this.renumberSteps();
            });
        }
    }

    renumberSteps() {
        const container = document.getElementById('stepsContainer');
        if (!container) return;
        
        const steps = container.querySelectorAll('.step-row');
        steps.forEach((step, index) => {
            const label = step.querySelector('.form-label');
            if (label) {
                label.textContent = `Paso ${index + 1}`;
            }
        });
    }

    handleImageUpload(files) {
        const previewContainer = document.getElementById('imagePreview');
        if (!previewContainer) return;
        
        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            if (!file.type.match('image.*')) continue;
            
            const reader = new FileReader();
            reader.onload = (e) => {
                this.showImagePreview(e.target.result, file.name);
            };
            reader.readAsDataURL(file);
        }
    }

    showImagePreview(url, filename = 'image') {
        const previewContainer = document.getElementById('imagePreview');
        if (!previewContainer) return;
        
        const previewDiv = document.createElement('div');
        previewDiv.className = 'preview-container';
        previewDiv.innerHTML = `
            <img src="${url}" class="preview-image" alt="Preview">
            <span class="preview-remove">&times;</span>
            <input type="hidden" name="image_url" value="${url}">
        `;
        
        previewContainer.appendChild(previewDiv);
        
        // Event listener para eliminar imagen
        const removeBtn = previewDiv.querySelector('.preview-remove');
        if (removeBtn) {
            removeBtn.addEventListener('click', () => previewDiv.remove());
        }
    }

    populateCocktailForm(cocktail) {
        // Llenar campos generales
        document.getElementById('cocktailName').value = cocktail.name || '';
        document.getElementById('cocktailSlug').value = cocktail.slug || '';
        document.getElementById('shortDescription').value = cocktail.short_description || '';
        document.getElementById('longDescription').value = cocktail.long_description || '';
        document.getElementById('glassType').value = cocktail.glass_type || '';
        document.getElementById('method').value = cocktail.method || '';
        document.getElementById('prepTime').value = cocktail.prep_time_minutes || '';
        document.getElementById('servings').value = cocktail.servings || 1;
        document.getElementById('difficulty').value = cocktail.difficulty || 'Fácil';
        document.getElementById('calories').value = cocktail.calories || '';
        document.getElementById('isPublished').checked = cocktail.is_published || false;
        
        // Llenar campos de metadata
        if (cocktail.tags) {
            document.getElementById('tags').value = Array.isArray(cocktail.tags) ? cocktail.tags.join(', ') : cocktail.tags;
        }
        
        if (cocktail.aromatics) {
            document.getElementById('aromatics').value = Array.isArray(cocktail.aromatics) ? cocktail.aromatics.join(', ') : cocktail.aromatics;
        }
        
        if (cocktail.garnish) {
            document.getElementById('garnish').value = Array.isArray(cocktail.garnish) ? cocktail.garnish.join(', ') : cocktail.garnish;
        }
        
        // Seleccionar opciones múltiples
        this.selectMultipleOptions('categories', cocktail.categories);
        this.selectMultipleOptions('bases', cocktail.bases);
        this.selectMultipleOptions('effects', cocktail.effects);
    }

    selectMultipleOptions(selectId, values) {
        const select = document.getElementById(selectId);
        if (!select || !values) return;
        
        const options = select.options;
        for (let i = 0; i < options.length; i++) {
            options[i].selected = values.includes(options[i].value);
        }
    }

    clearCocktailForm() {
        // Limpiar todos los campos del formulario
        const form = document.getElementById('cocktailModal');
        if (form) {
            const inputs = form.querySelectorAll('input, textarea, select');
            inputs.forEach(input => {
                if (input.type !== 'button' && input.type !== 'submit') {
                    input.value = '';
                }
                
                if (input.type === 'checkbox') {
                    input.checked = false;
                }
                
                if (input.tagName === 'SELECT' && input.multiple) {
                    const options = input.options;
                    for (let i = 0; i < options.length; i++) {
                        options[i].selected = false;
                    }
                }
            });
        }
        
        // Limpiar contenedores dinámicos
        const ingredientsContainer = document.getElementById('ingredientsContainer');
        if (ingredientsContainer) ingredientsContainer.innerHTML = '';
        
        const stepsContainer = document.getElementById('stepsContainer');
        if (stepsContainer) stepsContainer.innerHTML = '';
        
        const imagePreview = document.getElementById('imagePreview');
        if (imagePreview) imagePreview.innerHTML = '';
    }

    async saveCocktail() {
        // Validar formulario
        if (!this.validateCocktailForm()) {
            window.toastManager.show('Por favor, complete todos los campos requeridos', 'warning');
            return;
        }
        
        try {
            // Recopilar datos del formulario
            const formData = this.collectFormData();
            
            if (this.currentCocktail) {
                // Actualizar cóctel existente
                const index = this.cocktails.findIndex(c => c.id == this.currentCocktail.id);
                if (index !== -1) {
                    this.cocktails[index] = { ...this.cocktails[index], ...formData };
                }
            } else {
                // Crear nuevo cóctel
                const newId = Math.max(...this.cocktails.map(c => c.id), 0) + 1;
                formData.id = newId;
                formData.created_by = 1; // ID del usuario actual
                formData.timestamps = {
                    created_at: new Date().toISOString(),
                    updated_at: new Date().toISOString()
                };
                this.cocktails.push(formData);
            }
            
            // Guardar en localStorage
            localStorage.setItem('cocktailRecipes', JSON.stringify(this.cocktails));
            
            // Cerrar modal y recargar la lista
            bootstrap.Modal.getInstance(document.getElementById('cocktailModal')).hide();
            this.displayCocktails(this.cocktails);
            
            window.toastManager.show(`Cóctel ${this.currentCocktail ? 'actualizado' : 'creado'} correctamente`, 'success');
            
        } catch (error) {
            console.error('Error saving cocktail:', error);
            window.toastManager.show('Error al guardar el cóctel: ' + error.message, 'error');
        }
    }

    validateCocktailForm() {
        // Validar campos requeridos
        const name = document.getElementById('cocktailName');
        const shortDescription = document.getElementById('shortDescription');
        
        if (!name.value.trim()) {
            name.focus();
            return false;
        }
        
        if (!shortDescription.value.trim()) {
            shortDescription.focus();
            return false;
        }
        
        // Validar que haya al menos un ingrediente
        const ingredients = document.querySelectorAll('.ingredient-row');
        if (ingredients.length === 0) {
            window.toastManager.show('Debe agregar al menos un ingrediente', 'warning');
            return false;
        }
        
        // Validar que haya al menos un paso
        const steps = document.querySelectorAll('.step-row');
        if (steps.length === 0) {
            window.toastManager.show('Debe agregar al menos un paso de preparación', 'warning');
            return false;
        }
        
        return true;
    }

    collectFormData() {
        // Recopilar datos de todos los campos del formulario
        const formData = {
            name: document.getElementById('cocktailName').value,
            slug: document.getElementById('cocktailSlug').value || document.getElementById('cocktailName').value.toLowerCase().replace(/\s+/g, '-'),
            short_description: document.getElementById('shortDescription').value,
            long_description: document.getElementById('longDescription').value,
            glass_type: document.getElementById('glassType').value,
            method: document.getElementById('method').value,
            prep_time_minutes: parseInt(document.getElementById('prepTime').value) || 0,
            servings: parseInt(document.getElementById('servings').value) || 1,
            difficulty: document.getElementById('difficulty').value,
            calories: parseInt(document.getElementById('calories').value) || 0,
            is_published: document.getElementById('isPublished').checked,
            tags: document.getElementById('tags').value.split(',').map(t => t.trim()).filter(t => t),
            aromatics: document.getElementById('aromatics').value.split(',').map(a => a.trim()).filter(a => a),
            garnish: document.getElementById('garnish').value.split(',').map(g => g.trim()).filter(g => g),
            categories: Array.from(document.getElementById('categories').selectedOptions).map(o => o.value),
            bases: Array.from(document.getElementById('bases').selectedOptions).map(o => o.value),
            effects: Array.from(document.getElementById('effects').selectedOptions).map(o => o.value),
            ingredients: [],
            steps: [],
            image_urls: []
        };
        
        // Recopilar ingredientes
        const ingredientRows = document.querySelectorAll('.ingredient-row');
        ingredientRows.forEach(row => {
            const ingredientId = row.querySelector('[name="ingredient"]').value;
            const amount = row.querySelector('[name="amount"]').value;
            const unit = row.querySelector('[name="unit"]').value;
            const note = row.querySelector('[name="note"]').value;
            
            if (ingredientId && amount && unit) {
                formData.ingredients.push({
                    ingredient_id: parseInt(ingredientId),
                    amount: parseFloat(amount),
                    unit: unit,
                    note: note
                });
            }
        });
        
        // Recopilar pasos
        const stepRows = document.querySelectorAll('.step-row textarea');
        stepRows.forEach(textarea => {
            if (textarea.value.trim()) {
                formData.steps.push(textarea.value.trim());
            }
        });
        
        // Recopilar URLs de imágenes
        const imageInputs = document.querySelectorAll('input[name="image_url"]');
        imageInputs.forEach(input => {
            if (input.value) {
                formData.image_urls.push(input.value);
            }
        });
        
        return formData;
    }

    searchCocktails() {
        const searchTerm = document.getElementById('searchInput').value.toLowerCase();
        const categoryFilter = document.getElementById('categoryFilter').value;
        const baseFilter = document.getElementById('baseFilter').value;
        const difficultyFilter = document.getElementById('difficultyFilter').value;
        const statusFilter = document.getElementById('statusFilter').value;
        
        const filteredCocktails = this.cocktails.filter(cocktail => {
            // Filtrar por término de búsqueda
            if (searchTerm && !cocktail.name.toLowerCase().includes(searchTerm) && 
                !cocktail.short_description.toLowerCase().includes(searchTerm)) {
                return false;
            }
            
            // Filtrar por categoría
            if (categoryFilter && (!cocktail.categories || !cocktail.categories.includes(categoryFilter))) {
                return false;
            }
            
            // Filtrar por base alcohólica
            if (baseFilter && (!cocktail.bases || !cocktail.bases.includes(baseFilter))) {
                return false;
            }
            
            // Filtrar por dificultad
            if (difficultyFilter && cocktail.difficulty !== difficultyFilter) {
                return false;
            }
            
            // Filtrar por estado de publicación
            if (statusFilter === 'published' && !cocktail.is_published) {
                return false;
            }
            
            if (statusFilter === 'draft' && cocktail.is_published) {
                return false;
            }
            
            return true;
        });
        
        this.displayCocktails(filteredCocktails);
    }

    applyFilters() {
        this.searchCocktails();
    }
}

// Inicializar el manager de cócteles cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('cocktailsContainer')) {
        window.cocktailManager = new CocktailManager();
    }
});