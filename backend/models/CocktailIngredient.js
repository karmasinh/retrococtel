module.exports = (sequelize, DataTypes) => {
  return sequelize.define('cocktail_ingredients', {
    id: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true },
    cocktail_id: { type: DataTypes.INTEGER, allowNull: false },
    ingredient_id: { type: DataTypes.INTEGER, allowNull: false },
    amount: { type: DataTypes.DECIMAL(8,2), allowNull: false },
    unit: { type: DataTypes.STRING(20), allowNull: false },
    note: { type: DataTypes.TEXT },
    order_index: { type: DataTypes.INTEGER, defaultValue: 0 }
  })
}
