const { User, Role, sequelize } = require('../models')
const { Op } = require('sequelize')
const bcrypt = require('bcrypt')

exports.list = async (req, res) => {
  try {
    const q = req.query.q || ''
    const role_id = req.query.role_id ? parseInt(req.query.role_id, 10) : null
    const status = req.query.status || null
    const where = {}
    if (q) where[Op.or] = [
      { full_name: { [Op.like]: `%${q}%` } },
      { username: { [Op.like]: `%${q}%` } },
      { email: { [Op.like]: `%${q}%` } }
    ]
    if (role_id) where.role_id = role_id
    if (status) where.status = status
    const rows = await User.findAll({ where })
    const roles = await Role.findAll()
    const roleMap = Object.fromEntries(roles.map(r => [r.id, r.name]))
    const data = rows.map(u => ({
      id: u.id,
      full_name: u.full_name,
      username: u.username,
      email: u.email,
      avatar_url: u.avatar_url,
      role: roleMap[u.role_id] || String(u.role_id),
      status: u.status
    }))
    res.json(data)
  } catch (e) { res.status(500).json({ message: 'Error' }) }
}

exports.create = async (req, res) => {
  try {
    const d = req.body || {}
    const hash = await bcrypt.hash(d.password || '', 10)
    const u = await User.create({
      full_name: d.full_name,
      username: d.username,
      email: d.email,
      password_hash: hash,
      role_id: d.role_id,
      status: d.status || 'Activo',
      avatar_url: d.avatar_url || null,
      created_at: new Date(), updated_at: new Date()
    })
    res.json({ id: u.id })
  } catch (e) { res.status(500).json({ message: 'Error' }) }
}

exports.update = async (req, res) => {
  try {
    const id = parseInt(req.params.id, 10)
    const d = req.body || {}
    const u = await User.findByPk(id)
    if (!u) return res.status(404).json({ message: 'No encontrado' })
    const patch = {
      full_name: d.full_name,
      username: d.username,
      email: d.email,
      role_id: d.role_id,
      status: d.status,
      avatar_url: d.avatar_url,
      updated_at: new Date()
    }
    if (d.password) patch.password_hash = await bcrypt.hash(d.password, 10)
    await u.update(patch)
    res.json({ success: true })
  } catch (e) { res.status(500).json({ message: 'Error' }) }
}

exports.remove = async (req, res) => {
  try {
    const id = parseInt(req.params.id, 10)
    await User.destroy({ where: { id } })
    res.json({ success: true })
  } catch (e) { res.status(500).json({ message: 'Error' }) }
}
