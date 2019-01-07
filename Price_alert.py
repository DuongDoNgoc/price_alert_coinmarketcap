import json
import time
import pandas as pd
import requests     # for crawling data API
import pyttsx3   # for speech engine, require to install pywin32 module : pip/pip3 install pywin32   
from win10toast import ToastNotifier    # push notification to windows
notification_pusher = ToastNotifier()

df = pd.read_csv('Coins.csv', usecols = ['Symbol', 'Up', 'Down'])
df = df.to_json()
df = json.loads(df)

# reload data from json
symbols = df['Symbol']
Up_limits = df['Up']
Down_limits = df['Down']

# reload data from string
symbols = [symbols[x] for x in symbols]
Up_limits = [1000000 if Up_limits[x] is None else float(Up_limits[x]) for x in Up_limits]
Down_limits = [0 if Down_limits[x] is None else float(Down_limits[x]) for x in Down_limits]

current_price = [0] * len(symbols)
symbols_id = [0 for x in range(len(symbols))]

# get symbols_id of coins
api = 'https://api.coinmarketcap.com/v2/listings/'
data = requests.get(api).json()['data']
for currency in data :
    if currency['name'] in symbols:
        symbols_id[symbols.index(currency['name'])] = currency['id']

# get current_price of coins from symbols_id
api = 'https://api.coinmarketcap.com/v2/ticker/'
engine = pyttsx3.init();
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 25)

def printing_alert():
    while True:
        message = ""
        for index, symbol in enumerate(symbols):
            temp_api = api + str(symbols_id[index])
            data = requests.get(temp_api).json()
            current_price[index] = float(data['data']['quotes']['USD']['price'])  # get current_prince

            if current_price[index] > Up_limits[index]:
                #speak_alert("Alert ! The %-5s price is %.2f, higher than upper limit threshold %.2f" %(symbols[index], current_price[index], Up_limits[index]))
                msg = "%-6s price is %.2f; " %(symbols[index], current_price[index])
                #notification_pusher.show_toast("Price Alert", msg, duration=3,threaded=True)
                message += msg
            if current_price[index] < Down_limits[index]:
                #speak_alert("Alert ! The %-5s price is %.2f, lower than lower limit threshold %.2f" %(symbols[index], current_price[index], Down_limits[index]))
                msg = "%-6s price is %.2f; " %(symbols[index], current_price[index])
                #notification_pusher.show_toast("Price Alert", msg)
                message += msg
        #print(message)
        notification_pusher.show_toast("Price Alert",message, duration=20, threaded=True)
        time.sleep(600) # repeat a after 300s

def speak_alert(message):
    print(message)
    engine.say(message)
    engine.runAndWait()

printing_alert()

