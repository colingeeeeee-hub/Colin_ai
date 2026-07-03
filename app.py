import streamlit as st
import openai

st.set_page_config(page_title="老爸的专属AI", page_icon="👨‍👦")
st.title("👨‍👦 老爸的专属 AI 空间")

# 1. 让你爸输入只有你们知道的暗号，防止别人刷你的免费额度
password = st.sidebar.text_input("请输入专属暗号", type="password")

# 2. 免费的 API 配置（这里以国内良心的 SiliconFlow 平台为例，你可以去其官网免费注册拿 Key）
# 注：也可以直接用 DeepSeek 注册送的 Key
API_KEY = "这里填你注册拿到的免费_API_KEY"
BASE_URL = "https://api.siliconflow.cn/v1" 

if password == "老爸开门":
    # 初始化聊天历史
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 显示历史对话
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # 接收老爸的输入
    if prompt := st.chat_input("想问点什么？"):
        with st.chat_message("user"):
            st.write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 调用 AI 接口
        try:
            client = openai.OpenAI(api_key="sk-cubkmoblzsywgnblrjiluspbcoedqxhqdxurdiqfimoblifh", base_url=BASE_URL)
            with st.chat_message("assistant"):
                with st.spinner("AI 正在思考..."):
                    response = client.chat.completions.create(
                        model="deepseek-ai/DeepSeek-R1", # 使用免费额度里的顶级模型
                        messages=[{"role": "user", "content": prompt}]
                    )
                    answer = response.choices[0].message.content
                    st.write(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"出错了: {str(e)}")
else:
    st.info("💡 请在左侧边栏输入正确的暗号解锁 AI 助手。")