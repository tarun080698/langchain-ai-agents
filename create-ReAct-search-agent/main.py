from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from tavily import TavilyClient
from langchain_tavily import TavilySearch


# our custom tool to search the web using Tavily API and other tools to get current time and logged in user
tavily = TavilyClient()


@tool
def search(query: str) -> str:
    """
    Tool that searches the web for a query and returns the results as a string.

    Args:
        query (str): The search query.

    Returns:
        str: The search results.
    """
    print(f"Searching for: {query}")
    return tavily.search(query=query)


@tool
def get_current_time() -> str:
    """
    Tool that returns the current time as a string.

    Returns:
        str: The current time.
    """
    from datetime import datetime
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Current time: {current_time}")
    return current_time

@tool
def get_current_logged_in_user() -> str:
    """
    Tool that returns the current logged in user as a string.

    Returns:
        str: The current logged in user.
    """
    import getpass
    user = getpass.getuser()
    print(f"Current logged in user: {user}")
    return user


llm = ChatOpenAI()
# tools = [search, get_current_time, get_current_logged_in_user]
tools = [TavilySearch()]

agent = create_agent(model=llm, tools=tools)


def main():
    print("Hello from create-react-search-agent!")
    result = agent.invoke({"messages": [HumanMessage(content="find me the top 3 best courses on Udemy to learn Generative AI and get the links to those courses from udemy only, no external links")]})
    print(f"Agent result: {result}")


if __name__ == "__main__":
    main()
