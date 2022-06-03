import json
import os
import secrets
import sys
from time import sleep
from types import NoneType
from binance.client import Client
from binance import BinanceSocketManager
from binance.enums import *
from colorama import *
from termcolor import *

decimals = 3 #Amount of numbers after the , - Example: "0.003"
stopgain = float(1.03) #Example = float(1.30) [When the coin go 30% up it will sell]
stoploss = float(0.98) #Example = float(0.90) [If the price of the currency drops by 10% from the moment you buy, it will be sold as a stop loss.]
public_key  = "KEY"
private_key = "KEY"
client = Client(public_key, private_key, {"verify": True, "timeout": 20})

try:
    with open('buy_order.txt') as f:
        lines = f.readlines()

except FileNotFoundError:
    os.system("cls")
    print(Fore.GREEN + "[3]" + Fore.RED + f" Apparently the file that I'm looking for doesn't exists.  ", end="\r")
    sleep(1.5)
    print(Fore.YELLOW + "[2]" + Fore.RED + f" Apparently the file that I'm looking for doesn't exists.. ", end="\r")
    sleep(1.5)
    print(Fore.RED + "[1]" + Fore.RED + f" Apparently the file that I'm looking for doesn't exists...", end="\r")
    sleep(1.5)
    os.system("cls")
    print(Fore.RED + "[+]" + Fore.RED + f" Message: This message still appearing probably because you're running this python manually, this part of the code only will work propely when It's runned by main.py, if the error keeps appearing, delete all txts files generated by this code and run main.py again.")
    print(Fore.RED + "[+]" + Fore.RED + f" Please close this console")
    sleep(18000)

symbol = lines[1]
orderid = lines[0]
order = list(client.get_all_orders(symbol=str(symbol), orderId=int(orderid)))
sideOpenOrder = order[0]["side"] 
statusOpenOrder = order[0]["status"]
priceOpenOrder = order[0]["price"]
typeOpenOrder = order[0]["type"]
quantityOpenOrder = order[0]["origQty"]
f.close()

if sideOpenOrder == "BUY": #Just to make sure that the order is really BUY side
    while statusOpenOrder == "NEW":
        print(Fore.RED + f"[+]" + Fore.GREEN + f" Coin/Amount: {float(quantityOpenOrder)} {symbol} | Status: {statusOpenOrder} | Order ID: {orderid} | Market Price: {priceOpenOrder} | Side: {sideOpenOrder} | USD Amount: {round(float(quantityOpenOrder) * float(priceOpenOrder), 2)}$" + Fore.RESET)
        print("\n")
        print(Fore.RED + "\n[+]" + Fore.GREEN + " Waiting until the order get filled   ", end="\r")
        sleep(2)
        print(Fore.RED + "[+]" + Fore.GREEN + " Waiting until the order get filled.  ", end="\r")
        sleep(2)
        print(Fore.RED + "[+]" + Fore.GREEN + " Waiting until the order get filled.. ", end="\r")
        sleep(2)
        print(Fore.RED + "[+]" + Fore.GREEN + " Waiting until the order get filled...", end="\r")
        sleep(10)
        os.system("cls")
        order = list(client.get_all_orders(symbol=str(symbol), orderId=int(orderid)))
        statusOpenOrder = order[0]["status"]
        sleep(2)
        if statusOpenOrder != "NEW":
            break
    
    #WHEN THE ORDER GET FILLED!
    if statusOpenOrder == "FILLED":
        print("ORDER FILLED!")
        filtered_symbol = symbol.replace("USDT","").replace("BUSD","").replace("USDC","")
        q1 = client.get_asset_balance(asset=filtered_symbol)
        q2 = float(list(q1.values())[1])
        quantity = round((q2 * float(0.98)), 2)
        stopLossprice = round(float(priceOpenOrder) * stoploss, decimals)
        stopLimitprice = round(stopLossprice * float(0.9), decimals)
        stopGainprice = round(float(priceOpenOrder) * stopgain, decimals)

        create = client.create_oco_order(
        symbol=symbol,
        side=SIDE_SELL,
        stopLimitTimeInForce=TIME_IN_FORCE_GTC,
        quantity=round(float(quantityOpenOrder),2),
        stopPrice=str(stopLossprice),
        stopLimitPrice=str(stopLossprice),
        price=str(stopGainprice))
        print(Fore.RED + "[+]" + Fore.RED + " OCO ORDER CREATED, HERE COME SOME INFORMATIONS:")
        print(Fore.RED + "[+]" + Fore.RED + f" YOU'RE SELLING THE COIN {filtered_symbol}, YOU BOUGHT AT {priceOpenOrder}$, NOW THE COIN IS GOING TO BE SELLED AT {stopGainPrice}$ - If it reachs the stop gain - OR SELLED AT {stopLossPrice} - If it break on StopLoss!")
        sleep(100000)
    else:
        exit()
else:
    print(Fore.RED + "[+]" + Fore.RED + " Error SELL SIDE")
    

