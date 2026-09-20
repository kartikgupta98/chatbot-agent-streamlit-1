import streamlit as st
from langchain_groq import ChatGroq

st.set_page_config(page_title='My AI Chat', layout='centered')

st.title("🤖 The Groq Chatbot")
st.write("A fully integrated, memory-enabled AI assistant.")

# The Sidebar (API Key Security)
with st.sidebar:
    st.header("⚙️ Configuration")
    user_api_key = st.text_input('Enter the Groq API Key:', type='password')
    st.info('Your key is required to wake up the AI Brain')

# ------ 2. The Memory Vault -------
if 'messages' not in st.session_state:
    st.session_state.messages = []

# ----- 3. Display History ---------
for msg in st.session_state.messages:
    with st.chat_message(msg['role']): # This display human and ai message differently
        st.markdown(msg['content'])

# 4. Chat Input and Logic
if user_query := st.chat_input('Say something to the AI...'):
# := -> operator waits until the user enters the message and then stores it

    if not user_api_key:
        st.error('Please enter your api key in the sidebar first!')
    else:
        # Display the user message instantly
        with st.chat_message('user'):
            st.markdown(user_query)

        # Store the user messsages to the vault
        st.session_state.messages.append({'role':'user', 'content': user_query})


        # Initialise the Brain
        llm = ChatGroq(
            model = 'openai/gpt-oss-20b',
            temperature = 0.7, # Creativity level of the model
            api_key = user_api_key
        )

        with st.spinner('AI is thinking....'):
            response = llm.invoke(st.session_state.messages)
            bot_answer = response.content

            
        st.session_state.messages.append({'role':'assistant', 'content':bot_answer})
        with st.chat_message('assistant'):
            st.markdown(bot_answer)
