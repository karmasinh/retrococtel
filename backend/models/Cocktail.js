module.exports = (sequelize, DataTypes) => {
  return sequelize.define('cocktails', {
    id: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true },
    name: { type: DataTypes.STRING(100), allowNull: false },
    slug: { type: DataTypes.STRING(100), unique: true, allowNull: false },
    short_description: { type: DataTypes.TEXT },
    long_description: { type: DataTypes.TEXT },
    glass_type: { type: DataTypes.STRING(50) },
    method: { type: DataTypes.ENUM('Shaken','Stirred','Muddled','Blended','Built','Layered') },
    prep_time_minutes: { type: DataTypes.INTEGER },
    servings: { type: DataTypes.INTEGER, defaultValue: 1 },
    difficulty: { type: DataTypes.ENUM('Fácil','Moderado','Avanzado') },
    calories: { type: DataTypes.INTEGER },
    is_published: { type: DataTypes.BOOLEAN, defaultValue: false },
    created_by: { type: DataTypes.INTEGER },
    created_at: { type: DataTypes.DATE },
    updated_at: { type: DataTypes.DATE }
  })
}
