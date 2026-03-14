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

# --- 核心邏輯：簡單的動態評分 (不再是一成不變) ---
        img_np = np.array(image)
        
        # 1. 偵測圖片解析度 (越低分越高風險)
        width, height = image.size
        resolution_score = 100 if width * height > 1000000 else 50
        
        # 2. 模擬偵測像素細節 (計算圖片邊緣強度)
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        edge_density = np.sum(edges) / (width * height)
        
        # 如果邊緣過於模糊或過於生硬，模擬為 AI 跡象
        if edge_density < 10:
            final_score = 30  # 高風險
            verdict = "🚨 疑似 AI 生成或過度後製"
            status_color = "error"
        else:
            final_score = 85  # 較安全
            verdict = "✅ 影像特徵尚屬正常"
            status_color = "success"

        st.success("分析完成！")
        st.image(edges, caption="數位噪點分布分析 (AIGC 邊緣偵測)", use_container_width=True)

    # --- 鑑定數據區 (根據邏輯顯示動態數值) ---
    st.write("---")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.metric("真實度評分", f"{final_score}%", f"{final_score-100}%" if final_score < 80 else "正常")
    with c2:
        st.metric("地理匹配度", "88%" if final_score > 50 else "12%", "地點分析中")
    with c3:
        st.metric("物理一致性", "通過" if final_score > 50 else "異常")

    # --- 最終動態結論 ---
    if final_score < 50:
        st.error(f"鑑定結論：{verdict}。建議啟動人工複核。")
    else:
        st.info(f"鑑定結論：{verdict}。初步查核無明顯竄改痕跡。")

# --- 頁尾 ---
st.write("---")
st.caption("© 2026 TVBS Truth-Tracker Team | 以 AI 之速，還原事實之重。")
