import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG STREAMLIT (BẮT BUỘC Ở ĐẦU FILE)
# ---------------------------------------------------------
st.set_page_config(
    page_title="CỎ & MÂY Coffee",
    page_icon="☁️",
    layout="wide"
)

# ---------------------------------------------------------
# 2. CUSTOM CSS GIAO DIỆN & BỘ MÔ PHỎNG LY NƯỚC ĐỘNG
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
    
    /* Card Sản phẩm, Sách, Nhạc */
    .menu-card {
        background: #FFFFFF;
        border-radius: 15px;
        padding: 15px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        text-align: center;
        margin-bottom: 20px;
    }

    /* Container Bộ mô phỏng Ly nước */
    .visualizer-container {
        background: #FFFFFF;
        border: 3px solid #2D3748;
        border-radius: 24px;
        padding: 30px 20px;
        box-shadow: 6px 6px 0px #2D3748;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 440px;
    }
    
    /* Thân ly */
    .boba-cup {
        border: 4px solid #2D3748;
        border-top: none;
        border-radius: 0 0 35px 35px;
        position: relative;
        overflow: hidden;
        background: rgba(255, 255, 255, 0.5);
        box-shadow: inset 0 0 12px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        margin: 0 auto;
    }

    /* Ống hút */
    .straw {
        width: 14px;
        height: 80px;
        background: #E53E3E;
        position: absolute;
        top: -40px;
        left: 50%;
        transform: translateX(-50%) rotate(-8deg);
        border: 2px solid #2D3748;
        z-index: 10;
        border-radius: 6px;
    }

    /* Phần chất lỏng */
    .boba-liquid {
        position: absolute;
        bottom: 0;
        width: 100%;
        transition: height 0.4s ease, background-color 0.4s ease, opacity 0.4s ease;
        border-radius: 0 0 30px 30px;
    }

    /* Lớp Kem Cheese */
    .cheese-foam {
        position: absolute;
        top: 0;
        width: 100%;
        height: 25px;
        background-color: #FFFDD0;
        border-bottom: 2px dashed #D69E2E;
        z-index: 4;
    }

    /* Topping đáy ly */
    .topping-layer {
        position: absolute;
        bottom: 8px;
        width: 100%;
        text-align: center;
        font-size: 20px;
        z-index: 3;
        letter-spacing: 2px;
        user-select: none;
    }

    /* Viên Đá */
    .ice-cubes {
        position: absolute;
        top: 30px;
        width: 100%;
        text-align: center;
        font-size: 16px;
        z-index: 5;
        user-select: none;
    }

    /* Thông số bên dưới ly */
    .spec-tag {
        display: inline-block;
        background: #EBF8FF;
        border: 2px solid #3182CE;
        color: #2B6CB0;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: bold;
        margin: 3px;
        font-size: 0.85rem;
    }
    
    /* Khung ghi chú footer */
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
# 3. KHO DỮ LIỆU CÁC MỤC (MENU, SÁCH, NHẠC)
# ---------------------------------------------------------
SEASONS_
