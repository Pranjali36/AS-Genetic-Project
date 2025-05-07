import streamlit as st
import hashlib
import pandas as pd
import base64
import copy

# ---------- Helper Functions ----------

def encrypt_data(data, token):
    encoded = base64.b64encode(f"{data}:{token}".encode()).decode()
    return encoded

def decrypt_data(encrypted_data, token):
    decoded = base64.b64decode(encrypted_data).decode()
    original_data, provided_token = decoded.rsplit(":", 1)
    return original_data if provided_token == token else None

def calculate_hash(index, data, prev_hash):
    block_string = f"{index}{data}{prev_hash}"
    return hashlib.sha256(block_string.encode()).hexdigest()

def create_block(index, data, prev_hash):
    return {
        "Index": index,
        "Encrypted Data": data,
        "Previous Hash": prev_hash,
        "Hash": calculate_hash(index, data, prev_hash)
    }

def build_blockchain(data_records, admin_token):
    blockchain = []
    prev_hash = "0"  # Genesis block
    for i, record in enumerate(data_records):
        encrypted_data = encrypt_data(record, admin_token)
        block = create_block(i, encrypted_data, prev_hash)
        blockchain.append(block)
        prev_hash = block["Hash"]
    return blockchain

def tamper_blockchain(blockchain_copy, index_to_tamper, tampered_data, fake_token):
    encrypted = encrypt_data(tampered_data, fake_token)
    blockchain_copy[index_to_tamper]["Encrypted Data"] = encrypted
    # Recalculate hashes from tampered block onward
    for i in range(index_to_tamper, len(blockchain_copy)):
        prev_hash = blockchain_copy[i-1]["Hash"] if i > 0 else "0"
        blockchain_copy[i]["Previous Hash"] = prev_hash
        blockchain_copy[i]["Hash"] = calculate_hash(i, blockchain_copy[i]["Encrypted Data"], prev_hash)
    return blockchain_copy

def compare_chains(original_chain, tampered_chain):
    tampered_indices = []
    for i, (orig, temp) in enumerate(zip(original_chain, tampered_chain)):
        if orig["Hash"] != temp["Hash"]:
            tampered_indices.append(i)
    return tampered_indices

# ---------- Streamlit App ----------

st.set_page_config(layout="wide")
st.title("🧬 GeneBlock: Securing Genetic Data with Blockchain & Encryption")
st.markdown("---")

# Step 1: Define dummy genetic records
genetic_data = [
    "BRCA1 mutation, sample A12",
    "TP53 variant, sample B04",
    "CFTR abnormality, sample C89"
]

admin_token = "secure_token_123"

# Step 2: Build blockchain (first time only)
if "blockchain" not in st.session_state:
    st.session_state.blockchain = build_blockchain(genetic_data, admin_token)
    st.session_state.original_chain = copy.deepcopy(st.session_state.blockchain)
    st.session_state.tampered_chain = None
    st.session_state.report_view = False

# Step 3: Display Blockchain
st.subheader("🔗 Blockchain View")
df = pd.DataFrame(st.session_state.blockchain)
st.dataframe(df)

# Step 4: Tamper Simulation
st.subheader("⚠️ Attempt Hack on Blockchain")
if st.button("Simulate Hack Attempt"):
    st.session_state.tampered_chain = tamper_blockchain(copy.deepcopy(st.session_state.blockchain), 1, "Fake mutation, sample Z99", "hacker_token")
    st.session_state.report_view = True
    st.warning("Tampering attempt simulated on Block 1.")

# Step 5: Integrity Check
if st.session_state.report_view:
    if st.button("View Tamper Report"):
        tampered_indices = compare_chains(st.session_state.original_chain, st.session_state.tampered_chain)
        if tampered_indices:
            st.error(f"🔒 Alert: Blockchain integrity violated at Block(s): {tampered_indices}")
            report_df = pd.DataFrame(st.session_state.tampered_chain)
            st.dataframe(report_df.style.apply(
                lambda row: ['background-color: red' if row.name in tampered_indices else '' for _ in row], axis=1))
        else:
            st.success("✅ Blockchain verified: No tampering detected.")

# Step 6: Decryption (Admin-Only)
st.subheader("🔑 Admin Data Access")
user_token = st.text_input("Enter access token to decrypt records:", type="password")

if st.button("Decrypt Genetic Data"):
    decrypted = [decrypt_data(block["Encrypted Data"], user_token) for block in st.session_state.blockchain]
    if all(d is not None for d in decrypted):
        st.success("✅ Access granted.")
        for i, d in enumerate(decrypted):
            st.write(f"Record {i+1}: {d}")
    else:
        st.error("❌ Access denied. Invalid token.")

st.markdown("---")
st.caption("Built with ❤️ for Advanced Security in Genetic Data Systems")
