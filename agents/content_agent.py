from crewai import Agent,LLM
from crewai_tools import TavilySearchTool
# from langchain.tools import WikipediaQueryRun
# from langchain.utilities import WikipediaAPIWrapper
import os
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai

gemini_api_key = os.getenv('GEMINI_API_KEY')

llm = LLM(
    model='gemini/gemini-1.5-flash-latest',
    temperature=0.3,
    api_key=gemini_api_key,
    max_output_tokens=32768    
)

tavily_api_key = os.getenv('TAVILY_API_KEY')
tavily_search = TavilySearchTool(api_key=tavily_api_key)

# wiki_wrapper = WikipediaAPIWrapper(
#     lang='en', # English
#     top_k_results=1,
#     doc_content_chars_max=2000
# )
# wiki_tool = WikipediaQueryRun(api_wrapper = wiki_wrapper)

content_search_agent = Agent(
    role = "Content Research & Explanation Agent",
    goal = "Efficiently search for accurate and relevant information on the given topic, extract key insights,"
            "and simplify complex concepts into clear, beginner-friendly explanations.",
    backstory= ("An expert researcher with access to vast knowledge sources and a skilled teacher who can simplify complex concepts."
                "Always ensures the information is accurate, concise, and easy to understand for beginners."),
    llm = llm,
    tools = [tavily_search],
    verbose= True,
    allow_delegation=False,
    always_respond=True  
)