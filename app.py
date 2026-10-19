import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------------------------------------------------
# CẤU HÌNH TRANG (Phải là lệnh Streamlit đầu tiên)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Hệ Thống Tính Tiền Trà Sữa Chiikawa",
    page_icon="🧋",
    layout="wide"
)

# ---------------------------------------------------------
# CƠ SỞ DỮ LIỆU SẢN PHẨM & CẤU HÌNH
# ---------------------------------------------------------
# Danh sách menu, giá (VND) và tên file ảnh tương ứng
MENU_TEA = {
    "Trà Sữa Truyền Thống chika": {"price": 30000, "image": "TRASUA1.jpg"},
    "Trà Sữa Trân Châu Đường Đen usagi": {"price": 35000, "image": "TRASUA2.jpg"},
    "Trà Sữa Thái Xanh hachiware": {"price": 32000, "image": "TRASUA3.jpg"},
    "Trà sữa Gạo Rang": {"price": 30000, "image": "TRASUA4.jpg"},
    "Trà Sữa Ô Long": {"price": 35000, "image": "TRASUA5.jpg"},
    "Trà Sữa Matcha": {"price": 38000, "image": "TRASUA6.jpg"},
    "Trà Sữa Dâu Tây": {"price": 35000, "image": "TRASUA7.jpg"},
    "Trà Đào Cam Sả": {"price": 35000, "image": "TRASUA8.jpg"},
    "Trà Dâu Tằm": {"price": 32000, "image": "TRASUA9.jpg"},
}

SIZE_OPTIONS = {
    "S (Vừa)": 0,
    "M (Lớn)": 5000,
    "L (Đặc biệt)": 10000
}

TOPPING_OPTIONS = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 7000,
    "Thạch trái cây": 5000,
    "Pudding trứng": 8000,
    "Kem Cheese": 10000
}

# Danh sách quà tặng gấu bông Chiikawa (khi mua từ 5 món trở lên)
GIFT_OPTIONS = {
    "Gấu bông Chiikawa": "GAUBONG1.jpg",
    "Gấu bông Hachiware": "GAUBONG2.jpg",
    "Gấu bông Usagi": "GAUBONG3.jpg"
}

SUGAR_LEVELS = ["100% (Bình thường)", "70%", "50%", "30%", "0% (Không đường)"]
ICE_LEVELS = ["100% (Bình thường)", "70%", "50%", "30%", "0% (Không đá)"]

# Khởi tạo session state
if "cart" not in st.session_state:
    st.session_state.cart = []
if "invoice_paid" not in st.session_state:
    st.session_state.invoice_paid = False

# ---------------------------------------------------------
# HÀM XUẤT HÓA ĐƠN DẠNG TEXT (.TXT)
# ---------------------------------------------------------
def create_txt_invoice(customer_name, cart, total_amount, discount, final_amount, gift_item=None):
    """Tạo file hóa đơn dạng văn bản (TXT)"""
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    content = f"{'='*40}\n"
    content += f"{'HÓA ĐƠN BÁN HÀNG - BOBA TEA':^40}\n"
    content += f"{'='*40}\n"
    content += f"Ngày: {now}\n"
    content += f"Khách hàng: {customer_name if customer_name else 'Khách vãng lai'}\n"
    content += f"{'-'*40}\n"
    
    for idx, item in enumerate(cart, 1):
        content += f"{idx}. {item['Tên món']} ({item['Size']})\n"
        content += f"   - Đường: {item['Đường']} | Đá: {item['Đá']}\n"
        if item['Topping'] != "Không":
            content += f"   - Topping: {item['Topping']}\n"
        content += f"   SL: {item['Số lượng']} x {item['Đơn giá']:,} = {item['Thành tiền']:,} VNĐ\n"
        
    content += f"{'-'*40}\n"
    content += f"Tổng tiền món: {total_amount:,} VNĐ\n"
    content += f"Giảm giá: {discount}%\n"
    content += f"TỔNG THANH TOÁN: {final_amount:,} VNĐ\n"
    
    if gift_item:
        content += f"{'-'*40}\n"
        content += f"🎁 QUÀ TẶNG TRI ÂN: {gift_item}\n"
        
    content += f"{'='*40}\n"
    content += f"{'Cảm ơn quý khách và hẹn gặp lại!':^40}\n"
    return content

# ---------------------------------------------------------
# GIAO DIỆN CHÍNH
# ---------------------------------------------------------
st.title("🧋 QUÁN TRÀ SỮA CHIIKAWA")
st.markdown("---")

col_left, col_right = st.columns([1.1, 0.9])

# ==================== CỘT TRÁI: NHẬP THÔNG TIN ====================
with col_left:
    st.subheader("📝 Thông tin đơn hàng")
    
    # 1. Thông tin khách hàng
    customer_name = st.text_input("Tên khách hàng:", placeholder="Nhập tên khách hàng...")
    
    st.markdown("#### Chọn món nước & Tùy chọn")
    
    # 2. Chọn trà sữa & số lượng
    col_item, col_qty = st.columns([3, 1])
    with col_item:
        selected_tea = st.selectbox("Loại trà sữa:", list(MENU_TEA.keys()))
    with col_qty:
        quantity = st.number_input("Số lượng:", min_value=1, value=1, step=1)

    # Hiển thị ảnh món nước được chọn
    tea_img_path = MENU_TEA[selected_tea]["image"]
    try:
        st.image(tea_img_path, caption=f"Hình ảnh: {selected_tea}", width=250)
    except Exception:
        st.info(f"📌 [Ảnh món nước {tea_img_path} chưa được đặt đúng thư mục]")

    # 3. Size, Đường, Đá
    c_size, c_sugar, c_ice = st.columns(3)
    with c_size:
        selected_size = st.selectbox("Size:", list(SIZE_OPTIONS.keys()))
    with c_sugar:
        selected_sugar = st.selectbox("Mức đường:", SUGAR_LEVELS)
    with c_ice:
        selected_ice = st.selectbox("Mức đá:", ICE_LEVELS)

    # 4. Chọn topping
    selected_toppings = st.multiselect(
        "Loại Topping (có thể chọn nhiều):",
        options=list(TOPPING_OPTIONS.keys())
    )

    # Tính giá tiền từng ly
    base_price = MENU_TEA[selected_tea]["price"]
    size_price = SIZE_OPTIONS[selected_size]
    topping_price = sum(TOPPING_OPTIONS[t] for t in selected_toppings)
    unit_price = base_price + size_price + topping_price
    item_total = unit_price * quantity

    st.info(f"💡 Đơn giá 1 ly (đã gồm size & topping): **{unit_price:,} VNĐ**")

    # Nút thêm món vào giỏ
    if st.button("➕ Thêm vào hóa đơn", type="primary", use_container_width=True):
        topping_str = ", ".join(selected_toppings) if selected_toppings else "Không"
        item_data = {
            "Tên món": selected_tea,
            "Size": selected_size.split()[0], # Lấy ký tự S, M, L
            "Đường": selected_sugar.split()[0],
            "Đá": selected_ice.split()[0],
            "Topping": topping_str,
            "Đơn giá": unit_price,
            "Số lượng": quantity,
            "Thành tiền": item_total
        }
        st.session_state.cart.append(item_data)
        st.session_state.invoice_paid = False
        st.toast(f"Đã thêm **{quantity}x {selected_tea}** vào giỏ!", icon="✅")

# ==================== CỘT PHẢI: CHI TIẾT HÓA ĐƠN ====================
with col_right:
    st.subheader("🛒 Danh sách món đã gọi")

    if not st.session_state.cart:
        st.warning("Giỏ hàng hiện đang trống. Vui lòng chọn món ở cột bên trái.")
        selected_gift = None
    else:
        # Hiển thị giỏ hàng bằng Bảng Pandas
        df_cart = pd.DataFrame(st.session_state.cart)
        
        # Format
