from dotenv import load_dotenv
load_dotenv()
import os
from serpapi import SerpApiClient

def search(query: str) -> str:
    """
    一个基于SerpApi的实战网页搜索引擎工具。
    它会智能地解析搜索结果，优先返回直接答案或知识图谱信息。
    """
    print(f"🔍 正在执行 [SerpApi] 网页搜索: {query}")
    try:
        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key:
            return "错误:SERPAPI_API_KEY 未在 .env 文件中配置。"

        params = {
            "engine": "google",
            "q": query,
            "api_key": api_key,
            "gl": "cn",  # 国家代码
            "hl": "zh-cn", # 语言代码
        }
        
        client = SerpApiClient(params)
        results = client.get_dict()
        
        # 智能解析:优先寻找最直接的答案
        if "answer_box_list" in results:
            return "\n".join(results["answer_box_list"])
        if "answer_box" in results and "answer" in results["answer_box"]:
            return results["answer_box"]["answer"]
        if "knowledge_graph" in results and "description" in results["knowledge_graph"]:
            return results["knowledge_graph"]["description"]
        if "organic_results" in results and results["organic_results"]:
            # 如果没有直接答案，则返回前三个有机结果的摘要
            snippets = [
                f"[{i+1}] {res.get('title', '')}\n{res.get('snippet', '')}"
                for i, res in enumerate(results["organic_results"][:3])
            ]
            return "\n\n".join(snippets)
        
        return f"对不起，没有找到关于 '{query}' 的信息。"

    except Exception as e:
        return f"搜索时发生错误: {e}"

import math
def calculator(expression: str) -> str:
    """
    一个简单的计算器工具，用于执行基本的数学运算。
    支持加减乘除、括号和常用数学函数。
    """
    try:
        # 移除表达式中的空格
        expression = expression.strip()
        # 评估表达式
        result = eval(expression, {"__builtins__": None}, {
            "math": math,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "sqrt": math.sqrt,
            "pow": math.pow,
            "log": math.log,
            "log10": math.log10,
            "exp": math.exp,
        })
        return f"计算结果: {result}"
    except Exception as e:
        return f"计算错误: {e}"


from typing import Dict, Any

class ToolExecutor:
    """
    一个工具执行器，负责管理和执行工具。
    """
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}

    def registerTool(self, name: str, description: str, func: callable):
        """
        向工具箱中注册一个新工具。
        """
        if name in self.tools:
            print(f"警告:工具 '{name}' 已存在，将被覆盖。")
        self.tools[name] = {"description": description, "func": func}
        print(f"工具 '{name}' 已注册。")

    def getTool(self, name: str) -> callable:
        """
        根据名称获取一个工具的执行函数。
        """
        return self.tools.get(name, {}).get("func")

    def getAvailableTools(self) -> str:
        """
        获取所有可用工具的格式化描述字符串。
        """
        return "\n".join([
            f"- {name}: {info['description']}" 
            for name, info in self.tools.items()
        ])

if __name__ == '__main__':
    # 1. 初始化工具执行器
    toolExecutor = ToolExecutor()

    # 2. 注册我们的实战搜索工具
    search_description = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
    toolExecutor.registerTool("Search", search_description, search)
    calc_desc = """
    一个数学计算器。
    当用户的问题涉及数学计算、数值运算（如加减乘除、幂运算等）时，必须使用此工具。
    输入参数必须是一个合法的数学表达式字符串，不要包含文字。
    """
    toolExecutor.registerTool("Calculator", calc_desc, calculator)

    # 4. 打印看看现在的工具列表 (你会发现多了一个 Calculator)
    print("\n--- 当前可用工具列表 ---")
    print(toolExecutor.getAvailableTools())

    # 5. 测试一下计算器 (新增测试代码)
    print("\n--- 测试 Action: Calculator ---")
    tool_input = "(123 + 456) * 789 / 12"  # 题目要求的复杂计算
    tool_name = "Calculator"
    # # 3. 打印可用的工具
    # print("\n--- 可用的工具 ---")
    # print(toolExecutor.getAvailableTools())

    # # 4. 智能体的Action调用，这次我们问一个实时性的问题
    # print("\n--- 执行 Action: Search['英伟达最新的GPU型号是什么'] ---")
    # tool_name = "Search"
    # tool_input = "英伟达最新的GPU型号是什么"

    tool_function = toolExecutor.getTool(tool_name)
    if tool_function:
        observation = tool_function(tool_input)
        print("--- 观察 (Observation) ---")
        print(observation)
    else:
        print(f"错误:未找到名为 '{tool_name}' 的工具。")


