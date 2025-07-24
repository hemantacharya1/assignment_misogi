import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.2,
    )

def get_db_toolkit(db_path: str, llm):
    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    return create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )
