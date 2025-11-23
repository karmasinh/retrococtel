module.exports = (sequelize, DataTypes) => {
  return sequelize.define('roles', {
    id: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true },
    name: { type: DataTypes.STRING(50), unique: true, allowNull: false },
    description: { type: DataTypes.TEXT },
    permissions: { type: DataTypes.JSON },
    created_at: { type: DataTypes.DATE },
    updated_at: { type: DataTypes.DATE }
  })
}
