import hashlib
import time
import threading
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

def calculate_hash(index, previous_hash, timestamp, data, difficulty):
    nonce = 0
    while True:
        block_data = str(index) + previous_hash + str(timestamp) + data + str(nonce)
        block_hash = hashlib.sha256(block_data.encode()).hexdigest()
        if block_hash[:len(difficulty)] == difficulty:
            return block_hash
        nonce += 1

def calculate_previous_hash(blockchain):
    if len(blockchain) == 0:
        return "0"
    else:
        return blockchain[-1].hash

def create_genesis_block():
    return Block(0, "0", time.time(), "Genesis Block", calculate_hash(0, "0", time.time(), "Genesis Block", "00"))

def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = time.time()
    previous_hash = calculate_previous_hash(blockchain)
    hash = calculate_hash(index, previous_hash, timestamp, data, "00")
    return Block(index, previous_hash, timestamp, data, hash)

def timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def mine_block():
    global mining_timer, mining_transactions, current_block

    if len(mining_transactions) > 0:
        data = "\n".join(mining_transactions)
    else:
        data = "No transactions in this block."

    new_block = create_new_block(current_block, data)
    blockchain.append(new_block)
    current_block = new_block
    mining_transactions.clear()
    update_text()

    mining_timer = threading.Timer(20.0, mine_block)
    mining_timer.start()

def add_transaction():
    person_name = entry_person_name.get()
    amount = entry_amount.get()
    address = entry_address.get()
    transaction_data = f"Person: {person_name}\nAmount: {amount}\nAddress: {address}"
    mining_transactions.append(transaction_data)
    update_text()

def update_text():
    text.delete(1.0, tk.END)
    for block in blockchain:
        text.insert(tk.END, f"Block #{block.index}\n")
        text.insert(tk.END, f"Timestamp: {timestamp_to_datetime(block.timestamp)}\n")
        text.insert(tk.END, f"Previous Hash: {block.previous_hash}\n")
        text.insert(tk.END, f"Data:\n{block.data}\n")
        text.insert(tk.END, f"Hash: {block.hash}\n")
        text.insert(tk.END, "-"*30 + "\n")

# Initialize the blockchain with the genesis block
blockchain = [create_genesis_block()]
current_block = blockchain[0]

# List to hold pending transactions for mining
mining_transactions = []

# Timer for block mining
mining_timer = threading.Timer(20.0, mine_block)
mining_timer.start()

# Desktop Interface using tkinter
app = tk.Tk()
app.title("EASTSIDE Blockchain")
app.geometry("500x600")

label_person_name = tk.Label(app, text="Person's Name:")
label_person_name.pack()

entry_person_name = tk.Entry(app, width=40)
entry_person_name.pack()

label_amount = tk.Label(app, text="Amount:")
label_amount.pack()

entry_amount = tk.Entry(app, width=40)
entry_amount.pack()

label_address = tk.Label(app, text="Address:")
label_address.pack()

entry_address = tk.Entry(app, width=40)
entry_address.pack()

btn_add_transaction = tk.Button(app, text="Add Transaction", command=add_transaction)
btn_add_transaction.pack()

text = tk.Text(app)
text.pack()

update_text()

app.mainloop()
