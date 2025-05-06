import streamlit as st
import pandas as pd
import hashlib
import base64
import random
import copy

# ---------- Helper Functions ----------

def generate_sequence():
    return ''.join(random.choices('ATGC', k=10))

def encrypt_sequence(seq):
    return base64.b64encode(seq.encode()).decode()

def hash_block(index, encrypted_data, previous_hash):
    value = f"{index}{encrypted_data}{previous_hash}".encode()
    return hashlib.sha256(value).hexdigest()

def create_blockchain(data):
    blockchain = []
    previous_hash = '0'

    for i, row in data.iterrows():
        encrypted_data = encrypt_sequence(row['Sequence'])
        block_hash = hash_block(i, encrypted_data, previous_hash)
        blockchain.append({
            'Index': i,
            'Encrypted Data': encrypted_data,
            'Hash': block_hash,
            'Previous Hash': previous_hash
        })
        previous_hash = block_hash

    return blockchain

def attempt_hack_on_copy(blockchain_copy):
    tampered_index = random.choice(range(len(blockchain_copy)))
    blockchain_copy[tampered_index]['Encrypted Data'] = encrypt_sequence(generate_sequence())
    blockchain_copy[tampered_index]['Hash'] = hash_block(
        blockchain_copy[tampered_index]['Index'],
        blockchain_copy[tampered_index]['Encrypted Data'],
        blockchain_copy[tampered_index]['Previous Hash']
    )
    return tampered_index

def compare_blockchains(original, tampered):
    tampered_blocks = []
    for orig, tam in zip(original, tampered):
        if orig['Hash'] != tam['Hash']:
            tampered_blocks.append({
                'Block Index': orig['Index'],
                'Original Hash': orig['Hash'],
                'Tampered Hash': tam['Hash'],
                'Status': '❌ Tampered'
            })
        else:
            tampered_blocks.append({
                'Block Index': orig['Index'],
                'Original Hash': orig['Hash'],
                'Tampered Hash': tam['Hash'],
                'Status': '✅ Untouched'
            })
    return tampered_blocks

# ---------- Streamlit App ----------

st.title("🔐 App 2: Securing Genetic Data with Blockchain + Encryption")

# Step 1: Generate original data
if 'original_data' not in st.session_state:
    st.session_state.original_data = pd.DataFrame({
        'Person ID': [f'Person {i+1}' for i in range(10)],
        'Sequence': [generate_sequence() for _ in range(10)],
    })

# Step 2: Apply blockchain encryption
if st.button("🔗 Apply Blockchain + Encryption"):
    st.session_state.blockchain = create_blockchain(st.session_state.original_data)
    st.session_state.blockchain_applied = True
    st.success("Blockchain and encryption applied successfully.")

# Step 3: Attempt hack on a copy
if st.session_state.get('blockchain_applied', False):
    if st.button("🚨 Attempt Hack on Secured Data"):
        st.session_state.tampered_copy = copy.deepcopy(st.session_state.blockchain)
        tampered_index = attempt_hack_on_copy(st.session_state.tampered_copy)
        st.session_state.tampered_blocks = compare_blockchains(st.session_state.blockchain, st.session_state.tampered_copy)
        st.warning("🔒 Alert: Blockchain data integrity violated! Tampering attempt identified.")

# Step 4: View tamper report
if st.session_state.get('tampered_blocks', None):
    if st.button("📋 View Tamper Report"):
        tamper_df = pd.DataFrame(st.session_state.tampered_blocks)
        st.dataframe(tamper_df)

        if all(b['Status'] == '✅ Untouched' for b in st.session_state.tampered_blocks):
            st.success("Blockchain verified: No tampering detected.")
        else:
            st.error("Some blocks were tampered. Original blockchain remains intact.")

# Optional: Reset
st.sidebar.title("Options")
if st.sidebar.button("🔄 Reset App"):
    st.session_state.clear()
    st.experimental_rerun()
