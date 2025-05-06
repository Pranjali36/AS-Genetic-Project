import hashlib
import base64
import pandas as pd
import streamlit as st

# Simple XOR encryption function (for demonstration purposes)
def xor_encrypt(data, key=123):
    return ''.join(chr(ord(c) ^ key) for c in data)

# Simulate blockchain structure for storing encrypted data
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(previous_hash='0')

    def create_block(self, previous_hash):
        block = {
            'index': len(self.chain) + 1,
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

# Load or create the dataset (This should match the dataset in Cell 4)
df = pd.DataFrame({
    'Person_ID': range(1, 6),
    'Genetic_Sequence': ['ATCGATCGGT', 'CGTACGATAC', 'GCTAGCTAGG', 'TGCATGCAAG', 'ACGTACGTAA']
})

# Streamlit UI for Cell 5 - Encryption + Blockchain Simulation
st.write("## Encryption + Blockchain Simulation")
st.write("This is how genetic data can be secured using encryption and blockchain.")

# Initialize blockchain
blockchain = Blockchain()

# Add encrypted genetic data to the blockchain
for index, row in df.iterrows():
    block = blockchain.create_block(previous_hash=blockchain.chain[-1]['hash'])
    blockchain.add_data_to_block(block['index'] - 1, row['Genetic_Sequence'])

# Display the blockchain with encrypted genetic data
st.write("### Blockchain with Encrypted Data")
for block in blockchain.chain:
    st.write(f"Block {block['index']}: Data: {block['data']}, Hash: {block['hash']}, Previous Hash: {block['previous_hash']}")

# Validate blockchain integrity
def validate_blockchain(blockchain):
    for i in range(1, len(blockchain)):
        if blockchain[i]['previous_hash'] != blockchain[i-1]['hash']:
            return False, i  # Invalid blockchain at the given block
    return True, None

valid, error_block = validate_blockchain(blockchain)
if valid:
    st.write("Blockchain is valid. Data integrity is maintained.")
else:
    st.write(f"Blockchain is invalid at block {error_block}. Data integrity has been compromised!")
