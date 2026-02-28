import streamlit as st
import requests
import datetime

# --- 配置 ---
BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/24hr"
SYMBOL = "BTCUSDT"

# --- 页面配置 ---
st.set_page_config(
    page_title="比特币价格追踪",
    page_icon="₿",
    layout="centered"
)

# --- 数据获取函数 ---
def get_bitcoin_price_data():
    params = {"symbol": SYMBOL}
    try:
        response = requests.get(BINANCE_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        return {
            "current_price": float(data["lastPrice"]),
            "price_change_24h_percent": float(data["priceChangePercent"]),
            "price_change_24h_abs": float(data["priceChange"]),
            "last_updated": datetime.datetime.now()
        }
    except Exception as e:
        st.error(f"API 请求失败: {e}")
        return None

# --- UI 展示 ---
st.title("₿ 实时比特币价格追踪")
st.write("点击刷新按钮获取最新数据")

if 'bitcoin_data' not in st.session_state:
    st.session_state.bitcoin_data = None

if st.button("刷新价格"):
    st.session_state.bitcoin_data = None
    st.rerun()

if st.session_state.bitcoin_data is None:
    with st.spinner("获取中..."):
        st.session_state.bitcoin_data = get_bitcoin_price_data()

if st.session_state.bitcoin_data:
    data = st.session_state.bitcoin_data
    st.caption(f"最后更新: {data['last_updated'].strftime('%H:%M:%S')}")

    c1, c2 = st.columns(2)
    with c1:
        st.metric("价格 (USDT)", f"${data['current_price']:,.2f}")
    with c2:
        st.metric("24h 涨跌额", f"${data['price_change_24h_abs']:,.2f}", f"{data['price_change_24h_percent']:.2f}%")
else:
    st.error("获取失败，请重试。")

st.divider()
st.info("数据源: Binance API")
