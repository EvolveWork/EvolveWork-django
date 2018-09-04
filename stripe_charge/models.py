from stripe import Customer, Token
from stripe.error import CardError
from stripe.util import convert_to_stripe_object


class MockCustomer(Customer):
    @classmethod
    def create(cls, api_key=None, idempotency_key=None,
               stripe_account=None, **params):

        if params['card']['number'] != '4242424242424242':
            raise CardError('Invalid card number', None, 402)

        response = {
            "id": "cus_DXrGtyphP6ciCz",
            "object": "customer",
            "account_balance": 0,
            "created": 1536094499,
            "currency": "usd",
            "default_source": None,
            "delinquent": False,
            "description": None,
            "discount": None,
            "email": None,
            "invoice_prefix": "55CB6C8",
            "livemode": False,
            "metadata": {
            },
            "shipping": None,
            "sources": {
                "object": "list",
                "data": [

                ],
                "has_more": False,
                "total_count": 0,
                "url": "/v1/customers/cus_DXrGtyphP6ciCz/sources"
            },
            "subscriptions": {
                "object": "list",
                "data": [

                ],
                "has_more": False,
                "total_count": 0,
                "url": "/v1/customers/cus_DXrGtyphP6ciCz/subscriptions"
            },
            "tax_info": None,
            "tax_info_verification": None
        }
        return convert_to_stripe_object(response, api_key, stripe_account)


class MockToken(Token):
    @classmethod
    def create(cls, api_key=None, idempotency_key=None,
               stripe_account=None, **params):
        if params['card']['number'] != '4242424242424242':
            raise CardError('Invalid card number', None, 402)
        response = {
            "card": {
              "address_city": None,
              "address_country": None,
              "address_line1": None,
              "address_line1_check": None,
              "address_line2": None,
              "address_state": None,
              "address_zip": None,
              "address_zip_check": None,
              "brand": "Visa",
              "country": "US",
              "cvc_check": "unchecked",
              "dynamic_last4": None,
              "exp_month": 12,
              "exp_year": 2017,
              "fingerprint": "49gS1c4YhLaGEQbj",
              "funding": "credit",
              "id": "card_17XXdZGzvyST06Z022EiG1zt",
              "last4": "4242",
              "metadata": {},
              "name": None,
              "object": "card",
              "tokenization_method": None
          },
            "client_ip": "192.168.1.1",
            "created": 1453817861,
            "id": "tok_42XXdZGzvyST06Z0LA6h5gJp",
            "livemode": False,
            "object": "token",
            "type": "card",
            "used": False
        }
        return convert_to_stripe_object(response, api_key, stripe_account)