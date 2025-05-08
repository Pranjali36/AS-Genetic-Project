import streamlit as st
import hashlib
import base64
import copy
import random
from datetime import datetime
import pandas as pd

# ==== Encryption / Decryption ====
def encrypt_data(data):
    return base64.b64encode(data.encode()).decode()

def decrypt_data(encrypted_data):
    try:
        return base64.b64decode(encrypted_data.encode()).decode()
    except Exception:
        return "[Decryption Failed]"

# ==== Block Class ====
class Block:
    def __init__(self, index, timestamp, metadata, genetic_data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.metadata = metadata
        self.genetic_data = encrypt_data(genetic_data)
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_content = f"{self.index}{self.timestamp}{self.metadata}{self.genetic_data}{self.previous_hash}"
        return hashlib.sha256(block_content.encode()).hexdigest()

# ==== Create Blockchain ====
def create_blockchain():
    blockchain = []
    metadata_list = [
        {"Patient ID": "P001", "Test Date": "2023-08-01", "Sample Code": "S1"},
        {"Patient ID": "P002", "Test Date": "2023-08-02", "Sample Code": "S2"},
        {"Patient ID": "P003", "Test Date": "2023-08-03", "Sample Code": "S3"},
    ]
    dna_list = ["ATGCTACGATCG", "GGGCTAGCTTAC", "TACGGGCTAGCA"]
    prev_hash = "0"

    for i in range(3):
        block = Block(i, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), metadata_list[i], dna_list[i], prev_hash)
        blockchain.append(block)
        prev_hash = block.hash
    return blockchain

# ==== Setup Chains ====
original_chain = create_blockchain()
server_1 = copy.deepcopy(original_chain)
server_2 = copy.deepcopy(original_chain)
server_3 = copy.deepcopy(original_chain)
servers = {"Server 1": server_1, "Server 2": server_2, "Server 3": server_3}

if 'tamper_log' not in st.session_state:
    st.session_state.tamper_log = []

# ==== UI Setup ====
st.set_page_config(layout="wide")
st.title("🧬 GeneBlock App 4: Blockchain + Network Consensus")
st.markdown("Multiple server copies, admin-only access, real-time tamper detection, and **majority-based network validation**.")

# ==== Manual Tampering ====
st.subheader("🛠️ Tamper Block Metadata")
col1, col2 = st.columns(2)
with col1:
    server_to_edit = st.selectbox("Select Server:", ["Server 1", "Server 2", "Server 3"])
with col2:
    block_index = st.selectbox("Select Block Index to Edit:", [0, 1, 2])

target_block = servers[server_to_edit][block_index]
new_pid = st.text_input("New Patient ID", value=target_block.metadata["Patient ID"])
new_sample = st.text_input("New Sample Code", value=target_block.metadata["Sample Code"])

if st.button("✏Simulate Hack"):
    target_block.metadata["Patient ID"] = new_pid
    target_block.metadata["Sample Code"] = new_sample

    # Update this and all subsequent hashes
    chain = servers[server_to_edit]
    for i in range(block_index, len(chain)):
        prev_hash = chain[i-1].hash if i > 0 else "0"
        chain[i].previous_hash = prev_hash
        chain[i].hash = chain[i].calculate_hash()

    st.session_state.tamper_log.append({
        "Server": server_to_edit,
        "Block": block_index,
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Note": "Metadata manually tampered."
    })
    st.warning(f"⚠️ Block #{block_index} tampered on {server_to_edit}!")

# ==== Consensus Checking ====
def majority_hashes(index):
    hashes = [server[index].hash for server in servers.values()]
    return max(set(hashes), key=hashes.count)

def is_chain_valid(server_chain):
    for i, block in enumerate(server_chain):
        if block.hash != majority_hashes(i):
            return False
    return True

# ==== Display Chains with Consensus Status ====
st.subheader("🔗 Blockchain Status Across Network")
cols = st.columns(3)
color_map = {"valid": "#E8F5E9", "invalid": "#FFCDD2"}

for i, (label, chain) in enumerate(servers.items()):
    status = "valid" if is_chain_valid(chain) else "invalid"
    with cols[i]:
        st.markdown(f"**{label}** - {'✅ Accepted' if status == 'valid' else '❌ Rejected'}")
        for blk in chain:
            bg = color_map[status]
            st.markdown(f"""
                <div style="background-color:{bg}; padding:10px; border-radius:5px; margin-bottom:10px">
                    <strong>Block #{blk.index}</strong><br>
                    <strong>Timestamp:</strong> {blk.timestamp}<br>
                    <strong>Metadata:</strong> {blk.metadata}<br>
                    <strong>Prev Hash:</strong> {blk.previous_hash}...<br>
                    <strong>Hash:</strong> {blk.hash}...
                </div>
            """, unsafe_allow_html=True)

# ==== View Tamper Log ====
st.subheader("📄 Tamper Report")
if st.button("🕵️ View Tamper Report"):
    if st.session_state.tamper_log:
        st.dataframe(pd.DataFrame(st.session_state.tamper_log))
    else:
        st.success("✅ No tampering recorded.")

# ==== Admin Decryption ====
st.subheader("🔐 Admin Decryption Access")
admin_token = st.text_input("Enter admin token to decrypt genetic data:", type="password")
if st.button("🔓 Decrypt DNA"):
    if admin_token == "ADMIN123":
        for i, block in enumerate(original_chain):
            st.success(f"Block #{i} DNA: {decrypt_data(block.genetic_data)}")
    else:
        st.error("❌ Invalid token!")
