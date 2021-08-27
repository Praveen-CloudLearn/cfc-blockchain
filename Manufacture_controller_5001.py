#Importing the libraries
from flask import Flask, jsonify,request
from model.blockchain import Blockchain
from model.manufacturer import Manufacturer
from uuid import uuid4
import requests

app = Flask(__name__)

#Creating a blockchain
blockchain=Blockchain()

#Creating manufacturer
manufacturer=Manufacturer()

#creating an address for the node on the port 5001
node_address=str(uuid4()).replace('-','')

#Mining a new block
@app.route('/mine_block',methods=['GET'])
def mine_block():
    previous_block=blockchain.get_previous_block()
    previous_proof=previous_block['proof']
    proof=blockchain.proof_of_work(previous_proof)
    previous_hash=blockchain.hash(previous_block)
    block=blockchain.create_block(proof,previous_hash)
    response={'message':'Congratulations, you just mined a block!',
              'index':block['index'],
              'timestamp':block['timestamp'],
              'proof':block['proof'],
              'previous_hash':block['previous_hash'],
              'transactions':block['transactions']}
    return jsonify(response), 200

@app.route('/get_chain',methods=['GET'])
def get_chain():
    response={'chain':blockchain.chain,
              'length':len(blockchain.chain)}
    return jsonify(response), 200

@app.route('/is_valid',methods=['GET'])
def is_valid():
    is_valid=blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        return jsonify({'message':'All good.. The blockchain is valid.)'}),200
    else:
        return jsonify({'message':'Houston, we have a problem. The Blockchain is not valid'}),200
           
#connecting all the nodes 
@app.route('/connect_node',methods=['POST'])
def connect_node():
    json=request.get_json()
    nodes=json.get('nodes')
    if nodes is None:
        return 'No node',400
    for node in nodes:
        blockchain.add_node(node)
    response={'message':'All the nodes are connected now. It contains the following nodes:',
              'total_nodes':list(blockchain.nodes)}
    return jsonify(response),201

@app.route('/replace_chain',methods=['GET'])
def replace_chain():
    is_chain_replaced=blockchain.replace_chain()
    if is_chain_replaced==True:
        return jsonify({'message':'The nodes had different chains so the chain was replaced by the longest one.',
                        'new_chain':blockchain.chain}),200
    else:
        return jsonify({'message':'All good. The chain is the largest one.',
                        'actual_chain':blockchain.chain}),200

@app.route('/add_transaction',methods=['GET'])        
def add_transaction():
    url='http://129.146.67.39:2401/jderest/orchestrator/SK_Fetch from F4211'
    json_in={"username":"sourav",
          "password":"sourav",
          "environment":"JDV920",
          "Order Co 1":"00001",
          "Or Ty 1":"SO",
          "Add Num 1":"4243",
          "Order Date 1":"01/01/2021",
          "Next Stat 1":"580",
          "Last Stat 1":"560"}
    out=requests.post(url, json = json_in)
    status_code=out.status_code
    json_out=out.json()
    if(status_code!=200):
        print(status_code)
        return jsonify({'message' : json_out['message']}),200
    transactions=json_out["SK_Fetch from F4211"]["rowset"]
    transaction_count=0
    for trans in transactions:
        transaction_count=transaction_count+1
        json=trans
        transaction_keys=['sender','receiver','itemcode1','LOT','quantity']
        if not all (key in json for key in transaction_keys):
            return 'Some elements of the transation are missing for transaction number: '+str(transaction_count),400
        index=manufacturer.add_transaction(blockchain,json['sender'],json['receiver'],json['itemcode'],json['LOT'],json['quantity'])
    return jsonify({'message' : f'This transaction will be added to Block {index}'}),201

app.run(host='0.0.0.0',port=5001)