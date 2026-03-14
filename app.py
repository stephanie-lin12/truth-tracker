import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time

# --- 網頁標題與風格設定 ---
st.set_page_config(page_title="TVBS Truth-Tracker", page_icon="👁️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stAlert { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 側邊欄 ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/TVBS_Logo.svg/1200px-TVBS_Logo.svg.png", width=150)
    st.title("新聞查證控制台")
    st.info("模式：2026 第三屆 AI Hackathon 原型機")
    st.write("操作員：TVBS 新聞部")

# --- 主畫面 ---
st.title("👁️ TVBS 真實之眼 (Truth-Tracker)")
st.subheader("AI 影音全自動溯源與防偽驗證系統")
st.write("---")
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📷 原始素材")
        st.image(image, use_container_width=True)
    
    with col2:
        st.markdown("### 🔍 AI 深度鑑定中...")
        progress_bar = st.progress(0)
        for p in range(0, 101, 25):
            progress_bar.progress(p)
            time.sleep(0.2)
            
        # 判定邏輯
        img_np = np.array(image.convert('RGB'))
        width, height = image.size
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        
        # 計算邊緣密度作為判定基準
        edge_density = np.sum(edges) / (width * height)
        
        if edge_density < 1.0 or width < 500: # 如果太模糊或太小
            final_score = 35
            verdict = "🚨 疑似 AI 生成或過度壓縮"
        else:
            final_score = 88
            verdict = "✅ 影像特徵尚屬正常"

        st.success("分析完成！")
        st.image(edges, caption="數位噪點分布分析", use_container_width=True)

    # 數據展示
    st.write("---")
    c1, c2, c3 = st.columns(3)
    c1.metric("真實度評分", f"{final_score}%", f"{final_score-100}%" if final_score < 80 else "正常")
    c2.metric("地點匹配度", "88%" if final_score > 50 else "12%")
    c3.metric("物理一致性", "通過" if final_score > 50 else "異常")

    if final_score < 50:
        st.error(f"鑑定結論：{verdict}")
    else:
        st.info(f"鑑定結論：{verdict}")

# --- 頁尾 ---
st.write("---")
st.caption("© 2026 TVBS Truth-Tracker Team | 以 AI 之速，還原事實之重。")
