import streamlit as st
import hashlib
import base64
import uuid
import copy

# ====== Simulated Genetic Data ======
meta_data = [
    {"Patient ID": "P001", "Blood Group": "A+", "Date": "2025-05-10"},
    {"Patient ID": "P002", "Blood Group": "B-", "Date": "2025-05-09"},
    {"Patient ID": "P003", "Blood Group": "O+", "Date": "2025-05-08"}
]

real_dna_data = [
    {
        "SNP_ID": "rs333",
        "Chromosome": "3",
        "Position": "46414947",
        "Genotype": "∆32/∆32",
        "Trait": "HIV resistance"
    },
    {
        "SNP_ID": "rs1042713",
        "Chromosome": "5",
        "Position": "148206337",
        "Genotype": "Arg16Gly",
        "Trait": "Asthma risk"
    },
    {
        "SNP_ID": "rs429358",
        "Chromosome": "19",
        "Position": "44908684",
        "Genotype": "C/C",
        "Trait": "Alzheimer’s risk"
    }
]

# ===== Encryption Functions =====
def encrypt_data(data_dict):
    encoded = base64.b64encode(str(data_dict).encode("utf-8")).decode("utf-8")
    return encoded

def decrypt_data(encrypted_str):
    try:
        decoded = base64.b64decode(encrypted_str.encode("utf-8")).decode("utf-8")
        return decoded
    except Exception:
        return "Decryption failed"

# ===== Blockchain Block Class =====
class Block:
    def __init__(self, index, previous_hash, metadata, genetic_data):
        self.index = index
        self.previous_hash = previous_hash
        self.metadata = metadata
        self.genetic_data = encrypt_data(genetic_data)
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        content = str(self.index) + self.previous_hash + str(self.metadata) + self.genetic_data
        return hashlib.sha256(content.encode()).hexdigest()

# ===== Create Initial Blockchain =====
def create_blockchain():
    blockchain = []
    previous_hash = "0"
    for i in range(len(meta_data)):
        block = Block(i, previous_hash, meta_data[i], real_dna_data[i])
        blockchain.append(block)
        previous_hash = block.hash
    return blockchain

original_chain = create_blockchain()

# ====== App UI ======
st.set_page_config(page_title="GeneBlock App", layout="wide")

st.title("🧬 GeneBlock App: A Blockchain-Based Genetic Security Model")
st.markdown(
    "<h5 style='color:grey;'>Tamper-proof metadata, secure admin-only genetic data access, and real-time network consensus</h5>",
    unsafe_allow_html=True
)

# ====== Initialize Server Chains ======
if "server1" not in st.session_state:
    st.session_state.server1 = copy.deepcopy(original_chain)
if "server2" not in st.session_state:
    st.session_state.server2 = copy.deepcopy(original_chain)
if "server3" not in st.session_state:
    st.session_state.server3 = copy.deepcopy(original_chain)

# ====== Simulate Hack ======
st.markdown("### 🛠️ Simulate Data Tampering on Server 1")
tamper_index = st.number_input("Select Block Index to Tamper (Server 1)", min_value=0, max_value=len(original_chain)-1, step=1)
tamper_key = st.selectbox("Select Metadata Field to Edit", ["Patient ID", "Blood Group", "Date"])
tamper_value = st.text_input("Enter New Tampered Value")

if st.button("⚠️ Inject Tampering into Server 1"):
    st.session_state.server1[tamper_index].metadata[tamper_key] = tamper_value
    # Recalculate hash for tampered block and all next blocks
    for i in range(tamper_index, len(st.session_state.server1)):
        prev_hash = st.session_state.server1[i-1].hash if i > 0 else "0"
        st.session_state.server1[i].previous_hash = prev_hash
        st.session_state.server1[i].hash = st.session_state.server1[i].calculate_hash()
    st.warning("Tampering simulated on Server 1.")

# ====== Blockchain Display ======
st.markdown("### 🔗 Blockchain Status Across Servers")
cols = st.columns(3)
servers = [st.session_state.server1, st.session_state.server2, st.session_state.server3]
titles = ["Server 1", "Server 2", "Server 3"]
colors = ["#ffdede", "#e0ffe0", "#e0eaff"]

for col, server, title, color in zip(cols, servers, titles, colors):
    with col:
        st.markdown(f"#### 🖥️ {title}")
        for block in server:
            st.markdown(
                f"<div style='border:1px solid black; padding:5px; margin:5px; background-color:{color};'>"
                f"<b>Index:</b> {block.index}<br>"
                f"<b>Hash:</b> {block.hash[:10]}...<br>"
                f"<b>Prev Hash:</b> {block.previous_hash[:10]}...<br>"
                f"<b>Metadata:</b> {block.metadata}<br>"
                f"</div>",
                unsafe_allow_html=True
            )

# ====== Tamper Report Section ======
st.markdown("### 📋 Tamper Report Based on Consensus")

def is_chain_valid(chain1, chain2):
    return all(b1.hash == b2.hash for b1, b2 in zip(chain1, chain2))

def majority_valid():
    s1, s2, s3 = st.session_state.server1, st.session_state.server2, st.session_state.server3
    valids = [is_chain_valid(s1, s2), is_chain_valid(s2, s3), is_chain_valid(s1, s3)]
    majority = valids.count(True) >= 2
    return {
        "Server 1": is_chain_valid(s1, s2) or is_chain_valid(s1, s3),
        "Server 2": is_chain_valid(s2, s1) or is_chain_valid(s2, s3),
        "Server 3": is_chain_valid(s3, s1) or is_chain_valid(s3, s2),
        "Majority Agreement": majority
    }

status = majority_valid()
st.table([{"Server": k, "Status": v} for k, v in status.items()])

# ====== Admin Panel ======
st.markdown("---")
st.markdown("### 🛡️ Admin Panel")

admin_col1, admin_col2 = st.columns(2)
if "admin_key" not in st.session_state:
    st.session_state.admin_key = None

with admin_col1:
    admin_token = st.text_input("🔑 Enter Admin Password", type="password")
    if st.button("🧬 View Encrypted DNA Data (Admin Only)"):
        if admin_token == "ADMIN123":
            for i, block in enumerate(original_chain):
                decrypted = decrypt_data(block.genetic_data)
                st.success(f"Block #{i} Decrypted DNA:\n{decrypted}")
        else:
            st.error("❌ Invalid Admin Token")

with admin_col2:
    if st.button("🔐 Generate Secure Admin Access Key"):
        if admin_token == "ADMIN123":
            st.session_state.admin_key = str(uuid.uuid4())
            st.info("✅ Key Generated Successfully!")
            st.code(st.session_state.admin_key, language="text")
        else:
            st.error("❌ Invalid Admin Token")

# ====== Decryption by Trusted Party ======
st.markdown("### 🔓 Secure Key Decryption (Trusted Party Access)")
entered_key = st.text_input("Enter Secure Admin Key", type="password")
if st.button("🔍 Decrypt DNA with Secure Key"):
    if st.session_state.admin_key and entered_key == st.session_state.admin_key:
        for i, block in enumerate(original_chain):
            decrypted = decrypt_data(block.genetic_data)
            st.success(f"Block #{i} Decrypted DNA:\n{decrypted}")
    else:
        st.error("❌ Invalid key or key not generated.")
