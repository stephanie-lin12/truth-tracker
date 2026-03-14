import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time
import pandas as pd # 這是畫地圖用的零件

# --- 網頁配置 ---
st.set_page_config(page_title="TVBS Truth-Tracker", page_icon="👁️", layout="wide")

# --- 側邊欄 ---
with st.sidebar:
    st.title("新聞查證中心")
    st.write("2026 AI Hackathon 版")
    st.divider()
    st.write("💡 **小撇步：**")
    st.write("上傳清晰大圖 -> ✅ 通過")
    st.write("上傳模糊小圖 -> 🚨 警告")

# --- 主畫面標題 ---
st.title("👁️ TVBS 真實之眼 (Truth-Tracker)")
st.write("---")

# --- 1. 定義上傳按鈕 (這行最重要，沒它會報錯！) ---
uploaded_file = st.file_uploader("請上傳待查證的爆料照片", type=["jpg", "jpeg", "png"])

# --- 2. 判斷是否有檔案上傳 ---
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
            
        # --- 判定邏輯 ---
        img_np = np.array(image.convert('RGB'))
        width, height = image.size
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        
        # 簡單邏輯：根據解析度給分
        if width < 800: # 如果寬度小於 800 像素，視為高風險
            final_score = 35
            verdict = "🚨 疑似 AI 生成或經多次轉傳壓縮"
            location_match = 12
        else:
            final_score = 92
            verdict = "✅ 影像特徵尚屬正常"
            location_match = 98

        st.success("分析完成！")
        st.image(edges, caption="數位噪點分布分析", use_container_width=True)

    # --- 3. 數據展示 ---
    st.write("---")
    st.subheader("📊 查證鑑定報告")
    c1, c2, c3 = st.columns(3)
    c1.metric("真實度評分", f"{final_score}%", f"{final_score-100}%" if final_score < 80 else "正常")
    c2.metric("地點匹配度", f"{location_match}%")
    c3.metric("物理一致性", "通過" if final_score > 50 else "異常")

    if final_score < 50:
        st.error(f"鑑定結論：{verdict}")
    else:
        st.info(f"鑑定結論：{verdict}")

    # --- 4. 驚喜加分項目：地圖顯示 (模擬 TVBS 總部座標) ---
    st.write("---")
    st.subheader("📍 影像溯源地點預測")
    # 這裡我們模擬一個座標 (TVBS 總部)
    map_data = pd.DataFrame({
        'lat': [25.078],
        'lon': [121.567]
    })
    st.map(map_data)

else:
    # 如果還沒上傳檔案，顯示這個提示
    st.info("👋 您好！請上傳一張照片開始自動化查證。")
    st.image("https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&q=80&w=1000", caption="等待影像偵測中...", use_container_width=True)
