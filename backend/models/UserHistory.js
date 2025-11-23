module.exports = (sequelize, DataTypes) => {
  return sequelize.define('user_history', {
    id: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true },
    user_id: { type: DataTypes.INTEGER, allowNull: false },
    cocktail_id: { type: DataTypes.INTEGER, allowNull: false },
    action: { type: DataTypes.ENUM('view','create','prepare'), allowNull: false },
    created_at: { type: DataTypes.DATE }
  })
}
