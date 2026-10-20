import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG STREAMLIT
# ---------------------------------------------------------
st.set_page_config(
    page_title="CỎ & MÂY Coffee",
    page_icon="☁️",
    layout="wide"
)

# ---------------------------------------------------------
# 2. CUSTOM CSS GIAO DIỆN & MÔ PHỎNG LY NƯỚC (TỪ CODE 1)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Quicksand', sans-serif;
    }
    .stApp {
        background-color: #FAF8F5;
    }
    
    /* Header Branding */
    .brand-header {
        text-align: center;
        padding: 18px;
        background: linear-gradient(135deg, #A8E6CF, #DCEDC1);
        border-radius: 18px;
        margin-bottom: 25px;
        color: #2D5A27;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    /* Card Sản phẩm */
    .menu-card {
        background: #FFFFFF;
        border-radius: 15px;
        padding: 15px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        text-align: center;
        margin-bottom: 20px;
    }

    /* Hiển thị ly nước mô phỏng kiểu Oatside (Code 1) */
    .boba-cup {
        width: 130px;
        height: 190px;
        border: 4px solid #1A1A1A;
        border-radius: 0 0 25px 25px;
        margin: auto;
        position: relative;
        overflow: hidden;
        background: #FFFFFF;
        box-shadow: 4px 4px 0px #1A1A1A;
    }
    .boba-liquid {
        position: absolute;
        bottom: 0;
        width: 100%;
        transition: height 0.3s ease, background-color 0.3s ease;
    }
    .boba-topping {
        position: absolute;
        bottom: 5px;
        width: 100%;
        text-align: center;
        font-size: 22px;
        z-index: 5;
    }
    
    .footer-quote {
        text-align: center;
        font-size: 1.1rem;
        font-weight: 700;
        color: #2F855A;
        background: #EDFDFA;
        padding: 15px;
        border-radius: 12px;
        border: 2px dashed #38B2AC;
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. KHO DỮ LIỆU CÁC MỤC
# ---------------------------------------------------------
SEASONS_MENU = {
    "🌸 Mùa Xuân": [
        {"name": "Trà Đào Cam Sả", "img": "1.jpg", "color": "#FF9F43", "price": 45000},
        {"name": "Trà Dâu Tằm", "img": "2.jpg", "color": "#EE5253", "price": 42000},
        {"name": "Cold Brew Cam Quế", "img": "3.jpg", "color": "#D35400", "price": 50000},
        {"name": "Trà Ô Long Quế Hoa Xoài", "img": "4.jpg", "color": "#F1C40F", "price": 48000},
        {"name": "Matcha Latte", "img": "5.jpg", "color": "#1DD1A1", "price": 48000},
        {"name": "Dâu crunchy đá xay", "img": "6.jpg", "color": "#FF6B6B", "price": 55000},
    ],
    "☀️ Mùa Hạ": [
        {"name": "Trà Thạch Đào", "img": "7.jpg", "color": "#FF7851", "price": 42000},
        {"name": "Trà Ổi Hồng", "img": "8.jpg", "color": "#FF6B81", "price": 45000},
        {"name": "Trà Măng Cụt", "img": "9.jpg", "color": "#A55EEA", "price": 48000},
        {"name": "Cà Phê Muối Biển", "img": "10.jpg", "color": "#70A1FF", "price": 38000},
        {"name": "Đá Xay Bạc Hà", "img": "11.jpg", "color": "#00D2D3", "price": 52000},
        {"name": "Trà Nhãn Lài", "img": "12.jpg", "color": "#FECA57", "price": 42000},
    ],
    "🍂 Mùa Thu": [
        {"name": "Cold Brew kem muối caramel", "img": "13.jpg", "color": "#E1B12C", "price": 52000},
        {"name": "Cà Phê Đường Đen Gừng", "img": "14.jpg", "color": "#8C7AE6", "price": 42000},
        {"name": "Cà Phê Latte Hạnh Nhân Nướng", "img": "15.jpg", "color": "#CD84F1", "price": 48000},
        {"name": "Trà Sữa Chôm Chôm Nướng", "img": "16.jpg", "color": "#FFB8B8", "price": 45000},
        {"name": "Oolong Tứ Quý Sữa", "img": "17.jpg", "color": "#C8D6E5", "price": 45000},
        {"name": "Trà Long Nhãn Hạt Sen", "img": "18.jpg", "color": "#FFDA79", "price": 48000},
    ],
    "❄️ Mùa Đông": [
        {"name": "Latte gừng", "img": "19.jpg", "color": "#D35400", "price": 45000},
        {"name": "Trà Thạch Đào Nóng", "img": "20.jpg", "color": "#E67E22", "price": 42000},
        {"name": "Trà Gừng Mật Ong Thảo Mộc", "img": "21.jpg", "color": "#F39C12", "price": 40000},
        {"name": "Cà phê socola bạc hà", "img": "22.jpg", "color": "#2C3E50", "price": 48000},
        {"name": "Cà phê trứng Hà Nội", "img": "23.jpg", "color": "#F1C40F", "price": 45000},
        {"name": "Trà sữa khoai môn mochi dẻo", "img": "24.jpg", "color": "#9B59B6", "price": 50000},
    ]
}

ALL_DRINKS = {}
for
