const http = require('http')
const fs = require('fs').promises;

const HOST = 'localhost'
const PORT = 3000
const PAGES_DIR = __dirname + '/pages'

const ROUTEMAP = {
  '/feed': '/feed.html',
  '/register': '/register.html',
  '/login': '/login.html',
  '/post': '/postblog.html',
  '/analysis': '/analysis.html'
}

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

const serveRoute = (req, res) => {
  const route = ROUTEMAP[req.url]
  if (!route) return serve404(req, res)

  fs.readFile(PAGES_DIR + route)
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
  if (req.url.startsWith('/static')) return serveStatic(req, res)

  // redirect to feed if no route is specified
  if (req.url === '/') return redirectToFeed(req, res)

  // handle requests for routes
  serveRoute(req, res)
}

const server = http.createServer(router)
server.listen(PORT, HOST, () => console.log(`server running on http://${HOST}:${PORT}`))