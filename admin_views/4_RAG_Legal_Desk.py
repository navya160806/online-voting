import streamlit as st
from google import genai
from google.genai import types
import streamlit as st

# Safety check: Initialize the key if Streamlit pre-runs this file out of order
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state.get("authenticated", False):
    st.error("🔒 Unauthorized access. Please log in through the main portal.")
    st.stop()

st.title("🤖 AI Legal Desk & SOP Advisor (RAG)")
st.write("Plain-text explanations of complex automated decisions alongside local statutory references.")

# Internal regulatory documentation string acting as your local vector cache
MOCK_KNOWLEDGE_BASE = """
REGULATORY STANDARD OPERATING PROCEDURES (SOP)
Section 42-B (Signature Matches Validation): Borderline registration records containing automated signature match confidence scores between 60% and 70% MUST NOT be automatically rejected by the engine. The system administrator is legally bound to place the file into a 48-hour 'Verification Hold' queue and immediately trigger a physical notification mail out to the voter.
Section 14-A (Database Deadlocks / Cluster Failure): In the event of an infrastructure cluster failure or database deadlock in Region 4, the admin must execute the following sequence:
1. Force dump active configuration cryptographic key tables directly to secure backup storage.
2. Reboot master database node controllers sequentially.
3. Re-initialize active user session cryptographic handshakes to eliminate the vector of double ballot submissions.
"""

# Section 1: Explainable AI Engine
st.subheader("🔍 Explainable AI (XAI) Logs Explainer")
target_alert = st.selectbox("Choose Technical Incident Profile to Translate:", [
    "IP Flagged: 198.51.100.45 (Isolation Forest score -1, Contamination threshold passed)",
    "Voter Flagged: V-10294 (Signature Similarity score calculated at 65% index)"
])

if st.button("Synthesize Auditor Legal Explanation", type="primary"):
    with st.spinner("Decoding infrastructure decision vectors..."):
        client = genai.Client(api_key=st.secrets.get("GEMINI_API_KEY", "YOUR_API_KEY"))
        
        prompt = f"Deconstruct this incident and translate the system parameters into clear, auditable operational steps:\n{target_alert}"
        system_instruction = f"You are a Federal Election Security Auditor. Translate technical data metrics into clear, legally defensive justifications. Use this context strictly:\n{MOCK_KNOWLEDGE_BASE}"
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.1
            )
        )
        st.info(response.text)

st.write("---")

# Section 2: Conversational Copilot Chat Interface
st.subheader("💬 Active Disaster Runbook & Protocol Query Chat")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if query := st.chat_input("Ex: How do we safely reboot database nodes in Region 4 while preserving active session cryptography?"):
    st.chat_message("user").markdown(query)
    st.session_state.chat_history.append({"role": "user", "content": query})
    
    with st.chat_message("assistant"):
        with st.spinner("Querying vector reference framework..."):
            client = genai.Client(api_key=st.secrets.get("GEMINI_API_KEY", "YOUR_API_KEY"))
            system_instruction = f"Provide direct instructions based ONLY on this text documentation. Do not invent any outside info:\n{MOCK_KNOWLEDGE_BASE}"
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=query,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.1
                )
            )
            st.markdown(response.text)
            st.session_state.chat_history.append({"role": "assistant", "content": response.text})