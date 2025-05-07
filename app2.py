import streamlit as st
import hashlib
import random
import time
import pandas as pd
import base64
import copy
from datetime import datetime

# ---------------- ENCRYPTION ----------------
def encrypt_data(data):
    return base64.b64encode(data.encode()).decode()

def decrypt_data(encrypted_data):
    try:
        return base64.b64decode(encrypted_data.encode()).decode()
    except Exception:
        return "[Decryption Failed]"

# ---------------- BLOCKCHAIN CLASSES ----------------
class Block:
    def __init__(self, index, timestamp, metadata, genetic_data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.metadata = metadata  # Non-sensitive metadata only
        self.genetic_data = encrypt_data(genetic_data)  # Sensitive info encrypted
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_content = f"{self.index}{self.timestamp}{self.metadata}{self.genetic_data}{self.previous_hash}"
        return hashlib.sha256(block_content.encode()).hexdigest()

# ---------------- BLOCKCHAIN CREATION ----------------
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

# ---------------- INIT SERVER COPIES ----------------
original_blockchain = create_blockchain()
server_1 = copy.deepcopy(original_blockchain)
server_2 = copy.deepcopy(original_blockchain)
server_3 = copy.deepcopy(original_blockchain)

if 'tamper_log' not in st.session_state:
    st.session_state.tamper_log = []

# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="GeneBlock: Secure Genetic Storage", layout="wide")
st.title("🔒 GeneBlock: Blockchain Security for Genetic Data")
st.markdown("This system uses **blockchain and encryption** to secure sensitive genetic data.\n"
            "Multiple servers store redundant chains. Any tampering attempt is instantly detected.")

# ---------------- DISPLAY CHAINS ----------------
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

# ---------------- SIMULATE HACK ----------------
if st.button("🧨 Simulate Hack "):
    hacked_chain = servers["Server 3"]
    block_to_hack = random.choice([1, 2])
    hacked_chain[block_to_hack].genetic_data = encrypt_data("Tampered DNA: HACKED999")
    hacked_chain[block_to_hack].hash = hacked_chain[block_to_hack].calculate_hash()
    st.session_state.tamper_log.append({
        'Server': "Server 3",
        'Block': block_to_hack,
        'Time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    st.error(f"⚠️ Block {block_to_hack} on Server 3 has been tampered!")

# ---------------- TAMPER REPORT ----------------
if st.button("📄 View Tamper Report"):
    if st.session_state.tamper_log:
        df = pd.DataFrame(st.session_state.tamper_log)
        st.warning("🚨 Tampering Detected! See Details Below:")
        st.dataframe(df)
    else:
        st.success("✅ Blockchain verified: No tampering detected.")

# ---------------- DECRYPTION ----------------
st.subheader("🔐 Decryption Access")
admin_token = st.text_input("Enter access token to decrypt records:", type="password")

if st.button("🔓 Admin Decrypt Data"):
    if admin_token == "ADMIN123":
        for i, block in enumerate(original_blockchain):
            decrypted = decrypt_data(block.genetic_data)
            st.success(f"✅ Decrypted Block #{i} DNA: {decrypted}")
    else:
        st.error("❌ Invalid token! Only GenBank admin can decrypt data.")
