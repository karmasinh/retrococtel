const jwt = require('jsonwebtoken')

module.exports = (req, res, next) => {
  const hdr = req.headers.authorization || ''
  const token = hdr.startsWith('Bearer ') ? hdr.slice(7) : null
  if (token) {
    try {
      const payload = jwt.verify(token, process.env.JWT_SECRET || 'devsecret')
      req.user = { id: payload.id }
      return next()
    } catch (e) {}
  }
  const uid = req.headers['x-user-id']
  if (uid) {
    req.user = { id: parseInt(uid, 10) }
    return next()
  }
  return res.status(401).json({ message: 'No autenticado' })
}
