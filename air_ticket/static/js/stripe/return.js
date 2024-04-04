initialize();

async function initialize() {
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  const sessionId = urlParams.get('session_id');
  const url = `http://${domain}/orders/session-status/?session_id=${sessionId}`
  const response = await fetch(url);
  const session = await response.json();

  if (session.status == 'open') {
    window.replace(`http://${domain}/orders/checkout`)
  } else if (session.status == 'complete') {
    document.getElementById('success').classList.remove('hidden');
  }
}