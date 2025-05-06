import streamlit as st
import pandas as pd
import hashlib
import base64
import random

# Sample data for genetic sequences
data = {
    'Person_ID': [f'P{i}' for i in range(10)],
    'Genetic_Sequence': [
        'ATCGTACG', 'GGTCTAGG', 'AACGGTTC', 'CTAGCTAG', 'GTCTTCCA',
        'GACGTCAG', 'TGCATGCG', 'AACCTGGA', 'GGATACCA', 'TCGGAATA'
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Display original data in the sidebar
st.sidebar.header("Original Genetic Data")
st.sidebar.write(df)

# Generate a random genetic sequence for hacking attempts
def generate_sequence():
    return ''.join(random.choices('ACGT', k=8))

# Simulating a hack attempt (altering or deleting data)
def simulate_hack(df):
    # Randomly choose a row to alter or delete
    hack_index = random.choice(df.index)
    attack_type = random.choice(['alter', 'delete'])

    if attack_type == 'alter':
        # Alter the genetic sequence of the selected individual
        new_sequence = generate_sequence()
        df.at[hack_index, 'Genetic_Sequence'] = new_sequence
        return f"Data altered for Person {df.at[hack_index, 'Person_ID']}."

    elif attack_type == 'delete':
        # Delete the row for the selected individual
        df.drop(hack_index, inplace=True)
        return f"Data deleted for Person {df.at[hack_index, 'Person_ID']}."

# Simple XOR encryption function (for demonstration purposes)
def xor_encrypt(data, key=123):
    return ''.join(chr(ord(c) ^ key) for c in data)

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(previous_hash='0')  # Initialize with the first block, which will have encrypted data

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

# Initialize blockchain
blockchain = Blockchain()

# Simulate the hack attempt (alteration or deletion) and update the blockchain
hack_result = ''
if st.button('Simulate Hack Attempt'):
    hack_result = simulate_hack(df)
    st.write(hack_result)

# Display updated data after hack attempt
st.write("Updated Genetic Data (After Hack Attempt):")
st.write(df)

# Apply blockchain to secure the data
if st.button('Apply Blockchain & Encryption'):
    # First block should now have encrypted data (not 'INITIAL_BLOCK')
    block = blockchain.create_block(previous_hash='0')  # Create the first block
    blockchain.add_data_to_block(block['index'] - 1, df.iloc[0]['Genetic_Sequence'])  # Encrypt the first data point
    
    # Add encrypted genetic data to the blockchain
    for index, row in df.iterrows():
        block = blockchain.create_block(previous_hash=blockchain.chain[-1]['hash'])
        blockchain.add_data_to_block(block['index'] - 1, row['Genetic_Sequence'])

    # Display the blockchain with encrypted genetic data
    st.write("Blockchain with Encrypted Genetic Data:")
    blockchain_data = []
    for block in blockchain.chain:
        blockchain_data.append({
            'Block Index': block['index'],
            'Previous Hash': block['previous_hash'],
            'Encrypted Data': block['data'],
            'Hash': block['hash']
        })
    blockchain_df = pd.DataFrame(blockchain_data)
    st.write(blockchain_df)

# Comparison of original data and secured data
if st.button('Compare Original Data and Secured Data'):
    st.write("Comparison between Original Data and Secured Data:")
    
    original_data = df.copy()
    secured_data = []

    for block in blockchain.chain:
        # Show encrypted data as it is in blockchain
        secured_data.append({
            'Block Index': block['index'],
            'Encrypted Data': block['data']
        })
    
    comparison_df = pd.DataFrame(secured_data)
    st.write("Secured Data:")
    st.write(comparison_df)

    st.write("Original Data (Unchanged):")
    st.write(original_data)

# Final demonstration: Attempt to hack again after applying blockchain
if st.button('Simulate Hack Attempt Again (After Blockchain Applied)'):
    hack_result = simulate_hack(df)
    st.write(hack_result)
    
    # Blockchain data remains unaltered after hacking attempt
    blockchain_after_hack = []
    for block in blockchain.chain:
        blockchain_after_hack.append({
            'Block Index': block['index'],
            'Previous Hash': block['previous_hash'],
            'Encrypted Data': block['data'],
            'Hash': block['hash']
        })
    
    blockchain_after_hack_df = pd.DataFrame(blockchain_after_hack)
    st.write("Blockchain after Hack Attempt:")
    st.write(blockchain_after_hack_df)

    # Show that the original data remains intact (no tampering)
    comparison_df_after_hack = pd.DataFrame(secured_data)
    st.write("Secured Data (No Changes After Hack Attempt):")
    st.write(comparison_df_after_hack)
