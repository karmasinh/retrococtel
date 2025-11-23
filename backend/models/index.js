const Sequelize = require('sequelize')
const sequelize = require('../config/database')

const db = {}

db.Sequelize = Sequelize
db.sequelize = sequelize

db.Role = require('./Role')(sequelize, Sequelize.DataTypes)
db.User = require('./User')(sequelize, Sequelize.DataTypes)
db.Ingredient = require('./Ingredient')(sequelize, Sequelize.DataTypes)
db.Cocktail = require('./Cocktail')(sequelize, Sequelize.DataTypes)
db.CocktailIngredient = require('./CocktailIngredient')(sequelize, Sequelize.DataTypes)
db.CocktailStep = require('./CocktailStep')(sequelize, Sequelize.DataTypes)
db.CocktailImage = require('./CocktailImage')(sequelize, Sequelize.DataTypes)
db.CocktailCategory = require('./CocktailCategory')(sequelize, Sequelize.DataTypes)
db.CocktailTag = require('./CocktailTag')(sequelize, Sequelize.DataTypes)
db.CocktailBase = require('./CocktailBase')(sequelize, Sequelize.DataTypes)
db.CocktailAromatic = require('./CocktailAromatic')(sequelize, Sequelize.DataTypes)
db.CocktailGarnish = require('./CocktailGarnish')(sequelize, Sequelize.DataTypes)
db.CocktailEffect = require('./CocktailEffect')(sequelize, Sequelize.DataTypes)
db.UserPreference = require('./UserPreference')(sequelize, Sequelize.DataTypes)
db.UserFavorite = require('./UserFavorite')(sequelize, Sequelize.DataTypes)
db.UserHistory = require('./UserHistory')(sequelize, Sequelize.DataTypes)

db.Role.hasMany(db.User, { foreignKey: 'role_id' })
db.User.belongsTo(db.Role, { foreignKey: 'role_id' })

db.Cocktail.hasMany(db.CocktailStep, { foreignKey: 'cocktail_id' })
db.Cocktail.hasMany(db.CocktailImage, { foreignKey: 'cocktail_id' })
db.Cocktail.hasMany(db.CocktailCategory, { foreignKey: 'cocktail_id' })
db.Cocktail.hasMany(db.CocktailTag, { foreignKey: 'cocktail_id' })
db.Cocktail.hasMany(db.CocktailBase, { foreignKey: 'cocktail_id' })
db.Cocktail.hasMany(db.CocktailAromatic, { foreignKey: 'cocktail_id' })
db.Cocktail.hasMany(db.CocktailGarnish, { foreignKey: 'cocktail_id' })
db.Cocktail.hasMany(db.CocktailEffect, { foreignKey: 'cocktail_id' })
db.Cocktail.hasMany(db.UserFavorite, { foreignKey: 'cocktail_id' })
db.Cocktail.hasMany(db.UserHistory, { foreignKey: 'cocktail_id' })

db.CocktailIngredient.belongsTo(db.Cocktail, { foreignKey: 'cocktail_id' })
db.CocktailIngredient.belongsTo(db.Ingredient, { foreignKey: 'ingredient_id' })

db.UserPreference.belongsTo(db.User, { foreignKey: 'user_id' })
db.UserFavorite.belongsTo(db.User, { foreignKey: 'user_id' })
db.UserFavorite.belongsTo(db.Cocktail, { foreignKey: 'cocktail_id' })
db.UserHistory.belongsTo(db.User, { foreignKey: 'user_id' })
db.UserHistory.belongsTo(db.Cocktail, { foreignKey: 'cocktail_id' })

module.exports = db
