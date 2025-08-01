import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMMathChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent
from langchain.callbacks import StreamlitCallbackHandler


## from dotenv import load_dotenv
# load_dotenv()
## IF WE ARE USING ENVIRONMENT VARIABLES 
## GIVING THE API KEY IN THE .env file
## WE ARE GIVING THE API KEY FROM THE WEBSITE DIRECTLY


## SET UP THE STREAMLIT APP
st.set_page_config(page_title="Text To Math Problem Solver And Data Search Assistant", page_icon="🧮")
st.title("Text To Math Problem Solver Using Google Gemma 2")

## WHICH LLM MODEL WE ARE USING ?
## WE ARE USING GEMMA 2 MODEL FROM GROQ

groq_api_key = st.sidebar.text_input(label="Groq API Key", type="password")

if not groq_api_key:
    st.info("Please add your Groq API key to continue")
    st.stop()
    
llm = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

## INITIALIZING THE TOOLS

wikipedia_wrapper = WikipediaAPIWrapper()
wikipedia_tool = Tool(
    name="Wikipedia",
    func=wikipedia_wrapper.run,
    description="A tool for searching the Internet to find various information on the topics mentioned"
)
    
## If we want to run the app then we need to do the functn that is wikipedia_wrapper.run

## INITIALIZE THE MATH TOOL

math_chain = LLMMathChain.from_llm(llm=llm)
calculator = Tool(
    name="Calculator",
    func=math_chain.run,
    description="A tool for answering math related questions. Only input mathematical expression need to be provided"
)

prompt = """Your an agent tasked for solving users mathematical question. Logically arrive at the solution and provide a detailed explanation
and display it point wise for the question below
Question: {question}
Answer:
"""

prompt_template = PromptTemplate(
    input_variables=["question"],
    template=prompt
)

## COMBINE ALL THE TOOLS INTO CHAIN

## Before that we need to  create a llm chain 

chain = LLMChain(llm=llm, prompt=prompt_template)
    ## we need to create a chain for reasoning
    ## Reasoning tool for answering logic-based and reasoning questions
    
reasoning_tool = Tool(
    name="Reasoning tool",
    func=chain.run,
    description="A tool for answering logic-based and reasoning questions."
)


## INITIALIZE THE AGENTS

assistant_agent = initialize_agent(
    tools=[wikipedia_tool, calculator, reasoning_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True
)

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a helpful assistant that can answer math questions and search the internet for information."}
    ]
    
    
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])
    
    
## FUNCTION THE GENERATE THE RESPONSE

def generate_response(user_question):
    response = assistant_agent.invoke({"input": question})
    return response
 ## This function will take the user question and invoke the assistant agent to get the response
 
## LETS START THE INTERACTION
question=st.text_area("Enter youe question:","I have 5 bananas and 7 grapes. I eat 2 bananas and give away 3 grapes. Then I buy a dozen apples and 2 packs of blueberries. Each pack of blueberries contains 25 berries. How many total pieces of fruit do I have at the end?")

# if st.button("Find my answer"):
    
    ## RE UNDERSTAND HERE AND AGAIN 
    
if st.button("find my answer"):
    if question:
        with st.spinner("Generate response.."):
            st.session_state.messages.append({"role":"user","content":question})
            st.chat_message("user").write(question)

            st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
            response=assistant_agent.run(st.session_state.messages,callbacks=[st_cb]
                                         )
            st.session_state.messages.append({'role':'assistant',"content":response})
            st.write('### Response:')
            st.success(response)

    else:
        st.warning("Please enter the question")
