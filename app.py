import json
import requests
from openai import OpenAI

client = OpenAI()

# 1. Load the pre-configured tool schemas
with open("tools/agent_tools_schema.json", "r") as f:
    tools = json.load(f)

# 2. Tool Execution Dispatcher
def execute_tool(tool_name, arguments):
    if tool_name == "get_live_weather":
        url = f"[https://api.open-meteo.com/v1/forecast?latitude=](https://api.open-meteo.com/v1/forecast?latitude=){arguments['latitude']}&longitude={arguments['longitude']}&current_weather=true"
        return requests.get(url).json()
    elif tool_name == "web_reader":
        url = f"[https://r.jina.ai/](https://r.jina.ai/){arguments['url']}"
        return requests.get(url).text[:1500]
    elif tool_name == "duckduckgo_instant_answer":
        url = f"[https://api.duckduckgo.com/?q=](https://api.duckduckgo.com/?q=){arguments['query']}&format=json&no_html=1"
        return requests.get(url).json().get("AbstractText", "No instant answer found.")
    return {"error": "Tool not implemented"}

# 3. Agent Execution with Tool Calling
messages = [{"role": "user", "content": "Check the current weather in Tokyo (lat: 35.6762, lon: 139.6503)."}]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

# 4. Handle tool response
tool_call = response.choices[0].message.tool_calls[0]
result = execute_tool(tool_call.function.name, json.loads(tool_call.function.arguments))
print("Agent Tool Output:\n", result)

