const express = require('express');
const mysql = require('mysql');

const app = express();
const port = 3000;
const cors = require('cors');

//  Middleware
app.use(cors());

app.use(cors({
  origin: 'http://localhost:5173'
}));

// Configurar a conexão com o banco de dados
const db = mysql.createConnection({
  host: 'localhost',
  user: 'enrell',
  password: 'enrellsa10',
  database: 'bingoo'
});

// Iniciar o servidor
app.listen(port, () => {
  console.log(`Servidor iniciado na porta ${port}`);
});

app.get('/api/search', (req, res) => {
  const keywords = req.query.keyword.split(' ');

  // Consultar o banco de dados para cada palavra-chave
  const queries = keywords.map(keyword => {
    return new Promise((resolve, reject) => {
      db.query(
        'SELECT link FROM indexed_links WHERE keyword_id IN (SELECT id FROM keyword WHERE keyword = ?)',
        [keyword],
        (error, results) => {
          if (error) {
            reject(error);
          } else {
            const links = results.map(result => result.link);
            resolve(links);
          }
        }
      );
    });
  });

  // Executar todas as consultas em paralelo
  Promise.all(queries)
    .then(results => {
      // Armazenar os links únicos em um Set
      const uniqueLinks = new Set(results.flat());

      // Converter o Set de links para um array
      const links = Array.from(uniqueLinks);

      res.json({ links });
    })
    .catch(error => {
      console.error(error);
      res.status(500).json({ error: 'Erro ao consultar o banco de dados' });
    });
});
