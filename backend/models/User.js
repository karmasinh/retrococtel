module.exports = (sequelize, DataTypes) => {
  const User = sequelize.define('User', {
    id: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true },
    full_name: { type: DataTypes.STRING(100), allowNull: false },
    username: { type: DataTypes.STRING(50), unique: true, allowNull: false },
    email: { type: DataTypes.STRING(100), unique: true, allowNull: false },
    password_hash: { type: DataTypes.STRING(255), allowNull: false },
    role_id: { type: DataTypes.INTEGER, allowNull: false },
    status: { type: DataTypes.ENUM('Activo', 'Inactivo'), defaultValue: 'Activo' },
    avatar_url: { type: DataTypes.STRING(255) },
    created_at: { type: DataTypes.DATE },
    updated_at: { type: DataTypes.DATE }
  }, {
    tableName: 'users',
    timestamps: false,
    underscored: true
  });

  User.associate = (models) => {
    User.belongsTo(models.Role, {
      foreignKey: 'role_id'
    });
  };

  return User;
};
