import streamlit as st
import hashlib
import base64
import copy
import random
from datetime import datetime
import pandas as pd

# ==== Encryption / Decryption ====
def encrypt_data(data_dict):
    encoded = base64.b64encode(str(data_dict).encode("utf-8")).decode("utf-8")
    return encoded

def decrypt_data(encrypted_str):
    try:
        decoded = base64.b64decode(encrypted_str.encode("utf-8")).decode("utf-8")
        return decoded
    except Exception:
        return "Decryption failed"

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
    dna_list = [
        {
        "Patient ID": "P001",
        "SNP_ID": "rs333",
        "Chromosome": "3",
        "Position": "46414947",
        "Genotype": "∆32/∆32",
        "Trait": "HIV resistance"
    },
    {
        "Patient ID": "P002",
        "SNP_ID": "rs3365478",
        "Chromosome": "5",
        "Position": "148206337",
        "Genotype": "Arg16Gly",
        "Trait": "Asthma risk"
    },
    {
        "Patient ID": "P003",
        "SNP_ID": "rs429358",
        "Chromosome": "19",
        "Position": "44908684",
        "Genotype": "C/C",
        "Trait": "Alzheimer’s risk"
    }
    ]
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
# ========= Header =========
st.markdown("<h1 style='color:#4B0082;text-align: center;'>🧬 GeneBlock: Securing Genomic Data with Blockchain</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color:#2F4F4F;text-align: center;'>🌿 Visualizing server consensus, restricted access, and tamper-proof genetics</h3>", unsafe_allow_html=True)
st.markdown("---")

# ==== Manual Tampering ====
st.markdown("<h4 style='color:#1E90FF;'>🛠️ Tamper Metadata</h4>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    server_to_edit = st.selectbox("Select Server:", ["Server 1", "Server 2", "Server 3"])
with col2:
    block_index = st.selectbox("Select Block Index to Edit:", [0, 1, 2])

target_block = servers[server_to_edit][block_index]
new_pid = st.text_input("New Patient ID", value=target_block.metadata["Patient ID"])
new_sample = st.text_input("New Sample Code", value=target_block.metadata["Sample Code"])

if st.button("⚠️Simulate Hack"):
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
st.markdown("<h3 style='color:#1E90FF;'>🔗 Blockchain Status Across Servers</h3>", unsafe_allow_html=True)

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
if st.button("📄View Tamper Report"):
    if st.session_state.tamper_log:
        st.dataframe(pd.DataFrame(st.session_state.tamper_log))
    else:
        st.success("✅ No tampering recorded.")
        
# ==== Admin Decryption ====
st.subheader("🔐 Admin Decryption Panel")
admin_token = st.text_input("Enter Admin Password (Only for Admin)", type="password")

# Show Admin buttons only if correct password entered
if admin_token == "ADMIN123":
    if st.button("🔓 Decrypt All Genetic Data (Admin Only)"):
        for i, block in enumerate(original_chain):
            decrypted = decrypt_data(block.genetic_data)
            st.success(f"🔍 Block #{i} - Decrypted DNA: {decrypted}")

    if st.button("🔑 Generate Admin Access Key"):
        import uuid
        st.session_state.admin_key = str(uuid.uuid4())
        with st.expander("📥 Admin Key (Copy & Share Securely)", expanded=False):
            st.code(st.session_state.admin_key, language='text')
else:
    if admin_token:
        st.error("❌ Invalid Admin Password!")

# ========== Authorized Key Entry (Publicly Visible) ==========
st.markdown("### 🧬 Decrypt Genetic Data with Shared Key")
entered_key = st.text_input("🔐 Enter Secure Key Provided by Admin", type="password")

if st.button("🔓 Decrypt Data via Secure Key"):
    if st.session_state.get("admin_key") and entered_key == st.session_state.admin_key:
        for i, block in enumerate(original_chain):
            decrypted = decrypt_data(block.genetic_data)
            st.success(f"🔍 Block #{i} - Decrypted DNA: {decrypted}")
    else:
        st.error("❌ Invalid or Missing Key. Contact Admin.")
