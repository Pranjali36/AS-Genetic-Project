import streamlit as st
import hashlib
import random
import base64
import pandas as pd  # Import pandas for data handling

# Dummy data representing genetic data
data = {
    'ID': range(10),
    'Genetic_Sequence': [
        'ATGCATGCATGC', 'GTCAGTCA', 'AGTCTGAC', 'TGCATGCATGCT', 'GCTAGCTAG',
        'AGCTAGCTAG', 'TGCAGTGCAT', 'GATGAGTAGT', 'TGCAGTGCATG', 'TACGATGCAT'
    ]
}

# Function to encrypt genetic sequence (simple example)
def encrypt_sequence(sequence):
    return base64.b64encode(sequence.encode()).decode()

# Function to generate hash for blockchain
def hash_block(index, data, previous_hash):
    block_string = str(index) + str(data) + str(previous_hash)
    return hashlib.sha256(block_string.encode()).hexdigest()

# Blockchain class to handle the blocks and blockchain functionality
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(previous_hash='0')

    def create_block(self, previous_hash):
        block = {
            'Index': len(self.chain) + 1,
            'Previous Hash': previous_hash,
            'Encrypted Data': None,
            'Hash': None
        }
        block['Hash'] = self.hash_block(block)
        self.chain.append(block)
        return block

    def hash_block(self, block):
        block_string = str(block['Index']) + block['Previous Hash'] + str(block['Encrypted Data'])
        return hashlib.sha256(block_string.encode()).hexdigest()

    def add_data_to_block(self, block_index, data):
        encrypted_data = encrypt_sequence(data)
        self.chain[block_index]['Encrypted Data'] = encrypted_data
        self.chain[block_index]['Hash'] = self.hash_block(self.chain[block_index])

# Initialize blockchain
blockchain = Blockchain()

# Create blockchain and add encrypted data
for i, seq in enumerate(data['Genetic_Sequence']):
    block = blockchain.create_block(previous_hash=blockchain.chain[-1]['Hash'])
    blockchain.add_data_to_block(block['Index'] - 1, seq)

# Function to simulate a hack attempt
def attempt_hack_on_copy(blockchain_copy, tamper_probability=0.5):
    if random.random() < tamper_probability:
        tampered_index = random.choice(range(len(blockchain_copy)))
        blockchain_copy[tampered_index]['Encrypted Data'] = encrypt_sequence('ALTERED_SEQUENCE')
        blockchain_copy[tampered_index]['Hash'] = hash_block(
            blockchain_copy[tampered_index]['Index'],
            blockchain_copy[tampered_index]['Encrypted Data'],
            blockchain_copy[tampered_index]['Previous Hash']
        )
        return tampered_index  # Returns the tampered index
    else:
        return None  # No tampering this time

# Streamlit app for displaying the flow
st.title('Genetic Data Security: Blockchain & Encryption Demo')

st.subheader('Original Blockchain Data')

# Display original blockchain data
block_data = {
    'Index': [block['Index'] for block in blockchain.chain],
    'Previous Hash': [block['Previous Hash'] for block in blockchain.chain],
    'Encrypted Data': [block['Encrypted Data'] for block in blockchain.chain],
    'Hash': [block['Hash'] for block in blockchain.chain]
}
block_df = pd.DataFrame(block_data)
st.write(block_df)

# Create a copy of the blockchain for hacking
blockchain_copy = [block.copy() for block in blockchain.chain]

# Initialize tampered_index to None
tampered_index = None

# Buttons for actions
col1, col2 = st.columns(2)
with col1:
    if st.button('Attempt Hack'):
        tampered_index = attempt_hack_on_copy(blockchain_copy)
        if tampered_index is not None:
            tampered_block = blockchain_copy[tampered_index]
            st.error(f"🔓 Data altered for Person {tampered_block['Index']}!")
            st.write(pd.DataFrame([tampered_block]))
        else:
            st.success("No tampering detected. Blockchain is secure.")

with col2:
    if st.button('Check Blockchain Integrity'):
        if tampered_index is not None:
            tampered_blocks = [block for block in blockchain_copy if block['Hash'] != blockchain.chain[block['Index']-1]['Hash']]
            if len(tampered_blocks) > 0:
                st.error("🔒 Alert: Blockchain data integrity violated! Tampering attempt identified.")
                tampered_block_data = pd.DataFrame({
                    'Index': [block['Index'] for block in tampered_blocks],
                    'Previous Hash': [block['Previous Hash'] for block in tampered_blocks],
                    'Encrypted Data': [block['Encrypted Data'] for block in tampered_blocks],
                    'Hash': [block['Hash'] for block in tampered_blocks]
                })
                st.write(tampered_block_data)
            else:
                st.success("Blockchain verified: No tampering detected.")
        else:
            st.success("Blockchain verified: No tampering detected.")

# Display the comparison of original and tampered data
if tampered_index is not None:
    st.subheader("Original vs. Secured Data (After Hack Attempt)")
    comparison_df = pd.DataFrame({
        'Original Data': [block['Encrypted Data'] for block in blockchain.chain],
        'Secured Data (After Hack Attempt)': [block['Encrypted Data'] for block in blockchain_copy]
    })
    st.write(comparison_df)
