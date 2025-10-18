import streamlit as st
import boto3
from botocore.exceptions import ClientError
import json
from bedrock_utils import query_knowledge_base, generate_response, valid_prompt

# Page setup
st.set_page_config(page_title="AWS Bedrock Knowledge Base App", page_icon="🧠", layout="centered")
st.title("🧠 Bedrock Knowledge Base Chat")
st.write("Interact with your **Amazon Bedrock Knowledge Base** to retrieve and generate information about heavy machinery using LLMs.")

st.divider()

# Sidebar configuration
st.sidebar.header("Configuration")
model_id = st.sidebar.selectbox(
    "Select LLM Model",
    ["amazon.titan-text-express-v1", "anthropic.claude-3-haiku-20240307-v1:0"]
)
kb_id = st.sidebar.text_input("Knowledge Base ID", "<YOUR_KNOWLEDGE_BASE_ID>")
temperature = st.sidebar.select_slider("Temperature", [i/10 for i in range(0, 11)], 0.7)
top_p = st.sidebar.select_slider("Top_P", [i/10 for i in range(0, 11)], 0.9)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input field
if prompt := st.chat_input("Ask a question about heavy machinery..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Validate prompt
    if valid_prompt(prompt, model_id):
        st.info("🔍 Query accepted — retrieving information...")
        kb_results = query_knowledge_base(prompt, kb_id)

        # Build context from KB results
        if kb_results:
            st.write("### 📚 Knowledge Base Results:")
            context = "\n".join([result["content"]["text"] for result in kb_results])
            for i, res in enumerate(kb_results, 1):
                st.markdown(f"**Result {i}:** {res['content']['text']}")
                st.caption(f"Source: {res['location']['s3Location']['uri']} — Score: {res['score']:.3f}")
        else:
            st.warning("No relevant knowledge base results found.")
            context = "No relevant context found."

        # Generate model response
        st.info("🧠 Generating response using the selected model...")
        full_prompt = f"Context: {context}\n\nUser: {prompt}\n\n"
        response = generate_response(full_prompt, model_id, temperature, top_p)

    else:
        st.error("🚫 Query rejected. Please enter a heavy machinery–related query.")
        response = "I'm unable to answer this. Please try again with a heavy machinery topic."

    # Display assistant's response
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})