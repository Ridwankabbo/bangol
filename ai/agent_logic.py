from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import create_react_agent ,AgentExecutor
from langchain_classic import hub
from langchain_core.prompts import PromptTemplate
from .ai_tools import search_products, create_order_from_chat
from django.conf import settings
from langchain_google_genai import HarmBlockThreshold, HarmCategory
from langchain_core.messages import HumanMessage, AIMessage

def run_ecommerce_agent(user_querry, history_list=[]):
    
    llm = ChatGoogleGenerativeAI(
        model = 'gemini-2.5-flash', 
        temperature = 0,
        google_api_key=settings.GOOGLE_API_KEY,
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        },
    )
    
    tools = [search_products, create_order_from_chat]
    
    
    chat_history = []
    for role ,text in history_list:
        if role == 'user':
            chat_history.append(HumanMessage(content=text))
        else:
            chat_history.append(AIMessage(content=text))
            
    
    
    
    custom_instructions = """
    You are a helpful Bengali e-commerce assistant.
    If you find products to show, your 'Final Answer' must follow this EXACT structure:

    MESSAGE: [A friendly response in Bengali about the items found]
    DATA: [A JSON array of product objects with: "id", "name", "price", "category"]

    If no products are found or it's a general question, just provide the MESSAGE.
    """

    # 2. This is the standard ReAct structure that LangChain understands
    template = """Answer the following questions as best you can. You have access to the following tools:

        {tools}
        
        and Current Conversation:
        {chat_history}

        Use the following format:

        Question: the input question you must answer
        Analyse: if user has provious history analyse the user by his previous history 
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        """ + custom_instructions + """
        Final Answer: the final answer to the original input question

        Begin!

        Question: {input}
        Thought: {agent_scratchpad}
    """
    
    prompt = PromptTemplate.from_template(template)
    
    agent = create_react_agent(llm, tools, prompt)
    
    agent_executro = AgentExecutor(
        agent=agent,
        tools=tools,
        verbos=True,
        handle_parsing_errors=True
    )
    
    result = agent_executro.invoke({'input': user_querry, 'chat_history':chat_history})
    return result['output']