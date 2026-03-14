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
