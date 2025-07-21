# import streamlit as st
# from pathlib import Path 

# # In langchain we have secret agents  fore more you can 
# # Go and check the langchain ! as well ! for it ! 

# from langchain.agents import create_sql_agent

# ## Creating SQL DATA BASES 

# from langchain.sql_database import SQLDatabase            ## SQLDATABASES
# from langchain.agents.agent_types import AgentType
# from langchain.callbacks import StreamlitCallbackHandler
# from langchain.agents.agents_toolkits import SQLDatabasesTook    

# from sqlalchemy import create_engine  ## sQLALCHEMY -------> MAPPED THE  O/P THAT IS COMING  YOUR SQL DATABASE ! 
# import sqlite3 ## 
# from langchain_groq import ChatGroq



# ## sET OUR PAGE CONFIG. TITLE 

# st.set_page_config(page_title="LangChain: Chat with SQL DB", page_icon="🦜")
# st.title("🦜 LangChain: Chat with SQL DB")


# ## Creating a 2 Local and 2 Global Variables ! 
# ## Creating this 2 variables ! 

# LOCALDB="USE_LOCALDB"
# MYSQL="USE_MYSQL"

# ## We create some radio option 


# radio_opt=["Use SQLLite 3 Database- Student.db","Connect to you MySQL Database"]

# ## Use SQLLite 3 Database- Student.db" --------> 0th index ! 
# ## Connect to you MySQL Database --------------> 1st index ! 


# selected_opt=st.sidebar.radio(label="Choose the DB which you want to chat",options=radio_opt)

# if radio_opt.index(selected_opt) ==1:  ## here i will be selecting the index ! 
#     db_uri = MYSQL
#     myql_host = st.sidebar.text_input("Provide y SQl Host name")  ## First parameter required in order to connect with my sql workbench ! 
#     mysql_user=st.sidebar.text_input("MYSQL User")
#     mysql_password=st.sidebar.text_input("MYSQL password",type="password")
#     mysql_db=st.sidebar.text_input("MySQL database")
    
# ## If he select the 1st option ! 
# else:
#     db_uri = LOCALDB
    

# api_key=st.sidebar.text_input(label="GRoq API Key",type="password")

# ##  We will make sure that all buttons need to selected and all the api keys need to given ! 

# if not db_uri:
#     st.info("Please enter the database information and uri")

# if not api_key:
#     st.info("Please add the groq api key")
    
    
#  ## USING LLM MODELS WITH OUR SECRET TOOLS KIT ! 

# llm=ChatGroq(groq_api_key=api_key,model_name="Llama3-8b-8192",streaming=True)

# ## cREATING AN VERY IMPORTANT FUNCTION ! 
# ## here we use decorator 

# @st.cache_resource(ttl="2h")
# def configure_db(db_uri,mysql_host=None,mysql_user=None,mysql_password=None,mysql_db=None):
#     if db_uri==LOCALDB:
 
#  ## Will create a file path that is we are giving to db !
 
#         dbfilepath=(Path(__file__).parent/"student.db").absolute()
#         print(dbfilepath)
#         creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
#         return SQLDatabase(create_engine("sqlite:///", creator=creator))
    
#     elif db_uri==MYSQL:
#         if not (mysql_host and mysql_user and mysql_password and mysql_db):
#             ##  if any  of this is not excecuted then we can say tht its an error ! 
#             st.error("Please provide all MySQL connection details.")
#             st.stop()
#         return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))   


# if db_uri==MYSQL:
#     db=configure_db(db_uri,mysql_host,mysql_user,mysql_password,mysql_db)
# else:
#     db=configure_db(db_uri)
    
    
# ## This is mostly about the connecting the databases ! 




import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq

st.set_page_config(page_title="LangChain: Chat with SQL DB", page_icon="🦜")
st.title("🦜 LangChain: Chat with SQL DB")

LOCALDB="USE_LOCALDB"
MYSQL="USE_MYSQL"

radio_opt=["Use SQLLite 3 Database- Student.db","Connect to you MySQL Database"]

selected_opt=st.sidebar.radio(label="Choose the DB which you want to chat",options=radio_opt)

if radio_opt.index(selected_opt)==1:
    db_uri=MYSQL
    mysql_host=st.sidebar.text_input("Provide MySQL Host")
    mysql_user=st.sidebar.text_input("MYSQL User")
    mysql_password=st.sidebar.text_input("MYSQL password",type="password")
    mysql_db=st.sidebar.text_input("MySQL database")
else:
    db_uri=LOCALDB

api_key=st.sidebar.text_input(label="GRoq API Key",type="password")

if not db_uri:
    st.info("Please enter the database information and uri")

if not api_key:
    st.info("Please add the groq api key")

## LLM model
llm=ChatGroq(groq_api_key=api_key,model_name="Llama3-8b-8192",streaming=True)

@st.cache_resource(ttl="2h")
def configure_db(db_uri,mysql_host=None,mysql_user=None,mysql_password=None,mysql_db=None):
    if db_uri==LOCALDB:
        dbfilepath=(Path(__file__).parent/"student.db").absolute()
        print(dbfilepath)
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    elif db_uri==MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Please provide all MySQL connection details.")
            st.stop()
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))   
    
if db_uri==MYSQL:
    db=configure_db(db_uri,mysql_host,mysql_user,mysql_password,mysql_db)
else:
    db=configure_db(db_uri)
    
    
    
    
## DESIGNING THE TOOLKITS ! 


toolkit = SQLDatabaseToolkit(db=db,llm=llm)


agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose= True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

## hERE WE NEED TO CREATE TO CREATE A SESSION STATE AND HISTORY ! 

if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]


## WE HAVE TO INTEGRATED IN A MESSAGE AND APPENDING EVERYTHING INSIDE THE CHAT MESSAGE 

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_query=st.chat_input(placeholder="Ask anything from the database")


if user_query:
    
    ## wE NEED TO APPEND THE SPECIFIC STATE FROM THE USER ! 
    
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)


    with st.chat_message("assistant"):
        streamlit_callback=StreamlitCallbackHandler(st.container())
        ## aRE THE CALLS BACK WHAT CHAIN OF THOUGHTS !
        response=agent.run(user_query,callbacks=[streamlit_callback])
        st.session_state.messages.append({"role":"assistant","content":response})
        st.write(response)
#