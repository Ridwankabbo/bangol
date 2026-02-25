from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import create_react_agent ,AgentExecutor
from langchain_classic import hub
from .ai_tools import search_products, create_order_from_chat
from django.conf import settings
from langchain_google_genai import HarmBlockThreshold, HarmCategory

def run_ecommerce_agent(user_querry):
    
    llm = ChatGoogleGenerativeAI(
        model = 'gemini-2.5-flash', 
        temperature = 0,
        google_api_key=settings.GOOGLE_API_KEY,
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    },
    )
    
    tools = [search_products, create_order_from_chat]
    
    prompt = hub.pull("hwchase17/react")
    
    agent = create_react_agent(llm, tools, prompt)
    
    agent_executro = AgentExecutor(
        agent=agent,
        tools=tools,
        verbos=True,
        handle_parsing_errors=True
    )
    
    result = agent_executro.invoke({'input': user_querry})
    return result