import streamlit as st
from google import genai
from google.genai import types

# -------------------------------------------------------------------
# 1. PAGE SETUP & HEADER
# -------------------------------------------------------------------
st.title("🤖 AI Legal & SOP Command Center")
st.caption("Direct System-Aware Q&A Console with Persistent Session Memory")

# -------------------------------------------------------------------
# 2. SYSTEM PROMPT DEFINITION
# -------------------------------------------------------------------
SYSTEM_PROMPT = """
You are the Chief Legal & Electoral Compliance AI Agent for the Secure Voting System.
Your job is to provide direct, accurate, and authoritative guidance to voting administrators 
regarding electoral laws, security standard operating procedures (SOPs), voter registration guidelines, 
and protocol responses to cyber incidents.

Guidelines:
1. Speak professionally, concisely, and with authority.
2. Contextualize answers within standard election laws, audit requirements, and cyber threat protocols.
3. Maintain exact continuity with previous messages in the conversation thread.
4. Format responses cleanly using bold text, lists, or structured key points when explaining procedures.
"""

# -------------------------------------------------------------------
# 3. INITIALIZE GEMINI CLIENT & CHAT HISTORY
# -------------------------------------------------------------------
# Read API key from Streamlit secrets or fallback environment
api_key = st.secrets.get("GEMINI_API_KEY", None)

if not api_key:
    st.warning("⚠️ `GEMINI_API_KEY` missing. Please add it to `.streamlit/secrets.toml` or set environment variables.")

client = genai.Client(api_key=api_key) if api_key else None

# Initialize persistent memory in session state
if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = [
        {
            "role": "model",
            "content": "Greetings, Administrator. I am online and synced with electoral SOP protocols. How may I assist you with legal or operational compliance today?"
        }
    ]

# Sidebar control to clear conversation thread
with st.sidebar:
    st.markdown("### 💬 Memory Controls")
    if st.button("Clear Chat Memory", use_container_width=True):
        st.session_state["chat_messages"] = [
            {
                "role": "model",
                "content": "Chat history cleared. Standby for new compliance queries."
            }
        ]
        st.rerun()

# -------------------------------------------------------------------
# 4. RENDER PREVIOUS CONVERSATION HISTORY
# -------------------------------------------------------------------
for message in st.session_state["chat_messages"]:
    avatar = "🤖" if message["role"] in ["model", "assistant"] else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# -------------------------------------------------------------------
# 5. USER INPUT & CONVERSATION DISPATCH
# -------------------------------------------------------------------
if user_prompt := st.chat_input("Ask about electoral laws, SOP protocols, or emergency guidelines..."):
    # Render user input instantly in chat UI
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_prompt)
    
    # Store user message in history
    st.session_state["chat_messages"].append({"role": "user", "content": user_prompt})

    # Prepare historical context payload for Gemini API
    # Maps internal history to required format: list of Content objects
    api_contents = []
    for msg in st.session_state["chat_messages"]:
        api_contents.append(
            types.Content(
                role=msg["role"],
                parts=[types.Part.from_text(text=msg["content"])]
            )
        )

    # Generate response
    with st.chat_message("assistant", avatar="🤖"):
        if client:
            with st.spinner("Analyzing election protocols and compliance history..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=api_contents,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_PROMPT,
                            temperature=0.3, # Low temperature for accurate, factual responses
                        )
                    )
                    bot_response = response.text
                    st.markdown(bot_response)
                    
                    # Store model response in session state memory
                    st.session_state["chat_messages"].append({"role": "model", "content": bot_response})
                    
                except Exception as e:
                    st.error(f"Execution Error: {str(e)}")
        else:
            st.error("Client not initialized. Check your API Key configuration.")