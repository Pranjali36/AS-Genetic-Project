import streamlit as st
import uuid
import pandas as pd

st.set_page_config(page_title="GeneBlock: A Blockchain Model", layout="wide")

# ========= Header =========
st.markdown("<h1 style='color:#4B0082;'>🌿 GeneBlock: Securing Genomic Data with Blockchain</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='color:#2F4F4F;'>🔬 Visualizing server consensus, restricted access, and tamper-proof genetics</h4>", unsafe_allow_html=True)

st.markdown("---")

# ========= Simulated Blockchain Data =========
# Dummy Realistic DNA Data
sample_data = pd.DataFrame({
    "SNP ID": ["rs123", "rs456", "rs789"],
    "Chromosome": [3, 12, 6],
    "Position": [3452345, 7856341, 1298374],
    "Genotype": ["AA", "GT", "CC"],
    "Trait": ["HIV Resistant", "Unknown", "HIV Prone"]
})

# ========= Display DNA in Table =========
st.subheader("🧬 Encrypted Genetic Metadata Preview")
with st.expander("🔍 View Sample Genetic Info Table"):
    st.dataframe(sample_data, use_container_width=True)

# ========== Blockchain Status ================
st.markdown("<h3 style='color:#1E90FF;'>🔗 Blockchain Status Across Servers</h3>", unsafe_allow_html=True)
# (Placeholder logic or visualizations for blockchain status...)

# ========== Tamper Report ============
st.subheader("⚠️ Tamper Detection Report")
# Simulated tamper report
tamper_report = pd.DataFrame({
    "Server": ["Server A", "Server B", "Server C"],
    "Status": ["Valid", "Tampered", "Valid"]
})
st.table(tamper_report.style.set_properties(**{'border-color': 'black', 'border-width': '2px'}))

# ========== Admin Decryption & Key Panel =============
st.markdown("## 🔐 Admin Access Panel")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**🔑 Admin Login**")
    admin_token = st.text_input("Enter Admin Password", type="password", key="admin_pass")
    if st.button("🔓 View DNA Data"):
        if admin_token == "ADMIN123":
            st.success("Access Granted: Displaying Real Genetic Data")
            st.dataframe(sample_data, use_container_width=True)
        else:
            st.error("❌ Invalid Admin Password!")

with col2:
    st.markdown("**🔧 Generate Admin Key**")
    if "admin_key" not in st.session_state:
        st.session_state.admin_key = None
    if st.button("🗝️ Generate Key"):
        if admin_token == "ADMIN123":
            st.session_state.admin_key = str(uuid.uuid4())
            with st.expander("📥 Copy & Share Secure Admin Key", expanded=True):
                st.code(st.session_state.admin_key)
        else:
            st.error("❌ Unauthorized to generate key!")

with col3:
    st.markdown("**📤 Authorized Access**")
    entered_key = st.text_input("Enter Received Admin Key", type="password", key="entered_key")
    if st.button("📎 Decrypt with Key"):
        if st.session_state.admin_key and entered_key == st.session_state.admin_key:
            st.success("Key Verified. Decrypting Genetic Data:")
            st.dataframe(sample_data, use_container_width=True)
        else:
            st.error("❌ Invalid or missing key.")

# ========== Simulate Hack ===========
st.markdown("## 💥 Attempt to Simulate Hack")
if st.button("🚨 Trigger Tamper Simulation"):
    st.warning("⚠️ Unauthorized tampering attempt detected! Chain flagged and validated by consensus.")
