from zeep import Client

# Create a Zeep client for the SOAP service
client = Client('http://localhost:8000/?wsdl')

# Prompt user for input
amount = float(input("Enter amount to convert: "))
#from_currency = input("Enter source currency: ").upper()
to_currency = input("Enter target currency: ").upper()

# Call the 'convert_currency' method of the service
response = client.service.convert_currency(amount, "USD", to_currency)

# Print the response from the server
print(f"{amount} USD equals {response} {to_currency}")

