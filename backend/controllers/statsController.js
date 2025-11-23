const { sequelize, CocktailIngredient, Ingredient, Cocktail, User, UserPreference, CocktailCategory, CocktailTag, UserFavorite, UserHistory } = require('../models')
const { Op } = require('sequelize')

exports.topIngredients = async (req, res) => {
  try {
    const rows = await CocktailIngredient.findAll({
      attributes: ['ingredient_id', [sequelize.fn('COUNT', sequelize.col('ingredient_id')), 'count']],
      group: ['ingredient_id'],
      order: [[sequelize.literal('count'), 'DESC']],
      limit: 10,
      include: [{ model: Ingredient, attributes: ['name'] }]
    })
    res.json(rows)
  } catch (e) { res.status(500).json({ message: 'Error' }) }
}

exports.topCocktails = async (req, res) => {
  try {
    const rows = await UserFavorite.findAll({
      attributes: ['cocktail_id', [sequelize.fn('COUNT', sequelize.col('cocktail_id')), 'count']],
      group: ['cocktail_id'],
      order: [[sequelize.literal('count'), 'DESC']],
      limit: 10,
      include: [{ model: Cocktail, attributes: ['name', 'slug'] }]
    })
    res.json(rows)
  } catch (e) { res.status(500).json({ message: 'Error' }) }
}

exports.userPreferences = async (req, res) => {
  try {
    const prefs = await UserPreference.findAll()
    const agg = { Sweet: 0, Citrus: 0, Fresh: 0, Bitter: 0, Dry: 0, Fruity: 0, Herbal: 0, Spicy: 0 }
    prefs.forEach(p => {
      if (p.prefers_sweet) agg.Sweet++
      if (p.prefers_citrus) agg.Citrus++
      if (p.prefers_bitter) agg.Bitter++
      if (p.prefers_strong) agg.Dry++
      if (p.prefers_low_abv) agg.Fresh++
    })
    res.json(agg)
  } catch (e) { res.status(500).json({ message: 'Error' }) }
}

exports.cocktailsPerDay = async (req, res) => {
  try {
    const rows = await Cocktail.findAll({
      attributes: [[sequelize.fn('DATE', sequelize.col('created_at')), 'day'], [sequelize.fn('COUNT', '*'), 'count']],
      group: ['day'],
      order: [['day', 'ASC']]
    })
    res.json(rows)
  } catch (e) { res.status(500).json({ message: 'Error' }) }
}

exports.ingredientUsage = async (req, res) => {
  try {
    const rows = await CocktailIngredient.findAll({
      attributes: ['ingredient_id', [sequelize.fn('COUNT', sequelize.col('ingredient_id')), 'count']],
      group: ['ingredient_id'],
      include: [{ model: Ingredient, attributes: ['name'] }]
    })
    res.json(rows)
  } catch (e) { res.status(500).json({ message: 'Error' }) }
}

exports.tagsList = async (req, res) => {
  try {
    const rows = await CocktailTag.findAll({ attributes: [[sequelize.fn('DISTINCT', sequelize.col('tag')), 'tag']] })
    res.json(rows.map(r => r.get('tag')))
  } catch (e) { res.status(500).json({ message: 'Error' }) }
}

exports.topBases = async (req, res) => {
  try {
    const { CocktailBase, sequelize } = require('../models')
    const rows = await CocktailBase.findAll({
      attributes: ['base', [sequelize.fn('COUNT', sequelize.col('base')), 'count']],
      group: ['base'],
      order: [[sequelize.literal('count'), 'DESC']],
      limit: 10
    })
    res.json(rows)
  } catch (e) { res.status(500).json({ message: 'Error' }) }
}

exports.usersCount = async (req, res) => {
  try {
    const { User } = require('../models')
    const count = await User.count()
    res.json({ count })
  } catch (e) { res.status(500).json({ message: 'Error' }) }
}
