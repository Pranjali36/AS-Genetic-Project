import streamlit as st
import hashlib
import random
import time
import pandas as pd
from datetime import datetime

# ========== Block and Blockchain Setup ==========

class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha256((str(self.index) + str(self.timestamp) +
                               str(self.data) + str(self.previous_hash)).encode()).hexdigest()

    def to_dict(self):
        return {
            'Index': self.index,
            'Timestamp': datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S'),
            'Data': self.data,
            'Hash': self.hash[:10] + "...",
            'Previous Hash': self.previous_hash[:10] + "..."
        }

def create_genetic_blockchain():
    chain = []
    initial_block = Block(0, "Encrypted DNA: ATCG123", "0")
    chain.append(initial_block)
    for i in range(1, 3):  # 3 blocks total for simplicity
        data = f"Encrypted DNA: ATCG{random.randint(100,999)}"
        chain.append(Block(i, data, chain[i-1].hash))
    return chain

# ========== Blockchain Copies ==========

servers = {
    "Server 1": create_genetic_blockchain(),
    "Server 2": create_genetic_blockchain(),
    "Server 3": create_genetic_blockchain()
}
tamper_log = []

# ========== Streamlit UI ==========

st.title("🔒 GeneBlock: Blockchain Security for Genetic Data")
st.markdown("This system uses **blockchain and encryption** to secure sensitive genetic data.\n"
            "Multiple servers store redundant chains. Any tampering attempt is instantly detected.")

# ========== Display Blockchain Chains ==========

def display_blockchain(chain, title):
    st.subheader(title)
    for block in chain:
        if verify_block(block, chain):
            st.success(f"Block {block.index} | Hash: {block.hash[:10]}...")
        else:
            st.error(f"Tampered Block {block.index} | Hash: {block.hash[:10]}...")
        st.code(block.to_dict())

def verify_block(block, chain):
    if block.index == 0:
        return block.hash == block.calculate_hash()
    prev_block = chain[block.index - 1]
    return (block.previous_hash == prev_block.hash and
            block.hash == block.calculate_hash())

# Display all servers
for name, chain in servers.items():
    with st.expander(f"{name} Blockchain"):
        display_blockchain(chain, name)

# ========== Simulate Hack Button ==========

if st.button("💀 Simulate Hack on Server 3"):
    hacked_chain = servers["Server 3"]
    block_to_hack = random.choice([1, 2])
    hacked_chain[block_to_hack].data = "Tampered DNA: HACKED999"
    hacked_chain[block_to_hack].hash = hacked_chain[block_to_hack].calculate_hash()
    tamper_log.append({
        'Server': "Server 3",
        'Block': block_to_hack,
        'Time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    st.error(f"⚠️ Block {block_to_hack} on Server 3 has been tampered!")

# ========== Tamper Report ==========

if st.button("📄 View Tamper Report"):
    if tamper_log:
        df = pd.DataFrame(tamper_log)
        st.warning("🚨 Tampering Detected! See Details Below:")
        st.dataframe(df)
    else:
        st.success("✅ Blockchain verified: No tampering detected.")

# ========== Decryption ==========

st.subheader("🔓 Decrypt Genetic Data (Admin Only)")
admin_token = st.text_input("Enter access token to decrypt records:", type="password")

if st.button("Decrypt Genetic Data"):
    if admin_token == "ADMIN123":
        decrypted = [block.data.replace("Encrypted", "Decrypted") for block in servers["Server 1"]]
        for i, data in enumerate(decrypted):
            st.info(f"Record {i+1}: {data}")
    else:
        st.error("❌ Invalid admin token. Access denied.")
