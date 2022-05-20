from decimal import Decimal
import json
import os
import secrets
import sys
from time import sleep
from types import NoneType
from binance.client import Client
from binance import BinanceSocketManager
from binance.enums import *
from numpy import empty
from colorama import *
from termcolor import *

client = Client("brp2Txdw2Hspn1I8JGzJaIWgOfwfqX6Ad89Om4W5X0IxyBbgfDH6T5Af8vCg1lGE", "ZGybd3qYnHRcvmdQlJbzierxeZuK7TCx7C4DoEi1CbGZIV8SOlTWHlSwkDTvlX2z", {"verify": True, "timeout": 20})

stop_loss = 0.9962 #-0,38% Stop Loss
stop_gain = 1.0225 #2,25% Stop Gain
order = list(client.get_open_orders())

# To Do List
# - Black List Order Ids
# - Ignore Certain Transactions

mode = 0

#def create_oco(oco_id,oco_buy_price): 
#    create = client.create_oco_order(
#    symbol=symbolOpenOrder_last,
#    side=SIDE_SELL,
#    stopLimitTimeInForce=TIME_IN_FORCE_GTC,
#    quantity=real_free_balance,
#    stopPrice=str(stopLossprice),
#    stopLimitPrice=str(stopLimitprice),
#    price=str(stopGainprice))
#    print(oco_id)
#    print(oco_buy_price)
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
        orderIdOpenOrder = order[0]["orderId"]
        with open('blacklisted-ids.txt') as f:
            lines = f.readlines()
        if bool(order) == True:
            orderIdOpenOrder = order[0]["orderId"]
            sideOpenOrder = order[0]["side"]
            print(Fore.RED + "[+]" + Fore.GREEN + " Order Found!                               " + Fore.RESET)
            mode = 1
            
            
            
            
    if mode == 1: 
        if len(order) == 1:                         # SE HOUVER APENAS UMA TRANSAÇÃO EM ABERTO
            orderIdOpenOrder = order[0]["orderId"]  # SOLICITA O SIDE DA TRANSAÇÃO
            if sideOpenOrder != "BUY":              # SE A TRANSAÇÃO NÃO FOR DO BUY SIDE   
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
            os.system("cls")
            print(Fore.RED + "[+]" + Fore.GREEN + f" {len(order)} open orders, filtering by [Limit Order - Buy Side]..." + Fore.RESET)
            print(Fore.RED + "[+]" + Fore.GREEN + f" Printing open orders..." + Fore.RESET)
            
            repeater = 0
            while len(order) != repeater:
                sideOpenOrder = order[repeater]["side"] 
                orderIdOpenOrder = order[repeater]["orderId"]
                statusOpenOrder = order[repeater]["status"]
                symbolOpenOrder = order[repeater]["symbol"].replace("USDT", "")
                priceOpenOrder = order[repeater]["price"]
                typeOpenOrder = order[repeater]["type"]
                quantityOpenOrder = order[repeater]["origQty"]
                print(Fore.RED + f"[{repeater+1}]" + Fore.GREEN + f" Coin/Amount: {round(float(quantityOpenOrder), 1)} {symbolOpenOrder} | Status: {statusOpenOrder} | Order ID: {orderIdOpenOrder} | Market Price: {priceOpenOrder} | Side: {sideOpenOrder} | USD Amount: {round(float(quantityOpenOrder) * float(priceOpenOrder), 2)}$" + Fore.RESET)
                repeater+= 1
            
            
            
            
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
                    #create_oco(orderIdOpenOrder, priceOpenOrder)
                    sleep(2)
                    
                    
                    
                else:
                 with open("blacklisted-ids.txt", "a") as myfile: #INSERE O ID DA TRANSAÇÃO SELL SIDE NA BLACKLIST
                    myfile.write("\n" + str(orderIdOpenOrder).replace("\n", ""))
                    print(Fore.RED + "[+]" + Fore.RED + f" Transaction {orderIdOpenOrder} is now on blacklist..." + Fore.RESET)
                    sleep(2)
                    set += 1
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
        else: #CASO NÃO HAJA ORDENS ABERTAS
            print(Fore.RED + "[+]" + Fore.RED + "No Limit Order")
            sleep(5)
            mode = 0
            
        #WIERD DATA SHIT
        #print(order)
        #print(type(order))
        #print(orderIdOpenOrder)
        #print(sideOpenOrder)
        #print(len(order))
        #print(f"FIRST POSITION: {order[0]}")
        #print(f"SECOND POSITION: {order[1]}")        