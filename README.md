

# blockchain_demo


a blockchain demonstration made with python.




# initial setup

first you clone the repo with 

> **git clone https://github.com/bayramenes/blockchain_demo.git**

a file named  __setup.py__ will apear

run that file and you will be asked to enter a public and private key pair for that node that you will be running.

the keypair should be generated with ecdsa function with the curve being "secp256k1" which is the same as the one used by bitcoin.

>  **Note** : you can run the node first without adding a keypair and generating one through the webpage of the node

# setup environment

to run the node first you have to activate the virtual enviroment that includes all of the dependencies needed for the program to run.

#### to activate the virtual env on mac os or linux :

> chmod +x ./env/bin/activate

> source ./env/bin/activate


#### to activate the virtual env on windows :

> .\env\bin\activate


**after that you are ready to go :**

## running the node

into the terminal type flask run -p (the port desired for the node to operate at default 5000)

in the terminal a message from flask saying that the host is running at the localhost with specified port is now running

you can visit that ip in your browser and you will see the gui of the node with various options but most importantly the nodes registered on that particular node 

and the address of the node for transactions and this kind of thing





## feel free to tweek the code as you want optimize and if you improve on it or you have any suggestions please setup a pull request . thank you .


