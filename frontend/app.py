import streamlit as st
import requests

API_URL = "http://localhost:5000/api/find_orfs"  # Update if deployed

st.set_page_config(page_title="ORF Finder", layout="wide")
st.title("🧬 Open Reading Frame (ORF) Finder (Client)")

sequence_input = st.text_area("🔤 Paste your DNA sequence here (raw or FASTA format):", height=200)
min_length = st.slider("Minimum ORF length (in base pairs):", 30, 1000, 100, 10)

if st.button("🔍 Find ORFs"):
    if not sequence_input:
        st.warning("Please input a DNA sequence.")
    else:
        if sequence_input.startswith(">"):
            sequence_input = "\n".join(sequence_input.split("\n")[1:])

        try:
            response = requests.post(API_URL, json={
                "sequence": sequence_input,
                "min_length": min_length
            })

            if response.status_code == 200:
                data = response.json()
                orfs = data["orfs"]
                if not orfs:
                    st.error("No ORFs found.")
                else:
                    st.success(f"Found {len(orfs)} ORF(s).")
                    for i, orf in enumerate(orfs, 1):
                        with st.expander(f"ORF {i}: Frame {orf['frame']} on {orf['strand']} strand, Length {orf['length']} bp"):
                            st.code(f"Start: {orf['start']} | End: {orf['end']}\nSequence:\n{orf['sequence']}", language="text")
            else:
                st.error(f"Error: {response.json().get('error')}")
        except Exception as e:
            st.error(f"Could not connect to API: {e}")
