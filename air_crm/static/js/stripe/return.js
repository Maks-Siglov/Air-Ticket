
initialize();

async function initialize() {
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  const sessionId = urlParams.get('session_id');
  const url = `http://localhost:8000/orders/session-status?session_id=${sessionId}`
  const response = await fetch(url);
  const session = await response.json();

  console.log(session.status)

  if (session.status == 'open') {
    window.replace('http://localhost:8000/orders/checkout')
  } else if (session.status == 'complete') {
    document.getElementById('success').classList.remove('hidden');
    document.getElementById('customer-email').textContent = session.customer_email
  }
}