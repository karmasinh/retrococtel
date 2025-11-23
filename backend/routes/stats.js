const express = require('express')
const router = express.Router()
const c = require('../controllers/statsController')
const auth = require('../middleware/auth')

router.get('/top-ingredients', auth, c.topIngredients)
router.get('/top-cocktails', auth, c.topCocktails)
router.get('/user-preferences', auth, c.userPreferences)
router.get('/cocktails-per-day', auth, c.cocktailsPerDay)
router.get('/ingredient-usage', auth, c.ingredientUsage)
router.get('/tags', auth, c.tagsList)
router.get('/top-bases', auth, c.topBases)
router.get('/users-count', auth, c.usersCount)

module.exports = router
