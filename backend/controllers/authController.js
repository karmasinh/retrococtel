const { User, sequelize } = require('../models');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');

exports.login = async (req, res) => {
  try {
    const { username, email, password } = req.body;

    // Normalización de entrada (aceptar username o email en el mismo campo)
    const identifier = username || email;
    if (!identifier || !password) {
      return res.status(400).json({ message: 'Faltan datos' });
    }

    // Construcción dinámica del WHERE
    const where = {};
    if (identifier.includes('@')) where.email = identifier;
    else where.username = identifier;

    // 1) Buscar por ORM (siempre es preferible)
    let user = await User.findOne({ where });

    // 2) Si falla, fallback con query cruda normalizada
    if (!user) {
      const [rows] = await sequelize.query(
        `
        SELECT 
          id,
          full_name,
          username,
          email,
          password_hash,
          role_id,
          status,
          created_at,
          updated_at
        FROM users 
        WHERE username = :id OR email = :id
        LIMIT 1
        `,
        { replacements: { id: identifier } }
      );

      if (rows && rows.length > 0) {
        // Normalizar para que tenga exactamente los mismos keys que el modelo Sequelize
        user = {
          id: rows[0].id,
          full_name: rows[0].full_name,
          username: rows[0].username,
          email: rows[0].email,
          password_hash: rows[0].password_hash,
          role_id: rows[0].role_id,
          status: rows[0].status
        };
      }
    }

    // Si no existe el usuario
    if (!user) {
      return res.status(401).json({ message: 'Credenciales inválidas' });
    }

    // Verificación de contraseña
    const hash =
      user.password_hash ||
      user.password ||
      user.contrasena_hash ||
      '';

    const ok = await bcrypt.compare(password, hash);
    if (!ok) {
      return res.status(401).json({ message: 'Credenciales inválidas' });
    }

    // Token JWT
    const token = jwt.sign(
      {
        id: user.id,
        username: user.username,
        role_id: user.role_id
      },
      process.env.JWT_SECRET || 'devsecret',
      { expiresIn: '7d' }
    );

    return res.json({ token });

  } catch (err) {
    console.error('Login error:', err);
    return res.status(500).json({ message: 'Error de autenticación' });
  }
};
