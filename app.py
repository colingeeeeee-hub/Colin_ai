import streamlit as st
from openai import OpenAI

# ==============================================================================
# 🎨 1. ChatGPT 扁平化风格界面重塑 (Modern UI Overhaul)
# ==============================================================================
# 这里我们注入了极具辨识度的 ChatGPT 视觉语言：
# - 引入了 'Inter' 字体，这是许多现代科技应用的首选，字形扁平清晰、易读性极高
# - 整体采用 ChatGPT 的经典深色模式 (#343541)，而不是原本温馨的米浆色
# - 移除了冷冰冰的主标题，改为极简的“Coling's Dad AI”居中文字，模拟官网顶部的极简导航栏
# - 对话气泡完全重绘，采用扁平化设计，去掉了莫兰迪指示条和微光投影
# ==============================================================================

MODERN_CHATGPT_CSS = """
<style>
/* 导入现代极简字体 Inter */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* 重构整体背景与基础字体 */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background-color: #343541 !important; /* ChatGPT 经典深灰背景 */
    color: #ECECF1 !important; /* 浅灰文字，高对比度 */
}

/* 隐藏 Streamlit 官方冗余元素 */
#MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden;}

/* 重塑标题栏：移除大 H1，改为极简导航栏风格 */
.stMarkdown h3#coling-s-dad-ai {
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 16px !important;
    color: #ECECF1 !important;
    text-align: center;
    padding: 10px 0;
    margin: 0 !important;
    letter-spacing: -0.5px;
}

/* 侧边栏暗号区的扁平化美化 */
[data-testid="stSidebar"] {
    background-color: #202123 !important; /* 更深的侧边栏背景 */
    border-right: 1px solid #4D4D4F !important;
}

/* 扁平化输入框（ChatGPT 风格） */
div[data-testid="stChatInput"] {
    border-radius: 20px !important;
    border: 1px solid #565869 !important;
    background-color: #40414F !important;
    box-shadow: none !important; /* 移除了投影 */
    transition: all 0.2s ease;
}

div[data-testid="stChatInput"]:focus-within {
    border-color: #10A37F !important; /* 激活时呈 ChatGPT 的经典绿色 */
}

/* 聊天对话框容器 */
[data-testid="stChatMessage"] {
    padding: 16px !important;
    margin-bottom: 12px !important;
    border-radius: 12px !important;
    background-color: transparent !important; /* 背景透明 */
    box-shadow: none !important; /* 移除了投影 */
}

/* 👩 老爸的头像和气泡样式 (User) */
[data-testid="stChatMessage"][aria-label="user"] {
    border: none !important;
}

/* 🤖 AI 的头像和气泡样式 (Assistant) */
[data-testid="stChatMessage"][aria-label="assistant"] {
    border: none !important;
}

/* 模拟 ChatGPT 头像：使用 FontAwesome 图标，并通过伪元素注入样式 */
div[data-testid="stChatMessageAvatar"] {
    border-radius: 6px !important;
    background-color: transparent !important;
}

/* 注入 ChatGPT 的绿色图标 (助理头像) */
[data-testid="stChatMessage"][aria-label="assistant"] [data-testid="stChatMessageAvatar"]::after {
    content: '\\f10c'; /* FontAwesome circle-o */
    font-family: FontAwesome;
    font-size: 24px;
    color: #10A37F;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

/* 正文字体：使用 Inter，字号调整为 16px */
[data-testid="stChatMessage"] p, div[data-testid="stMarkdownContainer"] p {
    font-size: 16px !important;
    line-height: 1.6 !important;
    color: #ECECF1 !important;
}

/* 暗号提示卡片美化 */
.stAlert {
    border-radius: 12px !important;
    background-color: #202123 !important;
    border: 1px solid #E07A5F !important;
}
</style>
"""

# ==============================================================================
# 🚀 2. 核心逻辑控制 (Core Logic)
# ==============================================================================

# 设置页面配置
st.set_page_config(
    page_title="Coling's Dad AI", 
    page_icon="🤖", 
    layout="centered"
)

# 注入现代扁平化 CSS 样式
st.markdown(MODERN_CHATGPT_CSS, unsafe_allow_html=True)

# 初始化 API Key (请确保使用您自己的免费密钥)
SILICONFLOW_API_KEY = "sk-xxxxxxxx" # 请替换为您自己的 SiliconFlow Key

# 初始化聊天历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==============================================================================
# 🔒 3. 暗号锁防线 (Authorization Sidebar)
# ==============================================================================
with st.sidebar:
    st.markdown("<h4 style='text-align: center; color: #10A37F; padding: 10px 0;'>专属安全验证</h4>", unsafe_allow_html=True)
    password = st.text_input(
        "请输入您的专属暗号：", 
        type="password", 
        placeholder="在这里输入暗号..."
    )
    st.markdown("---")
    st.markdown("<p style='font-size: 12px; color: #9A9A9A; text-align: center;'>Coling's Dad AI<br>© 2026</p>", unsafe_allow_html=True)

# 专属小秘密暗号
CORRECT_PASSWORD = "岭南居士" # 替换成您的专属暗号

if password != CORRECT_PASSWORD:
    # 密码未通过时，展示极简的引导卡片
    st.markdown("### Coling's Dad AI", unsafe_allow_html=True)
    st.info("💡 请在左侧侧边栏输入您的【专属暗号】解锁空间。")
    # 替换为一个更扁平、现代的引导图片
    st.image("https://raw.githubusercontent.com/colingeeeeee-hub/dad_ai/main/assets/setup_dark.svg", use_container_width=True)
else:
    # 密码验证通过，解锁主界面
    st.markdown("### Coling's Dad AI", unsafe_allow_html=True)

    # 渲染历史对话记录
    for message in st.session_state.messages:
        # 为用户和助理设置不同的头像图标（FontAwesome 图标）
        avatar_icon = "user" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar_icon):
            st.markdown(message["content"])

    # 捕获用户新输入
    if prompt := st.chat_input("您好！有什么我可以帮您的吗？..."):
        # 在界面渲染用户说的话，使用 FontAwesome 人类头像
        with st.chat_message("user", avatar="user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 准备向大模型请求数据
        with st.chat_message("assistant", avatar="🤖"):
            # 建立进度条占位区
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                # 初始化客户端
                client = OpenAI(
                    api_key="sk-cubkmoblzsywgnblrjiluspbcoedqxhqdxurdiqfimoblifh",
                    base_url="https://api.siliconflow.cn/v1"
                )
                
                # 创建流式响应（Stream）
                response_stream = client.chat.completions.create(
                    model="deepseek-ai/DeepSeek-V3", # 确保使用您想用的模型
                    messages=[
                        # 系统设定：保留体贴、有耐心的角色设定
                        {"role": "system", "content": "你是由Coling专门为他父亲定制开发的专属AI助手。在对话中，你的语气要格外温柔、沉稳、极具耐心、关怀备至。用词要简练接地气，多用暖心的话，绝不能有机器人的冰冷感。像老朋友一样陪这位父亲聊天、解答各种生活小常识、天气、养生、新闻或者讲温暖的故事，让他感受到陪伴和快乐。"},
                        *st.session_state.messages
                    ],
                    stream=True
                )
                
                # 循环流式数据并实时渲染
                for chunk in response_stream:
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        # 实时更新气泡里的字，加上 ChatGPT 的扁平化打字光标
                        message_placeholder.markdown(full_response + " █")
                
                # 去除末尾打字光标
                message_placeholder.markdown(full_response)
                
            except Exception as e:
                # 友好的异常处理
                st.error("⚠️ 网络中断。请您尝试再次向我提问。")
                full_response = "网络遇到一点故障，老爸。请把您刚才的话再说一遍好吗？"
                message_placeholder.markdown(full_response)
                
        # 存入对话历史
        st.session_state.messages.append({"role": "assistant", "content": full_response})
