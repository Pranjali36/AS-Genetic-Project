import streamlit as st
import pandas as pd
import hashlib
import base64
import random

# Load the dataset
df = pd.DataFrame({
    'Person_ID': range(10),
    'Genetic_Sequence': [
        'ATCGGCTA', 'GATCAGCT', 'CGTAGCTA', 'TGCATGCG', 'GATGCTAG',
        'CTAGCTGA', 'ATCGGACT', 'GTACGCTA', 'ATGCGTAC', 'CGTACGAT'
    ]
})

# Simple XOR encryption function (for demonstration purposes)
def xor_encrypt(data, key=123):
    return ''.join(chr(ord(c) ^ key) for c in data)

# Simulate blockchain structure for storing encrypted data
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        # The genesis block does not hold data and is just the starting point
        genesis_block = {
            'index': 0,
            'previous_hash': '0',  # The previous hash is 0 for the first block
            'data': None,           # No data in the genesis block
            'hash': self.hash_block({
                'index': 0,
                'previous_hash': '0',
                'data': None
            })
        }
        self.chain.append(genesis_block)

    def create_block(self, previous_hash):
        block = {
            'index': len(self.chain),  # Index starts from 1 (after genesis block)
            'previous_hash': previous_hash,
            'data': None,  # Placeholder for encrypted data
            'hash': None
        }
        block['hash'] = self.hash_block(block)
        self.chain.append(block)
        return block

    def hash_block(self, block):
        block_string = str(block['index']) + block['previous_hash'] + str(block['data'])
        return hashlib.sha256(block_string.encode()).hexdigest()

    def add_data_to_block(self, block_index, data):
        encrypted_data = xor_encrypt(data)
        self.chain[block_index]['data'] = base64.b64encode(encrypted_data.encode()).decode()

# Initialize blockchain
blockchain = Blockchain()

# Add encrypted genetic data to the blockchain (starting from block 2)
for index, row in df.iterrows():
    block = blockchain.create_block(previous_hash=blockchain.chain[-1]['hash'])
    blockchain.add_data_to_block(block['index'], row['Genetic_Sequence'])

# Display the blockchain with encrypted data (skip the genesis block)
block_data = blockchain.chain[1:]  # Skip genesis block (block 0)

# Streamlit UI to simulate Blockchain & Encryption
st.title("Blockchain & Encryption Simulation for Genetic Data")

# Display buttons to trigger actions
display_blockchain = st.button("Show Blockchain & Encrypted Data")
simulate_hack = st.button("Simulate Hack Attempt")

# Only display the blockchain when the button is clicked
if display_blockchain:
    st.write("### Blockchain with Encrypted Genetic Data")
    for block in block_data:
        st.write(f"**Block {block['index']}**:")
        st.write(f"Previous Hash: {block['previous_hash']}")
        st.write(f"Encrypted Data: {block['data']}")
        st.write(f"Block Hash: {block['hash']}")
        st.write("\n")

# Simulate a hack attempt (altering or deleting data)
def simulate_hack(df):
    # Randomly choose a row to alter or delete
    hack_index = random.choice(df.index)
    attack_type = random.choice(['alter', 'delete'])

    if attack_type == 'alter':
        # Alter the genetic sequence of the selected individual
        new_sequence = ''.join(random.choices('ACGT', k=8))  # Generate a new random sequence
        df.at[hack_index, 'Genetic_Sequence'] = new_sequence
        return f"Data altered for Person {df.at[hack_index, 'Person_ID']}."

    elif attack_type == 'delete':
        # Delete the row for the selected individual
        df.drop(hack_index, inplace=True)
        return f"Data deleted for Person {df.at[hack_index, 'Person_ID']}."

# Display button to simulate hack
if simulate_hack:
    hack_result = simulate_hack(df)
    st.write(hack_result)

    # Display the updated DataFrame after hack attempt
    st.write("### Updated Genetic Data (After Hack Attempt)")
    st.write(df)
