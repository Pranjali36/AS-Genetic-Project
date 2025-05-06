import pandas as pd
import random
import streamlit as st

# Load or create the dataset
df = pd.DataFrame({
    'Person_ID': range(1, 6),
    'Genetic_Sequence': ['ATCGATCGGT', 'CGTACGATAC', 'GCTAGCTAGG', 'TGCATGCAAG', 'ACGTACGTAA']
})

# Function to generate random genetic sequences
def generate_sequence():
    return ''.join(random.choices('ACGT', k=10))

# Simulate hack (altering or deleting data)
def simulate_hack(df):
    hack_index = random.choice(df.index)
    attack_type = random.choice(['alter', 'delete'])
    if attack_type == 'alter':
        df.at[hack_index, 'Genetic_Sequence'] = generate_sequence()
        return f"Data altered for Person {df.at[hack_index, 'Person_ID']}."
    elif attack_type == 'delete':
        person_id = df.at[hack_index, 'Person_ID']
        df.drop(hack_index, inplace=True)
        return f"Data deleted for Person {person_id}."

# Streamlit UI for Cell 4 - Hack Attempt Simulation
st.write("## Hack Attempt Simulation")
st.write("This is the original genetic data.")

# Show original data
st.write("### Original Genetic Data")
st.dataframe(df)

# Button to simulate a hack attempt (alter or delete data)
if st.button("Simulate Hack"):
    hack_result = simulate_hack(df)
    st.write(hack_result)
    st.write("### Altered Genetic Data (After Hack Attempt)")
    st.dataframe(df)
