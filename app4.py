import streamlit as st
import hashlib
import base64
import copy
import pandas as pd
from datetime import datetime

# ========== Encryption & Decryption ==========

def encrypt_data(data):
    return base64.b64encode(data.encode()).decode()

def decrypt_data(encrypted_data):
    try:
        return base64.b64decode(encrypted_data.encode()).decode()
    except Exception:
        return "[Decryption Failed]"

# ========== Blockchain Block Structure ==========

class Block:
    def __init__(self, index, timestamp, metadata, genetic_data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.metadata = metadata
        self.genetic_data = encrypt_data(genetic_data)
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        content = f"{self.index}{self.timestamp}{self.metadata}{self.genetic_data}{self.previous_hash}"
        return hashlib.sha256(content.encode()).hexdigest()

# ========== Blockchain Setup ==========

def create_blockchain():
    metadata = [
        {"Patient ID": "P001", "Test Date": "2023-08-01", "Sample Code": "S1"},
        {"Patient ID": "P002", "Test Date": "2023-08-02", "Sample Code": "S2"},
        {"Patient ID": "P003", "Test Date": "2023-08-03", "Sample Code": "S3"},
    ]
    dna_data = ["ATGCTACGATCG", "GGGCTAGCTTAC", "TACGGGCTAGCA"]
    chain = []
    prev_hash = "0"

    for i in range(3):
        block = Block(i, datetime.now().timestamp(), metadata[i], dna_data[i], prev_hash)
        chain.append(block)
        prev_hash = block.hash

    return chain

# ========== Blockchain Initialization ==========

original_chain = create_blockchain()
server_1 = copy.deepcopy(original_chain)
server_2 = copy.deepcopy(original_chain)
server_3 = copy.deepcopy(original_chain)

servers = {"Server 1": server_1, "Server 2": server_2, "Server 3": server_3}

if 'tamper_log' not in st.session_state:
    st.session_state.tamper_log = []

# ========== UI Setup ==========

st.set_page_config(page_title="GeneBlock App 4", layout="wide")
st.title("🧬 GeneBlock App 4: Blockchain + Tamper Detection + Consensus")

# ========== Blockchain Display Section ==========

st.subheader("🔗 Blockchain Status Across Servers")
cols = st.columns(3)
server_colors = {"Server 1": "#E8F5E9", "Server 2": "#E3F2FD", "Server 3": "#FFF3E0"}

for i, (server_name, chain) in enumerate(servers.items()):
    with cols[i]:
        st.markdown(f"**{server_name}**")
        for idx, block in enumerate(chain):
            is_tampered = block.hash != original_chain[idx].hash
            block_color = "#FFCDD2" if is_tampered else server_colors[server_name]

            st.markdown(f"""
                <div style="background-color: {block_color}; padding: 10px; border-radius: 8px;
                            margin-bottom: 10px; font-size: 13px; word-wrap: break-word;">
                    <strong>Block #{block.index}</strong><br>
                    <strong>Timestamp:</strong> {datetime.fromtimestamp(block.timestamp).strftime('%Y-%m-%d %H:%M:%S')}<br>
                    <strong>Metadata:</strong> {block.metadata}<br>
                    <strong>Prev Hash:</strong> {block.previous_hash}<br>
                    <strong>Hash:</strong> {block.hash}
                </div>
            """, unsafe_allow_html=True)

# ========== Manual Tampering Interface ==========

st.subheader("✏️ Tamper a Block")

colA, colB = st.columns(2)
with colA:
    server_selected = st.selectbox("Choose Server", list(servers.keys()))
with colB:
    block_index = st.selectbox("Choose Block Index", [0, 1, 2])

selected_chain = servers[server_selected]
block_to_edit = selected_chain[block_index]

# Prevent tampering if any previous block is already tampered
tampered_before = any(
    selected_chain[i].hash != original_chain[i].hash
    for i in range(block_index)
)

if tampered_before:
    st.error("🚫 You cannot edit this block because a previous block in the chain has been tampered.")
else:
    new_pid = st.text_input("Edit Patient ID", value=block_to_edit.metadata["Patient ID"])
    new_sample = st.text_input("Edit Sample Code", value=block_to_edit.metadata["Sample Code"])

    if st.button("Apply Metadata Changes"):
        block_to_edit.metadata["Patient ID"] = new_pid
        block_to_edit.metadata["Sample Code"] = new_sample
        block_to_edit.hash = block_to_edit.calculate_hash()

        # Propagate hash change to downstream blocks
        for i in range(block_index + 1, len(selected_chain)):
            selected_chain[i].previous_hash = selected_chain[i - 1].hash
            selected_chain[i].hash = selected_chain[i].calculate_hash()

        st.session_state.tamper_log.append({
            "Server": server_selected,
            "Block": block_index,
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Note": "Metadata manually tampered."
        })

        st.warning(f"⚠️ Block #{block_index} on {server_selected} has been tampered!")

# ========== Tamper Log Viewer ==========

if st.button("📄 View Tamper Log"):
    if st.session_state.tamper_log:
        df = pd.DataFrame(st.session_state.tamper_log)
        st.dataframe(df)
    else:
        st.success("✅ Blockchain is clean. No tampering detected.")

# ========== Admin Decryption ==========

st.subheader("🔐 Admin-Only DNA Decryption")
token = st.text_input("Enter admin token to decrypt DNA:", type="password")

if st.button("🔓 Decrypt Genetic Data"):
    if token == "ADMIN123":
        for i, block in enumerate(original_chain):
            dna = decrypt_data(block.genetic_data)
            st.success(f"Block #{i} - Decrypted DNA: {dna}")
    else:
        st.error("❌ Invalid token.")
