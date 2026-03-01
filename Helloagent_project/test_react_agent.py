from dotenv import load_dotenv
from hello_agents import HelloAgentsLLM, ToolRegistry
from hello_agents.tools import CalculatorTool
from my_react_agent import MyReActAgent

# 加载环境变量
load_dotenv()

# 创建LLM实例
llm = HelloAgentsLLM()

# 创建工具注册表并注册计算器工具
tool_registry = ToolRegistry()
# calculator = CalculatorTool()
# tool_registry.register_tool(calculator)
try:
    from hello_agents import calculate
    tool_registry.register_function("calculate", "执行数学计算，支持基本的四则运算", calculate)
    print("✅ 计算器工具注册成功")
except ImportError:
    print("⚠️ 计算器工具未找到，跳过注册")


# ====== 测试1：基础计算任务 ======
print("=" * 50)
print("测试1：基础计算任务")
print("=" * 50)

agent = MyReActAgent(
    name="ReAct助手",
    llm=llm,
    tool_registry=tool_registry,
    max_steps=5
)
math_question = "请帮我计算：(25 + 15) * 3 - 8 的结果是多少？"
try:
    result1 = agent.run(math_question)
    print(f"\n🎯 测试1结果: {result1}")
except Exception as e:
    print(f"❌ 测试1失败: {e}")
# response = agent.run("请帮我计算 25 * 4 + 50")
# print(f"\n最终响应: {response}")

# ====== 测试2：查看对话历史 ======
# print("\n" + "=" * 50)
# print("测试2：查看对话历史")
# print("=" * 50)

# history = agent.get_history()
# print(f"历史消息数: {len(history)} 条")
# for msg in history:
#     print(f"  [{msg.role}] {msg.content[:50]}...")
