const { Cocktail, CocktailCategory, CocktailIngredient, Ingredient, UserPreference } = require('../models')
const { Op } = require('sequelize')

exports.list = async (req, res) => {
  try {
    const where = {}
    const include = []

    if (req.query.recommended === 'true') {
      const prefs = await UserPreference.findOne({ where: { user_id: req.user.id } })
      if (prefs) {
        if (prefs.preferred_categories) {
          include.push({ model: CocktailCategory, where: { category: { [Op.in]: prefs.preferred_categories } }, required: true })
        }
        if (prefs.preferred_ingredients) {
          include.push({ model: CocktailIngredient, include: [{ model: Ingredient, where: { name: { [Op.in]: prefs.preferred_ingredients } } }], required: true })
        }
      }
    }

    const ing = req.query.ingredients
    const category = req.query.category
    const tags = req.query.tags
    const base = req.query.base
    if (category) include.push({ model: CocktailCategory, where: { category }, required: true })
    if (base) include.push({ model: require('../models').CocktailBase, where: { base }, required: true })
    if (tags) include.push({ model: require('../models').CocktailTag, where: { tag: { [Op.in]: Array.isArray(tags) ? tags : [tags] } }, required: true })
    if (ing) include.push({ model: CocktailIngredient, include: [{ model: Ingredient, where: { name: { [Op.in]: Array.isArray(ing) ? ing : [ing] } } }], required: true })

    const sort = req.query.sort
    let order = []
    if (sort === 'recent') order = [['created_at', 'DESC']]
    if (sort === 'prep_time') order = [['prep_time_minutes', 'ASC']]
    if (sort === 'difficulty') order = [['difficulty', 'ASC']]
    if (sort === 'popular') {
      const { UserFavorite } = require('../models')
      include.push({ model: UserFavorite, required: false })
      order = [[UserFavorite, 'id', 'DESC']]
    }
    const cocktails = await Cocktail.findAll({ where, include, order })
    res.json(cocktails)
  } catch (e) {
    res.status(500).json({ message: 'Error al listar cócteles' })
  }
}

exports.ingredientsOfCocktail = async (req, res) => {
  try {
    const items = await CocktailIngredient.findAll({ where: { cocktail_id: req.params.id }, include: [{ model: Ingredient }] })
    res.json(items)
  } catch (e) { res.status(500).json({ message: 'Error' }) }
}

exports.meta = async (req, res) => {
  try {
    const m = require('../models')
    const cats = await m.CocktailCategory.findAll({ attributes: [[m.sequelize.fn('DISTINCT', m.sequelize.col('category')), 'category']] })
    const bases = await m.CocktailBase.findAll({ attributes: [[m.sequelize.fn('DISTINCT', m.sequelize.col('base')), 'base']] })
    const aromas = await m.CocktailAromatic.findAll({ attributes: [[m.sequelize.fn('DISTINCT', m.sequelize.col('aromatic')), 'aromatic']] })
    const garnishes = await m.CocktailGarnish.findAll({ attributes: [[m.sequelize.fn('DISTINCT', m.sequelize.col('garnish')), 'garnish']] })
    const effects = await m.CocktailEffect.findAll({ attributes: [[m.sequelize.fn('DISTINCT', m.sequelize.col('effect')), 'effect']] })
    const tags = await m.CocktailTag.findAll({ attributes: [[m.sequelize.fn('DISTINCT', m.sequelize.col('tag')), 'tag']] })
    res.json({ categories: cats.map(x=> x.get('category')), bases: bases.map(x=> x.get('base')), aromatics: aromas.map(x=> x.get('aromatic')), garnish: garnishes.map(x=> x.get('garnish')), effects: effects.map(x=> x.get('effect')), tags: tags.map(x=> x.get('tag')) })
  } catch (e) { res.status(500).json({ message: 'Error' }) }
}

exports.create = async (req, res) => {
  try {
    const m = require('../models')
    const data = req.body || {}
    const c = await Cocktail.create({
      name: data.name,
      slug: data.slug,
      short_description: data.short_description,
      long_description: data.long_description,
      glass_type: data.glass_type,
      method: data.method,
      prep_time_minutes: data.prep_time_minutes,
      servings: data.servings,
      difficulty: data.difficulty,
      calories: data.calories,
      is_published: data.is_published,
      created_by: req.user.id
    })

    const addMany = async (Model, field, list) => {
      if (Array.isArray(list)) {
        for (const v of list) await Model.create({ cocktail_id: c.id, [field]: v })
      }
    }
    await addMany(m.CocktailCategory, 'category', data.categories)
    await addMany(m.CocktailBase, 'base', data.bases)
    await addMany(m.CocktailAromatic, 'aromatic', data.aromatics)
    await addMany(m.CocktailGarnish, 'garnish', data.garnish)
    await addMany(m.CocktailEffect, 'effect', data.effects)
    await addMany(m.CocktailTag, 'tag', data.tags)

    if (Array.isArray(data.ingredients)) {
      for (const it of data.ingredients) {
        let ingId = it.ingredient_id
        if (!ingId && it.name) {
          const ing = await Ingredient.findOne({ where: { name: it.name } })
          ingId = ing ? ing.id : null
        }
        if (ingId) await CocktailIngredient.create({ cocktail_id: c.id, ingredient_id: ingId, amount: it.amount || 0, unit: it.unit || 'ml', note: it.note || '' })
      }
    }

    res.json({ success: true, id: c.id })
  } catch (e) { res.status(500).json({ message: 'Error al crear cóctel' }) }
}

exports.update = async (req, res) => {
  try {
    const m = require('../models')
    const id = req.params.id
    const data = req.body || {}
    const c = await Cocktail.findByPk(id)
    if (!c) return res.status(404).json({ message: 'No encontrado' })
    await c.update({
      name: data.name,
      slug: data.slug,
      short_description: data.short_description,
      long_description: data.long_description,
      glass_type: data.glass_type,
      method: data.method,
      prep_time_minutes: data.prep_time_minutes,
      servings: data.servings,
      difficulty: data.difficulty,
      calories: data.calories,
      is_published: data.is_published
    })
    await m.CocktailCategory.destroy({ where: { cocktail_id: id } })
    await m.CocktailBase.destroy({ where: { cocktail_id: id } })
    await m.CocktailAromatic.destroy({ where: { cocktail_id: id } })
    await m.CocktailGarnish.destroy({ where: { cocktail_id: id } })
    await m.CocktailEffect.destroy({ where: { cocktail_id: id } })
    await m.CocktailTag.destroy({ where: { cocktail_id: id } })
    const addMany = async (Model, field, list) => { if (Array.isArray(list)) { for (const v of list) await Model.create({ cocktail_id: id, [field]: v }) } }
    await addMany(m.CocktailCategory, 'category', data.categories)
    await addMany(m.CocktailBase, 'base', data.bases)
    await addMany(m.CocktailAromatic, 'aromatic', data.aromatics)
    await addMany(m.CocktailGarnish, 'garnish', data.garnish)
    await addMany(m.CocktailEffect, 'effect', data.effects)
    await addMany(m.CocktailTag, 'tag', data.tags)
    await m.CocktailIngredient.destroy({ where: { cocktail_id: id } })
    if (Array.isArray(data.ingredients)) {
      for (const it of data.ingredients) {
        let ingId = it.ingredient_id
        if (!ingId && it.name) {
          const ing = await Ingredient.findOne({ where: { name: it.name } })
          ingId = ing ? ing.id : null
        }
        if (ingId) await m.CocktailIngredient.create({ cocktail_id: id, ingredient_id: ingId, amount: it.amount || 0, unit: it.unit || 'ml', note: it.note || '' })
      }
    }
    res.json({ success: true })
  } catch (e) { res.status(500).json({ message: 'Error al actualizar cóctel' }) }
}

exports.remove = async (req, res) => {
  try {
    const id = req.params.id
    await Cocktail.destroy({ where: { id } })
    res.json({ success: true })
  } catch (e) { res.status(500).json({ message: 'Error al eliminar cóctel' }) }
}
