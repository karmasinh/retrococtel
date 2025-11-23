const { Sequelize } = require('sequelize')

const dbName = process.env.DB_NAME || 'retrococtel'
const dbUser = process.env.DB_USER || 'root'
const dbPass = process.env.DB_PASS || 'whitecat01'
const dbHost = process.env.DB_HOST || 'localhost'
const dbPort = process.env.DB_PORT ? parseInt(process.env.DB_PORT, 10) : 3306

const sequelize = new Sequelize(dbName, dbUser, dbPass, {
  host: dbHost,
  port: dbPort,
  dialect: 'mysql',
  logging: false,
  dialectOptions: {
    charset: 'utf8mb4',
  },
  define: {
    freezeTableName: true,
    timestamps: false
  }
})

module.exports = sequelize
