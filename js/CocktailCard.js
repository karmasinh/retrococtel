// Componente CocktailCard para mostrar tarjetas de cócteles
class CocktailCard extends HTMLElement {
    constructor() {
        super();
    }

    connectedCallback() {
        this.render();
    }

    static get observedAttributes() {
        return ['id', 'name', 'description', 'image', 'categories', 'prep-time', 'difficulty', 'calories', 'published'];
    }

    attributeChangedCallback(name, oldValue, newValue) {
        if (oldValue !== newValue) {
            this.render();
        }
    }

    render() {
        const id = this.getAttribute('id') || '';
        const name = this.getAttribute('name') || 'Cóctel';
        const description = this.getAttribute('description') || '';
        const image = this.getAttribute('image') || 'https://via.placeholder.com/300x200/3D8FC2/FFFFFF?text=Cóctel';
        const categories = this.getAttribute('categories') || '';
        const prepTime = this.getAttribute('prep-time') || '';
        const difficulty = this.getAttribute('difficulty') || '';
        const calories = this.getAttribute('calories') || '';
        const published = this.getAttribute('published') === 'true';

        const publishedStatus = published ? 
            '<span class="badge bg-success">Publicado</span>' : 
            '<span class="badge bg-secondary">Borrador</span>';

        const categoryBadges = categories.split(',').map(cat => 
            `<span class="badge bg-info me-1">${cat.trim()}</span>`
        ).join('');

        this.innerHTML = `
            <div class="card h-100">
                <img src="${image}" class="card-img-top cocktail-image" alt="${name}">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <h5 class="card-title">${name}</h5>
                        ${publishedStatus}
                    </div>
                    <p class="card-text">${description}</p>
                    <div class="mb-2">
                        ${categoryBadges}
                    </div>
                    <div class="cocktail-meta">
                        <div>
                            <span class="badge bg-primary">${prepTime} min</span>
                            <span class="badge bg-secondary">${difficulty}</span>
                        </div>
                        <div class="mt-2">
                            <span class="text-muted">${calories} cal</span>
                        </div>
                    </div>
                </div>
                <div class="card-footer bg-transparent d-flex justify-content-between">
                    <button class="btn btn-sm btn-outline-primary" data-action="edit" data-cocktail-id="${id}">
                        <i class="fas fa-edit me-1"></i> Editar
                    </button>
                    <button class="btn btn-sm btn-outline-danger" data-action="delete" data-item-type="cocktail" data-item-id="${id}" data-item-name="${name}">
                        <i class="fas fa-trash me-1"></i> Eliminar
                    </button>
                </div>
            </div>
        `;

        // Añadir event listeners para los botones
        const editBtn = this.querySelector('[data-action="edit"]');
        if (editBtn) {
            editBtn.addEventListener('click', () => {
                this.dispatchEvent(new CustomEvent('editCocktail', {
                    detail: { id: id },
                    bubbles: true
                }));
            });
        }

        const deleteBtn = this.querySelector('[data-action="delete"]');
        if (deleteBtn) {
            deleteBtn.addEventListener('click', () => {
                this.dispatchEvent(new CustomEvent('deleteCocktail', {
                    detail: { id: id, name: name },
                    bubbles: true
                }));
            });
        }
    }
}

// Registrar el componente personalizado
customElements.define('cocktail-card', CocktailCard);