#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask import Flask, request, render_template, jsonify
# from flask.ext.sqlalchemy import SQLAlchemy
from config import APIKey, InfuraKey, dbPW 
from web3 import Web3
from forms import *
import openai 
import os

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

# Counts per IP
request_counts = {}

# Connect to the Ethereum network using Infura
web3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{InfuraKey}"))

# Set the API key
openai.api_key = str(APIKey)
app = Flask(__name__) 

@app.route('/')
def index():
    # form = GenerateForm(request.form)
    return render_template('templates/pages/placeholder.home.html')  

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
    # try:
    #     # Connect to the database
    #     db = MySQLdb.connect(host="localhost", user="emelrizv_devemel", passwd=f"{dbPW}", db="emelrizv_dalle")
    #     cursor = db.cursor()
    # except MySQLdb.Error as e:
    #     return jsonify({'error': f'Error connecting to database: {e}'})

    # # Check if the user's IP is in the database
    # cursor.execute("SELECT * FROM request_counts WHERE ip=%s", (user_ip,))
    # result = cursor.fetchone()
    # if result is None:
    #     # If not, insert it into the table with a count of 1
    #     cursor.execute("INSERT INTO request_counts (ip, count, timestamp) VALUES (%s, 1, NOW())", (user_ip,))
    # else:
    #     # If it is, increment the count
    #     count = result[1] + 1
    #     cursor.execute("UPDATE request_counts SET count=%s WHERE ip=%s", (count, user_ip))

    # # Check if the user has made more than 5 requests today
    # cursor.execute("SELECT COUNT(*) FROM request_counts WHERE ip=%s AND timestamp > DATE_SUB(NOW(), INTERVAL 1 DAY)", (user_ip,))
    # result = cursor.fetchone()
    # if result[0] > 5:
    #     # If they have, delete the count from the table
    #     cursor.execute("DELETE FROM request_counts WHERE ip=%s AND timestamp < DATE_SUB(NOW(), INTERVAL 1 DAY)", (user_ip,))
    #     return jsonify({'error': 'You have exceeded the daily request limit.'})

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

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()