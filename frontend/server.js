const http = require('http')
const fs = require('fs').promises;

const HOST = 'localhost'
const PORT = 3000
const PAGES_DIR = __dirname + '/pages'

const redirectToFeed = (req, res) => {
  res.writeHead(302, { 'Location': '/feed' });
  res.end();
}

const serveStatic = (req, res) => {
  fs.readFile(__dirname + req.url)
    .then(contents => {
      res.writeHead(200);
      res.end(contents);
    })
    .catch(err => {
      res.writeHead(404);
      res.end(JSON.stringify(err))
    })
}

const serveFeed = (req, res) => {
  fs.readFile(PAGES_DIR + "/feed.html")
    .then(contents => {
      res.writeHead(200);
      res.end(contents);
    })
}

const serveRegister = (req, res) => {
  fs.readFile(PAGES_DIR + "/register.html")
    .then(contents => {
      res.writeHead(200);
      res.end(contents);
    })
}

const serveLogin = (req, res) => {
  fs.readFile(PAGES_DIR + "/login.html")
    .then(contents => {
      res.writeHead(200);
      res.end(contents);
    })
}

const serve404 = (req, res) => {
  res.writeHead(404)
  res.end('<html><body><h1>404</h1></body></html>')
}

const router = (req, res) => {
  // always return html
  res.setHeader("Content-Type", "text/html");

  // handle requests for static files
  if (req.url.length > 7 && req.url.substring(0, 7) === '/static') {
    return serveStatic(req, res)
  }

  // handle routes
  switch (req.url) {
    case '/':
      redirectToFeed(req, res);
      break
    case '/feed':
      serveFeed(req, res)
      break
    case '/register':
      serveRegister(req, res)
      break
    case '/login':
      serveLogin(req, res)
      break
    default:
      serve404(req, res)
  }
}

const server = http.createServer(router)
server.listen(PORT, HOST, () => console.log(`server running on http://${HOST}:${PORT}`))