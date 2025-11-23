module.exports = (sequelize, DataTypes) => {
  return sequelize.define('cocktail_images', {
    id: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true },
    cocktail_id: { type: DataTypes.INTEGER, allowNull: false },
    image_url: { type: DataTypes.STRING(255), allowNull: false },
    order_index: { type: DataTypes.INTEGER, defaultValue: 0 },
    is_primary: { type: DataTypes.BOOLEAN, defaultValue: false }
  })
}
