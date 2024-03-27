from spyne import Application, rpc, ServiceBase, Unicode, Float
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
import requests

class CurrencyConverterService(ServiceBase):
    @rpc(Float, Unicode, Unicode, _returns=Float)
    def convert_currency(ctx, amount, from_currency, to_currency):
        try:
            amount = float(amount)
            # Fetch latest currency conversion rates
            response = requests.get('https://cdn.jsdelivr.net/gh/ismartcoding/currency-api@main/latest/data.json')
            data = response.json()
            rates = data['quotes']
            
            # Convert currencies
            if from_currency.upper() in rates and to_currency.upper() in rates:
                converted_amount = amount * rates[to_currency.upper()] / rates[from_currency.upper()]
                return converted_amount
            else:
                return "Invalid currency code(s) provided"
        except Exception as e:
            return f"Error: {str(e)}"

if __name__ == '__main__':
    # Create the SOAP application
    soap_app = Application([CurrencyConverterService],
                           'currency_converter.soap',
                           in_protocol=Soap11(validator='lxml'),
                           out_protocol=Soap11())

    # Create WSGI application
    wsgi_application = WsgiApplication(soap_app)

    # Start the server
    server = make_server('0.0.0.0', 8000, wsgi_application)
    print("Currency Converter SOAP service serving at http://127.0.0.1:8000")
    server.serve_forever()
