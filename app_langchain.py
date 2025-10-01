# I NEED TO CLARIFY THE TWO DATABASES TO REDUCE CONFUSION

# from mcp import ClientSession, StdioServerParameters
# from mcp.client.stdio import stdio_client
# from langchain_mcp_adapters.tools import load_mcp_tools
# from langgraph.prebuilt import create_react_agent
# import asyncio
# from langchain_google_genai import ChatGoogleGenerativeAI
# import os


# model = ChatGoogleGenerativeAI(
#     model="gemini-2.0-flash-001")

# # server_params = StdioServerParameters(
# #     command="python",
# #     args=[
# #         "C:\\Users\\datas\\OneDrive\\Desktop\\maths.py"
# #       ]
# # )

# server_params = StdioServerParameters(
#     command="npx",
#     args=[
#         "-y",
#         "@modelcontextprotocol/server-filesystem@latest",
#         "C:\\testfolder"
#     ]
# )

# async def run_agent():
#     async with stdio_client(server_params) as (read, write):
#         async with ClientSession(read, write) as session:
#             # Initialize the connection
#             await session.initialize()

#             # Get tools
#             tools = await load_mcp_tools(session)

#             # Create and run the agent
#             agent = create_react_agent(model, tools)
#             agent_response = await agent.ainvoke({"messages": "How many files are present in testfolder?"})
#             return agent_response

# # Run the async function
# if __name__ == "__main__":
#     try:
#         result = asyncio.run(run_agent())
#         print(result)
#     except:
#         pass


"""
langchain_mcp_client_wconfig.py

This file implements a LangChain MCP client that:
  - Loads configuration from a JSON file specified.
  - Connects to one or more MCP servers defined in the config.
  - Loads available MCP tools from each connected server.
  - Uses the Google Gemini API (via LangChain) to create a React agent with access to all tools.
  - Runs an interactive chat loop where user queries are processed by the agent.

Detailed explanations:
  - Retries (max_retries=2): If an API call fails due to transient issues (e.g., timeouts), it will retry up to 2 times.
  - Temperature (set to 0): A value of 0 means fully deterministic output; increase this for more creative responses.
"""

import asyncio                        # For asynchronous operations
import os                             # To access environment variables and file paths
import sys                            # For system-specific parameters and error handling
import json                           # For reading and writing JSON data
from contextlib import AsyncExitStack # For managing multiple asynchronous context managers

# ---------------------------
# MCP Client Imports
# ---------------------------
from mcp import ClientSession, StdioServerParameters  # For managing MCP client sessions and server parameters
from mcp.client.stdio import stdio_client             # For establishing a stdio connection to an MCP server

# ---------------------------
# Agent and LLM Imports
# ---------------------------
from langchain_mcp_adapters.tools import load_mcp_tools  # Adapter to convert MCP tools to LangChain compatible tools
from langgraph.prebuilt import create_react_agent        # Function to create a prebuilt React agent using LangGraph
from langchain_google_genai import ChatGoogleGenerativeAI  # Wrapper for the Google Gemini API via LangChain



# ---------------------------
# Environment Setup
# ---------------------------
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from a .env file (e.g., GOOGLE_API_KEY)
# ---------------------------
# Custom JSON Encoder for LangChain objects
# ---------------------------
class CustomEncoder(json.JSONEncoder):
    """
    Custom JSON encoder to handle non-serializable objects returned by LangChain.
    If the object has a 'content' attribute (such as HumanMessage or ToolMessage), serialize it accordingly.
    """
    def default(self, o):
        # Check if the object has a 'content' attribute
        if hasattr(o, "content"):
            # Return a dictionary containing the type and content of the object
            return {"type": o.__class__.__name__, "content": o.content}
        # Otherwise, use the default serialization
        return super().default(o)

# ---------------------------
# Function: read_config_json
# ---------------------------
def read_config_json():
    """
    Reads the MCP server configuration JSON.

    Priority:
      1. Configuration file is loaded directly from "C:\\Users\\Richa Chopra\\Desktop\\Client\\mcp_config.json".
      2. If not set, fallback to a default file 'mcp_config.json' in the same directory.

    Returns:
        dict: Parsed JSON content with MCP server definitions.
    """
    # Attempt to get the config file path from the environment variable
    config_path = "C:\\Users\\Richa Chopra\\Desktop\\Client\\mcp_config.json"

    if not config_path:
        # If environment variable is not set, use a default config file in the same directory as this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, "mcp_config.json")
        print(f"⚠️  mcp_config not set. Falling back to: {config_path}")

    try:
        # Open and read the JSON config file
        with open(config_path, "r") as f:
            return json.load(f)
    except Exception as e:
        # If reading fails, print an error and exit the program
        print(f"❌ Failed to read config file at '{config_path}': {e}")
        sys.exit(1)

# ---------------------------
# Google Gemini LLM Instantiation
# ---------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",             # Specify the Google Gemini model variant to use
    temperature=0,                            # Set temperature to 0 for deterministic responses
    max_retries=2,                            # Set maximum retries for API calls to 2 in case of transient errors
    google_api_key="AIzaSyCITsocNmlmc2WE2EzvffSgrGElX153Nak"  # Retrieve the Google API key from environment variables
)


async def run_agent():
    """
    Connects to all MCP servers, loads their tools, creates a unified React agent,
    and starts an interactive loop to query the agent with conversation memory.
    """
    config = read_config_json()
    mcp_servers = config.get("mcpServers", {})
    if not mcp_servers:
        print("❌ No MCP servers found in the configuration.")
        return

    tools = []

    async with AsyncExitStack() as stack:
        for server_name, server_info in mcp_servers.items():
            print(f"\n🔗 Connecting to MCP Server: {server_name}...")
            server_params = StdioServerParameters(
                command=server_info["command"],
                args=server_info["args"]
            )
            try:
                read, write = await stack.enter_async_context(stdio_client(server_params))
                session = await stack.enter_async_context(ClientSession(read, write))
                await session.initialize()
                server_tools = await load_mcp_tools(session)
                for tool in server_tools:
                    print(f"\n🔧 Loaded tool: {tool.name}")
                    tools.append(tool)
                print(f"\n✅ {len(server_tools)} tools loaded from {server_name}.")
            except Exception as e:
                print(f"❌ Failed to connect to server {server_name}: {e}")

        if not tools:
            print("❌ No tools loaded from any server. Exiting.")
            return

        agent = create_react_agent(llm, tools)

        # <-- STEP 1: Initialize conversation history
        conversation_history = []

        print("\n🚀 MCP Client Ready! Type 'quit' to exit.")
        while True:
            query = input("\nQuery: ").strip()
            if query.lower() == "quit":
                break

            # The agent expects a list of messages. We will manage this list.
            # For the first turn, we only send the human message.
            # For subsequent turns, we send the whole history.
            
            # The create_react_agent expects the input to be in the format {"messages": [("human", "some message")]}
            # So we create the input for the current turn.
            current_turn_input = {"messages": [("human", query)]}
            
            # For a continuous conversation, we need to pass the previous messages as well.
            # We can modify the input to include the history.
            if conversation_history:
                current_turn_input["messages"] = conversation_history + [("human", query)]

        #     async def try_harder(agent, query):
        #         """Try to get a good reasonable answer using different tools, don't give up easily"""
        #         # First try
        #         response = await agent.ainvoke(current_turn_input)
        #         # Check if answer is bad
        #         answer_text = str(response)
        #         if "null" in answer_text.lower() or len(answer_text) < 30:
        #             # Second try with better instructions
        #             better_query = f"""
        #             {query}
        # IMPORTANT: If you don't get complete results on first try with the tool you use:
        #  1. Try each and every tool that might have this information
        #  2. Use different approaches with each and every available tool till you get a reasonable answer
        #  3. Keep trying until you find the answer
        #  4. If you still fail in finding the answer, do tell what exactly you gave as an input to each tool and what was the output.
        # """
        #         #  3. Use all the knowledge required for a good answer in each approach.
        #             response = await agent.ainvoke({"messages": [("human", better_query)]})
    
        #         return response

       
            # <-- STEP 3: Send the entire history to the agent
            response = await agent.ainvoke(current_turn_input)
            # response = await try_harder(agent, query)
            
            # <-- STEP 4: Append the user query and AI response to the history for the next turn
            conversation_history.append(("human", query))
            # The response['messages'] contains the full history of the turn.
            # The last message is the final AI response.
            conversation_history.append(response['messages'][-1])


            print("\nResponse:")
            try:
                formatted = json.dumps(response, indent=2, cls=CustomEncoder)
                print(formatted)
            except Exception:
                print(str(response))


# ---------------------------
# Entry Point
# ---------------------------
if __name__ == "__main__":
    # Run the asynchronous run_agent function using asyncio's event loop
    asyncio.run(run_agent())