const state = { cocktails: [], selectedIngredients: [], selectedFlavors: [] }

const FLAVORS = ["Sweet","Citrus","Fresh","Bitter","Dry","Fruity","Herbal","Spicy"]

function debounce(fn, wait){ let t; return (...args)=>{ clearTimeout(t); t=setTimeout(()=>fn(...args), wait) } }

function renderFlavorFilters(tags){ const list = tags && tags.length ? tags : FLAVORS; const el = document.getElementById('flavorFilters'); el.innerHTML=''; list.forEach(tag=>{ const b=document.createElement('button'); b.className='btn btn-outline-primary btn-sm animate__animated animate__fadeIn'; b.textContent=tag; b.onclick=()=>{ const i=state.selectedFlavors.indexOf(tag); if(i>=0){ state.selectedFlavors.splice(i,1); b.classList.remove('active') } else { state.selectedFlavors.push(tag); b.classList.add('active') } renderResults() }; el.appendChild(b) }) }

function addIngredientChip(name){ if(state.selectedIngredients.includes(name)) return; state.selectedIngredients.push(name); const el = document.getElementById('selectedIngredients'); const chip = document.createElement('span'); chip.className='badge bg-secondary animate__animated animate__zoomIn'; chip.textContent=name; chip.onclick=()=>{ const i=state.selectedIngredients.indexOf(name); if(i>=0) state.selectedIngredients.splice(i,1); chip.remove(); renderResults() }; el.appendChild(chip); renderResults() }

function renderSuggestions(items){ const s = document.getElementById('suggestions'); s.innerHTML=''; items.forEach(it=>{ const a=document.createElement('a'); a.className='list-group-item list-group-item-action'; a.textContent=it.name; a.onclick=()=>{ addIngredientChip(it.name); s.innerHTML='' }; s.appendChild(a) }) }

function scoreCocktail(c){ let score=0; const ingMatch = state.selectedIngredients.filter(n=> c.ingredientsNames && c.ingredientsNames.includes(n)).length; score+=ingMatch*2; const flavorMatch = state.selectedFlavors.filter(t=> c.tags && c.tags.includes(t)).length; score+=flavorMatch; return score }

function filterCocktails(){ const ing = state.selectedIngredients; const flv = state.selectedFlavors; return state.cocktails.filter(c=>{ const ingOk = ing.every(n=> c.ingredientsNames && c.ingredientsNames.includes(n)); const flavorOk = flv.length===0 || flv.some(t=> c.tags && c.tags.includes(t)); return ingOk && flavorOk }) }

function renderResults(){ const list = filterCocktails().sort((a,b)=> scoreCocktail(b)-scoreCocktail(a)); const el = document.getElementById('results'); el.innerHTML=''; list.forEach(c=>{ const col=document.createElement('div'); col.className='col-md-4'; const card=document.createElement('div'); card.className='card h-100 animate__animated animate__fadeInUp'; const body=document.createElement('div'); body.className='card-body'; const h=document.createElement('h5'); h.className='card-title'; h.textContent=c.name; const p=document.createElement('p'); p.className='card-text'; p.textContent=(c.short_description||''); body.appendChild(h); body.appendChild(p); card.appendChild(body); col.appendChild(card); el.appendChild(col) }) }

async function enrichCocktails(raw){ return Promise.all(raw.map(async c=>{ const ings = await window.apiClient.request(`/cocktails/${c.id}/ingredients`).catch(()=>[]); const tags = await window.apiClient.getTags().catch(()=>[]); return { ...c, ingredientsNames: (ings||[]).map(x=> x.Ingredient ? x.Ingredient.name : x.name).filter(Boolean), tags } })) }

async function init(){ const token = localStorage.getItem('authToken'); if(!token){ window.location.href='../pages/login.html'; return } const input = document.getElementById('ingredientInput'); const onType = debounce(async ()=>{ const q=input.value.trim(); if(!q){ document.getElementById('suggestions').innerHTML=''; return } const items = await window.apiClient.searchIngredients(q).catch(()=>[]); renderSuggestions(items) },300); input.addEventListener('input', onType); const raw = await window.apiClient.getCocktails().catch(()=>[]); state.cocktails = raw; try { const tags = await window.apiClient.getTags(); renderFlavorFilters(tags) } catch { renderFlavorFilters(FLAVORS) } renderResults() }

document.addEventListener('DOMContentLoaded', init)
