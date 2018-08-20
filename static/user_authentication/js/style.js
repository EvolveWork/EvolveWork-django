// $(function () {
//
//     $('#register_and_checkout_form').submit(function(){
//        var form = this;
//        var card = {
//            number: $('#credit_card_number').val(),
//            expiration_month: $('#expiration_month').val(),
//            expiration_year: $('#expiration_year').val(),
//            security_code: $('#security_code').val()
//        };
//
//        Stripe.createToken(card, function(status, response) {
//            if (status === 200) {
//                console.log((status, response));
//                $('#credit_card_errors').hide();
//                $('#id_stripe_id').val(response.id);
//                form.submit();
//            } else {
//                $('#stripe_error_message').text(response.error.message);
//                $('#credit_card_errors').show();
//                $('#user_submit').attr('disabled', false);
//            }
//        });
//        return false;
//     });
//
//
// });

var stripe = Stripe('pk_test_poCxJ09VXydXW4HdXO25miXw');

// Create an instance of Elements.
var elements = stripe.elements();

// Custom styling can be passed to options when creating an Element.
// (Note that this demo uses a wider set of styles than the guide below.)
var style = {
  base: {
    color: '#32325d',
    lineHeight: '18px',
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: 'antialiased',
    fontSize: '16px',
    '::placeholder': {
      color: '#aab7c4'
    }
  },
  invalid: {
    color: '#fa755a',
    iconColor: '#fa755a'
  }
};

// Create an instance of the card Element.
var card = elements.create('card', {style: style});

// Add an instance of the card Element into the `card-element` <div>.
card.mount('#card-element');

// Handle real-time validation errors from the card Element.
card.addEventListener('change', function(event) {
  var displayError = document.getElementById('card-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = '';
  }
});

// Handle form submission.
var form = document.getElementById('payment-form');
form.addEventListener('submit', function(event) {
  event.preventDefault();

  stripe.createToken(card).then(function(result) {
    if (result.error) {
      // Inform the user if there was an error.
      var errorElement = document.getElementById('card-errors');
      errorElement.textContent = result.error.message;
    } else {
      // Send the token to your server.
      stripeTokenHandler(result.token);
    }
  });
});
