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
# 2. CUSTOM CSS GIAO DIỆN & MÔ PHỎNG LY NƯỚC ĐỘNG
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

    /* Hiển thị ly nước mô phỏng kiểu Oatside nâng cấp */
    .boba-cup {
        width: 140px;
        height: 200px;
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
    /* Icon Đá rơi phía trên */
    .boba-ice {
        position: absolute;
        top: 20px;
        width: 100%;
        text-align: center;
        font-size: 16px;
        z-index: 6;
        user-select: none;
    }
    /* Icon Topping xếp đáy ly */
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

# Bản đồ quy đổi Đá thành Icon viên đá
ICE_ICON_MAP = {
    "0%": "",
    "30%": "🧊🧊 🧊 🧊",
    "50%": "🧊 🧊🧊 🧊 🧊 🧊🧊🧊 🧊 🧊 🧊 🧊🧊",
    "100%": "🧊 🧊 🧊🧊 🧊 🧊🧊 🧊 🧊🧊🧊🧊 🧊 🧊 🧊 🧊 🧊 🧊🧊 🧊 🧊🧊"
}

# Bản đồ quy đổi Topping thành Icon
TOPPING_ICON_MAP = {
    "Trân châu đen": "⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫",
    "Pudding trứng": "🍮🍮🍮🍮🍮",
    "Kem Cheese": "🧀🧀🧀🧀🧀🧀"
}

BOOKS_LIST = [
    {"title": "Kiêu Hãnh và Định Kiến", "img": "28.jpg"},
    {"title": "Những Người Khốn Khổ", "img": "29.jpg"},
    {"title": "Hoàng Tử Bé", "img": "30.jpg"},
    {"title": "Mắt Biếc", "img": "31.jpg"},
    {"title": "Còn Chút Gì Để Nhớ", "img": "32.jpg"},
    {"title": "Tôi Thấy Hoa Vàng Trên Cỏ Xanh", "img": "33.jpg"},
    {"title": "Cho Tôi Xin Một Vé Đi Tuổi Thơ", "img": "34.jpg"},
    {"title": "Nữ Sinh", "img": "35.jpg"},
]

MUSIC_LIST = [
    {"title": "Xúc Cảm Bộ Máy", "artist": "Cá Hồi Hoang ‧ 2023", "img": "36.jpg"},
    {"title": "Cho tôi đi theo", "artist": "Ngọt ‧ 2016", "img": "37.jpg"},
    {"title": "Điền vào ô trống (250)", "artist": "Cá Hồi Hoang ‧ 2018", "img": "38.jpg"},
    {"title": "HIỆN THỰC PHŨ PHÀNG", "artist": "Phùng Khánh Linh ‧ 2025", "img": "39.jpg"},
    {"title": "Thu Gọi", "artist": "Mạc Mai Sương ‧ 2023", "img": "40.jpg"},
    {"title": "nhớ ( mỗi tên anh thôi )", "artist": "gia x The Odo ‧ 2020", "img": "40.jpg"},
]

# ---------------------------------------------------------
# 4. THANH ĐIỀU HƯỚNG TRÊN CÙNG
# ---------------------------------------------------------
st.markdown("""
<div class="brand-header">
    <h1 style="margin:0; font-size: 2.3rem;">🍃 CỎ & MÂY COFFEE ☁️</h1>
    <p style="margin:5px 0 0 0; font-style: italic;">"Cỏ giữ chân bạn lại với sự ấm áp, Mây nâng tâm hồn bạn lên với sự nhẹ nhõm."</p>
</div>
""", unsafe_allow_html=True)

nav_tabs = st.tabs([
    "🍹 Menu Theo Mùa", 
    "📍 Vị Trí Quán", 
    "📖 Về Chúng Tôi", 
    "🛍️ Mua Ngay!", 
    "📚 Tủ Sách Của CỎ", 
    "🎶 Bản Nhạc Của MÂY"
])

# ---------------------------------------------------------
# TAB 1: MENU THEO MÙA
# ---------------------------------------------------------
with nav_tabs[0]:
    st.header("🍹 Menu Thức Uống Theo Mùa")
    
    st_xuan, st_ha, st_thu, st_dong = st.tabs(["🌸 Mùa Xuân", "☀️ Mùa Hạ", "🍂 Mùa Thu", "❄️ Mùa Đông"])
    
    with st_xuan:
        cols = st.columns(3)
        for idx, item in enumerate(SEASONS_MENU["Mùa Xuân"]):
            with cols[idx % 3]:
                st.markdown("<div class='menu-card'>", unsafe_allow_html=True)
                st.image(item["img"], caption=f"{item['name']} - {item['price']:,} VNĐ", use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

    with st_ha:
        cols = st.columns(3)
        for idx, item in enumerate(SEASONS_MENU["Mùa Hạ"]):
            with cols[idx % 3]:
                st.markdown("<div class='menu-card'>", unsafe_allow_html=True)
                st.image(item["img"], caption=f"{item['name']} - {item['price']:,} VNĐ", use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

    with st_thu:
        cols = st.columns(3)
        for idx, item in enumerate(SEASONS_MENU["Mùa Thu"]):
            with cols[idx % 3]:
                st.markdown("<div class='menu-card'>", unsafe_allow_html=True)
                st.image(item["img"], caption=f"{item['name']} - {item['price']:,} VNĐ", use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

    with st_dong:
        cols = st.columns(3)
        for idx, item in enumerate(SEASONS_MENU["Mùa Đông"]):
            with cols[idx % 3]:
                st.markdown("<div class='menu-card'>", unsafe_allow_html=True)
                st.image(item["img"], caption=f"{item['name']} - {item['price']:,} VNĐ", use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 2: VỊ TRÍ QUÁN
# ---------------------------------------------------------
with nav_tabs[1]:
    st.header("📍 Vị Trí Quán Cỏ & Mây")
    st.subheader("🏠 Địa chỉ: 306 Võ Văn Hát, phường Long Trường, TPHCM")
    st.image("25.jpg", caption="Bản đồ chỉ đường tới quán Cỏ & Mây (25.jpg)", use_container_width=True)

# ---------------------------------------------------------
# TAB 3: VỀ CHÚNG TÔI
# ---------------------------------------------------------
with nav_tabs[2]:
    st.header("📖 Về Chúng Tôi")
    sub_tab1, sub_tab2 = st.tabs(["💼 Cơ Hội Nghề Nghiệp", "✨ Câu Chuyện Thương Hiệu"])
    
    with sub_tab1:
        col_logo, col_text = st.columns([1, 2])
        with col_logo:
            st.image("26.jpg", caption="Logo CỎ & MÂY (26.jpg)", use_container_width=True)
        with col_text:
            st.write("""
            **"CỎ & MÂY"** đang tìm kiếm những ứng viên có thể giao tiếp bằng hai ngôn ngữ Việt Anh, 
            có niềm đam mê lớn trong ngành kinh doanh luôn tìm hiểu và đáp ứng nhu cầu khách hàng, 
            yêu thích làm việc nhóm, không quản ra về muộn và đi làm sớm; những bạn trẻ hiểu được rằng 
            sự cố gắng sẽ được tưởng thưởng xứng đáng không chỉ bằng thu nhập tốt mà còn bằng cơ hội phát triển 
            nghề nghiệp một cách chuyên nghiệp; những ứng viên có tình yêu lớn đối với cà phê và lịch sử của nó, 
            quan trọng hơn nữa là có tinh thần học hỏi cao và một tâm hồn rộng mở.
            
            Hãy đến với chúng tôi, **CỎ & MÂY** sẽ cùng bạn đi trên con đường phát triển một sự nghiệp bền vững 
            và cho bạn thấy cách chúng tôi giao hòa giữa **Trách Nhiệm Cộng Đồng, Sự Cam Kết, và Lòng Nhiệt Thành** 
            trong một Công ty tuyệt vời như CỎ & MÂY.
            """)
            st.markdown("### 📋 Các vị trí tuyển dụng gần đây:")
            st.markdown("""
            - ☕ Vị trí chuyên viên pha chế cà phê
            - 👥 Vị trí Quản lý nhóm
            - 🤝 Vị trí Trợ lý Quản lý quán
            - 🌐 Quản lý khu vực
            """)

    with sub_tab2:
        col_img, col_story = st.columns([1, 2])
        with col_img:
            st.image("27.jpg", caption="Hình ảnh thương hiệu (27.jpg)", use_container_width=True)
        with col_story:
            st.write("""
            Có một định luật rất lạ của tự nhiên: **Cỏ** luôn bám chặt vào mặt đất, cần mẫn xanh tươi dẫu có bao bước chân qua; 
            còn **Mây** lại thong thả bay lượn ở bầu trời cao, chẳng bận tâm đến ngày tháng. 
            Cỏ đại diện cho thực tại, cho những nhọc nhằn, bận rộn và đôi chân phải chạm đất mỗi ngày. 
            Mây đại diện cho ước mơ, cho sự tự do và những khoảng trời thả lỏng trong tâm trí.
            
            **CỎ & MÂY** ra đời từ một ý niệm rất đỗi mềm mại: Nơi mà bạn không cần phải chọn giữa việc *"phải cố gắng"* và *"được nghỉ ngơi"*. 
            Bạn có thể bước vào đây với đôi giày còn dính bụi đường (như ngọn cỏ), chọn một góc ngồi thật êm, ngước nhìn ly cà phê thơm 
            và để tâm hồn được bay bổng đôi chút (như áng mây). Cỏ giữ chân bạn lại với sự ấm áp, Mây nâng tâm hồn bạn lên với sự nhẹ nhõm.
            """)

# ---------------------------------------------------------
# TAB 4: MUA NGAY! (ĐÃ CẬP NHẬT HIỂN THỊ ĐÁ & ĐA TOPPING)
# ---------------------------------------------------------
with nav_tabs[3]:
    st.header("🛍️ Mua Ngay!")
    col_order, col_visual = st.columns([1.2, 1.0])

    with col_order:
        st.subheader("FREESTYLE - Ly nước của bạn")
        
        # 1. Chọn món
        selected_drink_name = st.selectbox("1. Chọn món nước yêu thích của bạn:", list(ALL_DRINKS.keys()))
        drink_info = ALL_DRINKS[selected_drink_name]
        
        # 2. Chọn size
        size_choice = st.radio("2. Chọn Size:", ["S (Vừa)", "M (Lớn)", "L (Đặc biệt)"], horizontal=True)
        
        # 3. Mức đường & 4. Mức đá
        c_sugar, c_ice = st.columns(2)
        with c_sugar:
            sugar_choice = st.selectbox("3. Mức đường:", ["100%", "70%", "50%", "30%", "0%"])
        with c_ice:
            ice_choice = st.select_slider("4. Mức đá:", options=["0%", "30%", "50%", "100%"])
            
        topping_choice = st.multiselect("Topping chọn thêm:", ["Trân châu đen", "Pudding trứng", "Kem Cheese"])
        quantity = st.number_input("5. Số lượng:", min_value=1, value=1, step=1)
        address = st.text_input("📍 Địa điểm chọn giao hàng:", placeholder="Nhập địa chỉ giao hàng...")

        # Tính toán giá tiền
        size_extra = 0 if "S" in size_choice else (5000 if "M" in size_choice else 10000)
        topping_extra = len(topping_choice) * 5000
        unit_price = drink_info["price"] + size_extra + topping_extra
        total_price = unit_price * quantity

        st.markdown(f"### 💰 Tổng tiền: **{total_price:,} VNĐ**")

        if st.button("💳 Bấm thanh toán bằng mã QR", type="primary", use_container_width=True):
            if not address:
                st.warning("Vui lòng nhập địa điểm giao hàng trước khi thanh toán!")
            else:
                st.success("Tạo đơn thành công! Vui lòng quét mã QR bên dưới để hoàn tất thanh toán:")
                qr_url = f"https://img.vietqr.io/image/MB-0000000000-compact2.png?amount={total_price}&addInfo=CoAndMay_{selected_drink_name}"
                st.image(qr_url, caption=f"Mã QR thanh toán: {total_price:,} VNĐ", width=260)

    # === CỘT MÔ PHỎNG LY NƯỚC (HIỂN THỊ ĐẦY ĐỦ ĐÁ VÀ TẤT CẢ TOPPING) ===
    with col_visual:
        st.markdown("<h4 style='text-align:center;'>Mô phỏng Ly của bạn</h4>", unsafe_allow_html=True)
        
        liquid_height = HEIGHT_MAP.get(size_choice, "70%")
        liquid_color = drink_info["color"]
        
        # 1. Ghép tất cả các Icon Topping được chọn
        topping_icons = [TOPPING_ICON_MAP[t] for t in topping_choice if t in TOPPING_ICON_MAP]
        topping_display = " ".join(topping_icons)
        
        # 2. Lấy Icon Đá tương ứng mức %
        ice_display = ICE_ICON_MAP.get(ice_choice, "")

        cup_html = f"""
        <div class="boba-cup">
            <div class="boba-ice">{ice_display}</div>
            <div class="boba-liquid" style="height: {liquid_height}; background-color: {liquid_color};"></div>
            <div class="boba-topping">{topping_display}</div>
        </div>
        <p style="text-align:center; margin-top: 15px;">
            <b>Size {size_choice.split()[0]} | Đường {sugar_choice} | Đá {ice_choice}</b>
        </p>
        """
        st.markdown(cup_html, unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 5: TỦ SÁCH CỦA CỎ
# ---------------------------------------------------------
with nav_tabs[4]:
    st.header("📚 Tủ Sách Của CỎ")
    cols_books = st.columns(4)
    for idx, book in enumerate(BOOKS_LIST):
        with cols_books[idx % 4]:
            st.markdown("<div class='menu-card'>", unsafe_allow_html=True)
            st.image(book["img"], caption=book["title"], use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
    st.markdown("""
    <div class="footer-quote">
        CÁC BẠN HÃY GHÉ CỎ & MÂY ĐỂ THƯỞNG THỨC NHỮNG BỘ SÁCH HAY NHÉ ^^ !
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 6: BẢN NHẠC CỦA MÂY
# ---------------------------------------------------------
with nav_tabs[5]:
    st.header("🎶 Bản Nhạc Của MÂY")
    cols_music = st.columns(3)
    for idx, song in enumerate(MUSIC_LIST):
        with cols_music[idx % 3]:
            st.markdown("<div class='menu-card'>", unsafe_allow_html=True)
            st.image(song["img"], caption=f"{song['title']} \n ({song['artist']})", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
    st.markdown("""
    <div class="footer-quote">
        CÁC BẠN HÃY GHÉ CỎ & MÂY ĐỂ THƯỞNG THỨC NHỮNG BẢN NHẠC HAY NHÉ ^^ !
    </div>
    """, unsafe_allow_html=True)
