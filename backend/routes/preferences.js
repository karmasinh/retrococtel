const express = require('express')
const router = express.Router()
const controller = require('../controllers/preferenceController')
const auth = require('../middleware/auth')

router.get('/', auth, controller.getPreferences)
router.post('/', auth, controller.updatePreferences)

module.exports = router
