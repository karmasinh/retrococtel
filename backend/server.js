require('dotenv').config()
const express = require('express')
const cors = require('cors')
const path = require('path')
const sequelize = require('./config/database')
const models = require('./models')

const app = express()
app.use(cors())
app.use(express.json())
app.use('/', express.static(path.join(__dirname, '..')))
app.use('/pages', express.static(path.join(__dirname, '..', 'pages')))
app.use('/frontend', express.static(path.join(__dirname, '..', 'frontend')))

app.use('/api/auth', require('./routes/auth'))
app.use('/api/cocktails', require('./routes/cocktails'))
app.use('/api/preferences', require('./routes/preferences'))
app.use('/api/ingredients', require('./routes/ingredients'))
app.use('/api/stats', require('./routes/stats'))
app.use('/api/users', require('./routes/users'))
app.use('/api/roles', require('./routes/roles'))

app.get('/health', (req, res) => res.json({ ok: true }))

const portEnv = parseInt(process.env.PORT || '3000', 10)

function startServer(startPort) {
  const server = app.listen(startPort, () => {
    console.log(`Servidor en puerto ${startPort}`)
  })
  server.on('error', (err) => {
    if (err.code === 'EADDRINUSE') {
      const next = startPort + 1
      if (next <= startPort + 5) {
        console.warn(`Puerto ${startPort} en uso, intentando ${next}...`)
        startServer(next)
      } else {
        console.error('No se encontró puerto disponible')
        process.exit(1)
      }
    } else {
      console.error('Error del servidor', err)
      process.exit(1)
    }
  })
}

app.get('/', (req, res) => res.redirect('/pages/index.html'))

sequelize.authenticate()
  .then(() => { console.log('DB conectada') })
  .catch(err => { console.error('Error de conexión DB', err) })
  .finally(() => { startServer(portEnv) })
