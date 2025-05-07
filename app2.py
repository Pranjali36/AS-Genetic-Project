import streamlit as st
import pandas as pd
import hashlib
import base64
import copy

# --- Helper Functions ---
def encrypt_data(data):
    encoded = base64.b64encode(data.encode('utf-8'))
    return encoded.decode('utf-8')

def decrypt_data(data):
    decoded = base64.b64decode(data.encode('utf-8'))
    return decoded.decode('utf-8')

def hash_block(block):
    block_string = f"{block['index']}{block['data']}{block['prev_hash']}"
    return hashlib.sha256(block_string.encode()).hexdigest()

def create_genesis_block():
    return {
        'index': 0,
        'data': 'INITIAL_BLOCK',
        'prev_hash': '0',
        'hash': hash_block({'index': 0, 'data': 'INITIAL_BLOCK', 'prev_hash': '0'})
    }

def create_block(index, data, prev_hash):
    block = {
        'index': index,
        'data': encrypt_data(data),
        'prev_hash': prev_hash
    }
    block['hash'] = hash_block(block)
    return block

def build_blockchain(records):
    blockchain = [create_genesis_block()]
    for i, data in enumerate(records, start=1):
        prev_hash = blockchain[-1]['hash']
        block = create_block(i, data, prev_hash)
        blockchain.append(block)
    return blockchain

def simulate_hack(chain_copy):
    tampered_chain = copy.deepcopy(chain_copy)
    tampered_chain[1]['data'] = encrypt_data("HACKED_SEQUENCE")
    tampered_chain[1]['hash'] = hash_block(tampered_chain[1])
    for i in range(2, len(tampered_chain)):
        tampered_chain[i]['prev_hash'] = tampered_chain[i - 1]['hash']
        tampered_chain[i]['hash'] = hash_block(tampered_chain[i])
    return tampered_chain

def compare_chains(original, tampered):
    tampered_indices = []
    for i in range(len(original)):
        if original[i]['hash'] != tampered[i]['hash']:
            tampered_indices.append(i)
    return tampered_indices

# --- Streamlit GUI ---
st.set_page_config(page_title="GeneBlock - Secure Genetic Data with Blockchain", layout="wide")
st.title("🔬 GeneBlock - Securing Genetic Data with Blockchain")

# Sample genetic records
genetic_records = ["ATCGATCG", "GGGTTTAA", "CTAGCTAG"]

# Create original blockchain
blockchain_main = build_blockchain(genetic_records)
# Copy for servers
blockchain_server2 = copy.deepcopy(blockchain_main)
blockchain_server3 = simulate_hack(copy.deepcopy(blockchain_main))

# Display all 3 server chains
st.subheader("🌐 Server Blockchains")
cols = st.columns(3)
for idx, chain in enumerate([blockchain_main, blockchain_server2, blockchain_server3]):
    with cols[idx]:
        st.markdown(f"**Server {idx + 1}** {'(Tampered)' if idx == 2 else '(Original)'}")
        for block in chain:
            st.code(f"Block {block['index']}:\nEncrypted: {block['data']}\nHash: {block['hash'][:15]}...\nPrev: {block['prev_hash'][:15]}...", language='text')

# Tamper report check
if st.button("🔍 View Tamper Report"):
    tampered_indices = compare_chains(blockchain_main, blockchain_server3)
    if tampered_indices:
        st.error("🔒 Alert: Blockchain data integrity violated on Server 3!")
        for i in tampered_indices:
            st.warning(f"⚠️ Block {i} was tampered.")
    else:
        st.success("✅ Blockchain verified: No tampering detected.")

# Admin token to decrypt
st.subheader("🔑 Decrypt Genetic Data")
admin_token = st.text_input("Enter access token to decrypt records:", type="password")
if st.button("Decrypt Genetic Data"):
    if admin_token == "ADMIN123":
        decrypted = [decrypt_data(block['data']) for block in blockchain_main[1:]]
        st.success("Access granted. Decrypted records:")
        st.table(pd.DataFrame({"Decrypted Data": decrypted}))
    else:
        st.error("❌ Invalid token. Access denied.")
