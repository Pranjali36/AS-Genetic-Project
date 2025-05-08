import streamlit as st
import hashlib
import base64
import copy
import random
from datetime import datetime
import pandas as pd

# ========== Encryption / Decryption ==========

def encrypt_data(data):
    return base64.b64encode(data.encode()).decode()

def decrypt_data(data):
    try:
        return base64.b64decode(data.encode()).decode()
    except Exception:
        return "[Decryption Failed]"

# ========== Blockchain Classes ==========

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

def create_blockchain():
    metadata_list = [
        {"Patient ID": "P001", "Sample Code": "S1"},
        {"Patient ID": "P002", "Sample Code": "S2"},
        {"Patient ID": "P003", "Sample Code": "S3"},
    ]
    dna_list = ["ATCG", "GGCT", "TACG"]

    blockchain = []
    for i in range(3):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prev_hash = blockchain[-1].hash if i > 0 else "0"
        block = Block(i, timestamp, metadata_list[i], dna_list[i], prev_hash)
        blockchain.append(block)

    return blockchain

# ========== Initialize Chains ==========

original_chain = create_blockchain()
server_1 = copy.deepcopy(original_chain)
server_2 = copy.deepcopy(original_chain)
server_3 = copy.deepcopy(original_chain)

servers = {
    "Server 1": server_1,
    "Server 2": server_2,
    "Server 3": server_3,
}

if 'tamper_log' not in st.session_state:
    st.session_state.tamper_log = []

# ========== Streamlit UI ==========

st.set_page_config(page_title="GeneBlock - Network Consensus", layout="wide")
st.title("🌐 GeneBlock App 4 - Blockchain Consensus & Tamper Detection")

st.markdown("This app shows how blockchain consensus protects genetic data. "
            "Only chains that match the majority are accepted.")

# ========== Tampering Panel ==========

st.sidebar.header("🔧 Manual Tampering")
tamper_server = st.sidebar.selectbox("Select server to tamper:", list(servers.keys()))
tamper_block = st.sidebar.selectbox("Select block index:", [0, 1, 2])
tamper_value = st.sidebar.text_input("New Patient ID to tamper:")

if st.sidebar.button("Apply Tampering"):
    selected = servers[tamper_server][tamper_block]
    selected.metadata["Patient ID"] = tamper_value
    selected.hash = selected.calculate_hash()

    # Recalculate hashes for following blocks
    for i in range(tamper_block + 1, len(servers[tamper_server])):
        prev_block = servers[tamper_server][i - 1]
        servers[tamper_server][i].previous_hash = prev_block.hash
        servers[tamper_server][i].hash = servers[tamper_server][i].calculate_hash()

    st.session_state.tamper_log.append({
        "Server": tamper_server,
        "Block": tamper_block,
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Note": "Tampered manually"
    })
    st.sidebar.warning(f"⚠️ Tampered block {tamper_block} on {tamper_server}")

# ========== Consensus Validation ==========

st.subheader("🔍 Consensus Status")
col1, col2, col3 = st.columns(3)

# Determine consensus chain (assume server_1 as reference)
reference_chain = server_1
for label, chain, col in zip(servers.keys(), servers.values(), [col1, col2, col3]):
    with col:
        st.markdown(f"### {label}")
        consistent = True
        for i in range(len(reference_chain)):
            if chain[i].hash != reference_chain[i].hash:
                consistent = False
                break
        status = "✅ Accepted" if consistent else "❌ Rejected by Network"
        color = "#E8F5E9" if consistent else "#FFEBEE"

        for block in chain:
            st.markdown(f"""
            <div style="background-color: {color}; padding: 10px; margin-bottom: 10px; border-radius: 5px;">
                <b>Block #{block.index}</b><br>
                <b>Time:</b> {block.timestamp}<br>
                <b>Metadata:</b> {block.metadata}<br>
                <b>Hash:</b> {block.hash[:10]}...<br>
                <b>Prev:</b> {block.previous_hash[:10]}...
            </div>
            """, unsafe_allow_html=True)

        st.info(f"**Status: {status}**")

# ========== Tamper Report ==========

st.subheader("📄 Tampering History")
if st.session_state.tamper_log:
    df = pd.DataFrame(st.session_state.tamper_log)
    st.dataframe(df)
else:
    st.success("✅ No tampering detected.")
