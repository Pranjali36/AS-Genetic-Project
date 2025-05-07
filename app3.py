import streamlit as st
import hashlib
import base64
import copy
import pandas as pd
from datetime import datetime

# ========= Helper Functions ==========

def encrypt_data(data):
    return base64.b64encode(data.encode()).decode()

def decrypt_data(encrypted_data):
    try:
        return base64.b64decode(encrypted_data.encode()).decode()
    except Exception:
        return "[Decryption Failed]"

# ========= Block Definition ==========

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

# ========= Create Blockchain ==========

def create_blockchain():
    blockchain = []
    metadata_list = [
        {"Patient ID": "P001", "Test Date": "2023-08-01", "Sample Code": "S1"},
        {"Patient ID": "P002", "Test Date": "2023-08-02", "Sample Code": "S2"},
        {"Patient ID": "P003", "Test Date": "2023-08-03", "Sample Code": "S3"}
    ]
    dna_list = ["ATGCTACGATCG", "GGGCTAGCTTAC", "TACGGGCTAGCA"]

    genesis_block = Block(0, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), metadata_list[0], dna_list[0], "0")
    blockchain.append(genesis_block)

    for i in range(1, 3):
        prev_hash = blockchain[i - 1].hash
        new_block = Block(i, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), metadata_list[i], dna_list[i], prev_hash)
        blockchain.append(new_block)

    return blockchain

# ========= Initialize Chains ==========

original_chain = create_blockchain()
server_1 = copy.deepcopy(original_chain)
server_2 = copy.deepcopy(original_chain)
server_3 = copy.deepcopy(original_chain)
servers = {"Server 1": server_1, "Server 2": server_2, "Server 3": server_3}
colors = {"Server 1": "#E8F5E9", "Server 2": "#E3F2FD", "Server 3": "#FFF3E0"}

if 'tamper_log' not in st.session_state:
    st.session_state.tamper_log = []

# ========= Streamlit UI ==========

st.set_page_config(page_title="GeneBlock App 3", layout="wide")
st.title("🛡️ GeneBlock - App 3: Real-Time Tamper Detection")
st.markdown("Modify metadata manually to simulate a real-time tamper attempt on a blockchain server.")

# ========= Tamper Input Section ==========

st.subheader("✏️ Simulate Manual Tampering")
colA, colB = st.columns(2)
with colA:
    server_selected = st.selectbox("Choose Server:", ["Server 1", "Server 2", "Server 3"])
with colB:
    block_index = st.selectbox("Choose Block to Edit (Index):", [0, 1, 2])

block_to_edit = servers[server_selected][block_index]

# Editable metadata fields
new_patient_id = st.text_input("Edit Patient ID", value=block_to_edit.metadata["Patient ID"])
new_sample_code = st.text_input("Edit Sample Code", value=block_to_edit.metadata["Sample Code"])

# Button to apply changes
if st.button("Apply Changes to Metadata"):
    block_to_edit.metadata["Patient ID"] = new_patient_id
    block_to_edit.metadata["Sample Code"] = new_sample_code
    block_to_edit.hash = block_to_edit.calculate_hash()

    if block_to_edit.hash != original_chain[block_index].hash:
        st.session_state.tamper_log.append({
            "Server": server_selected,
            "Block": block_index,
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Note": "Metadata manually tampered."
        })
        st.error(f"⚠️ Block #{block_index} on {server_selected} tampered manually!")

# ========= Display All Chains ==========

st.subheader("🔗 Blockchain Status Across Servers")
col1, col2, col3 = st.columns(3)
servers = {"Server 1": server_1, "Server 2": server_2, "Server 3": server_3}
colors = {"Server 1": "#E8F5E9", "Server 2": "#E3F2FD", "Server 3": "#FFF3E0"}

for idx, (label, chain) in enumerate(servers.items()):
    with [col1, col2, col3][idx]:
        st.markdown(f"**{label}**")
        for block in chain:
            bg_color = "#FFCDD2" if block.hash != original_blockchain[block.index].hash else colors[label]
            st.markdown(f"""
                <div style="background-color: {bg_color}; padding: 10px; border-radius: 5px; margin-bottom: 10px;
                            font-family: monospace; max-width: 100%; word-wrap: break-word; overflow-wrap: break-word;">
                    <strong>Block #{block.index}</strong><br>
                    <strong>Timestamp:</strong> {block.timestamp}<br>
                    <strong>Metadata:</strong> {block.metadata}<br>
                    <strong>Prev Hash:</strong> <span style="word-break: break-all;">{block.previous_hash}</span><br>
                    <strong>Hash:</strong> <span style="word-break: break-all;">{block.hash}</span>
                </div>
            """, unsafe_allow_html=True)

# ========= Tamper Report ==========

if st.button("📑 View Tamper Report"):
    if st.session_state.tamper_log:
        df = pd.DataFrame(st.session_state.tamper_log)
        st.warning("🚨 Tampering Activity Detected:")
        st.dataframe(df)
    else:
        st.success("✅ No tampering activity recorded.")

# ========= Admin Decryption ==========

st.subheader("🔐 Admin Decryption Panel")
token = st.text_input("Enter Admin Token to Decrypt DNA", type="password")
if st.button("🔓 Decrypt All Genetic Data"):
    if token == "ADMIN123":
        for i, block in enumerate(original_chain):
            decrypted = decrypt_data(block.genetic_data)
            st.success(f"Decrypted Block #{i} DNA: {decrypted}")
    else:
        st.error("❌ Invalid admin token!")
