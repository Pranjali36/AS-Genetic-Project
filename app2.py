import hashlib
import base64
import random
import pandas as pd
import streamlit as st

# Step 1: Generate dummy genetic data
def generate_dummy_data():
    data = {
        'Person_ID': [i for i in range(10)],
        'Genetic_Sequence': ['ATCG'*5 for _ in range(10)],
        'Accession_Number': ['ACC' + str(i).zfill(4) for i in range(10)]
    }
    return pd.DataFrame(data)

# Step 2: Simulate hack attempt (altering or deleting data)
def simulate_hack(df):
    # Reset index to avoid key errors when accessing rows after deletion
    df = df.reset_index(drop=True)
    hack_index = random.choice(df.index)
    attack_type = random.choice(['alter', 'delete'])

    if attack_type == 'alter':
        new_sequence = 'GCTA'*5  # Simulating a change in genetic sequence
        df.at[hack_index, 'Genetic_Sequence'] = new_sequence
        return df, f"Data altered for Person {df.at[hack_index, 'Person_ID']}."
    
    elif attack_type == 'delete':
        df.drop(hack_index, inplace=True)
        df = df.reset_index(drop=True)  # Reset index after deletion
        return df, f"Data deleted for Person {df.at[hack_index, 'Person_ID']}."

    return df, "No changes made."

# Step 3: Simple XOR encryption for demonstration
def xor_encrypt(data, key=123):
    return ''.join(chr(ord(c) ^ key) for c in data)

# Step 4: Simulate blockchain structure for storing encrypted data
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

# Step 5: Streamlit app for the user interaction
st.title("Genetic Data Security with Blockchain & Encryption")

# Step 6: Load original data
original_data = generate_dummy_data()
st.subheader("Original Genetic Data")
st.write(original_data)

# Store the modified data (hack attempt) in a session state variable
if 'hack_data' not in st.session_state:
    st.session_state.hack_data = original_data.copy()

# Step 7: Simulate hack attempt
hack_result = None

# Button to simulate hack attempt
if st.button("Simulate Hack Attempt"):
    # Perform hack attempt (modify or delete)
    st.session_state.hack_data, hack_result = simulate_hack(st.session_state.hack_data)
    st.write(hack_result)
    st.write("Updated Genetic Data (After Hack Attempt):")
    st.write(st.session_state.hack_data)

# Step 8: Apply Blockchain and Encryption
blockchain = Blockchain()  # Re-initialize blockchain to ensure fresh start
blockchain_applied = False  # Flag to track if blockchain has been applied
if st.button("Apply Blockchain & Encryption"):
    # Apply blockchain encryption to the original data
    for index, row in original_data.iterrows():
        block = blockchain.create_block(previous_hash=blockchain.chain[-1]['hash'])
        blockchain.add_data_to_block(block['index'] - 1, row['Genetic_Sequence'])

    blockchain_applied = True  # Set flag to True after blockchain is applied
    st.write("Blockchain and Encryption Applied!")
    st.write("Encrypted Blockchain Data:")
    st.write(blockchain.chain)

# Step 9: Simulate Hack Again (After Blockchain)
if blockchain_applied and st.button("Simulate Hack Again (After Blockchain)"):
    # Simulate the hack again after blockchain application
    st.session_state.hack_data, hack_result = simulate_hack(st.session_state.hack_data)
    st.write(hack_result)
    
    # Verify blockchain integrity after hack attempt
    st.write("Checking blockchain data integrity...")
    
    blockchain_integrity = True
    for block in blockchain.chain:
        if not block['hash'] == blockchain.hash_block(block):
            blockchain_integrity = False
    
    if blockchain_integrity:
        st.write("Blockchain verified: Data cannot be tampered!")
    else:
        st.write("Data integrity check failed!")
    
    # Display Original Data and Blockchain Data
    st.subheader("Original Data (Before Blockchain)")
    st.write(original_data)
    
    st.subheader("Secured Data (After Blockchain & Encryption)")
    for block in blockchain.chain:
        st.write(f"Block {block['index']} - Encrypted Data: {block['data']} - Hash: {block['hash']}")
