import json


from blockchain import BlockChain
from flask import Flask, render_template, request

app = Flask(__name__)

# telling flask not to sort the json keys but rather display them the way they are passed to the framework
app.config["JSON_SORT_KEYS"] = False

# to display the json in a pretty way
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True


# an instance of the class created
blockchain = BlockChain()


# the homepage of the website


@app.route("/")
def main():
    network = blockchain.getNetwork()
    addr = blockchain.nodeAddress
    return render_template(
        "index.html",
        nodes=network,
        balance=blockchain.checkBalance(addr),
        address=addr,
    )


# for other nodes to compare to their version
@app.route("/get_chain")
def getChain():
    return blockchain.getChain(), 200


# for the user to display the chain in a good way
@app.route("/chain")
def displayChain():
    chain = blockchain.getChain()
    return render_template(
        "blockchain.html", blocks=chain["chain"], chainLength=chain["length"]
    )


#  mine the block with the transactions given in the memepool
@app.route("/mine_block", methods=["GET"])
def mineBlock():
    return blockchain.mineBlock()


# add a transaction to the blockchain
@app.route("/add_transaction", methods=["GET", "POST"])
def addTx():

    if request.method == "POST":
        public = request.form.get("publicKey")
        sig = request.form.get("signature")
        sender = request.form.get("sender")
        receiver = request.form.get("receiver")
        amount = request.form.get("amount")

        msg = {"sender": sender, "receiver": receiver, "amount": amount}
        # return the answer from verify function which is a bool
        # the function checks whether the signature was the produces with the message and private key of the provided public key
        # and then checks whether that user is really the same user in order to prevent some one from sigining transaction of another person
        # because it will still be verified
        if blockchain.verifyTx(
            signature=sig,
            publicKey=public,
            message=json.dumps(msg),
            sender=sender,
            amount=amount,
        ):
            return blockchain.addTx(
                {"sender": sender, "receiver": receiver, "amount": float(amount)},
                index=1,
            )

    else:

        # if the user is accessing through the web page render a template
        return render_template("new_transaction.html")


# check the balance of a given address


@app.route("/balance_check", methods=["GET", "POST"])
def checkBalance():
    if request.method == "POST":
        address = request.form.get("addressToCheck")
        balance = blockchain.checkBalance(address=address)
        return {"address": address, "balance": balance}

    else:
        return render_template("balanceCheck.html")


# produce an ecdsa signature given the private key and the message the user want to sign


@app.route("/new_signature", methods=["GET", "POST"])
def newSig():
    if request.method == "POST":
        priv = request.form.get("privateKey")
        sender = request.form.get("sender")
        receiver = request.form.get("receiver")
        amount = request.form.get("amount")
        msg = {"sender": sender, "receiver": receiver, "amount": amount}
        return blockchain.genSig(privateKey=priv, message=json.dumps(msg))
    else:
        return render_template("new_signature.html")


# check the validity and integrity of the current blockchain by comparing each blocks prev hash section the previous blocks hash section
# and of course checking if the hash does in fact have that proof which is 4 leading zeros in the hash
@app.route("/validity")
def checkValidity():
    validity = blockchain.check_validity(blockchain.getChain()["chain"])
    if validity:
        return {"message": "The Chain is Valid", "validity": True}

    else:
        return {"message": "the Chain is not Valid", "validity": False}


# add a node to the copy of the network for that specific node


@app.route("/new_node", methods=["GET", "POST"])
def addNode():
    if request.method == "POST":
        node = request.form.get("nodeToAdd")

        if node is None:
            return "No nodes", 400
        blockchain.addNode(node)
        response = {
            "message": "added the node to the network successfully",
            "nodes": node,
        }
        return response
    else:
        return render_template("add_node.html")


# render a template in order to generate new key pair along with an address
# which is basically public key hashed with sha256
@app.route("/new_keys")
def newKeys():
    return render_template("new_keys.html")


# generate the new key pair
@app.route("/generate_keys")
def genKeys():
    return blockchain.genKeyPair()


# this endpoint expects a json shaped chain that should be sent by the requester
# basically the idea is that when a node on the network mines a new block it should broadcast it to the network so the idea is that
# that node sends a request to every and each node registered on the network with it's own version of the blockchain and the receiver check the length and the validity
# of the chain so if it is in fact long enough and valid it return true else it returns false
# and this is the endpoint where the node expects that chain to compare
@app.route("/replace_chain", methods=["POST"])
def replaceChain():
    chainToCompare = request.get_json()
    if len(chainToCompare) > len(blockchain.chain):
        if blockchain.check_validity(chain=chainToCompare):
            blockchain.replaceChain(newChain=chainToCompare)
            return {"message": "replaced the chain", "replaced": True}
        return {
            "message": "didn't replace the chain chain isn't valid",
            "replaced": False,
        }
    return {
        "message": "didn't replace the chain chain length is equal or less",
        "replaced": False,
    }


# display the details of a specific block by getting the index from the request and rendering data accordingly
@app.route("/block")
def showBlock():
    block = blockchain.getChain()["chain"][int(request.args.get("index"))]
    return render_template("block.html", blockToDisplay=block)
