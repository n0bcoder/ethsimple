from web3 import Web3
import bsett as set
import abi as key
import sys
import threading
import time
import requests
import json
from datetime import datetime 

class TINF():
    def __init__(self, token_address, pair_address, m1, m2, m3, m4, mp, symbol, sleep):
        self.w3 = self.connect()
        self.token_address = Web3.toChecksumAddress(token_address)
        self.pair = Web3.toChecksumAddress(pair_address)
        self.m1 = m1
        self.m2 = m2
        self.m3 = m3
        self.m4 = m4
        self.mp = mp
        self.p_symbol = symbol
        #sleep
        self.sleep = sleep

    def connect(self):
        nodes = set.nodes
        if bool(nodes) == False:
            print('Please input RPC/WSS url first!')
            sys.exit()
        if 'http' in nodes:
            w3 = Web3(Web3.HTTPProvider(nodes))
        else:
            w3 = Web3(Web3.WebsocketProvider(nodes))
        return w3
    
    def tcontract(self):
        trouter = self.w3.toChecksumAddress(self.token_address) 
        trouter_abi = key.sellAbi
        tcontract = self.w3.eth.contract(trouter, abi=trouter_abi)
        return tcontract
    
    def prouter(self):
        pancake_router_address = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'
        pancake_router_abi = key.pancake_router_abi
        prouter = self.w3.eth.contract(address=pancake_router_address, abi=pancake_router_abi)
        return prouter, pancake_router_address

    def t_decimals(self):
        t_decimals = 0
        try:
            calltokdecimals = self.tcontract().functions.decimals().call()
            if calltokdecimals == int(calltokdecimals):
                t_decimals = calltokdecimals
        except Exception as e:
            if 'execution reverted' in str(e):
                pass
        return t_decimals
        
    def token_info(self):
        #tokenname
        t_name = 'None'
        try:
            calltokname = self.tcontract().functions.name().call()
            if bool(calltokname) == True:
                t_name = calltokname
        except Exception as e:
            if 'execution reverted' in str(e):
                pass
        #tokendecimals
        t_decimals = 0
        try:
            calltokdecimals = self.tcontract().functions.decimals().call()
            if calltokdecimals == int(calltokdecimals):
                t_decimals = calltokdecimals
        except Exception as e:
            if 'execution reverted' in str(e):
                pass
        #tokensymbol
        t_symbol = 'None'
        try:
            calltoksysmbl = self.tcontract().functions.symbol().call()
            if calltoksysmbl == str(calltoksysmbl):
                t_symbol = calltoksysmbl
        except Exception as e:
            if 'execution reverted' in str(e):
                pass
        # max_tx_for_info
        info = self.maxtx()
        t_supply = int((info[0]) / (10**t_decimals))
        mx_tx = int((info[1]) / (10**t_decimals))
        mx_sl = int((info[2]) / (10**t_decimals))
        mx_wl = int((info[3]) / (10**t_decimals))
        # mx_tx_percent_for_info
        mx_tx_percent = float(mx_tx) / float(float(t_supply) / float(100))
        mx_sl_percent = float(mx_sl) / float(float(t_supply) / float(100))
        mx_wl_percent = float(mx_wl) / float(float(t_supply) / float(100))
        #convert_to_pair
        mx_p = 0
        ms_p = 0
        mw_p = 0
        ########
        try:
            mx_p = self.prouter()[0].functions.getAmountsOut(int(info[1]),[self.token_address, self.pair]).call()
            mx_p = self.w3.fromWei(mx_p[1],'ether')
        except Exception as e:
            if 'execution reverted' in str(e):
                pass
        try:
            ms_p = self.prouter()[0].functions.getAmountsOut(int(info[2]),[self.token_address, self.pair]).call()
            ms_p = self.w3.fromWei(ms_p[1],'ether')
        except Exception as e:
            if 'execution reverted' in str(e):
                pass
        try:
            mw_p = self.prouter()[0].functions.getAmountsOut(int(info[3]),[self.token_address, self.pair]).call()
            mw_p = self.w3.fromWei(mw_p[1],'ether')
        except Exception as e:
            if 'execution reverted' in str(e):
                pass
        return t_name, t_decimals, t_symbol, t_supply, mx_tx, mx_sl, mx_wl, mx_tx_percent, mx_sl_percent, mx_wl_percent, mx_p, ms_p, mw_p
    
    def maxtx(self):
        
        t_supply = 0
        mx_tx = 0
        mx_sl = 0
        mx_wl = 0
        #totalsupply
        try:
            callt_supply = str(self.tcontract().functions.totalSupply().call())
            if callt_supply.isdigit() == True:
                t_supply = int(callt_supply)
        except Exception as e:
            if 'execution reverted' in str(e):
                pass
        # maxtransaction
        try:
            callmx_tx = str(self.tcontract().functions._maxTxAmount().call())
            if callmx_tx.isdigit() == True:
                mx_tx = int(callmx_tx)
        except Exception as e:
            if 'execution reverted' in str(e):
                pass
        try:
            callmx_tx = str(self.tcontract().functions.maxBuyAmount().call())
            if callmx_tx.isdigit() == True:
                mx_tx = int(callmx_tx)
        except Exception as e:
            if 'execution reverted' in str(e):
                pass
        try:
            callmx_tx = str(self.tcontract().functions.maxTxAmount().call())
            if callmx_tx.isdigit() == True:
                mx_tx = int(callmx_tx)
        except Exception as e:
            if 'execution reverted' in str(e):
                pass
        try:
            callmx_tx = str(self.tcontract().functions.maxTxAmountBuy().call())
            if callmx_tx.isdigit() == True:
                mx_tx = int(callmx_tx)
        except Exception as e:
            if 'execution reverted' in str(e):
                pass
        try:
            callmx_tx = str(self.tcontract().functions.maxBuyLimit().call())
            if callmx_tx.isdigit() == True:
                mx_tx = int(callmx_tx)
        except Exception as e:
            if 'execution reverted' in str(e):
                pass
        try:
            callmx_tx = str(self.tcontract().functions._maxBuy().call())
            if callmx_tx.isdigit() == True:
                mx_tx = int(callmx_tx)
        except Exception as e:
            if 'execution reverted' in str(e):
                pass
        try:
            callmx_tx = str(self.tcontract().functions._maxBuyTxAmount().call())
            if callmx_tx.isdigit() == True:
                mx_tx = int(callmx_tx)
        except Exception as e:
            if 'execution reverted' in str(e):
                pass
        try:
            callmx_tx = str(self.tcontract().functions.maxBuyTxAmount().call())
            if callmx_tx.isdigit() == True:
                mx_tx = int(callmx_tx)
        except Exception as e:
            if 'execution reverted' in str(e):
                pass
        try:
            callmx_tx = str(self.tcontract().functions.checkMaxTxAmount().call())
            if callmx_tx.isdigit() == True:
                mx_tx = int(callmx_tx)
        except Exception as e:
            if 'execution reverted' in str(e):
                pass
        try:
            callmx_tx = str(self.tcontract().functions._getMaxTxAmount().call())
            if callmx_tx.isdigit() == True:
                mx_tx = int(callmx_tx)
        except Exception as e:
            if 'execution reverted' in str(e):
                pass
        try:
            callmx_tx = str(self.tcontract().functions.maxTransactionAmount().call())
            if callmx_tx.isdigit() == True:
                mx_tx = int(callmx_tx)
        except Exception as e:
            if 'execution reverted' in str(e):
                pass
        try:
            callmx_tx = str(self.tcontract().functions.maxSwapAmount().call())
            if callmx_tx.isdigit() == True:
                mx_tx = int(callmx_tx)
        except Exception as e:
            if 'execution reverted' in str(e):
                pass
        #maxsell
        try: 
            call_mxsl = str(self.tcontract().functions.maxSellAmount().call())
            if call_mxsl.isdigit() == True:
                mx_sl = int(call_mxsl)
        except Exception as e:
            if 'execution reverted' in str(e):
                pass
        try: 
            call_mxsl = str(self.tcontract().functions.maxSellLimit().call())
            if call_mxsl.isdigit() == True:
                mx_sl = int(call_mxsl)

        except Exception as e:
            if 'execution reverted' in str(e):
                pass    
        #maxwallet
        try: 
            call_mx_wl = str(self.tcontract().functions._walletMax().call())
            if call_mx_wl.isdigit() == True:
                mx_wl = int(call_mx_wl)
        except Exception as e:
            if 'execution reverted' in str(e):
                pass
        try: 
            call_mx_wl = str(self.tcontract().functions.maxWalletSize().call())
            if call_mx_wl.isdigit() == True:
                mx_wl = int(call_mx_wl)
        except Exception as e:
            if 'execution reverted' in str(e):
                pass
        try: 
            call_mx_wl = str(self.tcontract().functions._maxWalletToken().call())
            if call_mx_wl.isdigit() == True:
                mx_wl = int(call_mx_wl)
        except Exception as e:
            if 'execution reverted' in str(e):
                pass
        try: 
            call_mx_wl = str(self.tcontract().functions._maxWalletAmount().call())
            if call_mx_wl.isdigit() == True:
                mx_wl = int(call_mx_wl)
        except Exception as e:
            if 'execution reverted' in str(e):
                pass
        try: 
            call_mx_wl = str(self.tcontract().functions.maxWalletLimit().call())
            if call_mx_wl.isdigit() == True:
                mx_wl = int(call_mx_wl)
        except Exception as e:
            if 'execution reverted' in str(e):
                pass
        try: 
            call_mx_wl = str(self.tcontract().functions.checkMaxWalletToken().call())
            if call_mx_wl.isdigit() == True:
                mx_wl = int(call_mx_wl)
        except Exception as e:
            if 'execution reverted' in str(e):
                pass
        try: 
            call_mx_wl = str(self.tcontract().functions.maxWallet().call())
            if call_mx_wl.isdigit() == True:
                mx_wl = int(call_mx_wl)
        except Exception as e:
            if 'execution reverted' in str(e):
                pass
        try: 
            call_mx_wl = str(self.tcontract().functions._maxWalletSize().call())
            if call_mx_wl.isdigit() == True:
                mx_wl = int(call_mx_wl)
        except Exception as e:
            if 'execution reverted' in str(e):
                pass
        return t_supply, mx_tx, mx_sl, mx_wl

    def c_max_tx(self):
        t_info = self.maxtx()
        c_max_tx = 0
        if self.m1 == True or self.m2 == True:
            if self.mp == None:
                c_max = 1
            if self.mp != None:
                c_max = self.mp
            c_max_tx = int(float(t_info[0] / 100 * float(c_max)))
        #############################
        if self.m3 == True or self.m4 == True:
            #close_if_max_tx_more_than_20%
            t_big = int(t_info[0] / 100 * 20)
            c_max_tx = t_info[1]
            if c_max_tx == 0 or c_max_tx > t_big:
                print(key.CRED +'There is No Max transactions ! / Max transactions too big !'+key.RESET)
                sys.exit()
            else:
                c_max_tx = int(t_info[1])

        #maxtxconverttopairvalue
        mxp_real = c_max_tx
        mx_p = 0
        if self.m1 == True or self.m2 == True or self.m3 == True or self.m4 == True:
            mx_p = self.prouter()[0].functions.getAmountsOut(int(mxp_real),[self.token_address, self.pair]).call()
            mx_p = self.w3.fromWei(mx_p[1],'ether')

        return c_max_tx, mx_p

    def rtime_max(self):
        print('Max tx in BNB:')
        def loop():
            stop = False
            def normal():
                nonlocal stop
                while True:
                    try:
                        rtime_max = self.c_max_tx()[1]
                        print(str(rtime_max), end='\r')
                        if stop == True:
                            break
                    except KeyboardInterrupt:
                        sys.exit()
                        
                    except Exception as e:
                            continue
                normal = rtime_max
                return normal
            def get_input():
                nonlocal stop
                keystrk = input()
                stop = True
            n = threading.Thread(target=normal)
            i = threading.Thread(target=get_input) 
            n.start()
            i.start()
            n.join()
            i.join()
        loop()
        
    def gasinfo(self):
        Buygas = 0
        Sellgas = 0
        sender_address = set.account[0]
        nonce = self.w3.eth.get_transaction_count(sender_address)
        pair = self.pair
        try:
            bgascheck = self.prouter()[0].functions.swapExactETHForTokens(
            0,
            [pair,self.token_address],
            sender_address,
            (int(time.time()) + 10000)
            ).buildTransaction({
            'from': sender_address,
            'value': self.w3.toWei((set.nonimal1),'ether'),
            'gas': 30000000,
            'gasPrice': self.w3.toWei('5','gwei'),
            'nonce': nonce,
            })
            gasest = self.w3.eth.estimateGas(bgascheck)
            Buygas = gasest
        except Exception as e:
            if 'execution reverted' in str(e):
                pass
        try:
            sgascheck = self.prouter()[0].functions.swapExactETHForTokens(
            0,
            [self.token_address,pair],
            sender_address,
            (int(time.time()) + 10000)
            ).buildTransaction({
            'from': sender_address,
            'value': self.w3.toWei((set.nonimal1),'ether'),
            'gas': 3000000,
            'gasPrice': self.w3.toWei('5','gwei'),
            'nonce': nonce,
            })
            gasest = self.w3.eth.estimateGas(sgascheck)
            Sellgas = gasest
        except Exception as e:
            if 'execution reverted' in str(e):
                pass
                                  
        return Buygas, Sellgas
        

    def pricestream(self):
        t_supply = self.maxtx()[0]
        t_name = self.token_info()[0]
        symbol = self.p_symbol
        c_max = 1
        if self.mp == None:
            c_max = 1
        if self.mp != None:
            c_max = self.mp
        #current_price
        maxinp =  int(float(t_supply / 100 * float(c_max)))
        getprice = self.prouter()[0].functions.getAmountsOut(maxinp,[self.token_address, self.pair]).call()
        c_price_1 = self.w3.fromWei(getprice[1],'ether')

        while True:
            try:
                getprice = self.prouter()[0].functions.getAmountsOut(maxinp,[self.token_address, self.pair]).call()
                c_price_2 = self.w3.fromWei(getprice[1],'ether')
                time.sleep(0.7)
                if c_price_1 == c_price_2:
                    print('Name : '+key.CYELLOW+str(t_name)+key.RESET+'\n'
                    +f's price in {c_max}%:',c_price_1, symbol+'\n'
                    +f'c price in {c_max}%:',c_price_2, symbol+'\n'
                    +key.CYELLOW+'neutral'+key.RESET)
                if c_price_1 > c_price_2:
                    drop = float(c_price_1-c_price_2) / float(c_price_1 / 100)
                    print('Name : '+key.CYELLOW+str(t_name)+key.RESET+'\n'
                    +f's price in {c_max}%:',c_price_1, symbol+'\n'
                    +f'c price in {c_max}%:',c_price_2, symbol+'\n'
                    +key.CRED+f'drop {drop} %'+key.RESET)
                if c_price_1 < c_price_2:
                    gain = float(c_price_2-c_price_1) / float(c_price_1 / 100)
                    print('Name : '+key.CYELLOW+str(t_name)+key.RESET+'\n'
                    +f's price in {c_max}%:',c_price_1, symbol+'\n'
                    +f'c price in {c_max}%:',c_price_2, symbol+'\n'
                    +key.CGREEN+f'gain {gain} %'+key.RESET)
            except KeyboardInterrupt:
                sys.exit()

    def hpdotio(self):
        response = requests.get(set.honeypotdotio+self.token_address)
        TokInfo = (response.json())
        Honeypot = TokInfo['IsHoneypot']
        BuyTax = TokInfo['BuyTax']
        SellTax = TokInfo['SellTax']
        MaxTx = TokInfo['MaxTxAmount']
        try:
            if 'NoLiquidity'in TokInfo:
                MaxTx = TokInfo['MaxTxAmount']
            else:
                MaxTx = int(TokInfo['MaxTxAmount'] / (10**self.t_decimals()))
        except Exception as e:
            if 'execution reverted' in str(e):
                pass
        MaxTxinBNB = self.w3.fromWei(TokInfo['MaxTxAmountBNB'], 'ether')
        BuyGas = TokInfo['BuyGas']
        SellGas = TokInfo['SellGas']
        Error = TokInfo['Error']
        return Honeypot, BuyTax, SellTax, MaxTx, MaxTxinBNB, BuyGas, SellGas, Error
    
    def hpdotiorun(self):
        cek1 = self.hpdotio()
        print('---------------------------------'+'\n'
        +'*honeypot.is*'+'\n'
        +'---------------------------------'+'\n'
        +'Error : '+str(cek1[7])+'\n'
        +'Honeypot : '+str(cek1[0])+'\n'
        +'BuyTax : '+str(cek1[1])+' %'+'\n'
        +'SellTax : '+str(cek1[2])+' %'+'\n'
        +'MaxTx : '+str(cek1[3])+'\n'
        +'MaxTxinBNB : '+str(cek1[4])+' BNB'+'\n'
        +'BuyGas : '+str(cek1[5])+'\n'
        +'SellGas : '+str(cek1[6])+'\n'
        +'---------------------------------')
        sys.exit()

    #uniqe_contract_functions_detector
    def unq(self):
        try:
            unq = self.tcontract().functions.AB7().call()
            if unq == int(unq):
                unq = int(int(unq) / int(10**9))
                print(key.CYELLOW+f'AB7 found. max gwei {unq}'+key.RESET)
                print('---------------------------------')
        except Exception as e:
            if 'execution reverted' in str(e):
                pass

    #tokerbypass
    def tk(self):
        t_supply = self.maxtx()[0]
        c_max = 1
        #current_price
        maxinp =  int(float(t_supply / 100 * float(c_max)))
        getprice = self.prouter()[0].functions.getAmountsOut(maxinp,[self.token_address, self.pair]).call()
        c_price_1 = self.w3.fromWei(getprice[1],'ether')
        while True:
            print(key.CYELLOW+'We are trying to bypass toker !', end='\r'+key.RESET)
            try:
                getprice = self.prouter()[0].functions.getAmountsOut(maxinp,[self.token_address, self.pair]).call()
                c_price_2 = self.w3.fromWei(getprice[1],'ether')
                if c_price_1 < c_price_2:
                    break

            except KeyboardInterrupt:
                sys.exit()
        #sleep
        if self.sleep == 0:
            time.sleep(14.5)
        if float(self.sleep) > 0:
            time.sleep(float(self.sleep))


        