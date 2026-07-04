import streamlit as st
from openai import OpenAI

# ==============================================================================
# 🎨 1. 像素级复刻 ChatGPT 网页版 UI (The Ultimate Custom CSS)
# ==============================================================================
PERFECT_CHATGPT_CSS = """
<style>
/* 引入 ChatGPT 官方同款 Söhne/Inter 字体 */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

/* 1. 彻底抹平 Streamlit 原生布局与边距 */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    background-color: #212121 !important; /* ChatGPT 2026 最新官方主背景深色 */
    color: #ECECF1 !important;
}

/* 隐藏所有垃圾元素：顶部红线、Header 空白、Footer、右上角菜单 */
[data-testid="stHeader"], footer, #MainMenu { display: none !important; }
.main .block-container {
    padding-top: 2rem !important;
    padding-bottom: 7rem !important; /* 留出底部输入框的悬浮空间 */
    max-width: 48rem !important; /* ChatGPT 标志性的对话流宽度 (768px) */
}

/* 2. 复刻 ChatGPT 极简侧边栏 */
[data-testid="stSidebar"] {
    background-color: #171717 !important; /* 侧边栏更深 */
    border-right: 1px solid #2F2F2F !important;
    width: 260px !important;
}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    padding: 20px 12px !important;
}

/* 3. 彻底重写对话气泡：去掉方框感，改用 ChatGPT 无框横条流式布局 */
[data-testid="stChatMessage"] {
    background-color: transparent !important; /* 拒绝大方块！全部透明 */
    border: none !important;
    box-shadow: none !important;
    padding: 1.5rem 0rem !important;
    margin: 0 !important;
    border-bottom: 1px solid #2F2F2F !important; /* 淡淡的分割线 */
}

/* 4. 头像圆润化与ChatGPT配色 */
[data-testid="stChatMessageAvatar"] {
    background-color: transparent !important;
    border-radius: 50% !important; /* 完美的圆形头像 */
    width: 36px !important;
    height: 36px !important;
}

/* 5. 极致复刻：ChatGPT 悬浮底部输入框 */
div[data-testid="stChatInput"] {
    position: fixed !important;
    bottom: 24px !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: 100% !important;
    max-width: 48rem !important; /* 与对话流完美对齐 */
    background-color: #2F2F2F !important; /* 输入框标志性浅灰 */
    border: 1px solid #424242 !important;
    border-radius: 26px !important; /* 极致圆润 */
    box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
    padding: 6px 12px !important;
}

/* 移除输入框聚焦时的难看亮蓝边框 */
div[data-testid="stChatInput"]:focus-within {
    border-color: #565656 !important;
}

textarea {
    color: #F4F4F4 !important;
    font-size: 16px !important;
    background-color: transparent !important;
}

/* 6. 字体美化：让大模型的字看起来充满高级印刷感 */
[data-testid="stChatMessage"] p, div[data-testid="stMarkdownContainer"] p {
    font-size: 16px !important;
    line-height: 1.75 !important;
    color: #E3E3E3 !important;
    font-weight: 400 !important;
}

/* 极简提示框 */
.stAlert {
    background-color: #2F2F2F !important;
    border: 1px solid #424242 !important;
    border-radius: 12px !important;
}
</style>
"""

# ==============================================================================
# 🚀 2. 核心页面控制
# ==============================================================================
st.set_page_config(
    page_title="ChatGPT", 
    page_icon="🤖", 
    layout="centered"
)

# 强制注入终极美化 CSS
st.markdown(PERFECT_CHATGPT_CSS, unsafe_allow_html=True)

# 填入你的硅基流动 API Key
SILICONFLOW_API_KEY = "sk-xxxxxxxx" # 👈 请把这里换成你的真实 Key

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==============================================================================
# 🔒 3. 暗号锁防线（侧边栏极简验证）
# ==============================================================================
with st.sidebar:
    st.markdown("<p style='font-size: 13px; color: #B4B4B4; font-weight:500; margin-bottom:5px;'>🔐 访问验证</p>", unsafe_allow_html=True)
    password = st.text_input(
        "Password",
        type="password", 
        placeholder="输入专属暗号...",
        label_visibility="collapsed"
    )
    st.markdown("<div style='margin-top: 150px; text-align: center; color: #676767; font-size: 12px;'>Coling's Dad AI<br>v2.0 Beta</div>", unsafe_allow_html=True)

CORRECT_PASSWORD = "老爸第一" # 👈 你的专属暗号

# ==============================================================================
# 💬 4. 对话主战场
# ==============================================================================
if password != CORRECT_PASSWORD:
    # 未解锁时的ChatGPT经典极简欢迎语
    st.markdown("<h2 style='text-align: center; font-weight: 600; margin-top: 20vh; color: #FFF;'>有什么我可以帮您的？</h2>", unsafe_allow_html=True)
    st.info("💡 请在左侧边栏输入【专属暗号】解锁空间。")
else:
    # 已解锁：上方完全留空，营造极简空气感
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # 渲染历史记录（直接使用漂亮的内建头像）
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 捕获输入
    if prompt := st.chat_input("给“老爸的专属AI”发送消息..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                client = OpenAI(
                    api_key="sk-cubkmoblzsywgnblrjiluspbcoedqxhqdxurdiqfimoblifh",
                    base_url="https://api.siliconflow.cn/v1"
                )
                
                response_stream = client.chat.completions.create(
                    model="deepseek-ai/DeepSeek-V3", 
                    messages=[
                        {"role": "system", "content": "你是由Coling专门为他父亲定制开发的专属AI助手。在对话中，你的语气要格外温柔、沉稳、极具耐心、关怀备至。用词要简练接地气，多用暖心的话，绝不能有机器人的冰冷感。像老朋友一样陪这位父亲聊天、解答各种生活小常识、天气、养生、新闻或者讲温暖的故事，让他感受到陪伴和快乐。"},
                        *st.session_state.messages
                    ],
                    stream=True
                )
                
                for chunk in response_stream:
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        # ChatGPT 经典黑方块打字光标 █
                        message_placeholder.markdown(full_response + " █")
                
                message_placeholder.markdown(full_response)
                
            except Exception as e:
                st.error("⚠️ 网络连接似乎断开了。")
                full_response = "网络遇到了一点小故障，老爸。请把您刚才的话再说一遍好吗？"
                message_placeholder.markdown(full_response)
                
        st.session_state.messages.append({"role": "assistant", "content": full_response})
