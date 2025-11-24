const { Ingredient } = require('../models');
const { Op } = require('sequelize');

exports.search = async (req, res) => {
  try {
    const q = (req.query.search || '').trim();
    const where = q ? { name: { [Op.like]: `%${q}%` } } : {};
    const limit = parseInt(req.query.limit || '20', 10);
    const items = await Ingredient.findAll({ where, limit });
    res.json(items);
  } catch (e) {
    console.error(e);
    res.status(500).json({ message: 'Error al buscar ingredientes' });
  }
};
