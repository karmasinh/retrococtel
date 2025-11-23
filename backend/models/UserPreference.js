module.exports = (sequelize, DataTypes) => {
  return sequelize.define('user_preferences', {
    id: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true },
    user_id: { type: DataTypes.INTEGER, allowNull: false },
    prefers_sweet: { type: DataTypes.BOOLEAN },
    prefers_bitter: { type: DataTypes.BOOLEAN },
    prefers_citrus: { type: DataTypes.BOOLEAN },
    prefers_strong: { type: DataTypes.BOOLEAN },
    prefers_low_abv: { type: DataTypes.BOOLEAN },
    preferred_categories: { type: DataTypes.JSON },
    preferred_ingredients: { type: DataTypes.JSON },
    updated_at: { type: DataTypes.DATE }
  })
}
