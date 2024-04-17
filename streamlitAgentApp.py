# develop a Streamlit application that allows users to upload a .csv file and perform data-analysis using Langchain's CSV Agent:
# Upload a csv file
# Choose an LLM
# Input a query
# Visualize the response from the LLM
import os, tempfile
# import pinecone
from pathlib import Path
import streamlit as st
from unify import AsyncUnify,Unify
import asyncio
import nest_asyncio
# nest_asyncio.apply()


st.set_page_config(page_title="RAG")
st.title("Talk to your Data ")















def input_fields():
 
    with st.sidebar:
        if "UNIFY_KEY" in st.secrets:
            st.session_state.UNIFY_KEY = st.secrets.UNIFY_KEY
        else:
            st.session_state.UNIFY_KEY = st.text_input("Unify key", type="password")
        llm_options = ['llama-2-7b-chat', 'gemma-7b-it'] #conditional
        provider_options = ['anyscale', 'together-ai']
        
        
        llm1_selected_option = st.selectbox("Select LLM 1", llm_options)
        provider1_selected_option = st.selectbox("Select Provider 1", provider_options)
        llm2_selected_option = st.selectbox("Select LLM 2", llm_options)
        provider2_selected_option = st.selectbox("Select Provider 2", provider_options)
        
        st.session_state.llm1 = llm1_selected_option
        st.session_state.llm2 = llm2_selected_option
        st.session_state.provider1 = provider1_selected_option
        st.session_state.provider2 = provider2_selected_option
        # if "pinecone_api_key" in st.secrets:
        #     st.session_state.pinecone_api_key = st.secrets.pinecone_api_key
        # else: 
        #     st.session_state.pinecone_api_key = st.text_input("Pinecone API key", type="password")
        # #

    #
    # st.session_state.source_docs = st.file_uploader(label="Upload Documents", type="pdf", accept_multiple_files=True)
    #
    return

def process_documents():
    pass

async def a_query_llm(llm, provider,query):
    
    endpoint = str(llm+"@"+provider)
    async_unify = AsyncUnify(
        api_key=st.session_state.UNIFY_KEY,
        endpoint=endpoint
    )
    responses = await async_unify.generate(user_prompt=query)
    
    return responses

def query_llm(llm, provider,query):
    endpoint = str(llm+"@"+provider)  
    unify = Unify(
        api_key=st.session_state.UNIFY_KEY,
        endpoint=endpoint
    )
    responses = unify.generate(user_prompt=query)
    
    return responses

def boot():
    #
    input_fields()
    
    # st.button("Submit Documents", on_click=process_documents)
    
    #store messages in a list
    if "messages_1" not in st.session_state:
        st.session_state.messages1 = []
    
    if "messages_2" not in st.session_state:
        st.session_state.messages2 = []
    
    
    # if query := st.chat_input():

    #     st.session_state.messages1.append(("You", query))
    #     st.session_state.messages2.append(("You", query))
    
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(str(st.session_state.llm1 + '@' + st.session_state.provider1))
        # for message in st.session_state.messages1:
        #     st.chat_message('You').write(message[0])
        #     st.chat_message('1').write(message[1])   
    
    with col2:  
        st.subheader(str(st.session_state.llm2 + '@' + st.session_state.provider2))    
        # for message in st.session_state.messages2:
        #     st.chat_message('You').write(message[0])
        #     st.chat_message('2').write(message[1])    

    if query := st.chat_input(): 
        with col1:
            response1 = asyncio.run(a_query_llm(st.session_state.llm1,st.session_state.provider1, query))
            # response1 = query_llm(st.session_state.llm1,st.session_state.provider1, query)
            st.chat_message("1").write(response1)

            
        with col2:
            st.chat_message("You").write(query)
            # response2 = query_llm(st.session_state.llm2,st.session_state.provider2, query)
            response2 = asyncio.run(a_query_llm(st.session_state.llm2,st.session_state.provider2, query))
            st.chat_message("2").write(response2)





if __name__ == '__main__':
    
    boot()
    