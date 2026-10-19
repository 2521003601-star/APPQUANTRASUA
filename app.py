import streamlit as st
import pandas as pd
from datetime import datetime
st.image("TRASUA.jpg")

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
        
        # Format bảng hiển thị
        st.dataframe(
            df_cart[["Tên món", "Size", "Topping", "Số lượng", "Đơn giá", "Thành tiền"]],
            use_container_width=True,
            hide_index=True
        )

        # Nút xóa giỏ hàng
        if st.button("🗑️ Xóa tất cả món"):
            st.session_state.cart = []
            st.session_state.invoice_paid = False
            st.rerun()

        st.markdown("---")
        
        # Tính tổng số lượng ly nước và tổng tiền
        total_items_count = df_cart["Số lượng"].sum()
        total_price = df_cart["Thành tiền"].sum()

        # 🎁 CHƯƠNG TRÌNH TẶNG QUÀ TRI ÂN KHÁCH HÀNG
        selected_gift = None
        if total_items_count >= 5:
            st.success(f"🎉 Bạn đã mua **{total_items_count}** món nước (từ 5 món trở lên)! Bạn nhận được **1 gấu bông Chiikawa tri án**.")
            col_gift_select, col_gift_img = st.columns([2, 1])
            with col_gift_select:
                selected_gift = st.selectbox("🎁 Chọn quà tặng gấu bông:", list(GIFT_OPTIONS.keys()))
            with col_gift_img:
                gift_img_path = GIFT_OPTIONS[selected_gift]
                try:
                    st.image(gift_img_path, caption=selected_gift, width=100)
                except Exception:
                    st.caption(f"📌 [{gift_img_path}]")
        else:
            st.info(f"💡 Mua thêm **{5 - total_items_count}** món nước nữa để nhận ngay 1 gấu bông Chiikawa!")

        col_disc, col_pay = st.columns(2)
        with col_disc:
            discount = st.number_input("Giảm giá (%):", min_value=0, max_value=100, value=0, step=5)
        
        final_price = int(total_price * (1 - discount / 100))

        st.markdown(f"### Tổng tiền: **{total_price:,} VNĐ**")
        if discount > 0:
            st.markdown(f"### Sau giảm giá ({discount}%): <span style='color:red'>{final_price:,} VNĐ</span>", unsafe_allow_html=True)

        # Nút Bấm Thanh Toán
        if st.button("💳 XÁC NHẬN THANH TOÁN", type="primary", use_container_width=True):
            st.session_state.invoice_paid = True
            st.balloons()

# ---------------------------------------------------------
# XUẤT HÓA ĐƠN KHI ĐÃ THANH TOÁN
# ---------------------------------------------------------
if st.session_state.get("invoice_paid") and st.session_state.cart:
    st.markdown("---")
    st.success("🎉 Thanh toán thành công! Dưới đây là hóa đơn chi tiết:")

    # Hiển thị hóa đơn trực quan
    invoice_box = st.container(border=True)
    with invoice_box:
        st.markdown("<h2 style='text-align: center; color: #FF4B4B;'>🧋 HÓA ĐƠN BÁN HÀNG - BOBA TEA</h2>", unsafe_allow_html=True)
        st.write(f"**Thời gian:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        st.write(f"**Khách hàng:** {customer_name if customer_name else 'Khách vãng lai'}")
        
        st.table(pd.DataFrame(st.session_state.cart)[["Tên món", "Size", "Đường", "Đá", "Topping", "Số lượng", "Thành tiền"]])
        
        c1, c2 = st.columns(2)
        with c1:
            st.write(f"**Tổng tiền món:** {total_price:,} VNĐ")
            st.write(f"**Giảm giá:** {discount}%")
            if selected_gift:
                st.write(f"**🎁 Quà tặng kèm:** {selected_gift}")
        with c2:
            st.markdown(f"### TỔNG CỦA BẠN: <span style='color:red'>{final_price:,} VNĐ</span>", unsafe_allow_html=True)

    # Chuẩn bị file tải về dạng TXT
    txt_data = create_txt_invoice(customer_name, st.session_state.cart, total_price, discount, final_price, selected_gift)
    
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            label="📥 Tải hóa đơn (.TXT)",
            data=txt_data,
            file_name=f"HoaDon_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    with col_dl2:
        if st.button("🔄 Tạo đơn hàng mới", use_container_width=True):
            st.session_state.cart = []
            st.session_state.invoice_paid = False
            st.rerun()
