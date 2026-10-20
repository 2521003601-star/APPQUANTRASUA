import streamlit as st
import pandas as pd
import random

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG STREAMLIT
# ---------------------------------------------------------
st.set_page_config(
    page_title="CỎ & MÂY Coffee",
    page_icon="☁️",
    layout="wide"
)

# ---------------------------------------------------------
# 2. CUSTOM CSS GIAO DIỆN HỒNG PASTEL & CHẤM BI ĐA SẮC
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Quicksand', sans-serif;
    }
    
    /* Background Hồng Pastel kèm họa tiết Chấm bi pastel đa sắc */
    .stApp {
        background-color: #FFF0F5;
        background-image: 
            radial-gradient(#FFB6C1 15%, transparent 16%),
            radial-gradient(#B0E0E6 15%, transparent 16%),
            radial-gradient(#E6E6FA 15%, transparent 16%),
            radial-gradient(#FFFACD 15%, transparent 16%);
        background-size: 60px 60px;
        background-position: 0 0, 30px 30px, 30px 0, 0 30px;
    }
    
    /* Header Branding */
    .brand-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #FFB7B2, #FFDAC1);
        border-radius: 20px;
        margin-bottom: 25px;
        color: #6B4226;
        box-shadow: 0 6px 15px rgba(255, 182, 193, 0.4);
    }
    
    /* Card Sản phẩm & Nội dung */
    .menu-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 18px;
        padding: 15px;
        border: 2px solid #FFC0CB;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 20px;
    }

    /* Hiển thị ly nước mô phỏng kiểu Oatside */
    .boba-cup {
        width: 140px;
        height: 200px;
        border: 4px solid #4A3E3D;
        border-radius: 0 0 25px 25px;
        margin: auto;
        position: relative;
        overflow: hidden;
        background: #FFFFFF;
        box-shadow: 4px 4px 0px #FFB6C1;
    }
    .boba-liquid {
        position: absolute;
        bottom: 0;
        width: 100%;
        transition: height 0.3s ease, background-color 0.3s ease;
    }
    .boba-ice {
        position: absolute;
        top: 20px;
        width: 100%;
        text-align: center;
        font-size: 16px;
        z-index: 6;
        user-select: none;
    }
    .boba-topping {
        position: absolute;
        bottom: 5px;
        width: 100%;
        text-align: center;
        font-size: 20px;
        z-index: 5;
        letter-spacing: 2px;
        user-select: none;
    }
    
    .footer-quote {
        text-align: center;
        font-size: 1.1rem;
        font-weight: 700;
        color: #8B4513;
        background: #FFF5F7;
        padding: 15px;
        border-radius: 15px;
        border: 2px dashed #FFB6C1;
        margin-top: 30px;
    }
    
    /* Styling riêng cho Minigame */
    .game-box {
        background: rgba(255, 255, 255, 0.95);
        padding: 25px;
        border-radius: 20px;
        border: 3px solid #FFB6C1;
        box-shadow: 0 6px 15px rgba(0,0,0,0.05);
    }
    .positive-message {
        background-color: #E8F5E9;
        color: #2E7D32;
        padding: 12px 18px;
        border-radius: 12px;
        border-left: 5px solid #4CAF50;
        font-weight: 600;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. KHO DỮ LIỆU CÁC MỤC & DỮ LIỆU GAME
# ---------------------------------------------------------
SEASONS_MENU = {
    "Mùa Xuân": [
        {"name": "Trà Đào Cam Sả", "img": "1.jpg", "color": "#FF9F43", "price": 45000},
        {"name": "Trà Dâu Tằm", "img": "2.jpg", "color": "#EE5253", "price": 42000},
        {"name": "Cold Brew Cam Quế", "img": "3.jpg", "color": "#D35400", "price": 50000},
        {"name": "Trà Ô Long Quế Hoa Xoài", "img": "4.jpg", "color": "#F1C40F", "price": 48000},
        {"name": "Matcha Latte", "img": "5.jpg", "color": "#1DD1A1", "price": 48000},
        {"name": "Dâu crunchy đá xay", "img": "6.jpg", "color": "#FF6B6B", "price": 55000},
    ],
    "Mùa Hạ": [
        {"name": "Trà Thạch Đào", "img": "7.jpg", "color": "#FF7851", "price": 42000},
        {"name": "Trà Ổi Hồng", "img": "8.jpg", "color": "#FF6B81", "price": 45000},
        {"name": "Trà Măng Cụt", "img": "9.jpg", "color": "#A55EEA", "price": 48000},
        {"name": "Cà Phê Muối Biển", "img": "10.jpg", "color": "#70A1FF", "price": 38000},
        {"name": "Đá Xay Bạc Hà", "img": "11.jpg", "color": "#00D2D3", "price": 52000},
        {"name": "Trà Nhãn Lài", "img": "12.jpg", "color": "#FECA57", "price": 42000},
    ],
    "Mùa Thu": [
        {"name": "Cold Brew kem muối caramel", "img": "13.jpg", "color": "#E1B12C", "price": 52000},
        {"name": "Cà Phê Đường Đen Gừng", "img": "14.jpg", "color": "#8C7AE6", "price": 42000},
        {"name": "Cà Phê Latte Hạnh Nhân Nướng", "img": "15.jpg", "color": "#CD84F1", "price": 48000},
        {"name": "Trà Sữa Chôm Chôm Nướng", "img": "16.jpg", "color": "#FFB8B8", "price": 45000},
        {"name": "Oolong Tứ Quý Sữa", "img": "17.jpg", "color": "#C8D6E5", "price": 45000},
        {"name": "Trà Long Nhãn Hạt Sen", "img": "18.jpg", "color": "#FFDA79", "price": 48000},
    ],
    "Mùa Đông": [
        {"name": "Latte gừng", "img": "19.jpg", "color": "#D35400", "price": 45000},
        {"name": "Trà Thạch Đào Nóng", "img": "20.jpg", "color": "#E67E22", "price": 42000},
        {"name": "Trà Gừng Mật Ong Thảo Mộc", "img": "21.jpg", "color": "#F39C12", "price": 40000},
        {"name": "Cà phê socola bạc hà", "img": "22.jpg", "color": "#2C3E50", "price": 48000},
        {"name": "Cà phê trứng Hà Nội", "img": "23.jpg", "color": "#F1C40F", "price": 45000},
        {"name": "Trà sữa khoai môn mochi dẻo", "img": "24.jpg", "color": "#9B59B6", "price": 50000},
    ]
}

ALL_DRINKS = {}
for season_key in SEASONS_MENU:
    for drink in SEASONS_MENU[season_key]:
        ALL_DRINKS[drink["name"]] = drink

HEIGHT_MAP = {
    "S (Vừa)": "50%",
    "M (Lớn)": "75%",
    "L (Đặc biệt)": "95%"
}

ICE_ICON_MAP = {
    "0%": "",
    "30%": "🧊",
    "50%": "🧊 🧊",
    "100%": "🧊 🧊 🧊"
}

TOPPING_ICON_MAP = {
    "Trân châu đen": "🧋",
    "Pudding trứng": "🍮",
    "Kem Cheese": "🧀"
}

BOOKS_
