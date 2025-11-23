// Componente CardMetric para mostrar métricas en el dashboard
class CardMetric extends HTMLElement {
    constructor() {
        super();
    }

    connectedCallback() {
        this.render();
    }

    static get observedAttributes() {
        return ['value', 'label', 'icon', 'trend', 'trend-value'];
    }

    attributeChangedCallback(name, oldValue, newValue) {
        if (oldValue !== newValue) {
            this.render();
        }
    }

    render() {
        const value = this.getAttribute('value') || '0';
        const label = this.getAttribute('label') || 'Métrica';
        const icon = this.getAttribute('icon') || 'fa-chart-line';
        const trend = this.getAttribute('trend') || 'neutral';
        const trendValue = this.getAttribute('trend-value') || '';

        let trendIcon = '';
        let trendClass = '';

        if (trend === 'up') {
            trendIcon = 'fa-arrow-up';
            trendClass = 'text-success';
        } else if (trend === 'down') {
            trendIcon = 'fa-arrow-down';
            trendClass = 'text-danger';
        }

        this.innerHTML = `
            <div class="card card-metric h-100">
                <div class="metric-icon">
                    <i class="fas ${icon}"></i>
                </div>
                <h3 class="metric-value">${value}</h3>
                <p class="metric-label">${label}</p>
                ${trend !== 'neutral' ? `
                    <div class="metric-trend ${trendClass}">
                        <i class="fas ${trendIcon} me-1"></i>
                        ${trendValue}
                    </div>
                ` : ''}
            </div>
        `;
    }
}

// Registrar el componente personalizado
customElements.define('card-metric', CardMetric);