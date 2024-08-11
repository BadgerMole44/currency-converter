# Description: Acts as a server by using python zeroMQ to revieve requests from clients. When a resquest is revieved the currency is converted as
# specified by the request and then returned. Invalid requests prompt a usage return. 
import time, zmq, random, re, json
# Prompts 
def help_txt() -> str:   
    prompt = "# ------------------------------ #\nhelp - currencyConverterServer\n curriencies - Currencies that the application can convert from/too. Specifies the spelling. Example if currencies returns usd then specify usd and not $ in arguments.\n amount currency1 currency2 - Amount: Must be decimal value to the hundredths place. Currency1: The currency associated with amount. Currency2: The currency the amount is converted too.\nConversion reply: The reply will be a string. The first part will be the decimal value of the conversion to the hundredths place and the second will be the currency the value represents.\n# ------------------------------ #"
    return prompt 
def currencies_txt() -> str:
    currencies = get_currencies()
    prompt = f"# ------------------------------ #\ncurrencies - currencyConverterServer\n{json.dumps(currencies, indent=4)}\n# ------------------------------ #"
    return prompt
def usage_txt() -> str:
    prompt = "# ------------------------------ #\nInvalid Usage.\ncurrencyConverterServer Usage:\nhelp - See help txt.\ncurrencies - See avalible currencies and hardcoded exchange rates.\nAmount currency1 currency2 - converts the amount from currency1 to curency2.\n# ------------------------------ #"
    return prompt
# Currency and conversions 
def get_currencies() -> list:
    currencies = {
        'USD':{'EURO': .91, 'GBP': .78, 'YEN': 144.05},
        'EURO':{'USD': 1.10, 'GBP': .86, 'YEN': 157.84},
        'GBP':{'USD': 1.28, 'EURO': 1.17, 'YEN': 184.03},
        'YEN':{'USD': .0069, 'EURO': .0063, 'GBP': .0054}
    }
    return currencies
def convert(val: int, pre_currency: str, post_currency: str) -> str:
    currencies = get_currencies()
    exchange_rate = currencies[pre_currency.upper()][post_currency.upper()]
    converted = round(val * exchange_rate, 2)
    converted = format(converted, ".2f")
    return f"{converted} {post_currency}"
# Server 
if __name__ == "__main__":
    context = zmq.Context()                # sets up env for socket creation
    socket = context.socket(zmq.REP)       # specifies the reply socket
    socket.bind("tcp://*:5570")            # where the socket will listen on the network port
    print('Starting Server...')
    running = True
    while running:
        req = socket.recv()
        input_message = req.decode()
        print(f"Received request from the client: {input_message}")
        if input_message.lower() == 'help':
            socket.send_string(help_txt())
        elif input_message.lower() == "currencies":
            socket.send_string(currencies_txt())
        elif len(input_message) > 0:
            args = input_message.split()
            if len(args) == 3:
                p = r'^-?\d*(?:\.\d{0,2})?$'
                currencies = get_currencies()
                if re.match(p, args[0]) and args[1].upper() in currencies and args[2].upper() in currencies:
                    converted = convert(float(args[0]), args[1].upper(), args[2].upper())
                    socket.send_string(converted)
                else:
                    socket.send_string(usage_txt())
            else:
                socket.send_string(usage_txt()) 
        else:
            socket.send_string(usage_txt())
    print("Closing Server...")
    context.destroy()