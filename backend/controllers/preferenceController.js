const { UserPreference } = require('../models')

exports.getPreferences = async (req, res) => {
  try {
    const pref = await UserPreference.findOne({ where: { user_id: req.user.id } })
    res.json(pref || {})
  } catch (e) {
    res.status(500).json({ message: 'Error al obtener preferencias' })
  }
}

exports.updatePreferences = async (req, res) => {
  try {
    const [pref] = await UserPreference.findOrCreate({ where: { user_id: req.user.id }, defaults: req.body })
    await pref.update(req.body)
    res.json({ success: true, pref })
  } catch (e) {
    res.status(500).json({ message: 'Error al actualizar preferencias' })
  }
}
