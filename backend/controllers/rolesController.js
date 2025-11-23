const { Role } = require('../models')

exports.list = async (req, res) => {
  try {
    const rows = await Role.findAll()
    res.json(rows)
  } catch (e) { res.status(500).json({ message: 'Error' }) }
}

exports.create = async (req, res) => {
  try {
    const d = req.body || {}
    const r = await Role.create({ name: d.name, description: d.description || '', permissions: d.permissions || {}, created_at: new Date(), updated_at: new Date() })
    res.json({ id: r.id })
  } catch (e) { res.status(500).json({ message: 'Error' }) }
}

exports.update = async (req, res) => {
  try {
    const id = parseInt(req.params.id, 10)
    const d = req.body || {}
    const r = await Role.findByPk(id)
    if (!r) return res.status(404).json({ message: 'No encontrado' })
    await r.update({ name: d.name, description: d.description, permissions: d.permissions, updated_at: new Date() })
    res.json({ success: true })
  } catch (e) { res.status(500).json({ message: 'Error' }) }
}

exports.remove = async (req, res) => {
  try {
    const id = parseInt(req.params.id, 10)
    await Role.destroy({ where: { id } })
    res.json({ success: true })
  } catch (e) { res.status(500).json({ message: 'Error' }) }
}
