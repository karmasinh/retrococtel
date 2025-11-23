const { User, sequelize } = require('../models')
const jwt = require('jsonwebtoken')
const bcrypt = require('bcrypt')

exports.login = async (req, res) => {
  try {
    const { username, email, password } = req.body
    const where = {}
    const isEmailInput = username && username.includes('@') && !email
    if (isEmailInput) where.email = username
    else {
      if (username) where.username = username
      if (email) where.email = email
    }
    let user = await User.findOne({ where })
    if (!user) {
      const [rows] = await sequelize.query(
        'SELECT * FROM users WHERE username = :u OR email = :u LIMIT 1',
        { replacements: { u: username || email || '' } }
      )
      if (rows && rows.length) user = rows[0]
    }
    if (!user) return res.status(401).json({ message: 'Credenciales inválidas' })
    const hash = user.password_hash || ''
    const ok = await bcrypt.compare(password || '', hash)
    if (!ok) return res.status(401).json({ message: 'Credenciales inválidas' })
    const roleId = user.role_id || user.rol_id || null
    const uname = user.username || user.nombre_usuario
    const token = jwt.sign({ id: user.id, username: uname, role_id: roleId }, process.env.JWT_SECRET || 'devsecret', { expiresIn: '7d' })
    res.json({ token })
  } catch (e) {
    res.status(500).json({ message: 'Error de autenticación' })
  }
}
