import streamlit as st
import pandas as pd

# Blockchain data from your previous output
blockchain_data = [
    {'index': 1, 'previous_hash': '0', 'data': None, 'hash': 'b64435b03a72d115d882f41bbb2d7c60bd2554945101abb0656d75f1593b8574'},
    {'index': 2, 'previous_hash': 'b64435b03a72d115d882f41bbb2d7c60bd2554945101abb0656d75f1593b8574', 'data': 'ODo4PDovPDg8ODgvPDovODo8OC8vLzo8Lzo4Ojg4Lzw4PDo4Ojo4ODo8Ojw8PDo4Ojo=', 'hash': 'b729a682efa96be352acaec8ffec5c6e290db84d2be62c12627ce878ca8cd14a'},
    # Add all your blockchain data here
]

# Convert to a DataFrame
df = pd.DataFrame(blockchain_data)

# Streamlit interface
st.title("Blockchain Simulation")
st.write("This is the blockchain simulation for genetic data security.")
st.write("Each block contains an index, previous hash, data (encoded), and its own hash.")
st.dataframe(df)

# Optionally, add a selectbox to view details of each block
block_index = st.selectbox("Select a block to view details:", df['index'])
block_details = df[df['index'] == block_index].iloc[0]
st.write(f"Details for Block {block_index}:")
st.write(f"Previous Hash: {block_details['previous_hash']}")
st.write(f"Data: {block_details['data']}")
st.write(f"Hash: {block_details['hash']}")
