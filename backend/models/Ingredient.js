module.exports = (sequelize, DataTypes) => {
  return sequelize.define('ingredients', {
    id: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true },
    name: { type: DataTypes.STRING(100), allowNull: false },
    category: { type: DataTypes.ENUM('Alcohol','Jugo','Endulzante','Hierba','Refresco','Licor','Condimento','Básico','Fruta','Verdura','Especia','Otro'), allowNull: false },
    unit_default: { type: DataTypes.STRING(20), allowNull: false },
    calories_per_unit: { type: DataTypes.DECIMAL(6,2) },
    abv: { type: DataTypes.DECIMAL(5,2), defaultValue: 0 },
    effects: { type: DataTypes.JSON },
    stock: { type: DataTypes.DECIMAL(10,2) },
    reorder_threshold: { type: DataTypes.DECIMAL(10,2) },
    created_at: { type: DataTypes.DATE },
    updated_at: { type: DataTypes.DATE }
  })
}
