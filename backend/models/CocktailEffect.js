module.exports = (sequelize, DataTypes) => {
  return sequelize.define('cocktail_effects', {
    id: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true },
    cocktail_id: { type: DataTypes.INTEGER, allowNull: false },
    effect: { type: DataTypes.STRING(50), allowNull: false }
  })
}
