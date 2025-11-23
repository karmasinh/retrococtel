module.exports = (sequelize, DataTypes) => {
  return sequelize.define('user_favorites', {
    id: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true },
    user_id: { type: DataTypes.INTEGER, allowNull: false },
    cocktail_id: { type: DataTypes.INTEGER, allowNull: false },
    created_at: { type: DataTypes.DATE }
  })
}
