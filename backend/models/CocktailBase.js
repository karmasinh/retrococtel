module.exports = (sequelize, DataTypes) => {
  return sequelize.define('cocktail_bases', {
    id: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true },
    cocktail_id: { type: DataTypes.INTEGER, allowNull: false },
    base: { type: DataTypes.STRING(50), allowNull: false }
  })
}
