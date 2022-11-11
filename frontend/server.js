const http = require('http')
const fs = require('fs').promises;

const HOST = 'localhost'
const PORT = 3000

const redirectToFeed = (req, res) => {
  res.writeHead(302, { 'Location': '/feed' });
  res.end();
}

const serveFeed = (req, res) => {
  fs.readFile(__dirname + "/feed.html")
    .then(contents => {
      res.writeHead(200);
      res.end(contents);
    })
}

const serveRegister = (req, res) => {
  fs.readFile(__dirname + "/register.html")
    .then(contents => {
      res.writeHead(200);
      res.end(contents);
    })
}

const serveLogin = (req, res) => {
  fs.readFile(__dirname + "/login.html")
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