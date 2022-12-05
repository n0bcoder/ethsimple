from web3 import Web3
import bsett as set
import abi as key
import sys
import threading
import time
import re
import sys

class SWP():
    def __init__(self, token_address, pair_address, m1, m2, m3, m4, mp, symbol, wallet, bf, g, gs, ga, tp, ws, mb, sp, n, maxtx, gas, nb, csp, dap, cpair, bwallet):
        self.w3 = self.connect()
        self.token_address = Web3.toChecksumAddress(token_address)
        self.pair = Web3.toChecksumAddress(pair_address)
        self.cpair = cpair
        self.m1 = m1
        self.m2 = m2
        self.m3 = m3
        self.m4 = m4
        self.mp = mp
        self.p_symbol = symbol
        self.wl = wallet
        self.bwl = bwallet
        self.wls = self.wallets()
        self.bf = bf
        #gwei
        self.g = g
        self.gs = gs
        self.ga = ga
        #profit
        self.tp = tp
        self.ws = ws
        self.mb = mb
        #slippage
        self.sp = sp
        #amount
        self.n = n
        #maxtx
        self.max_tx = maxtx
        #gaslimit
        self.gas = gas
        #normalbuy
        self.nb = nb
        #customsellbypercent
        self.csp = csp
        #disable_approve_before_sell
        self.dap = dap
        
    
    def connect(self):
        nodes = set.nodes
        if bool(nodes) == False:
            print('Please input RPC/WSS url first!')
            sys.exit()
        if 'https' in nodes:
            w3 = Web3(Web3.HTTPProvider(nodes))
        else:
            w3 = Web3(Web3.WebsocketProvider(nodes))
        return w3
    
    def tcontract(self):
        trouter = self.w3.toChecksumAddress(self.token_address) 
        trouter_abi = key.sellAbi
        tcontract = self.w3.eth.contract(trouter, abi=trouter_abi)
        return tcontract
    
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
    
    def prouter(self):
        pancake_router_address = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'
        # pancake_router_address = '0x6929B3d71a400b95AEB61176559703436356e11a'
        pancake_router_abi = key.pancake_router_abi
        prouter = self.w3.eth.contract(address=pancake_router_address, abi=pancake_router_abi)
        return prouter, pancake_router_address
    
    def pairs_factory(self):
        pair = self.pair
        if self.cpair != None:
            pair = self.cpair
        pairs_address = pair
        pairs_address_abi = key.pairs_abi
        pairs_factory = self.w3.eth.contract(address=pairs_address, abi=pairs_address_abi)
        return pairs_factory

    def tx_to(self):
        tx_to = self.wls
        if self.bf == None or self.bwl == None:
            tx_to = tx_to[0]
        if self.bf != None:
            tx_to = [self.bf]
        if self.bwl != None:
            tx_to = self.backupwallets()
        return tx_to

    def wallets(self):
        #address
        add = set.account
        #privatekey
        prv = set.private
        tw = self.wl
        #totalwallets
        if tw == None:
            add = [add[0]]
            prv = [prv[0]]

        if tw != None:
            if tw.isdigit() == True:
                add = [add[int(tw)-1]]
                prv = [prv[int(tw)-1]]

            tw = str(tw)
            if ',' in tw:
                coma = []
                comp = []
                a = (re.findall(r"(\d+),", tw))
                b = (re.findall(r",(\d+)", tw))
                a = int(int(a[0])-1)
                b = int(b[0])
                for i in range(a,b):
                    coma.append(add[i])
                add = coma
                for i in range(a,b):
                    comp.append(prv[i])
                prv = comp
            if '.' in tw:
                a = (re.findall(r"(\d+).", tw))
                b = (re.findall(r".(\d+)", tw))
                a = int(a[0])-1
                b = int(b[0])-1
                add = [add[a],add[b]]
                prv = [prv[a],prv[b]]
            if tw == 'mw':
                add = set.account
                prv = set.private

        return add, prv
    
    def backupwallets(self):
        #address
        add = set.account
        tw = self.bwl
        #totalwallets
        if tw == None:
            add = [add[0]]

        if tw != None:
            if tw.isdigit() == True:
                add = [add[int(tw)-1]]

            tw = str(tw)
            if ',' in tw:
                coma = []
                comp = []
                a = (re.findall(r"(\d+),", tw))
                b = (re.findall(r",(\d+)", tw))
                a = int(int(a[0])-1)
                b = int(b[0])
                for i in range(a,b):
                    coma.append(add[i])
                add = coma
            if '.' in tw:
                a = (re.findall(r"(\d+).", tw))
                b = (re.findall(r".(\d+)", tw))
                a = int(a[0])-1
                b = int(b[0])-1
                add = [add[a],add[b]]

        return add

    def gwei(self):
        g = set.gwei1
        if self.g == None:
            g = g
        if self.g != None:
            g = self.g
        gs = set.gsell
        if self.gs == None:
            gs = gs
        if self.gs != None:
            gs = self.gs
        ga = set.gaprv
        if self.ga == None:
            ga = ga
        if self.ga != None:
            ga = self.ga
        g = int(float(g) * int(10**9))
        gs = int(float(gs) * int(10**9))
        ga = int(float(ga) * int(10**9))
        return g, gs, ga

    def gass(self):
        gass =  set.gas
        if self.gas == None:
            gass =  set.gas
        if self.gas == 'l' or self.gas == 'L':
            gass = 500000
        if self.gas == 'm' or self.gas == 'M':
            gass = 1500000
        if self.gas == 'h' or self.gas == 'H':
            gass = 4000000        
        return gass

    def approvecheck(self):
        router_address = self.prouter()
        add = self.wls[0]
        for i in range(0,len(add)):
            checkaprv = self.tcontract().functions.allowance(add[i], router_address[1]).call()
            if checkaprv == 0:
                print(f'wallet {i+1} : Token not Approved yet')
            else:
                print(f'wallet {i+1} : Token Approved')
        sys.exit()

    def profit_stream(self):
        print(key.CYELLOW+'Checking Profit!'+key.RESET)
        add = self.wallets()[0]
        wbnb = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
        busd = '0x4Fabb145d64652a948d72533023f6E7A623C7C53'
        while True:
            try:
                t_balance = self.tcontract().functions.balanceOf(add[0]).call()
                if int(t_balance) == int(0):
                    print(key.CYELLOW+'Token not detected yet', end='\r'+key.RESET)
                if int(t_balance) > int(0):
                    break
            except Exception as e:
                if 'execution reverted' in str(e):
                    continue
            except KeyboardInterrupt:
                sys.exit()
        if self.tp == None:
            pass
        if self.tp != None:
            tp = float(self.n) + float(float(self.n)/float(100)*float(self.tp))
            print(key.CRED+'Profit Target '+str(self.tp)+'% / '+str(tp)+' '+str(self.p_symbol)+key.RESET)
        while True:
            try:
                if self.cpair != None:
                    pair = self.cpair
                else:
                    pair = self.pair
                t_balance = self.tcontract().functions.balanceOf(add[0]).call()
                c_balance = self.prouter()[0].functions.getAmountsOut(int(t_balance),[self.token_address, pair]).call()
                p_value = self.w3.fromWei(c_balance[1],'ether')
                if self.tp != None:
                    tp = float(self.n) + float(float(self.n)/float(100)*float(self.tp))
                    if float(p_value) > float(tp):
                        break
                if pair == wbnb:
                    to_usd = self.prouter()[0].functions.getAmountsOut(int(c_balance[1]),[pair, busd]).call()
                    usd = self.w3.fromWei(to_usd[1],'ether')
                    print(key.CYELLOW+'Your Profit: '+key.RESET+key.CGREEN+str(p_value)+' '+str(self.p_symbol)+key.RESET+' | '+key.CYELLOW+str(usd)+' '+'USD', end='\r'+key.RESET)
                    time.sleep(1)
                else:
                    print(key.CYELLOW+' Your Profit: '+key.RESET+key.CGREEN+str(p_value)+' '+str(self.p_symbol), end='\r'+key.RESET)
                    time.sleep(1)
            except Exception as e:
                if 'execution reverted' in str(e):
                    continue
            except KeyboardInterrupt:
                break

    def approve(self):
        add = self.wallets()[0]
        prv = self.wallets()[1]
        router_address = self.prouter()
        hash = []
        for i in range(0,len(add)):
            check_approve = self.tcontract().functions.allowance(add[i], router_address[1]).call()
            if check_approve == 0:
                tamount = 115792089237316195423570985008687907853269984665640564039457584007913129639935
                approve = self.tcontract().functions.approve(router_address[1], int(tamount)).buildTransaction({
                'from': add[i],
                'gasPrice': self.gwei()[2],
                'nonce': self.w3.eth.get_transaction_count(add[i],'pending'),
                })
                signed_txn = self.w3.eth.account.sign_transaction(approve, private_key=prv[i])
                tx_token2 = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
                buyhash = (self.w3.toHex(tx_token2))
                hash.append(buyhash)
            else:
                pass

        return hash

    def approve_manual(self):
        add = self.wallets()[0]
        approve = self.approve()
        if bool(approve) == False:
            print('Token Approved Already')
            sys.exit()
        else:
            for i in range(0,len(approve)):
                txhash = self.w3.eth.wait_for_transaction_receipt(approve[i])
                if txhash['status'] == 1:
                    print(f'wallet {i+1}'+key.CGREEN+' Token Approved'+key.RESET)
                if txhash['status'] == 0:
                    print(f'wallet {i+1}'+key.CRED+' Token Approved failed'+key.RESET)
        sys.exit()
    
    def revoke(self):
        add = self.wallets()[0]
        prv = self.wallets()[1]
        router_address = self.prouter()
        def rvk():
            hash = []
            for i in range(0,len(add)):
                approve = self.tcontract().functions.approve(router_address[1], 0).buildTransaction({
                'from': add[i],
                'gasPrice': self.gwei()[2],
                'nonce': self.w3.eth.get_transaction_count(add[i],'pending'),
                })
                signed_txn = self.w3.eth.account.sign_transaction(approve, private_key=prv[i])
                tx_token2 = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
                buyhash = (self.w3.toHex(tx_token2))
                hash.append(buyhash)
            return hash
        rvk = rvk()
        if bool(rvk) == False:
            pass
        else:
            for i in range(0,len(rvk)):
                txhash = self.w3.eth.wait_for_transaction_receipt(rvk[i])
                if txhash['status'] == 1:
                    print(f'wallet {i+1}'+key.CGREEN+' Token Revoked'+key.RESET)
                if txhash['status'] == 0:
                    print(f'wallet {i+1}'+key.CRED+' Token Revoked failed'+key.RESET)

        sys.exit()
        
    
    def approve_pair(self):
        add = self.wallets()[0]
        prv = self.wallets()[1]
        router_address = self.prouter()
        def pair_approve():
            hash = []
            for i in range(0,len(add)):
                check_approve = self.pairs_factory().functions.allowance(add[i], router_address[1]).call()
                if check_approve == 0:
                    tamount = 115792089237316195423570985008687907853269984665640564039457584007913129639935
                    approve = self.pairs_factory().functions.approve(router_address[1], int(tamount)).buildTransaction({
                    'from': add[i],
                    'gasPrice': self.gwei()[2],
                    'nonce': self.w3.eth.get_transaction_count(add[i],'pending'),
                    })
                    signed_txn = self.w3.eth.account.sign_transaction(approve, private_key=prv[i])
                    tx_token2 = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
                    buyhash = (self.w3.toHex(tx_token2))
                    hash.append(buyhash)
                else:
                    pass
            return hash
        approve =  pair_approve()
        if bool(approve) == False:
            pass
        else:
            for i in range(0,len(approve)):
                txhash = self.w3.eth.wait_for_transaction_receipt(approve[i])
                if txhash['status'] == 1:
                    print(f'wallet {i+1}'+key.CGREEN+' Pair Approved'+key.RESET)
                if txhash['status'] == 0:
                    print(f'wallet {i+1}'+key.CRED+' Pair Approved failed'+key.RESET)


    def buy_approve(self):
        print(key.CVIOLET +'Buying Token'+key.RESET)
        add = self.wallets()[0]
        prv = self.wallets()[1]
        router_address = self.prouter()
        wbnb = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
        recipient = self.tx_to()

        def buy():
            #multibuy
            mb = 1
            if self.mb == None:
                mb = 1
            if self.mb != None:
                mb = self.mb
            #amount_normal_buy
            if self.nb  == False:
                amount = self.n
                if amount == None:
                    amount = set.nonimal1
                if amount != None:
                    amount = self.n
            hash = []
            for i in range(int(mb)):
                for i in range(0,len(add)):
                    if self.pair == wbnb:
                        token_pair_list = [self.pair,self.token_address]
                        #buywithbnb
                        if self.nb == False:
                            buys = self.prouter()[0].functions.swapExactETHForTokens
                            # #slippage
                            amountinout = 0
                            if self.sp == None:
                                amountinout = 0
                            if self.sp != None:
                                sp = self.sp
                                getprice = float(amount) * int(10**18)
                                minreceive = self.prouter()[0].functions.getAmountsOut(int(getprice),[self.pair, self.token_address]).call()
                                amountinout = int(minreceive[1] - (minreceive[1]/100*float(sp)))
                        #custom_pair_buy_usdt_busd_pair_with_bnb
                        if self.nb == True:
                            buys = self.prouter()[0].functions.swapETHForExactTokens
                            token_pair_list = [self.pair, self.cpair, self.token_address]
                            #amount
                            amount = self.n
                            eth_value = int(float(amount) * int(10**18))
                            #convert_eth_usd
                            eth_usd = self.prouter()[0].functions.getAmountsOut(int(eth_value),[self.pair, self.cpair]).call()
                            get_price = self.prouter()[0].functions.getAmountsOut(int(eth_usd[1]),[self.cpair, self.token_address]).call()
                            amountinout = int(get_price[1]-(get_price[1] / 100 * float(self.sp)))
                        #buymax
                        if self.m1 == True or self.m2 == True or self.m3 == True or self.m4 == True:
                            buys = self.prouter()[0].functions.swapETHForExactTokens
                            amountinout = self.max_tx[0]
                            amount = self.max_tx[1]
                            if self.n == None:
                                amount = (amount +(amount / 100 * set.sp))
                            if self.n != None:
                                amount = self.n
                        #########################################
                        pancakeswap2_txn = buys(
                        int(amountinout),
                        token_pair_list,
                        recipient[i],
                        (int(time.time()) + 10000)
                        ).buildTransaction({
                        'from': add[i],
                        'value': self.w3.toWei((amount),'ether'),
                        'gas': self.gass(),
                        'gasPrice': self.gwei()[0],
                        'nonce': self.w3.eth.get_transaction_count(add[i],'pending'),
                        })

                    if self.pair != wbnb:
                        self.approve_pair()
                        token_pair_list = [self.pair, self.token_address]
                        amountb = int(float(self.n) * int(10**18))
                        #approvepairbeforebuyforusdpair
                        if self.m1 == True or self.m2 == True or self.m3 == True or self.m4 == True:
                            buys = self.prouter()[0].functions.swapTokensForExactTokens
                            amountb = self.max_tx[0]
                            max_r = self.prouter()[0].functions.getAmountsOut(int(amountb),[self.token_address, self.pair]).call()
                            if self.n == None:
                                amountinout = (max_r[1]+(max_r[1] / 100 * set.sp))
                            if self.n != None:
                                amountinout = int(float(self.n) * int(10**18))
                        if self.cpair != None:
                            buys = self.prouter()[0].functions.swapExactTokensForTokensSupportingFeeOnTransferTokens
                            token_pair_list = [self.pair, self.cpair, self.token_address]
                            #convert_usd_eth
                            usd_eth = self.prouter()[0].functions.getAmountsOut(int(amountb),[self.pair, self.cpair]).call()
                            get_price = self.prouter()[0].functions.getAmountsOut(int(usd_eth[1]),[self.cpair, self.token_address]).call()
                            amountinout = int(get_price[1]-(get_price[1] / 100 * float(self.sp)))
                        #normalbuy_direct_pair
                        else:
                            buys = self.prouter()[0].functions.swapExactTokensForTokensSupportingFeeOnTransferTokens
                            # #slippage
                            amountinout = 0
                            if self.sp == None:
                                amountinout = 0
                            if self.sp != None:
                                sp = self.sp
                                getprice = float(amount) * int(10**18)
                                minreceive = self.prouter()[0].functions.getAmountsOut(int(getprice),[self.pair, self.token_address]).call()
                                amountinout = int(minreceive[1] - (minreceive[1]/100*float(sp)))
                        pancakeswap2_txn = buys(
                        int(amountb),
                        int(amountinout),
                        token_pair_list,
                        recipient[i],
                        (int(time.time()) + 10000)
                        ).buildTransaction({
                        'from': add[i],
                        'gas': self.gass(),
                        'gasPrice': self.gwei()[0],
                        'nonce': self.w3.eth.get_transaction_count(add[i],'pending'),
                        })
                    signed_txn = self.w3.eth.account.sign_transaction(pancakeswap2_txn, private_key=prv[i])
                    tx_token = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
                    buyhash = (self.w3.toHex(tx_token))
                    print(key.CYELLOW +f'wallet {i+1} '+'https://etherscan.io/tx/'+buyhash+key.RESET)
                    hash.append(buyhash)
            return hash

        #buyhashcheck
        hashck = buy()
        self.approve()
        for i in range(0,len(hashck)):
            #checking transaction status
            txhash = self.w3.eth.wait_for_transaction_receipt(hashck[i])
            if txhash['status'] == 1:
                print(f'wallet {i+1}'+key.CGREEN+' ✓'+key.RESET)
            if txhash['status'] == 0:
                print(f'wallet {i+1}'+key.CRED+' X'+key.RESET)
        #exit_if_buy_for_other_wallet        
        if self.bf == None or self.bwl == None:
            pass
        if self.bf != None or self.bwl != None:
            sys.exit()
        


    def sell_approve(self):
        print(key.CGREEN+'Swapping Token.........'+key.RESET)
        add = self.wallets()[0]
        prv = self.wallets()[1]
        router_address = self.prouter()
        wbnb = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
        def sell():
            hash = []
            for i in range(0,len(add)):
                balance = self.tcontract().functions.balanceOf(add[i]).call()
                if balance > 0:
                    amountinout = 0
                    sell = self.prouter()[0].functions.swapExactTokensForETHSupportingFeeOnTransferTokens
                    pair = wbnb
                    if self.pair == wbnb:
                        sell = self.prouter()[0].functions.swapExactTokensForETHSupportingFeeOnTransferTokens
                        pair = wbnb
                    if self.pair != wbnb:
                        sell = self.prouter()[0].functions.swapExactTokensForTokensSupportingFeeOnTransferTokens
                        pair = self.pair
                    if self.cpair != None:
                        pair = self.cpair
                        if self.cpair == wbnb:
                            sell = self.prouter()[0].functions.swapExactTokensForETHSupportingFeeOnTransferTokens
                        if self.cpair != wbnb:
                            sell = self.prouter()[0].functions.swapExactTokensForTokensSupportingFeeOnTransferTokens
                    if self.csp == None:
                        balance = self.tcontract().functions.balanceOf(add[i]).call()
                    if self.csp != None:
                        balance = (balance/100)*int(self.csp)      
                    if self.sp == None:
                        amountinout = 0
                    if self.sp != None:
                        sp = self.sp
                        minreceive = self.prouter()[0].functions.getAmountsOut(int(balance),[self.token_address, pair]).call()
                        amountinout = int(minreceive[1] - (minreceive[1]/100*float(sp)))
                    pancakeswap2_txn = sell(
                    int(balance),int(amountinout),
                    [self.token_address, pair],
                    add[i],
                    (int(time.time()) + 1000000)
                    ).buildTransaction({
                    'from': add[i],
                    'gas': self.gass(),
                    'gasPrice': self.gwei()[1],
                    'nonce': self.w3.eth.get_transaction_count(add[i], 'pending'),
                    })
                    signed_txn = self.w3.eth.account.sign_transaction(pancakeswap2_txn, private_key=prv[i])
                    tx_token3 = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
                    shash = (self.w3.toHex(tx_token3))
                    print(key.CYELLOW +f'wallet {i+1} '+'https://etherscan.io/tx/'+shash+key.RESET)
                    hash.append(shash)
                if balance == 0:
                    pass
            return hash
        
        #checkapprovebeforesell
        if self.dap == False:
            approve =  self.approve()
            if bool(approve) == False:
                pass
            else:
                for i in range(0,len(approve)):
                    txhash = self.w3.eth.wait_for_transaction_receipt(approve[i])
                    if txhash['status'] == 1:
                        print(f'wallet {i+1}'+key.CGREEN+' Token Approved'+key.RESET)
                    if txhash['status'] == 0:
                        print(f'wallet {i+1}'+key.CRED+' Token Approved failed'+key.RESET)
        else:
            pass

        #sellhashcheck
        hashck = sell()
        for i in range(0,len(hashck)):
            #checking transaction status
            txhash = self.w3.eth.wait_for_transaction_receipt(hashck[i])
            if txhash['status'] == 1:
                print(f'wallet {i+1}'+key.CGREEN+' ✓'+key.RESET)
            if txhash['status'] == 0:
                print(f'wallet {i+1}'+key.CRED+' X'+key.RESET)
        
        #check_balance
        for i in range(0,len(add)):
            pair = wbnb
            if self.pair == wbnb:
                pair = wbnb
            if self.pair != wbnb:
                pair = self.pair
            if self.cpair != None:
                pair = self.cpair
            if self.nb == True or pair != wbnb:
                t_balance = self.pairs_factory().functions.balanceOf(add[i]).call()
                t_read = self.w3.fromWei(t_balance,'ether')
                print(f'wallet {i+1}', t_read,self.p_symbol)
            if pair == wbnb:
                eth = self.w3.eth.getBalance(add[i])
                read = self.w3.fromWei(eth,'ether')
                print(f'wallet {i+1}', read,self.p_symbol)
        
        sys.exit()
        
    def bal(self):
        add = set.account
        busd = '0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56'
        def balance(bl):
            output = []
            for i in range(0,len(bl)):
                wbal = self.w3.eth.getBalance(add[i])
                rmbal = self.w3.fromWei(wbal,'ether')
                fl = float(rmbal)
                print(f'wallet {i+1}', fl, self.p_symbol)
                output.append(float(fl))
            return output
        total = sum(balance(add))
        c_total = self.w3.toWei(total,'ether')
        bcheck = self.prouter()[0].functions.getAmountsOut(int(c_total),[self.pair, busd]).call()
        busdr = self.w3.fromWei(bcheck[1],'ether')
        print('total : ', total, 'ETH /', busdr, 'USD')
        sys.exit()


        
        


                
                




