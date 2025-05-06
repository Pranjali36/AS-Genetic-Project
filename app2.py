import streamlit as st
import pandas as pd
import hashlib
import base64
import random

st.title("🔐 App 2: Genetic Data Protection Using Blockchain & Encryption")

# Step 1: Sample Genetic Data (same as App1)
def generate_sequence(length=10):
    return ''.join(random.choices('ATCG', k=length))

data = {
    'Person_ID': [f'P{i+1}' for i in range(10)],
    'Genetic_Sequence': [generate_sequence() for _ in range(10)],
}
df = pd.DataFrame(data)
st.subheader("Step 1: Original Genetic Data")
st.dataframe(df)

# Step 2: Encryption function
def xor_encrypt(data, key=123):
    return ''.join(chr(ord(c) ^ key) for c in data)

# Step 3: Blockchain structure
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(data="INITIAL_BLOCK")

    def create_block(self, data):
        previous_hash = self.chain[-1]['hash'] if self.chain else '0'
        block = {
            'index': len(self.chain),
            'data': data,
            'previous_hash': previous_hash,
            'hash': self.hash_block(data, previous_hash)
        }
        self.chain.append(block)

    def hash_block(self, data, previous_hash):
        raw = str(data) + previous_hash
        return hashlib.sha256(raw.encode()).hexdigest()

# Step 4: Encrypt and add each row to blockchain
blockchain = Blockchain()
encrypted_data = []

for _, row in df.iterrows():
    encrypted_seq = xor_encrypt(row['Genetic_Sequence'])
    encoded = base64.b64encode(encrypted_seq.encode()).decode()
    encrypted_data.append(encoded)
    blockchain.create_block(encoded)

st.subheader("Step 2: Blockchain with Encrypted Genetic Data")
block_data = pd.DataFrame([{
    'Block Index': blk['index'],
    'Encrypted Data': blk['data'],
    'Hash': blk['hash']
} for blk in blockchain.chain])
st.dataframe(block_data)

# Step 5: Attempt to hack encrypted blockchain (should fail)
if st.button("🚫 Attempt Hack on Secured Data"):
    hacked_index = random.randint(0, len(blockchain.chain)-1)

    if hacked_index == 0:
        st.warning("Tampering Genesis Block skipped. Selecting another block.")
        hacked_index = 1

    original_hash = blockchain.chain[hacked_index]['hash']
    blockchain.chain[hacked_index]['data'] = "HACKED_DATA"
    blockchain.chain[hacked_index]['hash'] = blockchain.hash_block("HACKED_DATA", blockchain.chain[hacked_index]['previous_hash'])

    # Verify integrity
    for i in range(1, len(blockchain.chain)):
        expected_hash = blockchain.hash_block(
            blockchain.chain[i]['data'], blockchain.chain[i]['previous_hash']
        )
        if blockchain.chain[i]['hash'] != expected_hash:
            st.error("🔐 ALERT: Blockchain tampering detected! Unauthorized data change rejected.")
            break
    else:
        st.success("✅ Blockchain is intact. Data remains secure.")

    st.subheader("Final Blockchain State")
    st.dataframe(pd.DataFrame([{
        'Block Index': blk['index'],
        'Encrypted Data': blk['data'],
        'Hash': blk['hash']
    } for blk in blockchain.chain]))
