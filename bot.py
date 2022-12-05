from web3 import Web3
import time
import abi as key
import bsett as set
import argparse
from tinfo import TINF
from swap import SWP
from lp import LP
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--a", help="Token address")
parser.add_argument("-c", "--c", action="store_true", help="Sniperbot Check Mode")
parser.add_argument("-c1", "--c1", action="store_true", help="Check Mode With honeypot.is")
parser.add_argument("-g", "--g", help="Custom Gwei")
parser.add_argument("-gs", "--gs", help="Custom Gwei for Sell")
parser.add_argument("-ga", "--ga", help="Custom Gwei for Approve")
parser.add_argument("-ak", "--ak", help="Select which account to use eg: -ak 2 (Second account) etc")
parser.add_argument("-ak1", "--ak1", help="Select which backup account to use eg: -ak 2 (Second account) etc")
parser.add_argument("-apr", "--apr", action="store_true", help="Approve Token")
parser.add_argument("-rvk", "--rvk", action="store_true", help="Revoke Token")
parser.add_argument("-aprc", "--aprc", action="store_true", help="Check Approve status")
parser.add_argument("-mw", "--mw", action="store_true", help="Multiwallet")
parser.add_argument("-bf", "--bf", help="Buy For / custom Recipient")
parser.add_argument("-t", "--t", action="store_true", help="Help you measure node speed")
parser.add_argument("-b", "--b", action="store_true", help="Run SniperBot")
parser.add_argument("-ps", "--ps", action="store_true", help="Price Stream")
parser.add_argument("-toi", "--toi", action="store_true", help="Disable Token Info")
parser.add_argument("-lp", "--lp", action="store_true", help="Disable LP checker")
parser.add_argument("-p", "--p", help="Select Your Pair eg: -p 1 for busd , -p 2 usdt, -p 3 for usdc")
parser.add_argument("-p1", "--p1", help="Select Your Custom Pair eg: Default None, p1 1 for busd , -p1 2 usdt, -p1 3 usdc")
parser.add_argument("-n", "--n", help="Amount of BNB you want to spend")
parser.add_argument("-m1", "--m1", action="store_true", help="custom Max Tx. PAUSE MODE")
parser.add_argument("-m2", "--m2", action="store_true", help="custom Max Tx. AUTO MODE")
parser.add_argument("-m3", "--m3", action="store_true", help="Max Tx Exact Amount token . PAUSE MODE")
parser.add_argument("-m4", "--m4", action="store_true", help="Max Tx Exact Amount token . AUTO MODE")
parser.add_argument('-mp', "--mp", help="set max buy in percent")
parser.add_argument("-d", "--d", help="Skip Deadblock eg: -d 2 (You will skip 2 blocks)")
parser.add_argument("-cd", "--cd", action="store_true", help="Disable Trade checker and Tax checker")
parser.add_argument("-txd", "--txd", action="store_true", help="Disable Tax checker")
parser.add_argument("-trd", "--trd", action="store_true", help="Disable Trade checker")
parser.add_argument("-tp", "--tp", help="Take Profit eg: -tp 200 (Automatic sell when get 200 percents profit )")
parser.add_argument("-ws", "--ws", action="store_true", help="Watch & Sell")
parser.add_argument("-was", "--was", action="store_true", help="Wait Tax drop and Sell")
parser.add_argument("-mb", "--mb", help="Multi Buy")
parser.add_argument("-sp", "--sp", help="Slippage")
parser.add_argument("-so", "--so", action="store_true", help="Sell Only")
parser.add_argument("-bo", "--bo", action="store_true", help="Buy Only")
parser.add_argument("-gas", "--gas", help="Costum Gas limit, l for low 500k, m for medium 1500k, h for high 4M")
parser.add_argument('-nb', "--nb", action="store_true", help="buy custom pair with BNB")
parser.add_argument("-csp", "--csp", help="Costum Amount of sell in percent")
parser.add_argument("-dap", "--dap", action="store_true", help="Disabled Approve check Before sell")
parser.add_argument("-bl", "--bl", action="store_true", help="Check Balance")
parser.add_argument("-tk", "--tk", action="store_true", help="Toker bypass")
parser.add_argument("-tr", "--tr", help="sleep in second")
args = parser.parse_args()

class SniperBot():
    def __init__(self):
        self.w3 = self.node()
        self.include()
    
    def node(self):
        nodes = set.nodes
        if bool(nodes) == False:
            print('Please input RPC/WSS url first!')
            sys.exit()
        if 'http' in nodes:
            w3 = Web3(Web3.HTTPProvider(nodes))
        else:
            w3 = Web3(Web3.WebsocketProvider(nodes))
        return w3
    
    def Welcome(self):
        if args.c == True:
            print("---------------------------------")
            pass
        else:
            print("---------------------------------")
    
    def include(self):
        self.token = self.w3.toChecksumAddress(self.shit())
        self.pair = self.spairs()
        self.cpair = self.cpairs()
        #custommaxtx
        self.m1 = args.m1
        self.m2 = args.m2
        self.m3 = args.m3
        self.m4 = args.m4
        self.mp = args.mp
        self.symbol = self.p_symbol()
        #normal_wallet
        self.wallet = self.wallet()
        #backup_wallet
        self.bwallet = self.bwallet()
        self.bf = args.bf
        #gwei
        self.g = args.g
        self.gs = args.gs
        self.ga = args.ga
        #profit
        self.tp = args.tp
        self.ws = args.ws
        self.mb = args.mb
        self.bf = args.bf
        #slippage
        self.sp = args.sp
        #amount
        self.n =  args.n
        #gaslimit
        self.gas = args.gas
        #enable_custom_pair
        self.nb = args.nb
        #customsell
        self.csp = args.csp
        self.dap = args.dap
        #sleep
        self.sleep = self.sleep()





    def shit(self):
        shit = args.a
        if args.bl == False:
            if bool(args.a) == False:
                print(key.CRED +'Enter Contract Address:'+key.RESET)
                token = input().lower()
                remletter = token.replace('zero', '0').replace('one', '1').replace('two', '2').replace('three', '3').replace('four', '4').replace('five', '5').replace('six', '6').replace('seven', '7').replace('eight', '8').replace('nine', '9').replace('ten', '10').replace('eleven', '11').replace('twelve', '12').replace('thirteen', '13').replace('fourteen', '14').replace('fifteen', '15').replace('sixteen', '16').replace('seventeen', '17').replace('eighteen', '18').replace('nineteen', '19').replace('twenty', '20').replace('remove', '').replace('delete', '').replace('beginning', '').replace('middle', '').replace('end', '').replace('first', '').replace('second', '').replace('third', '').replace('space', '').replace('part', '')
                shit = remletter
                efirst = r"(\([0-9][^a-zA-Z0-9_][0-9]\))"
                matches = re.findall(efirst, shit)
                for i in range(0,len(matches)):
                    if bool(matches) == True:
                        efirst = r"(\([0-9][^a-zA-Z0-9_][0-9]\))"
                        matches = re.findall(efirst, shit)
                        rem = matches[0].replace('(', '').replace(')', '')
                        conint = eval(rem)
                        jst = shit.replace(str(matches[0]),str(conint))
                        shit = jst
                    else:
                        shit = remletter
                wtext = re.sub(r'[^a-zA-Z0-9]','',shit)
                shit = wtext
            else:
                shit = args.a
        else:
            shit = self.spairs()
        return shit
    
    def spairs(self):
        if args.p == None:
            spairs = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'#wbnb
        if args.p == '1':
            spairs = '0x4Fabb145d64652a948d72533023f6E7A623C7C53'#busd
        if args.p == '2':
            spairs = '0xdAC17F958D2ee523a2206206994597C13D831ec7'#usdt
        if args.p == '3':
            spairs = '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'#usdc
        return spairs
    
    #custom_pair_
    def cpairs(self):
        if args.p1 == None:
            cpairs = None
        if args.p1 == '1':
            cpairs = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'#wbnb
        if args.p1 == '2':
            cpairs = '0x4Fabb145d64652a948d72533023f6E7A623C7C53'#busd
        if args.p1 == '3':
            cpairs = '0xdAC17F958D2ee523a2206206994597C13D831ec7'#usdt
        if args.p1 == '4':
            cpairs = '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'#usdc
        return cpairs

    def sleep(self):
        sleep = 0
        if args.tr == None:
            sleep = 0
        if args.tr != None:
            sleep = args.tr
        return sleep

    def pairs_factory(self):
        pair = self.spairs()
        if args.p1 != None:
            pair = self.cpairs()
        pairs_address = pair
        pairs_address_abi = key.pairs_abi
        pairs_factory = self.w3.eth.contract(address=pairs_address, abi=pairs_address_abi)
        return pairs_factory
    
    def p_symbol(self):
        symbolr = self.pairs_factory().functions.symbol().call()
        p_symbol = symbolr.replace('W', '')
        return p_symbol

    def prouter(self):
        pancake_router_address = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'
        pancake_router_abi = key.pancake_router_abi
        prouter = self.w3.eth.contract(address=pancake_router_address, abi=pancake_router_abi)
        return prouter, pancake_router_address


    #normal_wallet
    def wallet(self):
        wallet = args.ak
        if args.ak == None:
            wallet == args.ak
        if args.ak != None:
            wallet == (args.ak)
        if args.mw == True:
            wallet =  'mw'
        return wallet
    
    #backup_wallet
    def bwallet(self):
        bwallet = args.ak1
        if args.ak1 == None:
            bwallet == args.ak1
        if args.ak1 != None:
            bwallet == (args.ak1)
        return bwallet

    def tokinfo(self):
        if args.c == True:
            if args.toi == False:
                t_info = self.TINF.token_info()
                gas = self.TINF.gasinfo()
                # tokenInfo
                print('*Token Informations*'+'\n'
                +'---------------------------------'+'\n'
                +'Name : '+str(t_info[0])+'\n'
                +'Decimals : '+str(t_info[1])+'\n'
                +'Symbol : '+str(t_info[2])+'\n'
                +'Total Supply : '+str(t_info[3])+'\n'
                +'MaxTx : '+str(t_info[4])+' / '+str(t_info[7])+'%'+' / '+str(t_info[10])+' '+str(self.symbol)+'\n'
                +'Max_Sell : '+str(t_info[5])+' / '+str(t_info[8])+'%'+' / '+str(t_info[11])+' '+str(self.symbol)+'\n'
                +'Max_Wallet : '+str(t_info[6])+' / '+str(t_info[9])+'%'+' / '+str(t_info[12])+' '+str(self.symbol)+'\n'
                +'Buy_gas : ' +str(gas[0])+'\n'
                +'Sell_gas : ' +str(gas[0])+'\n'
                +'---------------------------------')
                #uniqe_contract_functions_detector
                self.TINF.unq()
            else:
                pass
        else:
            pass

    def max_tx(self):
        i_max = self.TINF.c_max_tx()
        max_tx = i_max[0]
        mx_p = i_max[1]
        return max_tx, mx_p
    
    def rtime_max(self):
        rtime_max = self.TINF.rtime_max()
        return rtime_max
    
    def lpcheck(self):
        if args.lp == False:
            lpcheck = self.LP.pairs()
        else:
            pass
    
    def deadblock(self):
        block = self.w3.eth.blockNumber
        dead2 = args.d
        if dead2 != None and (int(dead2) > int(0)):
                rdead = block+int(dead2)
                dead = rdead
                print(key.CGREEN+'Current block :'+str(block)+key.RESET+'\n'
                +key.CRED+'Skiping '+dead2+' block'+key.RESET+'\n'
                +key.CVIOLET+'Buying at block :'+str(rdead)+key.RESET)
                fdead = dead-1
                while True:
                    block = self.w3.eth.blockNumber
                    if block == fdead:
                        break
        if args.d == None:
            pass
    
    def pricestream(self):
        if args.ps == True:
            self.lpcheck()
            self.TINF.pricestream()
        

    def sniper(self):
        if args.b == True or args.c == True:
            self.Welcome()
            start = time.time()
            self.tokinfo()
            self.lpcheck()
            #bypass_toker
            if args.tk == True:
                self.TINF.tk()
            #############
            self.deadblock()
            if args.c == True:
                end = time.time()
                if args.t == True:
                    print(end-start, 'Seconds')
                    print('Check Mode !'+'\n'+'---------------------------------')
                    sys.exit()
                print('Check Mode !'+'\n'+'---------------------------------')
                sys.exit()
            if self.m1 == True or self.m3 == True:
                self.TINF.rtime_max()
            else:
                pass                        

    def Runme(self):
        self.TINF = TINF(self.token, self.pair, self.m1, self.m2, self.m3, self.m4, self.mp, self.symbol, self.sleep)
        self.LP = LP(self.token, self.pair)
        #Sniper_and_checker
        self.sniper()
        #toker_bypass
        self.SWP = SWP(self.token, self.pair, self.m1, self.m2, self.m3, self.m4, self.mp, self.symbol, self.wallet, self.bf, self.g, self.gs, self.ga, self.tp, self.ws, self.mb, self.sp, self.n, self.max_tx(), self.gas, self.nb, self.csp, self.dap, self.cpair, self.bwallet)
        #buyonly
        if args.bo == True:
            self.SWP.buy_approve()
            sys.exit()
        #sellonly
        if args.so == True:
            self.SWP.sell_approve()
            sys.exit()
        #check_all_wallet
        if args.bl == True:
            self.SWP.bal()
        #approve
        if args.apr == True:
            self.SWP.approve_manual()
        #revoke
        if args.rvk == True:
            self.SWP.revoke()
        #approve_check
        if args.aprc == True:
            self.SWP.approvecheck()
        #watchsell
        if args.ws == True:
            self.SWP.profit_stream()
            self.SWP.sell_approve()
        #wait_tax_sell_lower
        if args.was == True:
            self.SWP.sell_approve()
        #Honeypotdotio
        if args.c1 == True:
            self.TINF.hpdotiorun()
        #price_stream    
        self.pricestream()
        #Normal_mode
        self.SWP.buy_approve()
        self.SWP.profit_stream()
        self.SWP.sell_approve()
        
SniperBot().Runme()
