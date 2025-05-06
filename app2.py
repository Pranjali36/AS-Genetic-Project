import streamlit as st
import pandas as pd
import hashlib
import base64
import copy

# --- Utility Functions ---
def xor_encrypt(data, key=123):
    return ''.join(chr(ord(char) ^ key) for char in data)

def hash_block(index, previous_hash, data):
    block_string = f"{index}{previous_hash}{data}"
    return hashlib.sha256(block_string.encode()).hexdigest()

# --- Blockchain Class ---
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = {
            'index': 0,
            'previous_hash': '0',
            'data': 'INITIAL_BLOCK',
            'hash': hash_block(0, '0', 'INITIAL_BLOCK')
        }
        self.chain.append(genesis_block)

    def add_block(self, data):
        index = len(self.chain)
        previous_hash = self.chain[-1]['hash']
        encrypted_data = base64.b64encode(xor_encrypt(data).encode()).decode()
        block_hash = hash_block(index, previous_hash, encrypted_data)
        block = {
            'index': index,
            'previous_hash': previous_hash,
            'data': encrypted_data,
            'hash': block_hash
        }
        self.chain.append(block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            prev = self.chain[i - 1]
            curr = self.chain[i]
            recalculated_hash = hash_block(curr['index'], curr['previous_hash'], curr['data'])
            if curr['hash'] != recalculated_hash or curr['previous_hash'] != prev['hash']:
                return False
        return True

# --- App UI ---
st.title("App 2: Encryption and Blockchain Secured Genetic Data")

# Step 1: Generate Dummy Data
df = pd.DataFrame({
    'Name': [f'Person {i}' for i in range(10)],
    'Age': [30 + i for i in range(10)],
    'Gender': ['M', 'F'] * 5,
    'Genetic_Sequence': [f"ATGCGA{i}" for i in range(10)]
})

if 'blockchain' not in st.session_state:
    blockchain = Blockchain()
    for seq in df['Genetic_Sequence']:
        blockchain.add_block(seq)
    st.session_state.blockchain = blockchain
    st.session_state.original_chain = copy.deepcopy(blockchain.chain)

st.write("✅ Blockchain applied and genetic data encrypted & stored securely.")

# Step 2: View Blockchain
if st.button("Show Encrypted Blockchain Data"):
    display_df = pd.DataFrame(st.session_state.blockchain.chain)
    st.dataframe(display_df[['index', 'data', 'hash']])

# Step 3: Attempt to Tamper Copy (not original)
if st.button("Attempt Hack on Secured Data"):
    tampered_chain = copy.deepcopy(st.session_state.blockchain.chain)
    tampered_index = 5  # Let's try to tamper block 5
    tampered_chain[tampered_index]['data'] = base64.b64encode("HACKED_SEQUENCE".encode()).decode()
    
    # Validate tampered chain against original
    original = st.session_state.original_chain
    status = []
    for i in range(len(original)):
        if i < len(tampered_chain):
            is_same = tampered_chain[i]['data'] == original[i]['data'] and tampered_chain[i]['hash'] == original[i]['hash']
        else:
            is_same = False
        status.append("✔️ Unchanged" if is_same else "❌ Tampered")

    comp_df = pd.DataFrame({
        'Index': [blk['index'] for blk in tampered_chain],
        'Data': [blk['data'] for blk in tampered_chain],
        'Hash': [blk['hash'] for blk in tampered_chain],
        'Status': status
    })

    st.warning("⚠️ Hack Attempt Detected! The following blocks were verified:")
    st.dataframe(comp_df)

    if all(s == "✔️ Unchanged" for s in status):
        st.success("✅ Blockchain verified: No tampering detected.")
    else:
        st.error("🔒 Alert: Blockchain data integrity violated! Tampering attempt identified.")

# Final Note
st.markdown("""
---
🔐 This demo shows that even if someone tries to alter data on a copy, the **original blockchain remains intact**. 
Only GenBank admins with authority can access or approve sequence submissions.
""")
