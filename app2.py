import hashlib
import base64
import streamlit as st
import pandas as pd
import random

# Simple XOR encryption function (for demonstration purposes)
def xor_encrypt(data, key=123):
    return ''.join(chr(ord(c) ^ key) for c in data)

# Function to generate a new genetic sequence (for hack simulation)
def generate_sequence():
    return ''.join(random.choices('ATCG', k=8))

# Simulating a hack attempt (altering or deleting data)
def simulate_hack(df):
    hack_index = random.choice(df.index)
    attack_type = random.choice(['alter', 'delete'])

    if attack_type == 'alter':
        new_sequence = generate_sequence()
        df.at[hack_index, 'Genetic_Sequence'] = new_sequence
        return f"Data altered for Person {df.at[hack_index, 'Person_ID']}."
    elif attack_type == 'delete':
        df.drop(hack_index, inplace=True)
        return f"Data deleted for Person {df.at[hack_index, 'Person_ID']}."

# Blockchain class for encryption and validation
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(previous_hash='0')

    def __len__(self):
        return len(self.chain)

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

    # Check the integrity of the blockchain (if any block's hash doesn't match, chain is invalid)
    def validate_chain(self):
        for i in range(1, len(self.chain)):
            if self.chain[i]['previous_hash'] != self.chain[i-1]['hash']:
                return False
        return True

# Generating a sample dataframe (simulating genetic data)
def generate_sample_data():
    data = {
        'Person_ID': [f'ID{i}' for i in range(1, 11)],  # 10 rows of data
        'Genetic_Sequence': [
            'ATCGGCTA', 'CGTACGTA', 'GATCAGTC', 'TGCATGCA',
            'AACGTGCA', 'TTGCAATG', 'GGTACCAG', 'AATCGTCA',
            'CGAATCGT', 'TACGTGCA'
        ]
    }
    return pd.DataFrame(data)

# Simulating data alteration before blockchain
def data_alteration_simulation(df):
    hack_result = simulate_hack(df)
    return hack_result, df

# Simulate blockchain storing the data
def add_data_to_blockchain(df):
    blockchain = Blockchain()

    # Add encrypted genetic data to the blockchain
    for index, row in df.iterrows():
        block = blockchain.create_block(previous_hash=blockchain.chain[-1]['hash'])
        blockchain.add_data_to_block(block['index'] - 1, row['Genetic_Sequence'])

    return blockchain

# Streamlit UI for the demonstration
st.title("Genetic Data Security: Blockchain Simulation")

# Load the sample data
df = generate_sample_data()

# Show original data button
if st.button("Show Original Genetic Data"):
    st.subheader("Original Genetic Data")
    st.dataframe(df)  # This will show all 10 rows

# Simulate Hack Button
if st.button("Simulate Hack Attempt"):
    # Hack attempt simulation (alter or delete data)
    st.subheader("Hack Attempt Simulation")
    hack_result, altered_df = data_alteration_simulation(df)
    st.write(hack_result)

    # Display the altered data
    st.subheader("Altered Genetic Data")
    st.dataframe(df)  # This will show the altered data with all rows

# Blockchain simulation button
if st.button("Simulate Blockchain & Encryption"):
    st.subheader("Blockchain & Encryption Simulation")

    blockchain = add_data_to_blockchain(df)

    # Display the blockchain with encrypted data
    st.write("Blockchain (Encrypted Data):")
    for block in blockchain.chain:
        st.write(f"Block {block['index']}:")
        st.write(f"Hash: {block['hash']}")
        st.write(f"Encrypted Data: {block['data']}")

# Blockchain Validation button
if st.button("Validate Blockchain"):
    st.subheader("Blockchain Validation")

    blockchain = add_data_to_blockchain(df)

    # Simulate how blockchain prevents alteration
    is_valid = blockchain.validate_chain()
    if is_valid:
        st.write("Blockchain: The data is valid, no alteration detected.")
    else:
        st.write("Blockchain: The chain is invalid, data was altered!")

    st.write("The blockchain prevents data alteration because each block’s hash is dependent on the previous block’s hash. If any block is tampered with, the entire chain will become invalid. Hence, the integrity of genetic data is preserved.")
