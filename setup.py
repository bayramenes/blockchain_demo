import json

privateKey = input("please enter the private key :\n")
publicKey = input("please enter the public key of this private key :\n")
file = open("nodes.json", "r+")
fileData = json.load(file)
fileData["self"] = {"private": privateKey, "public": publicKey}
file.seek(0)
json.dump(fileData, file, indent=4)

file.close()
