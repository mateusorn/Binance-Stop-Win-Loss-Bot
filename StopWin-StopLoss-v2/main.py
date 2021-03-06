from decimal import Decimal
import json
import os
import secrets
import sys
from time import sleep
from binance.client import Client
from binance import BinanceSocketManager
from binance.enums import *
from colorama import *
from pathlib import Path

#Hi, I recorded a video about this bot, here is the link:
#Remember, when you are working with cryptocurrencies you need to stay aware all the time, the market can change insanely, this bot can help you
#but It don't mean that you can forget about your money, if you lose your money, It's not my problem.
#we have a lot of sleep timer on this code cause binance sucks, if you make a lot of requests in a short amount of time, they'are you going to stop your application, then i set up this timers, it make the code works fine watching 3 orders at the same time
#Advice: This bot isn't made to make super fast transactions, the bot just start watching the coin when a new console open showing the informations about the coin that you wanna buy, If you create a order and it get instantly filled, example: "If you wanna to buy a crypto for 12$ and it costs 12.01$, the order probably is going to get filled instatly and the chances of the bot capture the transaction is super low, so, create limit open order to get filled inside a time of 1 minute or more.

with open(r'config.json') as f:
    config = json.load(f)

client = Client(config['public_api'], config['private_api'], {"verify": True, "timeout": 100}) #Request from Binance informations about your account

order = list(client.get_open_orders()) #Get the list of open orders on your account
path = os.path.abspath(__file__) #Save the path where this code is running for later usage

def register(orderIdOpenOrder):
    try:
        with open("blacklisted-ids.txt", "a") as myfile: #BLACKLIST
            myfile.write("\n" + str(orderIdOpenOrder))
    except FileNotFoundError:
        with open("blacklisted-ids.txt", "w") as myfile: #BLACKLIST
            myfile.write("\n" + str(orderIdOpenOrder))

mode = 0
while (mode < 10):
    if mode == 0:
        os.system("cls")
        print(Fore.YELLOW + "[+]" + Fore.WHITE + " Looking for Limit Orders on Buy side.  ", end="\r")
        sleep(1)
        print(Fore.YELLOW + "[+]" + Fore.WHITE + " Looking for Limit Orders on Buy side.. ", end="\r")
        sleep(1)
        print(Fore.YELLOW + "[+]" + Fore.WHITE + " Looking for Limit Orders on Buy side...", end="\r")
        sleep(1)
        order = list(client.get_open_orders()) #Get the list of open orders on your account
        if bool(order) == True: #Check if is in there any open order, asking if the list "order' is empty or not
            orderIdOpenOrder = order[0]["orderId"]
            register(orderIdOpenOrder)
        else:
            print(Fore.YELLOW + "[+]" + Fore.WHITE + " You don't have any open orders at the moment")
            sleep(10)
            mode = 0
            break
        if bool(order) == True:
            orderIdOpenOrder = order[0]["orderId"]
            register(orderIdOpenOrder)
            sideOpenOrder = order[0]["side"]
            print(Fore.YELLOW + "[+]" + Fore.WHITE + " An order was found!                               \n" + Fore.RESET)
            mode = 1

    if mode == 1: 
        if len(order) == 1:  #asks if the amount of open orders is 1.                    
            sideOpenOrder = order[0]["side"] 
            orderIdOpenOrder = order[0]["orderId"]
            statusOpenOrder = order[0]["status"]
            symbolOpenOrder = order[0]["symbol"].replace("USDT", "")
            symbolOpenOrderUSD = order[0]["symbol"]
            priceOpenOrder = order[0]["price"]
            typeOpenOrder = order[0]["type"]
            quantityOpenOrder = order[0]["origQty"]
            print(Fore.RED + f"[ORDER]" + Fore.WHITE + f" Coin/Amount: {round(float(quantityOpenOrder), 1)} {symbolOpenOrder} | Status: {statusOpenOrder} | Order ID: {orderIdOpenOrder} | Market Price: {round(float(priceOpenOrder),2)}$ | Side:"+Fore.RED+f" {sideOpenOrder} "+Fore.WHITE+f"| USD Amount: {round(float(quantityOpenOrder) * float(priceOpenOrder), 2)}$\n" + Fore.RESET) #print informations about the order, if it existis
            
            if sideOpenOrder == "BUY": #check if the order is on buy side
                with open('blacklisted-ids.txt') as f:
                    lines = f.readlines()
                especialorderIdOpenOrder = str(orderIdOpenOrder) + "\n"
                if especialorderIdOpenOrder in lines:
                    print(Fore.YELLOW + "[+]" + Fore.WHITE + f" Transaction {orderIdOpenOrder} already blacklisted..." + Fore.RESET)
                    mode = 0
                else:
                    print(Fore.RED + "\n[+]" + Fore.RED + f" Starting bot..." + Fore.RESET)
                    with open(f"buy_order.txt", "w") as buytransaction: #register in the transaction in the buy list, this number is going to be used later by the run.py
                        buytransaction.write(str(orderIdOpenOrder) + "\n" + symbolOpenOrderUSD)
                    register(orderIdOpenOrder) #REGISTER ON BLACKLIST
                    path_run = path.replace("main.py", "")
                    os.system(f'cd "{path_run}" && start run.py')
                    
                    print("\n" +Fore.YELLOW + "[+]" + Fore.WHITE + f" Looking for new transactions in 60 seconds..." + Fore.RESET)
                    sleep(60)
                    mode = 0

            else: 
                sideOpenOrder = order[0]["side"] 
                orderIdOpenOrder = order[0]["orderId"]
                statusOpenOrder = order[0]["status"]
                symbolOpenOrder = order[0]["symbol"]
                priceOpenOrder = order[0]["price"]
                typeOpenOrder = order[0]["type"]
                quantityOpenOrder = order[0]["origQty"]
                print(Fore.YELLOW + "[+]" + Fore.RED + " Unhapply isn't in there a lot that this bot can do, since It isn't a Buy Order, but I'm going to register this transaction and it will be ignored next time...")
                register(orderIdOpenOrder) #REGISTER ON BLACKLIST
                print("\n" +Fore.YELLOW + "[+]" + Fore.WHITE + f" Looking for new transactions in 20 seconds..." + Fore.RESET)
                sleep(20)
                mode = 0
                
        elif len(order) > 1: #IF IS IN THERE MORE THAN ONE TRANSACTION, DO
            order = list(client.get_open_orders())
            os.system("cls")
            print(Fore.YELLOW + "[+]" + Fore.WHITE + f" {len(order)} open orders, filtering by [Limit Order - Buy Side]..." + Fore.RESET)
            print(Fore.YELLOW + "[+]" + Fore.WHITE + f" Printing open orders..." + Fore.RESET)
            print("\n") #New line to look cool
            repeater = 0 #PRINT INFORMATIONS ABOUT EVERY OPEN ORDER, BUY AND SELL SIDE
            while len(order) != repeater:
                sideOpenOrder = order[repeater]["side"] 
                orderIdOpenOrder = order[repeater]["orderId"]
                statusOpenOrder = order[repeater]["status"]
                symbolOpenOrder = order[repeater]["symbol"].replace("USDT", "")
                priceOpenOrder = order[repeater]["price"]
                typeOpenOrder = order[repeater]["type"]
                quantityOpenOrder = order[repeater]["origQty"]
                if sideOpenOrder == "BUY":
                    sleep(0.5)
                    print(Fore.YELLOW + f"[ORDER {repeater+1}]" + Fore.WHITE + f" Coin/Amount: {round(float(quantityOpenOrder), 1)} {symbolOpenOrder} | Status: {statusOpenOrder} | Order ID: {orderIdOpenOrder} | Market Price: {round(float(priceOpenOrder),2)}$ | Side:"+Fore.GREEN+f" {sideOpenOrder} "+Fore.WHITE+f"| USD Amount: {round(float(quantityOpenOrder) * float(priceOpenOrder), 2)}$" + Fore.RESET)
                else:
                    sleep(0.5)
                    print(Fore.YELLOW + f"[ORDER {repeater+1}]" + Fore.WHITE + f" Coin/Amount: {round(float(quantityOpenOrder), 1)} {symbolOpenOrder} | Status: {statusOpenOrder} | Order ID: {orderIdOpenOrder} | Market Price: {round(float(priceOpenOrder),2)}$ | Side:"+Fore.RED+f" {sideOpenOrder} "+Fore.WHITE+f"| USD Amount: {round(float(quantityOpenOrder) * float(priceOpenOrder), 2)}$" + Fore.RESET)
                repeater+= 1
            print("\n") #New line to look cool
            set = 0
            while len(order) != set: #Jump transaction buy transaction and check if the transaction is buy or sell side, if it is a sell side one, the order is going to be blacklisted and ignored next time the code look for new transactions
                sideOpenOrder = order[set]["side"] 
                orderIdOpenOrder = order[set]["orderId"]
                statusOpenOrder = order[set]["status"]
                symbolOpenOrder = order[set]["symbol"]
                priceOpenOrder = order[set]["price"]
                typeOpenOrder = order[set]["type"]
                quantityOpenOrder = order[set]["origQty"]
                with open('blacklisted-ids.txt') as f:
                    lines = f.readlines()
                especialorderIdOpenOrder = str(orderIdOpenOrder) + "\n"
                if especialorderIdOpenOrder in lines: #Check if the transaction is arealdy blacklisted
                    set += 1
                    print(Fore.YELLOW + "[+]" + Fore.WHITE + f" Transaction {orderIdOpenOrder} already blacklisted..." + Fore.RESET)
                    sleep(2)

                    #IF THE ORDER IS A VALID BUY SIDE ONE:
                    #REGISTER ID OF THE TRANSACTION
                    #OPEN THE RUN.PY
                    #ADD THIS TRANSACTION ON BLACKLIST
                    #CHECK IF THIS SECTOR IS BLOCKING BLACKLISTED TRANSACTIONS EVEN IF THEY ARE BUY SIDE
                elif sideOpenOrder == "BUY":
                    print(Fore.YELLOW + "[+]" + Fore.WHITE + f" We found a buy transaction! Coin: {symbolOpenOrder} | Status: {statusOpenOrder} | Order ID: {orderIdOpenOrder} | Price: {priceOpenOrder}" + Fore.RESET)
                    print(Fore.RED + "\n[+]" + Fore.RED + f" Starting bot..." + Fore.RESET)
                    with open(f"buy_order.txt", "w") as buytransaction:
                        buytransaction.write(str(orderIdOpenOrder) + "\n" + symbolOpenOrder)
                    register(orderIdOpenOrder) #REGISTER ON BLACKLIST
                    path_run = path.replace("main.py", "")
                    os.system(f'cd "{path_run}" && start run.py')
                    sleep(5)
                    mode = 0
                    break
                    #OBSERVATION: I made the code break every time it find and register a buy transaction cause of a wierd bug that was making the last buy transaction be executed twice.
                else:
                    register(orderIdOpenOrder) #REGISTER ON BLACKLIST
                    print(Fore.YELLOW + "[+]" + Fore.WHITE + f" Transaction {orderIdOpenOrder} is now on blacklist..." + Fore.RESET)
                    sleep(2)
                    set += 1
            print("\n")
            print(Fore.YELLOW + "[+]" + Fore.WHITE + f" Looking for new transactions in 60 seconds..." + Fore.RESET)
            sleep(60)
            mode=0
