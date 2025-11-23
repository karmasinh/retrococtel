const express = require('express')
const router = express.Router()
const controller = require('../controllers/cocktailController')
const auth = require('../middleware/auth')

router.get('/', auth, controller.list)

module.exports = router
