const express = require('express')
const router = express.Router()
const controller = require('../controllers/ingredientController')
const auth = require('../middleware/auth')

router.get('/', auth, controller.search)

module.exports = router
