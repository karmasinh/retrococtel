module.exports = (sequelize, DataTypes) => {
  return sequelize.define('cocktail_tags', {
    id: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true },
    cocktail_id: { type: DataTypes.INTEGER, allowNull: false },
    tag: { type: DataTypes.STRING(50), allowNull: false }
  })
}
