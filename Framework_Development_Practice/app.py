import streamlit as st
import requests
import json
import datetime

# --- 配置 ---
# CoinGecko API 的基础URL
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"
# 要查询的加密货币ID（比特币）
CURRENCY_PAIR_ID = "bitcoin"
# 要兑换的法币单位（美元）
VS_CURRENCIES = "usd"

# --- Streamlit 页面配置 ---
st.set_page_config(
    page_title="比特币实时价格显示",
    page_icon="₿",
    layout="centered"
)

# --- 数据获取函数 ---
def get_bitcoin_price_data():
    """
    从 CoinGecko API 获取比特币的实时价格和24小时变化数据。
    返回一个包含价格、变化数据和更新时间的字典，
    或在发生错误时返回 None 并显示错误信息。
    """
    params = {
        "ids": CURRENCY_PAIR_ID,
        "vs_currencies": VS_CURRENCIES,
        "include_24hr_change": "true" # 请求包含24小时价格变化百分比
    }

    try:
        # 发送HTTP GET请求，设置10秒超时
        response = requests.get(COINGECKO_API_URL, params=params, timeout=10)
        # 检查HTTP响应状态码，如果不是200，则抛出HTTPError
        response.raise_for_status()

        data = response.json()

        # 检查返回的数据结构是否符合预期
        if CURRENCY_PAIR_ID in data and VS_CURRENCIES in data[CURRENCY_PAIR_ID]:
            current_price = data[CURRENCY_PAIR_ID][VS_CURRENCIES]
            # 获取24小时价格变化百分比
            price_change_24h_percent = data[CURRENCY_PAIR_ID].get(f"{VS_CURRENCIES}_24h_change")

            price_change_24h_abs = None
            if price_change_24h_percent is not None:
                # 根据当前价格和百分比计算24小时前的价格
                # current_price = price_24h_ago * (1 + price_change_24h_percent / 100)
                # price_24h_ago = current_price / (1 + price_change_24h_percent / 100)

                # 避免除以零的情况，尽管在正常价格数据中不太可能发生
                if (1 + price_change_24h_percent / 100) != 0:
                    price_24h_ago = current_price / (1 + price_change_24h_percent / 100)
                    price_change_24h_abs = current_price - price_24h_ago
                else:
                    price_change_24h_abs = 0.0 # 理论上价格归零，变化额也为当前价格
            else:
                st.warning("API返回数据中缺少24小时价格变化百分比，无法计算涨跌额。")

            return {
                "current_price": current_price,
                "price_change_24h_percent": price_change_24h_percent,
                "price_change_24h_abs": price_change_24h_abs,
                "last_updated": datetime.datetime.now() # 记录数据更新时间
            }
        else:
            st.error("API返回数据结构异常，请检查CoinGecko API响应内容。")
            st.json(data) # 打印原始数据方便调试
            return None

    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP请求错误: {e}. 状态码: {response.status_code if 'response' in locals() else '未知'}")
        if 'response' in locals() and response.status_code == 429:
            st.info("可能是请求频率过高，CoinGecko API有频率限制，请稍后再试。")
        return None
    except requests.exceptions.ConnectionError as e:
        st.error(f"网络连接错误: 请检查您的网络连接或CoinGecko API服务是否可用。详细: {e}")
        return None
    except requests.exceptions.Timeout as e:
        st.error(f"请求超时: CoinGecko API响应时间过长。详细: {e}")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"请求错误: 发生未知网络或HTTP错误。详细: {e}")
        return None
    except json.JSONDecodeError as e:
        st.error(f"JSON解析错误: API返回了无效的JSON数据。详细: {e}")
        if 'response' in locals():
            st.text(response.text) # 打印原始响应文本
        return None
    except Exception as e:
        st.error(f"发生未预期错误: {e}")
        return None

# --- 主应用逻辑 ---
st.title("₿ 比特币实时价格")

# 使用 Streamlit 的 session state 存储比特币数据，以便在刷新后保持
# 只有当 st.session_state.bitcoin_data 为 None 时，才会重新获取数据
if 'bitcoin_data' not in st.session_state:
    st.session_state.bitcoin_data = None

# "刷新价格"按钮。点击按钮时，会将 st.session_state.bitcoin_data 设置为 None，
# 从而强制应用重新运行并获取最新数据。
if st.button("刷新价格", help="点击以获取最新的比特币价格"):
    st.session_state.bitcoin_data = None
    st.rerun() # 强制Streamlit重新运行整个脚本以立即显示加载状态并获取新数据

# 如果 session state 中没有数据（首次加载或用户点击刷新），则获取数据
if st.session_state.bitcoin_data is None:
    with st.spinner("正在获取比特币价格数据..."):
        st.session_state.bitcoin_data = get_bitcoin_price_data()

# 显示数据
if st.session_state.bitcoin_data:
    data = st.session_state.bitcoin_data
    current_price = data["current_price"]
    price_change_24h_percent = data["price_change_24h_percent"]
    price_change_24h_abs = data["price_change_24h_abs"]
    last_updated = data["last_updated"]

    st.markdown(f"**数据更新于**: {last_updated.strftime('%Y-%m-%d %H:%M:%S')}")

    # 使用两列布局美化显示
    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="当前价格 (USD)", value=f"${current_price:,.2f}") # 格式化为美元货币，保留两位小数

    with col2:
        if price_change_24h_percent is not None and price_change_24h_abs is not None:
            # 根据涨跌幅设置颜色：绿色表示上涨，红色表示下跌
            delta_color = "normal"
            if price_change_24h_percent > 0:
                delta_color = "inverse" # Streamlit metric中 "inverse" 通常用于绿色（正向变化）
            elif price_change_24h_percent < 0:
                delta_color = "off" # Streamlit metric中 "off" 通常用于红色（负向变化）

            st.metric(
                label="24小时价格变化",
                value=f"${price_change_24h_abs:,.2f}", # 格式化为美元货币，保留两位小数
                delta=f"{price_change_24h_percent:+.2f}%", # 格式化为百分比，带正负号
                delta_color=delta_color
            )
        else:
            # 如果缺少24小时变化数据，则显示N/A
            st.metric(label="24小时价格变化", value="N/A", delta="N/A")
else:
    # 如果 st.session_state.bitcoin_data 为 None，且没有显示任何错误信息
    # 可能是首次加载失败，或者刷新后仍然失败
    st.warning("未能获取比特币价格数据，请稍后重试或检查网络连接。")

st.markdown("---")
st.info("**数据来源**：CoinGecko API。由于API限制，数据可能不会实时秒级更新，但刷新按钮将始终尝试获取最新数据。")
