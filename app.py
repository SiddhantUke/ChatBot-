import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper,WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun,DuckDuckGoSearchRun
from langchain.agents import initialize_agent,AgentType
from langchain.callbacks import StreamlitCallbackHandler ## Communicate  all tools within themselves.
import os 
from dotenv import load_dotenv

# DuckDuckGoSearchRun --------> For search from an internet !



## INITIALIZE THE TOOLS THAT IS ARXIV AND WIKIPEDIA TOOLS 

arxiv_wrapper = ArxivAPIWrapper(top_k_result=1, doc_content_chars_max=200)
arxiv = ArxivQueryRun(api_wrapper=arxiv_wrapper)

api_wrapper = WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=200)
wiki = WikipediaQueryRun(api_wrapper=api_wrapper)

## The Kind of Task that we want to do from duck duck go search !

search=DuckDuckGoSearchRun(name="Search")


## Title 

st.title("🔎 LangChain - Chat-Agent")
"""
Meet the chatbot that doesn’t just respond — it investigates.

Built with LangChain and Groq’s lightning-fast LLM, this assistant intelligently decides when to search the live web, when to pull academic insights from arXiv, 
and when to explore Wikipedia — all while revealing its thought process in real time through a dynamic Streamlit interface.
"""


## Help us to what action and agent that actually work with it ! or when it is interacting with the tools.




## Creating side bar for calling any api ! for 
## Sidebar for setting

st.sidebar.title("Settings")
api_key=st.sidebar.text_input("Enter your Groq API Key:",type="password")



## So now my entire conversation happend along with the chat history ! 


if "messages" not in st.session_state:
    st.session_state["messages"]=[
        {"role":"assisstant","content":"Hi,I'm a chatbot who can search the web."}  ## Default assisstant information that we have ! 
    ]


for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])
    
    
if prompt:=st.chat_input(placeholder="How can i help you ?"):
    st.session_state.messages.append({"role":"user","content":prompt})
    st.chat_message("user").write(prompt)
    
    ## Inside this  groq we have to create llm 
    
    llm = ChatGroq(groq_api_key = api_key,model_name = "Llama3-8b-8192" , streaming=True)
    ## We have to take this groq api key with a parameter with a input itself.
    
    ## We have to initialize the tools ------> wiki,arxiv and search !
    tools = [search,arxiv,wiki]
    
    ## We have to convert that  entire tools into an agent so we able to invoke this 
    
    search_agent=initialize_agent(tools,llm,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,handling_parsing_errors=True)
    
    ##ZERO_SHOT_REACT_DESCRIPTION AND CHAT_ZERO_SHOT_REACT_DESCRIPTION (CHECK DOC )
    
    # basically lies in how they handle context and memory and how they generate prompt from the language model 
    
    ######## ZERO_SHOT_REACT_DESCRIPTION --------------> THEY RELAY ON THE CHAT  HISTORY ! 
    
    ######## CHAT_ZERO_SHOT_REACT_DESCRIPTION ------------> IT USES A CHAT HISTORY TO REMEMBERED THE CONTEXT OF THE CHAT HISTORY OF THE CONVERSATION ! 
    ######## IT ACCESS A CERTAIN STRUCTURE IN THE CHAT HISTORY MIGHT RAISED AN ERROR IF IT DOES NOT FIND IT ! 
    ######## WE ARE USING HERE ---------------> ZERO_SHOT 
    
    with st.chat_message("assistant"):
        st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
        
        ## once we use this streamlit callback handle it is display the thoughts and action in agent in inter active streamlit app 
        ### SO NOW WHENEVER MY AGENT IS COMMUNICATE WITH ITSELF  
        
        response=search_agent.run(st.session_state.messages,callbacks=[st_cb])
        
        st.session_state.messages.append({'role':'assistant',"content":response})
        
        st.write(response)

    
    