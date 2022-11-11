// this is the login button click handler copy this into a <script> tag in the login html and attach it to the login button

const PORT = 8000

const login = (e) => {
  e.preventDefault();
  const email = document.getElementById('PUT_EMAIL_ID_HERE').value;
  const password = document.getElementById('PUT_PASSWORD_ID_HERE').value;
  const payload = { email, password }

  return fetch(`http://localhost:${PORT}/api/auth`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
    .then(res => {
      if (res.ok) window.location = '/feed'
      else res.text().then(text => console.error(text))
    })
    .catch(error => console.error(error));
}