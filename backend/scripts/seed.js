require('dotenv').config()
const bcrypt = require('bcrypt')
const { sequelize, User, Role } = require('../models')

async function ensureRole(name, id) {
  const [role] = await Role.findOrCreate({ where: { id }, defaults: { id, name, description: `${name} role`, permissions: {} } })
  return role
}

async function ensureUser({ full_name, username, email, password, role_id }) {
  const existing = await User.findOne({ where: { username } })
  if (existing) return existing
  const hash = await bcrypt.hash(password, 10)
  return User.create({ full_name, username, email, password_hash: hash, role_id, status: 'Activo', created_at: new Date(), updated_at: new Date() })
}

async function run() {
  try {
    await sequelize.authenticate()
    console.log('DB OK')
    await ensureRole('Administrador', 1)
    await ensureRole('Bartender', 2)
    await ensureRole('Mixólogo', 3)
    await ensureRole('Usuario', 4)

    const u = await ensureUser({ full_name: 'Karma Admin', username: 'karma', email: 'karma@coctelmatch.com', password: '12345', role_id: 1 })
    console.log('Usuario sembrado:', u.username)
    process.exit(0)
  } catch (e) {
    console.error('Error en seed', e)
    process.exit(1)
  }
}

run()
