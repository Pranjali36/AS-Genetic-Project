import streamlit as st
import hashlib
import base64
import copy
import pandas as pd
from datetime import datetime

# ================= Encryption Functions =================

def encrypt_data(data):
    return base64.b64encode(data.encode()).decode()

def decrypt_data(encrypted_data):
    try:
        return base64.b64decode(encrypted_data.encode()).decode()
    except Exception:
        return "[Decryption Failed]"

# ================= Block and Blockchain =================

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
    blockchain = []
    metadata_list = [
        {"Patient ID": "P001", "Test Date": "2023-08-01", "Sample Code": "S1"},
        {"Patient ID": "P002", "Test Date": "2023-08-02", "Sample Code": "S2"},
        {"Patient ID": "P003", "Test Date": "2023-08-03", "Sample Code": "S3"}
    ]
    dna_list = ["ATGCTACGATCG", "GGGCTAGCTTAC", "TACGGGCTAGCA"]

    genesis = Block(0, datetime.now().timestamp(), metadata_list[0], dna_list[0], "0")
    blockchain.append(genesis)

    for i in range(1, 3):
        prev_hash = blockchain[i-1].hash
        block = Block(i, datetime.now().timestamp(), metadata_list[i], dna_list[i], prev_hash)
        blockchain.append(block)

    return blockchain

# ================= Initialize Chains =================

original_chain = create_blockchain()
server_1 = copy.deepcopy(original_chain)
server_2 = copy.deepcopy(original_chain)
server_3 = copy.deepcopy(original_chain)
servers = {
    "Server 1": server_1,
    "Server 2": server_2,
    "Server 3": server_3
}

if 'tamper_log' not in st.session_state:
    st.session_state.tamper_log = []

# ================= Streamlit UI =================

st.set_page_config(page_title="App 4 - Blockchain Lock Demo", layout="wide")
st.title("🔐 App 4: Blockchain Chain Lock After Tampering")

# ================= Blockchain Display =================

st.subheader("🧬 Blockchain Servers View")
cols = st.columns(3)
color_map = {"Server 1": "#E8F5E9", "Server 2": "#E3F2FD", "Server 3": "#FFF3E0"}

for i, (server_name, chain) in enumerate(servers.items()):
    with cols[i]:
        st.markdown(f"**{server_name}**")
        for idx, block in enumerate(chain):
            # Determine block color
            expected_hash = original_chain[idx].hash
            bg_color = "#FFCDD2" if block.hash != expected_hash else color_map[server_name]

            # Style for word wrap
            st.markdown(f"""
                <div style="background-color: {bg_color}; padding: 10px; border-radius: 8px;
                            margin-bottom: 10px; font-size: 13px; word-wrap: break-word;">
                    <strong>Block #{block.index}</strong><br>
                    <strong>Timestamp:</strong> {datetime.fromtimestamp(block.timestamp).strftime('%Y-%m-%d %H:%M:%S')}<br>
                    <strong>Metadata:</strong> {block.metadata}<br>
                    <strong>Prev Hash:</strong> {block.previous_hash}<br>
                    <strong>Hash:</strong> {block.hash}
                </div>
            """, unsafe_allow_html=True)

# ================= Manual Tampering with Chain Lock =================

st.subheader("✏ Simulate Manual Tampering")

colA, colB = st.columns(2)
with colA:
    server_selected = st.selectbox("Choose Server:", ["Server 1", "Server 2", "Server 3"])
with colB:
    block_index = st.selectbox("Choose Block to Edit (Index):", [0, 1, 2])

selected_chain = servers[server_selected]

# Prevent edits beyond first tampered block
tampered = False
for i in range(block_index):
    if selected_chain[i].hash != original_chain[i].hash:
        tampered = True
        break

if tampered:
    st.error("🚫 You cannot edit this block because a previous block in this chain has been tampered.")
else:
    blk = selected_chain[block_index]
    new_pid = st.text_input("Edit Patient ID", value=blk.metadata["Patient ID"])
    new_sample = st.text_input("Edit Sample Code", value=blk.metadata["Sample Code"])

    if st.button("Apply Changes to Metadata"):
        blk.metadata["Patient ID"] = new_pid
        blk.metadata["Sample Code"] = new_sample
        blk.hash = blk.calculate_hash()

        st.session_state.tamper_log.append({
            "Server": server_selected,
            "Block": block_index,
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Note": "Metadata manually tampered."
        })
        st.error(f"⚠️ Block #{block_index} on {server_selected} has been manually tampered!")

# ================= Tamper Report =================

if st.button("📄 View Tamper Report"):
    if st.session_state.tamper_log:
        df = pd.DataFrame(st.session_state.tamper_log)
        st.warning("🚨 Tampering Detected! See Details Below:")
        st.dataframe(df)
    else:
        st.success("✅ Blockchain verified: No tampering detected.")

# ================= Admin Decryption =================

st.subheader("🔑 Admin Decryption (Token Required)")
token = st.text_input("Enter admin token to view genetic data:", type="password")
if st.button("🔓 Decrypt DNA"):
    if token == "ADMIN123":
        for i, block in enumerate(original_chain):
            decrypted = decrypt_data(block.genetic_data)
            st.success(f"Block #{i}: {decrypted}")
    else:
        st.error("❌ Invalid token!")
