module.exports = (sequelize, DataTypes) => {
  return sequelize.define('cocktail_steps', {
    id: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true },
    cocktail_id: { type: DataTypes.INTEGER, allowNull: false },
    step_number: { type: DataTypes.INTEGER, allowNull: false },
    instruction: { type: DataTypes.TEXT, allowNull: false }
  })
}
