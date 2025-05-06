import streamlit as st
import pandas as pd
import random
import hashlib
import base64

st.set_page_config(page_title="Blockchain Simulation", layout="wide")

st.title("🔐 Blockchain & Encryption Simulation for Genetic Data Security")

# Session state initialization
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame({
        'Person_ID': [f'P{i:03}' for i in range(10)],
        'Name': [f'Person_{i}' for i in range(10)],
        'Age': [random.randint(20, 50) for _ in range(10)],
        'Gender': [random.choice(['M', 'F']) for _ in range(10)],
        'Location': [random.choice(['City A', 'City B']) for _ in range(10)],
        'Disease': [random.choice(['None', 'Diabetes', 'Cancer', 'Flu']) for _ in range(10)],
        'Sample_Date': pd.date_range(start='2023-01-01', periods=10, freq='M').strftime('%Y-%m-%d'),
        'Genetic_Sequence': [''.join(random.choices('ATCG', k=20)) for _ in range(10)],
        'Accession_Number': [f'ACN{i:05}' for i in range(10)],
        'Verified': ['Yes'] * 10
    })

if 'original_data' not in st.session_state:
    st.session_state.original_data = st.session_state.df.copy()

if 'blockchain_applied' not in st.session_state:
    st.session_state.blockchain_applied = False

# --------------------- Utility Functions ---------------------

def generate_sequence():
    return ''.join(random.choices('ATCG', k=20))

def simulate_hack(df):
    hack_index = random.choice(df.index)
    attack_type = random.choice(['alter', 'delete'])

    if attack_type == 'alter':
        new_sequence = generate_sequence()
        df.at[hack_index, 'Genetic_Sequence'] = new_sequence
        return f"⚠️ Data ALTERED for Person {df.at[hack_index, 'Person_ID']}.", df

    elif attack_type == 'delete':
        deleted_person = df.at[hack_index, 'Person_ID']
        df.drop(hack_index, inplace=True)
        return f"⚠️ Data DELETED for Person {deleted_person}.", df

def xor_encrypt(data, key=123):
    return ''.join(chr(ord(c) ^ key) for c in data)

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(previous_hash='0')

    def create_block(self, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'previous_hash': previous_hash,
            'data': None,
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

# ------------------ Streamlit UI Logic ------------------

st.markdown("### Step 1: Simulate Hack Attempt")
st.info("This step simulates an attack on the genetic data before any security is applied.")

if st.button("🛠️ Simulate Hack Attempt"):
    if not st.session_state.blockchain_applied:
        result, updated_df = simulate_hack(st.session_state.df)
        st.session_state.df = updated_df
        st.warning(result)
        st.write("📊 Updated Genetic Data (After Hack Attempt):")
        st.dataframe(st.session_state.df)
    else:
        st.error("❌ Hack attempt failed. Blockchain security is active.")
        st.write("🔐 Secured Genetic Data remains unchanged:")
        st.dataframe(st.session_state.df)

st.markdown("---")
st.markdown("### Step 2: Apply Blockchain Encryption")
st.info("Now, we apply encryption and store the data in a blockchain. This will prevent future tampering.")

if st.button("🔐 Apply Blockchain & Encrypt Data"):
    blockchain = Blockchain()
    for index, row in st.session_state.df.iterrows():
        block = blockchain.create_block(previous_hash=blockchain.chain[-1]['hash'])
        blockchain.add_data_to_block(block['index'] - 1, row['Genetic_Sequence'])

    st.session_state.blockchain_applied = True

    st.success("✅ Blockchain Encryption Applied. Here's the secured data:")
    for block in blockchain.chain[1:]:  # Skip genesis block
        st.write(f"**Block {block['index']}** | Hash: `{block['hash']}`")
        st.write(f"🔒 Encrypted Data: `{block['data']}`")

st.markdown("---")
st.markdown("### Step 3: Final Comparison to Prove Data Integrity")
st.info("After blockchain encryption, we compare the current data with the original to prove it is untampered.")

if st.session_state.blockchain_applied:
    comparison_df = pd.DataFrame({
        'Original Genetic Sequence': st.session_state.original_data['Genetic_Sequence'],
        'Secured Genetic Sequence': st.session_state.df['Genetic_Sequence']
    })
    comparison_df['Match'] = comparison_df['Original Genetic Sequence'] == comparison_df['Secured Genetic Sequence']
    st.dataframe(comparison_df)
else:
    st.warning("⚠️ Apply Blockchain encryption first to see the comparison.")
