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

def is_chain_valid_until(chain, index):
    """
    Returns False if any block at or before the given index is tampered.
    """
    for i in range(index + 1):
        if chain[i].hash != original_chain[i].hash:
            return False
    return True

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
st.title("🧬 GeneBlock App: A Blockchain Network")
st.markdown("Multiple server copies, admin-only access, real-time tamper detection, and **majority-based network validation**.")

# ========= Manual Tampering Section with Chain Break Protection ==========

st.subheader("✏ Simulate Manual Tampering")
colA, colB = st.columns(2)
with colA:
    server_selected = st.selectbox("Choose Server:", ["Server 1", "Server 2", "Server 3"])
with colB:
    block_index = st.selectbox("Choose Block to Edit (Index):", [0, 1, 2])

block_to_edit = servers[server_selected][block_index]

# Check if block is valid before allowing edit
if not is_chain_valid_until(servers[server_selected], block_index - 1):
    st.error(f"⛔ Block #{block_index} or earlier has been tampered. Editing is disabled.")
else:
    # Editable metadata fields
    new_patient_id = st.text_input("Edit Patient ID", value=block_to_edit.metadata["Patient ID"])
    new_sample_code = st.text_input("Edit Sample Code", value=block_to_edit.metadata["Sample Code"])

    if st.button("Apply Changes to Metadata"):
        block_to_edit.metadata["Patient ID"] = new_patient_id
        block_to_edit.metadata["Sample Code"] = new_sample_code
        block_to_edit.hash = block_to_edit.calculate_hash()

        # Propagate changes to downstream blocks
        chain = servers[server_selected]
        for i in range(block_index + 1, len(chain)):
            chain[i].previous_hash = chain[i - 1].hash
            chain[i].hash = chain[i].calculate_hash()

        if block_to_edit.hash != original_chain[block_index].hash:
            st.session_state.tamper_log.append({
                "Server": server_selected,
                "Block": block_index,
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Note": "Metadata manually tampered."
            })
            st.error(f"⚠️ Block #{block_index} on {server_selected} tampered manually!")

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
st.subheader("🔗 Blockchain Status Across Servers")

col1, col2, col3 = st.columns(3)
server_colors = {
    "Server 1": "#E8F5E9",  # light green
    "Server 2": "#E3F2FD",  # light blue
    "Server 3": "#FFF3E0",  # light orange
}

for idx, (label, chain) in enumerate(servers.items()):
    with [col1, col2, col3][idx]:
        st.markdown(f"**{label}**")
        for i, block in enumerate(chain):
            # Check if this block is tampered compared to original
            original_hash = original_chain[i].hash
            if block.hash != original_hash:
                bg_color = "#FFCDD2"  # red for tampered or affected block
            else:
                bg_color = server_colors[label]

            st.markdown(f"""
                <div style="
                    background-color: {bg_color}; 
                    padding: 17px; 
                    border-radius: 5px; 
                    margin-bottom: 15px;
                    word-wrap: break-word;
                    overflow-wrap: break-word;
                    white-space: normal;
                    font-size: 16px;">
                    <strong>Block #{block.index}</strong><br>
                    <strong>Timestamp:</strong> {block.timestamp}<br>
                    <strong>Metadata:</strong> {block.metadata}<br>
                    <strong>Prev Hash:</strong> {block.previous_hash}...<br>
                    <strong>Hash:</strong> {block.hash}...
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
