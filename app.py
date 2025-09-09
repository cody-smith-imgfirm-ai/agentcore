import boto3
import streamlit as st
import uuid
import json

client = boto3.client('bedrock-agentcore', region_name='us-east-1')

if st.text_input("Password", type="password") != "rhino123":
    st.stop()

st.title("Bedrock AgentCore Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask your agent..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = client.invoke_agent_runtime(
            agentRuntimeArn='arn:aws:bedrock-agentcore:us-east-1:241533114932:runtime/my_agent-jMBdrN9uzu',
            payload=json.dumps({'prompt': prompt}).encode(),
            runtimeSessionId=str(uuid.uuid4())
        )
        # print(response)

        # Read the streaming response
        response_body = response['response'].read()
        result = json.loads(response_body.decode('utf-8'))

        # Extract the actual message text
        message_text = result['result']['content'][0]['text']
        st.markdown(message_text)
        st.session_state.messages.append({"role": "assistant", "content": message_text})