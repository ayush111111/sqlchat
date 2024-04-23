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
st.title("Talk to your Data")


def input_fields():
 
    with st.sidebar:
        if "UNIFY_KEY" in st.secrets:
            st.session_state.UNIFY_KEY = st.secrets.UNIFY_KEY
        else:
            st.session_state.UNIFY_KEY = st.text_input("Unify key", type="password")
        llm_options = ['llama-2-7b-chat', 'gemma-7b-it'] #conditional
        provider_options = ['anyscale', 'together-ai']
        
        
        llm_selected_option = st.selectbox("Select LLM ", llm_options)
        provider_selected_option = st.selectbox("Select Provider ", provider_options)
        
        # llm1_selected_option = st.selectbox("Select LLM 1", llm_options)
        # provider1_selected_option = st.selectbox("Select Provider 1", provider_options)
        # llm2_selected_option = st.selectbox("Select LLM 2", llm_options)
        # provider2_selected_option = st.selectbox("Select Provider 2", provider_options)
        
        st.session_state.llm = llm_selected_option
        # st.session_state.llm2 = llm2_selected_option
        st.session_state.provider = provider_selected_option
        # st.session_state.provider2 = provider2_selected_option
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


# async def fetch_responses(query):
#     response1 = a_query_llm(st.session_state.llm1, st.session_state.provider1, query)
#     response2 = a_query_llm(st.session_state.llm2, st.session_state.provider2, query)
#     return await asyncio.gather(response1, response2)

def query_llm(llm, provider, query):
    endpoint = f"{llm}@{provider}"  
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
    
    # store messages in a list
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    # if "messages1" not in st.session_state:
    #     st.session_state.messages1 = []
    
    # if "messages2" not in st.session_state:
    #     st.session_state.messages2 = []
    
    
    # if query := st.chat_input():

    #     st.session_state.messages.append(("You", query))
        # st.session_state.messages1.append(("You", query))
    #     st.session_state.messages2.append(("You", query))
    
    st.subheader(f"{st.session_state.llm}@{st.session_state.provider}")
    for message in st.session_state.messages:
        st.chat_message('You').write(message[0])
        st.chat_message('LLM').write(message[1])       
    # col1, col2 = st.columns(2)
    # st.subheader(f"{st.session_state.llm1}@{st.session_state.provider1}")
    # for message in st.session_state.messages1:
    #     st.chat_message('You').write(message[0])
    #     st.chat_message('1').write(message[1])      
    # with col1:
    #     st.subheader(f"{st.session_state.llm1}@{st.session_state.provider1}")
    #     for message in st.session_state.messages1:
    #         st.chat_message('You').write(message[0])
    #         st.chat_message('1').write(message[1])   
    
    # with col2:  
    #     st.subheader(f"{st.session_state.llm2}@{st.session_state.provider2}")
    #     for message in st.session_state.messages2:
    #         st.chat_message('You').write(message[0])
    #         st.chat_message('2').write(message[1])    

    if query := st.chat_input(): 
        # responses = asyncio.run(fetch_responses(query))
        # responses = asyncio.run(fetch_responses(query))
        responses = query_llm(st.session_state.llm, st.session_state.provider, query)
         # Update the message histories
        st.session_state.messages.append((query, responses))
        # st.session_state.messages1.append((query, responses[0]))
        # st.session_state.messages2.append((query, responses[1]))

        st.chat_message("You").write(query)
        st.chat_message("LLM").write(responses)
        # with col1:
        #     st.chat_message("You").write(query)
            
        #     # response1 = query_llm(st.session_state.llm1,st.session_state.provider1, query)
        #     st.chat_message("1").write(responses[0])

            
        # with col2:
        #     st.chat_message("You").write(query)
        #     # response2 = query_llm(st.session_state.llm2,st.session_state.provider2, query)
            
        #     st.chat_message("2").write(responses[1])

    # input_fields()
    # #
    # st.button("Submit Documents", on_click=process_documents)
    # #
    # if "messages" not in st.session_state:
    #     st.session_state.messages = []
    # #
    # for message in st.session_state.messages:
    #     st.chat_message('human').write(message[0])
    #     st.chat_message('ai').write(message[1])    
    # #
    # if query := st.chat_input():
    #     st.chat_message("human").write(query)
    #     response = query_llm(st.session_state.retriever, query)
    #     st.chat_message("ai").write(response)



if __name__ == '__main__':
    
    boot()
    