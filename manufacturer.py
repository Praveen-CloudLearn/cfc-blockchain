

class Manufacturer:
    
    def add_transaction(self,blockchain,sender,distributor,itemcode,lot,quantity):
        index=blockchain.add_transaction(sender,distributor,itemcode,lot,quantity)
        return index
    
#    def private_public_key()