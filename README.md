# GeneBlock: Securing Genomic Data with Blockchain

GeneBlock is a prototype system designed to demonstrate a more secure and transparent way of storing and sharing genetic data using blockchain-inspired mechanisms and access control. This project simulates how encrypted genomic information can be protected from tampering and unauthorized access, while maintaining visibility of general metadata.

## 🔍 Why This Matters

Blockchain is a decentralized, tamper-evident ledger system that ensures data integrity by linking blocks of information using cryptographic hashes. Once a block is added, it cannot be altered without invalidating the entire chain.

Today, large amounts of sensitive health data — including genetic profiles — are collected and stored online. Many users are unaware that this data is often shared or sold to third-party agencies, which can lead to unsolicited insurance calls or privacy breaches.

**GeneBlock** is my attempt to present a secure, educational prototype of how this data could be stored more safely — ensuring immutability, auditability, and restricted access to the most sensitive parts of an individual's genome.

---
## 🔐 Key Features

**Encrypted Genetic Data:** 

Sensitive DNA fields (e.g., SNP ID, Genotype, Trait) are encoded using base64 for simplicity in this prototype. This mimics real-world encryption workflows and restricts direct visibility. For stronger security in production environments, methods like AES (Advanced Encryption Standard) or public-key encryption could be applied.

**Hash-Based Blockchain Security:**

Each block generates a SHA-256-like hash based on its contents and the previous block's hash.

Blocks are linked together to form a chain.

Changes in any block will break the hash chain, visually showing tampering.

**Simulated Multi-Server Blockchain:**

For demonstration, the blockchain is visually replicated across 3 independent server chains.

A majority consensus mechanism checks for integrity and flags any server chain that has been altered.

**Admin-Controlled Access:**

Admin can view encrypted DNA data with a password (Pranjali123) and generate a temporary access key for authorized users (e.g., hospitals).

**Real-Time Tamper Logs:**

A report is generated that shows which fields and servers were affected.

---

🎥 Concept Walkthrough
Watch this short demo to understand blockchain and encryption:

▶️ YouTube Video: GeneBlock - Blockchain & Encryption for Genetic Data
https://youtu.be/_160oMzblY8?si=eMMMjZyWmvJlU8eN

🧪 App Demonstrations

App 2

Simulates a hack directly on encrypted genetic data and shows what happens when data is tampered without a blockchain.

App 3

Introduces blockchain structure. Shows how tampered data breaks the hash chain and how the system detects and reports it in real-time.

App 3.6

Adds admin access and decryption control. Shows server consensus, multiple blockchain replicas, and who can decrypt sensitive DNA.

## 🧬 Data Structure (Per Patient Record)

- **Visible Metadata**:
  - Patient ID
  - Blood Group
  - Date
- **Encrypted Genetic Data**:
  - SNP_ID
  - Chromosome
  - Position
  - Genotype
  - Trait (e.g., HIV resistance)

## 🚀 How to Run the App

To run GeneBlock locally or deploy your own version:

- Clone my Repo
- Create a Streamlit Cloud Account:
- Go to https://streamlit.io/cloud
- Log in with your GitHub account
- Select “New app” and link your GitHub repo
- Choose Your Branch and File:
- Set the main file to app3.py or app3.6.py depending on the version you want to deploy.

Customize (Optional):

You can edit app3.6.py to change sample DNA, adjust admin keys, or add more patient records.

Launch App:

Click “Deploy” and your app will be live with a public link.

🛡️ Tech Stack
Python
Streamlit
Simulated Blockchain & Encryption Logic

👥 Developed by- Pranjali Thakur, student at Universituy of Geneva
Developed as part of an academic submission on Advanced Security
