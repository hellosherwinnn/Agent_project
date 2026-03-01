from dotenv import load_dotenv
from hello_agents import HelloAgentsLLM

load_dotenv()

llm = HelloAgentsLLM() 

# 框架内部日志会显示检测到 provider 为 'ollama' 
messages = [{"role": "user", "content": "你好！"}]
for chunk in llm.think(messages):
    print(chunk, end="")
