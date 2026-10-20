import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG (Phải đặt ở ĐẦU TIÊN)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Chiikawa Boba POS",
    page_icon="🧋",
    layout="wide"
)

# ---------------------------------------------------------
# 2. CUSTOM CSS GIAO DIỆN
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Tông màu chủ đạo */
    .stApp {
        background-color: #FAF5EF;
    }
    /* Card món ăn */
    .menu-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #FFE4E1;
        margin-bottom: 10px;
    }
    .menu-title {
        font-weight: bold;
        color: #D2691E;
        font-size: 1.1rem;
    }
    .menu-price {
        color: #E65100;
        font-weight: 600;
    }
    /* Total Box */
    .total-box {
        background-color: #FFF0F5;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #FFB6C1;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. DỮ LIỆU SẢN PHẨM & SESSION STATE
# ---------------------------------------------------------
MENU_TEA = {
    "Trà Sữa Truyền Thống Chika": {"price": 30000, "cat": "Trà Sữa"},
    "Trà Sữa Trân Châu Usagi": {"price": 35000, "cat": "Trà Sữa"},
    "Trà Sữa Thái Xanh Hachiware": {"price": 32000, "cat": "Trà Sữa"},
    "Trà Sữa Ô Long": {"price": 35000, "cat": "Trà Sữa"},
    "Trà Sữa Matcha": {"price": 38000, "cat": "Trà Sữa"},
    "Trà Đào Cam Sả": {"price": 35000, "cat": "Trà Trái Cây"},
    "Trà Dâu Tằm": {"price": 32000, "cat": "Trà Trái Cây"},
}

SIZE_OPTIONS = {"S (Vừa)": 0, "M (Lớn)": 5000, "L (Đặc biệt)": 10000}
TOPPING_OPTIONS = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 7000,
    "Thạch trái cây": 5000,
    "Pudding trứng": 8000,
    "Kem Cheese": 10000
}
SUGAR_LEVELS = ["100%", "70%", "50%", "30%", "0%"]
ICE_LEVELS = ["100%", "70%", "50%", "30%", "0%"]

if "cart" not in st.session_state:
    st.session_state.cart = []
if "invoice_paid" not in st.session_state:
    st.session_state.invoice_paid = False

# ---------------------------------------------------------
# 4. TIÊU ĐỀ ỨNG DỤNG
# ---------------------------------------------------------
col_header1, col_header2 = st.columns([1, 4])
with col_header1:
    # Bạn có thể thay đường dẫn ảnh local hoặc online
    st.image("https://cdn-icons-png.flaticon.com/512/3081/3081162.png", width=90)
with col_header2:
    st.title("QUÁN TRÀ SỮA CHIIKAWA 🧋")
    st.caption("Hệ thống Order & Tính tiền nhanh chóng")

st.markdown("---")

# ---------------------------------------------------------
# 5. GIAO DIỆN CHÍNH (2 CỘT)
# ---------------------------------------------------------
col_left, col_right = st.columns([1.2, 0.8])

# ==================== CỘT TRÁI: ORDER MÓN ====================
with col_left:
    st.subheader("📋 Order Món")
    customer_name = st.text_input("👤 Tên khách hàng:", placeholder="Nhập tên khách...")

    # Chọn món
    selected_tea = st.selectbox("🥤 Chọn món nước:", list(MENU_TEA.keys()))
    
    c_qty, c_size = st.columns(2)
    with c_qty:
        quantity = st.number_input("Số lượng:", min_value=1, value=1, step=1)
    with c_size:
        selected_size = st.selectbox("Size:", list(SIZE_OPTIONS.keys()))

    c_sugar, c_ice = st.columns(2)
    with c_sugar:
        selected_sugar = st.selectbox("Đường:", SUGAR_LEVELS)
    with c_ice:
        selected_ice = st.selectbox("Đá:", ICE_LEVELS)

    selected_toppings = st.multiselect("🧋 Topping đi kèm:", options=list(TOPPING_OPTIONS.keys()))

    # Tính đơn giá
    base_price = MENU_TEA[selected_tea]["price"]
    size_price = SIZE_OPTIONS[selected_size]
    topping_price = sum(TOPPING_OPTIONS[t] for t in selected_toppings)
    unit_price = base_price + size_price + topping_price
    item_total = unit_price * quantity

    st.info(f"💰 Đơn giá: **{unit_price:,} VNĐ** / ly  ➔ Thành tiền: **{item_total:,} VNĐ**")

    if st.button("➕ THÊM VÀO GIỎ HÀNG", type="primary", use_container_width=True):
        topping_str = ", ".join(selected_toppings) if selected_toppings else "Không"
        item_data = {
            "Tên món": selected_tea,
            "Size": selected_size.split()[0],
            "Đường": selected_sugar,
            "Đá": selected_ice,
            "Topping": topping_str,
            "Đơn giá": unit_price,
            "Số lượng": quantity,
            "Thành tiền": item_total
        }
        st.session_state.cart.append(item_data)
        st.session_state.invoice_paid = False
        st.toast(f"Đã thêm **{quantity}x {selected_tea}**!", icon="✅")

# ==================== CỘT PHẢI: GIỎ HÀNG & THANH TOÁN ====================
with col_right:
    st.subheader("🛒 Giỏ Hàng Hiện Tại")

    if not st.session_state.cart:
        st.info("Giỏ hàng đang trống. Chọn món bên trái để bắt đầu order!")
    else:
        # Hiển thị giỏ hàng kèm nút xóa từng mục
        for idx, item in enumerate(st.session_state.cart):
            with st.container():
                c_info, c_del = st.columns([4, 1])
                with c_info:
                    st.markdown(f"**{idx+1}. {item['Tên món']}** ({item['Size']}) x{item['Số lượng']}")
                    st.caption(f"Đường: {item['Đường']} | Đá: {item['Đá']} | Topping: {item['Topping']}")
                    st.markdown(f"👉 **{item['Thành tiền']:,} VNĐ**")
                with c_del:
                    if st.button("❌", key=f"del_{idx}"):
                        st.session_state.cart.pop(idx)
                        st.rerun()
                st.markdown("---")

        total_price = sum(item["Thành tiền"] for item in st.session_state.cart)
        
        # Mã giảm giá / Discount
        discount = st.slider("🎉 Giảm giá (%):", min_value=0, max_value=50, value=0, step=5)
        final_price = int(total_price * (1 - discount / 100))

        st.markdown(f"""
        <div class="total-box">
            <h4>Tổng tiền món: {total_price:,} VNĐ</h4>
            <h3 style="color: #D2691E;">Thanh toán: {final_price:,} VNĐ</h3>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        col_pay_btn, col_clear_btn = st.columns([2, 1])
        with col_pay_btn:
            if st.button("💳 THANH TOÁN", type="primary", use_container_width=True):
                st.session_state.invoice_paid = True
                st.balloons()
        with col_clear_btn:
            if st.button("🗑️ Xóa hết", use_container_width=True):
                st.session_state.cart = []
                st.session_state.invoice_paid = False
                st.rerun()

# ---------------------------------------------------------
# 6. HIỂN THỊ HÓA ĐƠN & TẠO MA QR
# ---------------------------------------------------------
if st.session_state.get("invoice_paid") and st.session_state.cart:
    st.markdown("---")
    st.success("🎉 Đơn hàng đã xác nhận thanh toán thành công!")

    col_inv, col_qr = st.columns([1.2, 0.8])

    with col_inv:
        with st.container(border=True):
            st.markdown("<h3 style='text-align: center;'>🧋 HÓA ĐƠN BÁN HÀNG</h3>", unsafe_allow_html=True)
            st.write(f"**Khách hàng:** {customer_name if customer_name else 'Khách vãng lai'}")
            st.write(f"**Thời gian:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            
            df_display = pd.DataFrame(st.session_state.cart)
            st.dataframe(df_display[["Tên món", "Size", "Topping", "Số lượng", "Thành tiền"]], hide_index=True, use_container_width=True)
            
            st.markdown(f"**Tổng tiền thanh toán:** <span style='color:red; font-size:1.3rem;'>{final_price:,} VNĐ</span>", unsafe_allow_html=True)

    with col_qr:
        with st.container(border=True):
            st.markdown("<h4 style='text-align: center;'>📱 Quét mã VietQR</h4>", unsafe_allow_html=True)
            # Tạo link QuickLink VietQR động dựa trên số tiền
            # Bạn có thể thay BANK_ID và ACCOUNT_NO bằng tài khoản thật
            bank_id = "MB"
            account_no = "0000000000"
            qr_url = f"https://img.vietqr.io/image/{bank_id}-{account_no}-compact2.png?amount={final_price}&addInfo=TraSuaChiikawa"
            
            st.image(qr_url, caption="Mã QR thanh toán tự động theo số tiền", use_container_width=True)
