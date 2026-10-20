import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CẤU HÌNH TRANG
st.set_page_config(
    page_title="Chiikawa Boba Visualizer",
    page_icon="🧋",
    layout="wide"
)

# ---------------------------------------------------------
# 2. CUSTOM CSS: BỘ MÔ PHỎNG LY TRÀ SỮA ĐỘNG
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Fredoka', sans-serif;
    }
    .stApp {
        background-color: #FAF5EF;
    }
    
    /* Khung chứa ly nước */
    .visualizer-container {
        background: #FFFFFF;
        border: 3px solid #2B2B2B;
        border-radius: 20px;
        padding: 30px 20px;
        box-shadow: 6px 6px 0px #2B2B2B;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 420px;
    }
    
    /* Thân ly trà sữa */
    .boba-cup {
        border: 4px solid #2B2B2B;
        border-top: none;
        border-radius: 0 0 35px 35px;
        position: relative;
        overflow: hidden;
        background: rgba(255, 255, 255, 0.4);
        box-shadow: inset 0 0 10px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }

    /* Ống hút */
    .straw {
        width: 14px;
        height: 80px;
        background: #FF6B6B;
        position: absolute;
        top: -40px;
        left: 50%;
        transform: translateX(-50%) rotate(-8deg);
        border: 2px solid #2B2B2B;
        z-index: 10;
        border-radius: 5px;
    }

    /* Phần chất lỏng (Trà sữa) */
    .boba-liquid {
        position: absolute;
        bottom: 0;
        width: 100%;
        transition: height 0.4s ease, background-color 0.4s ease, opacity 0.4s ease;
        border-radius: 0 0 30px 30px;
    }

    /* Lớp Kem Cheese phủ trên mặt */
    .cheese-foam {
        position: absolute;
        top: 0;
        width: 100%;
        height: 25px;
        background-color: #FFFDD0;
        border-bottom: 2px dashed #E6C280;
        z-index: 4;
    }

    /* Topping đáy ly */
    .topping-layer {
        position: absolute;
        bottom: 6px;
        width: 100%;
        text-align: center;
        font-size: 20px;
        z-index: 3;
        letter-spacing: 2px;
        user-select: none;
    }

    /* Hiển thị các viên đá */
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
        background: #FFE4E1;
        border: 2px solid #2B2B2B;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: bold;
        margin: 3px;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. DỮ LIỆU SẢN PHẨM & MÀU SẮC MÔ PHỎNG
# ---------------------------------------------------------
MENU_TEA = {
    "Trà Sữa Truyền Thống Chika": {"price": 30000, "color": "#D2B48C"},  # Nâu trà sữa
    "Trà Sữa Trân Châu Usagi": {"price": 35000, "color": "#C59B27"},     # Nâu đường đen
    "Trà Sữa Thái Xanh Hachiware": {"price": 32000, "color": "#7BB661"},  # Xanh Thái
    "Trà Sữa Ô Long": {"price": 35000, "color": "#C19A6B"},               # Ô long đậm
    "Trà Sữa Matcha": {"price": 38000, "color": "#86A53B"},               # Xanh Matcha
    "Trà Đào Cam Sả": {"price": 35000, "color": "#FF7F50"},               # Cam đào
    "Trà Dâu Tằm": {"price": 32000, "color": "#8B0000"},                  # Đỏ thẫm
}

SIZE_OPTIONS = {
    "S (Vừa)": {"price": 0, "height": "160px", "width": "110px", "fill": "70%"},
    "M (Lớn)": {"price": 5000, "height": "190px", "width": "125px", "fill": "82%"},
    "L (Đặc biệt)": {"price": 10000, "height": "220px", "width": "135px", "fill": "92%"}
}

TOPPING_OPTIONS = {
    "Trân châu đen": {"price": 5000, "icon": "⚫⚫⚫"},
    "Trân châu trắng": {"price": 7000, "icon": "⚪⚪⚪"},
    "Thạch trái cây": {"price": 5000, "icon": "🟥🟩🟨"},
    "Pudding trứng": {"price": 8000, "icon": "🍮"},
    "Kem Cheese": {"price": 10000, "icon": "🧀"} # Phủ ở trên
}

SUGAR_LEVELS = {
    "100% (Bình thường)": {"opacity": "1.0", "label": "100% Đường"},
    "70%": {"opacity": "0.9", "label": "70% Đường"},
    "50%": {"opacity": "0.8", "label": "50% Đường"},
    "30%": {"opacity": "0.7", "label": "30% Đường"},
    "0% (Không đường)": {"opacity": "0.55", "label": "0% Đường"}
}

ICE_LEVELS = {
    "100% (Bình thường)": {"cubes": "🧊 🧊 🧊", "label": "100% Đá"},
    "70%": {"cubes": "🧊 🧊", "label": "70% Đá"},
    "50%": {"cubes": "🧊 🧊", "label": "50% Đá"},
    "30%": {"cubes": "🧊", "label": "30% Đá"},
    "0% (Không đá)": {"cubes": "", "label": "0% Đá"}
}

if "cart" not in st.session_state:
    st.session_state.cart = []

# ---------------------------------------------------------
# 4. GIAO DIỆN CHÍNH
# ---------------------------------------------------------
st.title("QUÁN TRÀ SỮA CHIIKAWA 🧋")
st.caption("Trải nghiệm tùy chỉnh & Mô phỏng ly nước trực tiếp")
st.markdown("---")

col_input, col_visual, col_cart = st.columns([1.1, 1.0, 1.1])

# ==================== CỘT 1: CHỌN CẤU HÌNH LY ====================
with col_input:
    st.subheader("📝 Tùy chỉnh Ly nước")
    
    selected_tea = st.selectbox("1. Chọn Loại Trà Sữa:", list(MENU_TEA.keys()))
    selected_size = st.selectbox("2. Chọn Size:", list(SIZE_OPTIONS.keys()))
    
    c1, c2 = st.columns(2)
    with c1:
        selected_sugar = st.selectbox("3. Mức Đường:", list(SUGAR_LEVELS.keys()))
    with c2:
        selected_ice = st.selectbox("4. Mức Đá:", list(ICE_LEVELS.keys()))
        
    selected_toppings = st.multiselect("5. Chọn Topping:", list(TOPPING_OPTIONS.keys()))
    quantity = st.number_input("6. Số lượng:", min_value=1, value=1, step=1)

    # Tính đơn giá
    base_price = MENU_TEA[selected_tea]["price"]
    size_price = SIZE_OPTIONS[selected_size]["price"]
    topping_price = sum(TOPPING_OPTIONS[t]["price"] for t in selected_toppings)
    unit_price = base_price + size_price + topping_price
    item_total = unit_price * quantity

    st.markdown(f"#### Đơn giá: **{unit_price:,} VNĐ**")

    if st.button("➕ Thêm vào hóa đơn", type="primary", use_container_width=True):
        st.session_state.cart.append({
            "Tên món": selected_tea,
            "Size": selected_size.split()[0],
            "Đường": selected_sugar.split()[0],
            "Đá": selected_ice.split()[0],
            "Topping": ", ".join(selected_toppings) if selected_toppings else "Không",
            "Đơn giá": unit_price,
            "Số lượng": quantity,
            "Thành tiền": item_total
        })
        st.toast(f"Đã thêm **{quantity}x {selected_tea}**!", icon="✅")

# ==================== CỘT 2: MÔ PHỎNG LY NƯỚC ĐỘNG ====================
with col_visual:
    st.subheader("🎨 Mô phỏng Trực quan")
    
    # Lấy thông số cấu hình
    cup_h = SIZE_OPTIONS[selected_size]["height"]
    cup_w = SIZE_OPTIONS[selected_size]["width"]
    fill_h = SIZE_OPTIONS[selected_size]["fill"]
    drink_color = MENU_TEA[selected_tea]["color"]
    sugar_op = SUGAR_LEVELS[selected_sugar]["opacity"]
    ice_cubes = ICE_LEVELS[selected_ice]["cubes"]
    
    # Xử lý Topping hiển thị
    has_cheese = "Kem Cheese" in selected_toppings
    bottom_toppings = [TOPPING_OPTIONS[t]["icon"] for t in selected_toppings if t != "Kem Cheese"]
    topping_html = " ".join(bottom_toppings) if bottom_toppings else ""

    # HTML Render Ly Nước
    cheese_html = '<div class="cheese-foam"></div>' if has_cheese else ''
    
    st.markdown(f"""
    <div class="visualizer-container">
        <div class="boba-cup" style="height: {cup_h}; width: {cup_w};">
            <div class="straw"></div>
            {ice_cubes and f'<div class="ice-cubes">{ice_cubes}</div>'}
            <div class="boba-liquid" style="height: {fill_h}; background-color: {drink_color}; opacity: {sugar_op};">
                {cheese_html}
            </div>
            <div class="topping-layer">{topping_html}</div>
        </div>
        <div style="margin-top: 20px; text-align: center;">
            <span class="spec-tag">Size {selected_size.split()[0]}</span>
            <span class="spec-tag">{SUGAR_LEVELS[selected_sugar]['label']}</span>
            <span class="spec-tag">{ICE_LEVELS[selected_ice]['label']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==================== CỘT 3: GIỎ HÀNG & THANH TOÁN ====================
with col_cart:
    st.subheader("🛒 Giỏ hàng")
    
    if not st.session_state.cart:
        st.info("Chưa có món nào được chọn.")
    else:
        df_cart = pd.DataFrame(st.session_state.cart)
        st.dataframe(df_cart[["Tên món", "Size", "Số lượng", "Thành tiền"]], hide_index=True, use_container_width=True)
        
        total_amount = sum(item["Thành tiền"] for item in st.session_state.cart)
        st.markdown(f"### Tổng cộng: **{total_amount:,} VNĐ**")
        
        if st.button("🗑️ Xóa giỏ hàng", use_container_width=True):
            st.session_state.cart = []
            st.rerun()
