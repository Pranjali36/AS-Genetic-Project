import streamlit as st
import uuid
import random

# Simulated Blockchain Block Class
class Block:
    def __init__(self, index, metadata, genetic_data, previous_hash=''):
        self.index = index
        self.metadata = metadata
        self.genetic_data = genetic_data
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        return str(hash((self.index, str(self.metadata), self.genetic_data, self.previous_hash)))

# Sample realistic metadata and DNA data
def create_realistic_blocks():
    meta_data = [
        {"Patient ID": "P001", "Blood Group": "A+", "Date": "2025-05-10"},
    {"Patient ID": "P002", "Blood Group": "B-", "Date": "2025-05-09"},
    {"Patient ID": "P003", "Blood Group": "O+", "Date": "2025-05-08"}
    ]
    dna_data = [
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
    chain = []
    previous_hash = "0"
    for i in range(len(meta_data)):
        block = Block(i, meta_data[i], dna_data[i], previous_hash)
        previous_hash = block.hash
        chain.append(block)
    return chain

# Create multiple server copies (simulate)
original_chain = create_realistic_blocks()
server_copies = {
    "Server A": original_chain.copy(),
    "Server B": original_chain.copy(),
    "Server C": original_chain.copy()
}

# Streamlit UI
st.set_page_config(page_title="GeneBlock", layout="wide")
st.title("🧬 GeneBlock App: A Blockchain Model for Genetic Data Security")
st.markdown("<h4 style='color:#4B8BBE;'>Secure storage with admin-only DNA access, tamper detection, and network consensus</h4>", unsafe_allow_html=True)
st.markdown("---")

# Simulate Tampering
st.subheader("🛠️ Simulate Tampering")
server_to_tamper = st.selectbox("Select Server to Tamper:", list(server_copies.keys()))
block_to_tamper = st.number_input("Enter Block Index to Tamper:", min_value=0, max_value=2, step=1)
new_value = st.text_input("Enter new Genotype value (e.g., TT):")

if st.button("⚠️ Tamper Block"):
    server_copies[server_to_tamper][block_to_tamper].metadata["Genotype"] = new_value
    server_copies[server_to_tamper][block_to_tamper].hash = server_copies[server_to_tamper][block_to_tamper].compute_hash()
    st.warning("Block tampered successfully.")

# Blockchain Status
st.subheader("🔗 Blockchain Status Across Servers")
for server, chain in server_copies.items():
    st.markdown(f"**{server}**")
    for i, block in enumerate(chain):
        st.markdown(f"- Block {i} | Hash: `{block.hash}`")

# Tamper Report
st.subheader("📋 Tamper Detection Report")
def check_chain_consistency(chains):
    base = [block.hash for block in chains["Server A"]]
    report = []
    for server, chain in chains.items():
        current = [block.hash for block in chain]
        is_valid = current == base
        report.append({"Server": server, "Status": "✅ Valid" if is_valid else "❌ Rejected"})
    return report

report = check_chain_consistency(server_copies)
st.table(report)

# Admin Panel
st.markdown("---")
st.subheader("🛡️ Admin Panel")

admin_pass = st.text_input("🔐 Enter Admin Password", type="password")
if "admin_key" not in st.session_state:
    st.session_state.admin_key = None

col1, col2 = st.columns(2)

with col1:
    if st.button("🔑 Generate Admin Key"):
        if admin_pass == "ADMIN123":
            st.session_state.admin_key = str(uuid.uuid4())
            st.success("Admin Key generated.")
            with st.expander("📥 Admin Key (Share Securely)", expanded=True):
                st.code(st.session_state.admin_key)
        else:
            st.error("❌ Invalid admin password.")

with col2:
    if st.button("📖 View DNA Data (Admin Only)"):
        if admin_pass == "ADMIN123":
            for i, block in enumerate(original_chain):
                st.markdown(f"**Block {i} DNA Sequence:** `{block.genetic_data}`")
        else:
            st.error("❌ Invalid admin password. Access denied.")

# Key Authentication Section
st.markdown("---")
st.subheader("👥 Authorized Access with Secure Key")
entered_key = st.text_input("🔐 Enter Secure Admin Key", type="password")

if st.button("🔓 Decrypt DNA with Key"):
    if st.session_state.admin_key and entered_key == st.session_state.admin_key:
        for i, block in enumerate(original_chain):
            st.markdown(f"**Block {i} DNA Sequence:** `{block.genetic_data}`")
    else:
        st.error("❌ Invalid key or key not generated.")

# Public Metadata
st.markdown("---")
st.subheader("📊 Genetic Metadata Overview")
for i, block in enumerate(original_chain):
    st.markdown(f"**Block {i} Metadata:**")
    st.table(block.metadata)
