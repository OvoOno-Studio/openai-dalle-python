import openai 
import os
from web3 import Web3
from flask import Flask, request, render_template, jsonify
from config import APIKey, InfuraKey
import urllib.request
import datetime

# Counts per IP
request_counts = {}

# Connect to the Ethereum network using Infura
web3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{InfuraKey}"))

# Set the API key
openai.api_key = str(APIKey)

app = Flask(__name__) 

class Form:
    def __init__(self):
        self.text = ""

@app.route('/')
def index():
    return render_template('index.html')  

@app.route('/donate', methods=['POST'])
def donate():
    # Get the user's wallet address and the amount they want to donate
    wallet_address = request.form['wallet_address']
    amount = request.form['amount']

    # Check that the user has enough Ethereum in their wallet
    balance = web3.eth.getBalance(wallet_address)
    if balance < amount:
        return "Error: Not enough Ethereum in wallet"

    # Set the amount to donate in wei (1 ether = 10^18 wei)
    amount_in_wei = web3.toWei(amount, 'ether')

    # Set the recipient address to your wallet address
    recipient_address = '0xe4b3d35CA83ea2f66e26c6EFB81F3FCa35c6C331'

    # Set the transaction details
    transaction = {
        'to': recipient_address,
        'value': amount_in_wei,
        'gas': 21000,
        'gasPrice': web3.toWei('20', 'gwei'),
        'nonce': web3.eth.getTransactionCount(wallet_address)
    }

    # Sign the transaction with the user's wallet private key
    wallet_private_key = 'YOUR-WALLET-PRIVATE-KEY'
    signed_tx = web3.eth.account.signTransaction(transaction, wallet_private_key)

    # Send the transaction to the Ethereum network
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    return f'Transaction sent: {tx_hash}'

@app.route('/generate', methods=['POST', 'GET'])
def generate():
    # Get the user's IP
    user_ip = request.remote_addr

    # Check if the user's IP is in the dictionary
    if user_ip not in request_counts:
        # If not, add it and set the count to 1
        request_counts[user_ip] = {'count': 1, 'timestamp': datetime.datetime.now()}
    else:
        # If it is, increment the count
        request_counts[user_ip]['count'] += 1

    # Check if the user has made more than 5 requests today
    if request_counts[user_ip]['count'] > 5:
        # If they have, return an error message
        return jsonify({'error': 'You have exceeded the daily request limit.'})

    # Get the text to generate an image for
    text = request.data
    # Set the prompt for the image 
    prompt = str(text)
    model = "image-alpha-001"
    num_images = 1
    size = "1024x1024"
    response_format = "url"
    # Generate the image
    response = openai.Image.create( 
        model=model,
        prompt=prompt,
        n=num_images,
        size=size,
        response_format=response_format 
    )   
    
    # Return the generated image URL to the client 
    return jsonify({'url': response['data'][0]['url']})

if __name__ == '__main__':
    app.run()