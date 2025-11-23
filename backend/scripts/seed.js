require('dotenv').config()
const bcrypt = require('bcrypt')
const { sequelize, Role, User, Ingredient, Cocktail, CocktailCategory, CocktailIngredient, UserPreference } = require('../models')

async function run() {
  try {
    await sequelize.authenticate()
    console.log('Conectado a MySQL')

    const [role] = await Role.findOrCreate({
      where: { name: 'Admin' },
      defaults: { description: 'Administrador', permissions: {} }
    })

    const adminPassword = process.env.SEED_ADMIN_PASSWORD || 'admin123'
    const password_hash = await bcrypt.hash(adminPassword, 10)
    const [user] = await User.findOrCreate({
      where: { username: 'admin' },
      defaults: { full_name: 'Administrador', email: 'admin@example.com', password_hash, role_id: role.id, status: 'Activo' }
    })

    const [ingredient] = await Ingredient.findOrCreate({
      where: { name: 'Jugo de Naranja' },
      defaults: { category: 'Jugo', unit_default: 'ml', calories_per_unit: 0, abv: 0 }
    })

    const [cocktail] = await Cocktail.findOrCreate({
      where: { slug: 'margarita-demo' },
      defaults: {
        name: 'Margarita Demo',
        slug: 'margarita-demo',
        short_description: 'Cóctel de ejemplo cítrico y refrescante',
        long_description: 'Una margarita de demostración para probar recomendaciones.',
        glass_type: 'Copa Margarita',
        method: 'Shaken',
        prep_time_minutes: 3,
        servings: 1,
        difficulty: 'Fácil',
        calories: 180,
        is_published: true,
        created_by: user.id
      }
    })

    await CocktailCategory.findOrCreate({
      where: { cocktail_id: cocktail.id, category: 'Refrescante' },
      defaults: { cocktail_id: cocktail.id, category: 'Refrescante' }
    })

    await CocktailIngredient.findOrCreate({
      where: { cocktail_id: cocktail.id, ingredient_id: ingredient.id },
      defaults: { cocktail_id: cocktail.id, ingredient_id: ingredient.id, amount: 30, unit: 'ml', note: 'zumo fresco', order_index: 1 }
    })

    await UserPreference.findOrCreate({
      where: { user_id: user.id },
      defaults: {
        user_id: user.id,
        prefers_citrus: true,
        preferred_categories: ['Refrescante'],
        preferred_ingredients: ['Jugo de Naranja']
      }
    })

    console.log('Seed completado')
    process.exit(0)
  } catch (e) {
    console.error('Error en seed:', e)
    process.exit(1)
  }
}

run()
