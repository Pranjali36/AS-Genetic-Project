st.subheader("🔐 Admin Authentication Panel")

# Session flags
if "is_admin_authenticated" not in st.session_state:
    st.session_state.is_admin_authenticated = False
if "admin_key" not in st.session_state:
    st.session_state.admin_key = None

# Admin login
admin_password = st.text_input("Enter Admin Password", type="password")
if st.button("✅ Login as Admin"):
    if admin_password == "ADMIN123":
        st.session_state.is_admin_authenticated = True
        st.success("✅ Admin authenticated successfully.")
    else:
        st.session_state.is_admin_authenticated = False
        st.error("❌ Invalid admin password.")

# Show only to authenticated admin
if st.session_state.is_admin_authenticated:

    # --- Function 1: View Encrypted DNA Data ---
    if st.button("🔓 Decrypt All Genetic Data"):
        for i, block in enumerate(original_chain):
            decrypted = decrypt_data(block.genetic_data)
            st.success(f"Decrypted Block #{i} DNA: {decrypted}")

    # --- Function 2: Generate Admin Key ---
    if st.button("🔑 Generate Admin Access Key"):
        import uuid
        st.session_state.admin_key = str(uuid.uuid4())
        with st.expander("📥 Admin Key (Copy & Share Securely)", expanded=False):
            st.text(f"{st.session_state.admin_key}")

    st.markdown("---")

    # --- Key-based Decryption (Simulated Key Sharing) ---
    st.markdown("**Authorized party enters the received secure key below to decrypt DNA:**")
    entered_key = st.text_input("🔐 Enter Secure Admin Key", type="password")

    if st.button("🔓 Decrypt Genetic Data Using Shared Key"):
        if st.session_state.admin_key and entered_key == st.session_state.admin_key:
            for i, block in enumerate(original_chain):
                decrypted = decrypt_data(block.genetic_data)
                st.success(f"Block #{i} DNA: {decrypted}")
        else:
            st.error("❌ Invalid key or key not generated. Please contact admin.")
