const express = require('express')
const router = express.Router()
const controller = require('../controllers/cocktailController')
const auth = require('../middleware/auth')

router.get('/', auth, controller.list)
router.get('/:id/ingredients', auth, controller.ingredientsOfCocktail)
router.get('/meta', auth, controller.meta)
router.post('/', auth, controller.create)
router.put('/:id', auth, controller.update)
router.delete('/:id', auth, controller.remove)

module.exports = router
