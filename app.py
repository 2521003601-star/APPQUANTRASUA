import streamlit as st
import pandas as pd
import random

# Cấu hình trang
st.set_page_config(page_title="Chiikawa Boba - OATSIDE Style", page_icon="🧋", layout="wide")

# ---------------------------------------------------------
# OATSIDE BRANDING - CUSTOM CSS & ANIMATIONS
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Fredoka', cursive, sans-serif;
    }
    .stApp {
        background-color: #FFF8EE;
    }
    /* Card kiểu Oatside */
    .oatside-card {
        background: #FFFFFF;
        border: 3px solid #1A1A1A;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 5px 5px 0px #1A1A1A;
        margin-bottom: 20px;
        transition: transform 0.2s;
    }
    .oatside-card:hover {
        transform: translate(-2px, -2px);
        box-shadow: 7px 7px 0px #1A1A1A;
    }
    /* Hiển thị ly nước mô phỏng */
    .boba-cup {
        width: 120px;
        height: 180px;
        border: 4px solid #1A1A1A;
        border-radius: 0 0 25px 25px;
        margin: auto;
        position: relative;
        overflow: hidden;
        background: #FFF;
    }
    .boba-liquid {
        position: absolute;
        bottom: 0;
        width: 100%;
        background-color: #E6C280;
        transition: height 0.3s ease;
    }
    .boba-topping {
        position: absolute;
        bottom: 5px;
        width: 100%;
        text-align: center;
        font-size: 18px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 1: FLAVOR FINDER (TÌM MÓN THEO TÂM TRẠNG - KIỂU OATSIDE)
# ---------------------------------------------------------
st.title("🧋 CHIIKAWA BOBA WORLD")
st.caption("Trải nghiệm Order Trà Sữa Phong Cách OATSIDE!")

tab_order, tab_mood, tab_secret = st.tabs(["🛒 Order Nhanh", "🎯 Gợi Ý Theo Tâm Trạng", "🎲 Món Quà Bất Ngờ"])

with tab_mood:
    st.markdown("### 🎭 Hôm nay năng lượng của bạn thế nào?")
    
    col_q1, col_q2 = st.columns(2)
    with col_q1:
        mood = st.radio("1. Bạn đang cảm thấy...", ["Cực kỳ năng động ⚡", "Cần chạy deadline 💻", "Hơi suy / Buồn xỉu ☁️", "Thèm ngọt đỉnh điểm 🍩"])
    with col_q2:
        sweet_pref = st.select_slider("2. Mức độ thèm ngọt:", options=["Nhẹ nhàng", "Vừa đủ", "Đậm đà", "Bùng nổ"])

    if st.button("✨ Tìm Ly Trà Sữa Chân Truyền", type="primary"):
        st.markdown("<div class='oatside-card'>", unsafe_allow_html=True)
        if "Cực kỳ năng động" in mood:
            st.subheader("🎉 Món gợi ý: Trà Đào Cam Sả Hachiware!")
            st.write("Sảng khoái, tươi mát, giúp bạn duy trì 200% năng lượng quậy phá cả ngày.")
        elif "deadline" in mood:
            st.subheader("⚡ Món gợi ý: Trà Sữa Ô Long Kem Cheese!")
            st.write("Vị trà đậm đà tỉnh táo kết hợp lớp kem béo ngậy nạp lại năng lượng trí não.")
        else:
            st.subheader("🧋 Món gợi ý: Trà Sữa Trân Châu Đường Đen Usagi!")
            st.write("Ngọt ngào êm dịu xoa dịu mọi nỗi buồn.")
        st.markdown("</div>", unsafe_allow_html=True)

with tab_secret:
    st.markdown("### 🎲 Không biết uống gì? Để Usagi chọn giúp!")
    if st.button("🎰 Quay Số Chọn Món Ngẫu Nhiên"):
        drinks = ["Trà Sữa Truyền Thống", "Trà Sữa Thái Xanh", "Trà Sữa Matcha", "Trà Dâu Tằm"]
        toppings = ["Trân châu đen", "Pudding trứng", "Kem Cheese"]
        chosen_drink = random.choice(drinks)
        chosen_topping = random.choice(toppings)
        
        st.success(f"🎯 Usagi gợi ý cho bạn: **{chosen_drink}** kèm **{chosen_topping}**!")

with tab_order:
    # ---------------------------------------------------------
    # TRỰC QUAN HÓA LY TRÀ SỮA ĐỘNG (VISUAL CUSTOMIZER)
    # ---------------------------------------------------------
    col_input, col_visual = st.columns([1.2, 0.8])
    
    with col_input:
        tea_choice = st.selectbox("Món nước:", ["Trà Sữa Truyền Thống", "Trà Sữa Thái Xanh", "Trà Sữa Ô Long"])
        size_choice = st.radio("Size:", ["S", "M", "L"], horizontal=True)
        ice_choice = st.select_slider("Đá:", ["0%", "30%", "50%", "100%"])
        topping_choice = st.multiselect("Topping:", ["Trân châu đen", "Pudding trứng", "Kem Cheese"])

    with col_visual:
        st.markdown("<h4 style='text-align:center;'>Mô phỏng Ly của bạn</h4>", unsafe_allow_html=True)
        
        # Tính toán chiều cao nước theo Size
        height_map = {"S": "50%", "M": "75%", "L": "95%"}
        color_map = {
            "Trà Sữa Truyền Thống": "#D2B48C",
            "Trà Sữa Thái Xanh": "#8FBC8F",
            "Trà Sữa Ô Long": "#C19A6B"
        }
        
        liquid_height = height_map.get(size_choice, "70%")
        liquid_color = color_map.get(tea_choice, "#D2B48C")
        topping_icon = "🧋" if "Trân châu đen" in topping_choice else "🍮" if "Pudding trứng" in topping_choice else ""

        # Render HTML/CSS Ly nước động
        st.markdown(f"""
        <div class="boba-cup">
            <div class="boba-liquid" style="height: {liquid_height}; background-color: {liquid_color};"></div>
            <div class="boba-topping">{topping_icon}</div>
        </div>
        <p style="text-align:center; margin-top: 10px;"><b>Size {size_choice} | {ice_choice} Đá</b></p>
        """, unsafe_allow_html=True)
