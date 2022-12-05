from web3 import Web3
import bsett as set
import abi as key

class LP():
    def __init__(self, token_address, pair_address):
        self.w3 = self.connect()
        self.token_address = Web3.toChecksumAddress(token_address)
        self.pair = Web3.toChecksumAddress(pair_address)
        self.symbol = self.p_symbol()

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

    def pancake_factory(self):
        pancake_factory_address = '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'
        pancake_factory_abi = key.pancake_factory_abi
        pancake_factory = self.w3.eth.contract(address=pancake_factory_address, abi=pancake_factory_abi)
        return pancake_factory
    
    def pairs_factory(self):
        pairs_address = self.pair
        pairs_address_abi = key.pairs_abi
        pairs_factory = self.w3.eth.contract(address=pairs_address, abi=pairs_address_abi)
        return pairs_factory
    
    def p_symbol(self):
        symbolr = self.pairs_factory().functions.symbol().call()
        p_symbol = symbolr.replace('W', '')
        return p_symbol

    def pairs(self):
        token1 = self.pair
        token2 = self.token_address
        none = '0x0000000000000000000000000000000000000000'
        check_pairs = self.pancake_factory().functions.getPair(token1,token2).call()
        if check_pairs == none:
            print(key.CBLUE + 'Cheking Pair Please Wait.....'+key.RESET+'\n'+key.CGREEN + 'Pair Not Detected '+'\n'+key.RESET+key.CVIOLET+'Waiting Pairs !'+key.RESET)
            while True:
                try:
                    check_pairs = self.pancake_factory().functions.getPair(token1,token2).call()
                    if check_pairs != none:
                        break
                except KeyboardInterrupt:
                    sys.exit()

        check_pairs = check_pairs
        checkLP = self.pairs_factory().functions.balanceOf(check_pairs).call()
        TotalLP = self.w3.fromWei(checkLP,'ether')
        if TotalLP < set.minLP:
            print(key.CRED + 'Liquadity Not Detected '+'\n'+key.RESET+key.CVIOLET+'Waiting Dev Add The Liquadity !'+key.RESET)
            while True:
                try:
                    check_pairs = check_pairs
                    checkLP = self.pairs_factory().functions.balanceOf(check_pairs).call()
                    TotalLP = self.w3.fromWei(checkLP,'ether')
                    if TotalLP > set.minLP:
                        break
                except KeyboardInterrupt:
                    sys.exit()
        print(key.CGREEN + 'Liquadity is Detected '+'\n'+key.RESET+str(TotalLP) +key.CYELLOW+' '+str(self.symbol)+key.RESET+'\n'+key.CRED+'Checking Trade Status !'+key.RESET)

    