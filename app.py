import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG (Đặt ở đầu tiên)
# ---------------------------------------------------------
st.set_page_config(
    page_title="CÀ PHÊ CỎ - Menu & Order",
    page_icon="🌿",
    layout="wide"
)

# ---------------------------------------------------------
# 2. GIAO DIỆN & CUSTOM CSS (PHONG CÁCH "CỎ" MỘC MẠC)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Quicksand', sans-serif;
    }
    
    /* Màu nền nhã nhặn, tự nhiên */
    .stApp {
        background-color: #F4F6F0;
    }
    
    /* Khung mô phỏng ly nước */
    .visualizer-card {
        background: #FFFFFF;
        border: 2px solid #3B5E44;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 4px 6px 12px rgba(0,0,0,0.06);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 420px;
    }
    
    /* Thân ly */
    .drink-cup {
        border: 3px solid #2C3E2E;
        border-top: none;
        border-radius: 0 0 30px 30px;
        position: relative;
        overflow: hidden;
        background: rgba(255, 255, 255, 0.5);
        box-shadow: inset 0 0 10px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }

    /* Ống hút giấy thân thiện môi trường */
    .straw {
        width: 12px;
        height: 75px;
        background: #D8C3A5;
        position: absolute;
        top: -35px;
        left: 50%;
        transform: translateX(-50%) rotate(-6deg);
        border: 2px solid #2C3E2E;
        z-index: 10;
        border-radius: 4px;
    }

    /* Phần chất lỏng */
    .drink-liquid {
        position: absolute;
        bottom: 0;
        width: 100%;
        transition: height 0.4s ease, background-color 0.4s ease, opacity 0.4s ease;
        border-radius: 0 0 26px 26px;
    }

    /* Lớp Kem Macchiato / Bọt Cà Phê */
    .foam-layer {
        position: absolute;
        top: 0;
        width: 100%;
        height: 22px;
        background-color: #FFFDF0;
        border-bottom: 2px dashed #C0B283;
        z-index: 4;
    }

    /* Topping dưới đáy */
    .topping-bottom {
        position: absolute;
        bottom: 6px;
        width: 100%;
        text-align: center;
        font-size: 18px;
        z-index: 3;
        letter-spacing: 2px;
    }

    /* Viên đá */
    .ice-display {
        position: absolute;
        top: 25px;
        width: 100%;
        text-align: center;
        font-size: 16px;
        z-index: 5;
    }

    /* Tag thông số */
    .spec-tag {
        display: inline-block;
        background: #E2E9E1;
        color: #2C3E2E;
        border: 1px solid #3B5E44;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: 600;
        margin: 3px;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. CƠ SỞ DỮ LIỆU MENU QUÁN CÀ PHÊ "CỎ"
# ---------------------------------------------------------
MENU_COFFEE = {
    # Cà phê
    "Cà Phê Muối CỎ": {"price": 32000, "color": "#4A2C11", "cat": "Cà Phê"},
    "Cà Phê Sữa Đá": {"price": 29000, "color": "#6F4E37", "cat": "Cà Phê"},
    "Bạc Xỉu Mầm Cỏ": {"price": 35000, "color": "#D7B594", "cat": "Cà Phê"},
    "Espresso Cold Brew": {"price": 38000, "color": "#2B1B10", "cat": "Cà Phê"},
    
    # Trà & Đồ uống Thảo mộc
    "Trà Mơ Lên Men": {"price": 35000, "color": "#E69A2A", "cat": "Trà & Thảo Mộc"},
    "Trà Mùa Hè (Hoa Cúc & Hạt Chia)": {"price": 32000, "color": "#DAA520", "cat": "Trà & Thảo Mộc"},
    "Trà Xanh Matcha Mầm Xanh": {"price": 39000, "color": "#556B2F", "cat": "Trà & Thảo Mộc"},
}

SIZE_OPTIONS = {
    "S (Vừa)": {"price": 0, "height": "160px", "width": "110px", "fill": "70%"},
    "M (Lớn)": {"price": 6000, "height": "190px", "width": "125px", "fill": "82%"},
    "L (Đặc biệt)": {"price": 10000, "height": "220px", "width": "135px", "fill": "92%"}
}

TOPPING_OPTIONS = {
    "Sương sáo thủ công": {"price": 5000, "icon": "⬛⬛"},
    "Hạt chia organic": {"price": 5000, "icon": "░░"},
    "Kem Macchiato": {"price": 8000, "icon": "🥛"}, # Phủ mặt trên
    "Shot Espresso": {"price": 10000, "icon": "☕"}
}

SWEET_LEVELS = {
    "100% (Chuẩn vị)": {"opacity": "1.0", "label": "100% Ngọt"},
    "70% (Ít ngọt)": {"opacity": "0.88", "label": "70% Ngọt"},
    "50% (Thanh nhẹ)": {"opacity": "0.75", "label": "50% Ngọt"},
    "0% (Không đường)": {"opacity": "0.60", "label": "0% Đường"}
}

ICE_LEVELS = {
    "100% (Bình thường)": {"cubes": "🧊 🧊 🧊", "label": "100% Đá"},
    "50% (Ít đá)": {"cubes": "🧊 🧊", "label": "50% Đá"},
    "0% (Nóng / Không đá)": {"cubes": "", "label": "Không Đá"}
}

if "cart" not in st.session_state:
    st.session_state.cart = []

# ---------------------------------------------------------
# 4. HEADER QUÁN CỎ
# ---------------------------------------------------------
st.title("🌿 CÀ PHÊ CỎ")
st.caption("Góc nhỏ bình yên – Tùy chỉnh ly nước theo gu của bạn")
st.markdown("---")

col_order, col_visual, col_cart = st.columns([1.1, 1.0, 1.1])

# ==================== CỘT 1: CHỌN MÓN ====================
with col_order:
    st.subheader("📋 Lựa chọn đồ uống")
    
    selected_drink = st.selectbox("1. Chọn món:", list(MENU_COFFEE.keys()))
    selected_size = st.selectbox("2. Kích cỡ (Size):", list(SIZE_OPTIONS.keys()))
    
    c_sweet, c_ice = st.columns(2)
    with c_sweet:
        selected_sweet = st.selectbox("3. Độ ngọt:", list(SWEET_LEVELS.keys()))
    with c_ice:
        selected_ice = st.selectbox("4. Mức đá:", list(ICE_LEVELS.keys()))
        
    selected_toppings = st.multiselect("5. Topping thêm:", list(TOPPING_OPTIONS.keys()))
    quantity = st.number_input("6. Số lượng:", min_value=1, value=1, step=1)

    # Tính đơn giá
    base_p = MENU_COFFEE[selected_drink]["price"]
    size_p = SIZE_OPTIONS[selected_size]["price"]
    topping_p = sum(TOPPING_OPTIONS[t]["price"] for t in selected_toppings)
    unit_price = base_p + size_p + topping_p
    item_total = unit_price * quantity

    st.markdown(f"#### Đơn giá: **{unit_price:,} VNĐ**")

    if st.button("➕ Thêm vào giỏ hàng", type="primary", use_container_width=True):
        st.session_state.cart.append({
            "Tên món": selected_drink,
            "Size": selected_size.split()[0],
            "Độ ngọt": selected_sweet.split()[0],
            "Đá": selected_ice.split()[0],
            "Topping": ", ".join(selected_toppings) if selected_toppings else "Không",
            "Đơn giá": unit_price,
            "Số lượng": quantity,
            "Thành tiền": item_total
        })
        st.toast(f"Đã thêm **{quantity}x {selected_drink}** vào đơn!", icon="🌿")

# ==================== CỘT 2: MÔ PHỎNG LY NƯỚC trực quan ====================
with col_visual:
    st.subheader("🎨 Mô phỏng Ly nước")
    
    # Lấy dữ liệu cấu hình
    cup_h = SIZE_OPTIONS[selected_size]["height"]
    cup_w = SIZE_OPTIONS[selected_size]["width"]
    fill_h = SIZE_OPTIONS[selected_size]["fill"]
    drink_color = MENU_COFFEE[selected_drink]["color"]
    sweet_op = SWEET_LEVELS[selected_sweet]["opacity"]
    ice_cubes = ICE_LEVELS[selected_ice]["cubes"]
    
    # Xử lý Topping
    has_macchiato = "Kem Macchiato" in selected_toppings
    bottom_toppings = [TOPPING_OPTIONS[t]["icon"] for t in selected_toppings if t != "Kem Macchiato"]
    topping_html = " ".join(bottom_toppings) if bottom_toppings else ""

    foam_html = '<div class="foam-layer"></div>' if has_macchiato else ''
    
    # Render Ly Nước Động bằng HTML/CSS
    st.markdown(f"""
    <div class="visualizer-card
