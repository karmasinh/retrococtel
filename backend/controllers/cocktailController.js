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

    const cocktails = await Cocktail.findAll({ where, include })
    res.json(cocktails)
  } catch (e) {
    res.status(500).json({ message: 'Error al listar cócteles' })
  }
}
