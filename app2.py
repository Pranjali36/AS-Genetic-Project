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

# Save a copy of the original data for comparison later (no alteration allowed)
original_data = df.copy()

# Simple XOR encryption function (for demonstration purposes)
def xor_encrypt(data, key=123):
    return ''.join(chr(ord(c) ^ key) for c in data)

# Simulate blockchain structure for storing encrypted data
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = {
            'index': 0,
            'previous_hash': '0',
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
            'index': len(self.chain),  
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

# Explanation of the flow
st.write("### Step 1: Genetic Data and Hack Attempt")
st.write("""
Before applying any security measures, let's simulate the hack attempt and alter the genetic data.
Click the button below to simulate a hack attempt on the data.
""")

# Display button to simulate hack attempt
simulate_hack = st.button("Simulate Hack Attempt")

if simulate_hack:
    # Simulate a hack attempt (altering or deleting data)
    hack_index = random.choice(df.index)
    attack_type = random.choice(['alter', 'delete'])

    if attack_type == 'alter':
        # Alter the genetic sequence of the selected individual
        new_sequence = ''.join(random.choices('ACGT', k=8))  # Generate a new random sequence
        df.at[hack_index, 'Genetic_Sequence'] = new_sequence
        st.write(f"Data altered for Person {df.at[hack_index, 'Person_ID']}.")
    elif attack_type == 'delete':
        # Delete the row for the selected individual and reset the index
        df.drop(hack_index, inplace=True)
        df.reset_index(drop=True, inplace=True)  # Reset the index to avoid KeyError
        st.write(f"Data deleted for Person {df.at[hack_index, 'Person_ID']}.")

    st.write("### Updated Genetic Data (After Hack Attempt)")
    st.write(df)

    st.write("#### What happens now?")
    st.write("In the current dataset, you can see that the genetic data has been altered or deleted.")

# Provide instruction for next step
st.write("""
### Step 2: Apply Blockchain & Encryption
Now that we have simulated a hack attempt and seen how the data can be altered or deleted, 
let's apply blockchain and encryption to prevent unauthorized changes to the data.
Click the button below to apply blockchain and encryption, which will secure the data.
""")

# Display button to apply blockchain and encryption
display_blockchain = st.button("Apply Blockchain & Encryption")

if display_blockchain:
    # Display the blockchain with encrypted data
    st.write("### Blockchain with Encrypted Genetic Data")
    for block in block_data:
        st.write(f"**Block {block['index']}**:")
        st.write(f"Previous Hash: {block['previous_hash']}")
        st.write(f"Encrypted Data: {block['data']}")
        st.write(f"Block Hash: {block['hash']}")
        st.write("\n")

    st.write("""
    #### What happens now?
    Notice how the genetic data is encrypted and stored in the blockchain.
    If any attempt is made to alter the data, the hash of the block will change, invalidating the entire chain.
    Blockchain ensures the integrity of genetic data by preventing unauthorized changes.
    """)

    # Save the state after blockchain has been applied
    st.session_state.blockchain_applied = True
    st.session_state.df = df.copy()  # Save the df after blockchain application for consistency

# If blockchain has been applied, simulate unsuccessful hack attempt
if 'blockchain_applied' in st.session_state and st.session_state.blockchain_applied:
    st.write("""
    ### Attempt to Hack After Blockchain Applied
    Since blockchain and encryption are now applied, any attempt to alter the data will fail.
    Try to alter the data by clicking the button below.
    """)

    # Display button for hacking attempt after blockchain
    simulate_hack_post_blockchain = st.button("Simulate Hack Attempt After Blockchain")

    if simulate_hack_post_blockchain:
        # Show message explaining that tampering is no longer possible due to blockchain
        st.write("#### Hack Attempt Failed!")
        st.write("Any attempt to alter the data will now invalidate the blockchain and prevent unauthorized changes.")
        st.write("Blockchain technology has successfully protected the data integrity.")

        # Show the blockchain after attempted hack
        st.write("### Blockchain Data After Hack Attempt")
        for block in blockchain.chain[1:]:  # Skip genesis block
            st.write(f"**Block {block['index']}**:")
            st.write(f"Previous Hash: {block['previous_hash']}")
            st.write(f"Encrypted Data: {block['data']}")
            st.write(f"Block Hash: {block['hash']}")
            st.write("\n")

        st.write("### Comparison of Original and Secured Data")
        st.write("""
        Let's compare the original genetic data (before tampering) and the secured data after blockchain encryption.
        Notice how the genetic data has remained unchanged despite the hacking attempt.
        """)

        # Display original data vs secured data (side-by-side)
        # Display original vs secured genetic sequences only
            comparison_df = pd.DataFrame({
            'Original Genetic Sequence': original_data['Genetic_Sequence'],
        'Secured Genetic Sequence': st.session_state.df['Genetic_Sequence']
})
st.write(comparison_df)

# Final step: Show the original, untampered data to prove the integrity
st.write("""
### Final Step: Showing the Original Untampered Data
Now, let's show the original, untampered data again to prove that even after applying blockchain and encryption, 
the data remains intact and secure from hacking attempts.
""")

st.write("### Original Genetic Data (Before Any Tampering)")

# Display the original data, which could not be altered
st.write(original_data)

comparison_df['Match'] = comparison_df['Original Genetic Sequence'] == comparison_df['Secured Genetic Sequence']
st.write(comparison_df)

