#importing module and libraries

import requests
import time
import json
from datetime import datetime



# In this variable we are storing link of coindesk to fetch  bitcoin price from Server

BITCOIN_API_URL = 'https://api.coindesk.com/v1/bpi/currentprice.json' #coindesk server link to get latest bitcoin price
class Bitcoin():
    def __init__(self):
        pass
    #This function is getting latest bitcoin Price
    
    def latest_bitcoin_prices(self) :
        response = requests.get(BITCOIN_API_URL)
        response_json = response.json()
        BITCOIN_PRICE = response_json["bpi"]['USD']['rate']
        BITCOIN_PRICE = BITCOIN_PRICE.replace(",", "")
        return float(BITCOIN_PRICE)
    #In this function we are sending emergency price to ifttt app
    def send_emergrncy_price_on_IFTTT_app(self,event, value) :
        data = {'value1' : value}
        IFTTT_url_for_IFTTT_app = 'https://maker.ifttt.com/trigger/{}/with/key/eO1lZip0ctU82Auuk9MHHvtrpsfVqm2APq6J8gPZoCp' #IFTTT API Link
        ifttt_event_url =  IFTTT_url_for_IFTTT_app.format(event)
        requests.post(ifttt_event_url , json = data)
    #In this function we are sending updated price to telegram messaging app
    def send_price_update_to_telegram(self,event,value):
        data = {'value1' : value}
        IFTTT_url_for_telegram_message = 'https://maker.ifttt.com/trigger/{}/with/key/eO1lZip0ctU82Auuk9MHHvtrpsfVqm2APq6J8gPZoCp'
        ifttt_event_url =  IFTTT_url_for_telegram_message.format(event)
        requests.post(ifttt_event_url , json = data)
    
    
    def format_bitcoin_history(self,bitcoin_history) :
        latest_five_bitcoin_prices = []
        for bitcoin_price in bitcoin_history :
            date = bitcoin_price['date'].strftime('%d.%m.%Y ')
            time = bitcoin_price['date'].strftime('%H:%M:%S')
            price = bitcoin_price['price']
            row = '<b> The price of Bitcoin is ${} at Time {} on Date {} </b>'.format(price, time, date)
            latest_five_bitcoin_prices.append(row)

        return '<br>'.join(latest_five_bitcoin_prices)
    
    #This is the main fuction from where execution of program starts
    
    def main(self) :
        
        #Here we are taking threshold price so that we can return our emergency price
        BITCOIN_PRICE_THRESHOLD = int(input("Enter your bitcoin price threshold value : \n"))
        bitcoin_history = []
        while True :
             price = self.latest_bitcoin_prices()
             print("Latest Bitcoin Price is :" ,price,"dollars")
             date = datetime.now()
             bitcoin_history.append({'date': date, 'price': price})
             
             if price < BITCOIN_PRICE_THRESHOLD :
                self.send_emergrncy_price_on_IFTTT_app("Bitcoin_Price_Emergency", price)
            
             if len(bitcoin_history) == 5 :
                self.send_price_update_to_telegram("bitcoin_price_update",self.format_bitcoin_history(bitcoin_history))
            # Reset the history
                bitcoin_history = []
                print("DO YOU WANT TO EXIT")
                user_input = input("Enter yes or no :\n") 
                if user_input == "yes" :
                    return
                else :
                    continue
            # Sleep for 1 seconds
             time.sleep(1)

if __name__ == "__main__":
     print("WELCOME TO BITCOIN PRICE NOTIFICATION")

     bitcoinprice = Bitcoin()
     bitcoinprice.main()

