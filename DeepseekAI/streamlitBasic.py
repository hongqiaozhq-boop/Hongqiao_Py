import streamlit as st

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",

    #布局
    layout="wide",

    #侧边烂
    initial_sidebar_state="expanded",

    #超链接
    menu_items={}
)


#标题
st.title("大标题")
st.header("一级标题")
st.subheader("二级标题")


#段落文字
st.write("家里有一只猫")
st.write("但是没有狗")

#图片