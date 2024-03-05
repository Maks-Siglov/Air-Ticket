// This is your test publishable API key.
const stripe = Stripe("pk_test_51OfnD9A3hlBNn6LWxGxANdslhCJvuhrJ4I7oKwCaQatrZbq5rQHbwhtRJPGYVFpOdQGv2c2bSQ5F2qJ6lvMfkp6600RWXc71Fa");

initialize();
// Create a Checkout Session as soon as the page loads
async function initialize() {

  const csrftoken = getCookie('csrftoken');

  const url = "http://localhost:8000/orders/create-checkout-session/"+ticket_pk

  const response = await fetch(url, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
  });

  const { clientSecret } = await response.json();

  const checkout = await stripe.initEmbeddedCheckout({
    clientSecret,
  });

  // Mount Checkout
  checkout.mount('#checkout');
}

function getCookie(name) {
        const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
        return cookieValue ? cookieValue.pop() : '';
    }