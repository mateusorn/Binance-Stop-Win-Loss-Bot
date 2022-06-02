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
from termcolor import *
from pathlib import Path

public_key = "key"
private_key = "key"
client = Client(public_key, private_key, {"verify": True, "timeout": 20})

order = list(client.get_open_orders())
path = os.path.abspath(__file__)

mode = 0
while (mode < 10):
    if mode == 0:
        os.system("cls")
        print("Looking for Limit Orders on Buy side.  ", end="\r")
        sleep(1)
        print("Looking for Limit Orders on Buy side.. ", end="\r")
        sleep(1)
        print("Looking for Limit Orders on Buy side...", end="\r")
        sleep(1)
        order = list(client.get_open_orders())
        if bool(order) == True:
            orderIdOpenOrder = order[0]["orderId"]
        else:
            print(Fore.RED + "[+]" + Fore.RED + " You don't have any open orders at the moment")
            sleep(10)
            mode = 0
            break
        try:
            with open("blacklisted-ids.txt", "a") as myfile: #INSERE O ID DA TRANSAÇÃO SELL SIDE NA BLACKLIST
                myfile.write("\n" + str(orderIdOpenOrder))
        except FileNotFoundError:
            with open("blacklisted-ids.txt", "w") as myfile: #INSERE O ID DA TRANSAÇÃO SELL SIDE NA BLACKLIST
                myfile.write("\n" + str(orderIdOpenOrder))
        if bool(order) == True:
            orderIdOpenOrder = order[0]["orderId"]
            sideOpenOrder = order[0]["side"]
            print(Fore.RED + "[+]" + Fore.GREEN + " Order Found!                               " + Fore.RESET)
            mode = 1

    if mode == 1: 
        if len(order) == 1:  #SE EXISTIR APENAS UMA TRANSAÇÃO EM ABERTO                      
            sideOpenOrder = order[0]["side"] 
            orderIdOpenOrder = order[0]["orderId"]
            statusOpenOrder = order[0]["status"]
            symbolOpenOrder = order[0]["symbol"].replace("USDT", "")
            symbolOpenOrderUSD = order[0]["symbol"]
            priceOpenOrder = order[0]["price"]
            typeOpenOrder = order[0]["type"]
            quantityOpenOrder = order[0]["origQty"]
            print(Fore.RED + f"[+]" + Fore.GREEN + f" Coin/Amount: {round(float(quantityOpenOrder), 1)} {symbolOpenOrder} | Status: {statusOpenOrder} | Order ID: {orderIdOpenOrder} | Market Price: {priceOpenOrder} | Side: {sideOpenOrder} | USD Amount: {round(float(quantityOpenOrder) * float(priceOpenOrder), 2)}$" + Fore.RESET)
            
            if sideOpenOrder == "BUY":
                with open('blacklisted-ids.txt') as f:
                    lines = f.readlines()
                especialorderIdOpenOrder = str(orderIdOpenOrder) + "\n"
                if especialorderIdOpenOrder in lines:
                    print(Fore.RED + "[+]" + Fore.RED + f" Transaction {orderIdOpenOrder} already blacklisted..." + Fore.RESET)
                    mode = 0
                else:
                    print(Fore.RED + "[+]" + Fore.BLUE + f" Starting bot..." + Fore.RESET)
                    with open(f"buy_order.txt", "w") as buytransaction: #INSE
                        buytransaction.write(str(orderIdOpenOrder) + "\n" + symbolOpenOrderUSD)
                    with open("blacklisted-ids.txt", "a") as myfile: #INSERE O ID DA TRANSAÇÃO SELL SIDE NA BLACKLIST
                        myfile.write("\n" + str(orderIdOpenOrder))
                    path_run = path.replace("main.py", "")
                    os.system(f'cd "{path_run}" && start run.py')
                    
                    print("\n" +Fore.RED + "[+]" + Fore.RED + f" Looking for new transactions in 60 seconds..." + Fore.RESET)
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
                print(Fore.RED + "[+]" + Fore.GREEN + f" We found a transaction! Coin: {symbolOpenOrder} | Status: {statusOpenOrder} | Order ID: {orderIdOpenOrder} | Price: {priceOpenOrder}" + Fore.RESET)
                print(Fore.RED + "[+]" + Fore.RED + " Unhapply isn't in there a lot that this bot can do, since It isn't a Buy Order, but I'm going to register this transaction and it will be ignored next time...")
                with open("blacklisted-ids.txt", "a") as myfile: #INSERE O ID DA TRANSAÇÃO SELL SIDE NA BLACKLIST
                    myfile.write("\n" + orderIdOpenOrder)
                mode = 0 #RETORNA PARA O COMEÇO
                sleep(10)
                
        elif len(order) > 1: #SE EXISTIR MAIS DE 1 UMA TRANSAÇÃO ABERTA, FAÇA:
            order = list(client.get_open_orders())
            os.system("cls")
            print(Fore.RED + "[+]" + Fore.GREEN + f" {len(order)} open orders, filtering by [Limit Order - Buy Side]..." + Fore.RESET)
            print(Fore.RED + "[+]" + Fore.GREEN + f" Printing open orders..." + Fore.RESET)
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
                    print(Fore.RED + f"[{repeater+1}]" + Fore.GREEN + f" Coin/Amount: {round(float(quantityOpenOrder), 1)} {symbolOpenOrder} | Status: {statusOpenOrder} | Order ID: {orderIdOpenOrder} | Market Price: {priceOpenOrder} | Side: {sideOpenOrder} | USD Amount: {round(float(quantityOpenOrder) * float(priceOpenOrder), 2)}$" + Fore.RESET)
                else:
                    print(Fore.RED + f"[{repeater+1}]" + Fore.RED + f" Coin/Amount: {round(float(quantityOpenOrder), 1)} {symbolOpenOrder} | Status: {statusOpenOrder} | Order ID: {orderIdOpenOrder} | Market Price: {priceOpenOrder} | Side: {sideOpenOrder} | USD Amount: {round(float(quantityOpenOrder) * float(priceOpenOrder), 2)}$" + Fore.RESET)
                repeater+= 1
            print("\n") #New line to look cool
            set = 0
            while len(order) != set: #FAZ PULAR DE NÚMERO EM NÚMERO DE TRANSAÇÕES E SÓ IMPRIMI AS BUYSIDE
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
                if especialorderIdOpenOrder in lines:
                    set += 1
                    print(Fore.RED + "[+]" + Fore.RED + f" Transaction {orderIdOpenOrder} already blacklisted..." + Fore.RESET)
                    sleep(2)

                elif sideOpenOrder == "BUY":
                    print(Fore.RED + "[+]" + Fore.GREEN + f" We found a buy transaction! Coin: {symbolOpenOrder} | Status: {statusOpenOrder} | Order ID: {orderIdOpenOrder} | Price: {priceOpenOrder}" + Fore.RESET)
                    print(Fore.RED + "[+]" + Fore.BLUE + f" Starting bot..." + Fore.RESET)
                    #REGISTER ID OF THE TRANSACTION
                    #OPEN THE BOT.PY
                    #ADD THIS TRANSACTION ON BLACKLIST
                    #CHECK IF THIS SECTOR IS BLOCKING BLACKLISTED TRANSACTIONS EVEN IF THEY ARE BUY SIDE
                    with open(f"buy_order.txt", "w") as buytransaction: #INSE
                        buytransaction.write(str(orderIdOpenOrder) + "\n" + symbolOpenOrder)
                    with open("blacklisted-ids.txt", "a") as myfile: #INSERE O ID DA TRANSAÇÃO SELL SIDE NA BLACKLIST
                        myfile.write("\n" + str(orderIdOpenOrder))

                    path_run = path.replace("main.py", "")
                    os.system(f'cd "{path_run}" && start run.py')
                    sleep(5)
                    mode = 0
                    break
                    #OBSERVATION: I made the code break every time it find and register a buy transaction cause of a wierd bug that was making the last buy transaction be executed twice
                else:
                 with open("blacklisted-ids.txt", "a") as myfile: #INSERE O ID DA TRANSAÇÃO SELL SIDE NA BLACKLIST
                    myfile.write("\n" + str(orderIdOpenOrder).replace("\n", ""))
                    print(Fore.RED + "[+]" + Fore.RED + f" Transaction {orderIdOpenOrder} is now on blacklist..." + Fore.RESET)
                    sleep(2)
                    set += 1
            print("\n")
            print(Fore.RED + "[+]" + Fore.RED + f" Looking for new transactions in 60 seconds..." + Fore.RESET)
            sleep(60)