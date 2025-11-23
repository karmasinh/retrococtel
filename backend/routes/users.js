const router = require('express').Router()
const auth = require('../middleware/auth')
const c = require('../controllers/usersController')

router.get('/', auth, c.list)
router.post('/', auth, c.create)
router.put('/:id', auth, c.update)
router.delete('/:id', auth, c.remove)

module.exports = router
