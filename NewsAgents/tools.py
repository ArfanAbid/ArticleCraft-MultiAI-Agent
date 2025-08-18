import os
from crewai_tools import SerperDevTool
from load_dotenv import load_dotenv

load_dotenv()

google_search_tool = SerperDevTool(
    serper_api_key=os.getenv("SERPER_API_KEY"),
)

