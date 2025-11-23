require('dotenv').config()
const express = require('express')
const cors = require('cors')
const sequelize = require('./config/database')
const models = require('./models')

const app = express()
app.use(cors())
app.use(express.json())

app.use('/api/auth', require('./routes/auth'))
app.use('/api/cocktails', require('./routes/cocktails'))
app.use('/api/preferences', require('./routes/preferences'))

const port = process.env.PORT || 3000
sequelize.authenticate()
  .then(() => {
    console.log('DB conectada')
  })
  .catch(err => {
    console.error('Error de conexión DB', err)
  })
  .finally(() => {
    app.listen(port, () => console.log(`Servidor en puerto ${port}`))
  })
