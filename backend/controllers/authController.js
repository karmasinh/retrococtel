const { User } = require('../models')
const jwt = require('jsonwebtoken')
const bcrypt = require('bcrypt')

exports.login = async (req, res) => {
  try {
    const { username, email, password } = req.body
    const where = {}
    if (username) where.username = username
    if (email) where.email = email
    const user = await User.findOne({ where })
    if (!user) return res.status(401).json({ message: 'Credenciales inválidas' })
    const ok = await bcrypt.compare(password || '', user.password_hash || '')
    if (!ok) return res.status(401).json({ message: 'Credenciales inválidas' })
    const token = jwt.sign({ id: user.id, username: user.username, role_id: user.role_id }, process.env.JWT_SECRET || 'devsecret', { expiresIn: '7d' })
    res.json({ token })
  } catch (e) {
    res.status(500).json({ message: 'Error de autenticación' })
  }
}
