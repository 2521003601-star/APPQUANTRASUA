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
# 2. CUSTOM CSS GIAO DIỆN & BỘ MÔ PHỎNG LY NƯỚC
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
        background: rgba(255, 255, 255, 0.6);
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
        top: 25px;
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
# 3. KHO DỮ LIỆU
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

ALL_DRINKS = {item["name"]: item for season in SEASONS_MENU.values() for item in season}

SIZE_OPTIONS = {
    "S (Vừa)": {"price": 0, "height": "160px", "width": "110px", "fill": "70%"},
    "M (Lớn)": {"price": 5000, "height": "190px", "width": "125px", "fill": "82%"},
    "L (Đặc biệt)": {"price": 10000, "height": "220px", "width": "135px", "fill": "92%"}
}

SUGAR_LEVELS = {
    "100% (Bình thường)": {"opacity": "1.0", "label": "100% Đường"},
    "70%": {"opacity": "0.85", "label": "70% Đường"},
    "50%": {"opacity": "0.72", "label": "50% Đường"},
    "30%": {"opacity": "0.60", "label": "30% Đường"},
    "0% (Không đường)": {"opacity": "0.45", "label": "0% Đường"}
}

ICE_LEVELS = {
    "100% (Bình thường)": {"cubes": "🧊 🧊 🧊", "label": "100% Đá"},
    "70%": {"cubes": "🧊 🧊", "label": "70% Đá"},
    "50%": {"cubes": "🧊 🧊", "label": "50% Đá"},
    "30%": {"cubes": "🧊", "label": "30% Đá"},
    "0% (Không đá)": {"cubes": "", "label": "0% Đá"}
}

TOPPING_OPTIONS = {
    "Trân châu đen": {"price": 5000, "icon": "⚫⚫⚫"},
    "Trân châu trắng": {"price": 7000, "icon": "⚪⚪⚪"},
    "Thạch trái cây": {"price": 5000, "icon": "🟩🟨🟥"},
    "Pudding trứng": {"price": 8000, "icon": "🍮"},
    "Kem Cheese": {"price": 10000, "icon": "🧀"}
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
    season_tabs = st.tabs(list(SEASONS_MENU.keys()))
    
    for (s_name, items), tab_obj in zip(SEASONS_MENU.items(), season_tabs):
        with tab_obj:
            cols = st.columns(3)
            for idx, item in enumerate(items):
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
# TAB 4: MUA NGAY! (ĐÃ SỬA LỖI MÔ PHỎNG LY NƯỚC HTML/CSS)
# ---------------------------------------------------------
with nav_tabs[3]:
    st.header("🛍️ Mua Ngay!")
    col_order, col_visual = st.columns([1.2, 1.0])

    with col_order:
        st.subheader("FREESTYLE - Ly nước của bạn")
        
        selected_drink_name = st.selectbox("1. Chọn món nước yêu thích của bạn:", list(ALL_DRINKS.keys()))
        drink_info = ALL_DRINKS[selected_drink_name]
        
        selected_size = st.selectbox("2. Chọn Size:", list(SIZE_OPTIONS.keys()))
        
        c_sugar, c_ice = st.columns(2)
        with c_sugar:
            selected_sugar = st.selectbox("3. Mức đường:", list(SUGAR_LEVELS.keys()))
        with c_ice:
            selected_ice = st.selectbox("4. Mức đá:", list(ICE_LEVELS.keys()))
            
        selected_toppings = st.multiselect("Topping chọn thêm:", list(TOPPING_OPTIONS.keys()))
        quantity = st.number_input("5. Số lượng:", min_value=1, value=1, step=1)
        address = st.text_input("📍 Địa điểm chọn giao hàng:", placeholder="Nhập địa chỉ giao hàng...")

        base_price = drink_info["price"]
        size_price = SIZE_OPTIONS[selected_size]["price"]
        topping_price = sum(TOPPING_OPTIONS[t]["price"] for t in selected_toppings)
        unit_price = base_price + size_price + topping_price
        total_price = unit_price * quantity

        st.markdown(f"### 💰 Tổng tiền: **{total_price:,} VNĐ**")

        if st.button("💳 Bấm thanh toán bằng mã QR", type="primary", use_container_width=True):
            if not address:
                st.warning("Vui lòng nhập địa điểm giao hàng trước khi thanh toán!")
            else:
                st.success("Tạo đơn thành công! Vui lòng quét mã QR bên dưới để hoàn tất thanh toán:")
                qr_url = f"https://img.vietqr.io/image/MB-0000000000-compact2.png?amount={total_price}&addInfo=CoAndMay_{selected_drink_name}"
                st.image(qr_url, caption=f"Mã QR thanh toán: {total_price:,} VNĐ", width=260)

    # === CỘT MÔ PHỎNG LY NƯỚC ĐÃ SỬA LỖI XUẤT HTML ===
    with col_visual:
        st.subheader("🎨 Mô phỏng trực quan ly nước")
        
        cup_h = SIZE_OPTIONS[selected_size]["height"]
        cup_w = SIZE_OPTIONS[selected_size]["width"]
        fill_h = SIZE_OPTIONS[selected_size]["fill"]
        drink_color = drink_info["color"]
        sugar_op = SUGAR_LEVELS[selected_sugar]["opacity"]
        ice_cubes = ICE_LEVELS[selected_ice]["cubes"]
        
        has_cheese = "Kem Cheese" in selected_toppings
        bottom_toppings = [TOPPING_OPTIONS[t]["icon"] for t in selected_toppings if t != "Kem Cheese"]
        topping_html = " ".join(bottom_toppings) if bottom_toppings else ""
        cheese_html = '<div class="cheese-foam"></div>' if has_cheese else ''
        ice_html = f'<div class="ice-cubes">{ice_cubes}</div>' if ice_cubes else ''

        # Ghép chuỗi HTML rõ ràng, chuẩn định dạng
        visual_html = f"""
        <div class="visualizer-container">
            <div class="boba-cup" style="height: {cup_h}; width: {cup_w};">
                <div class="straw"></div>
                {ice_html}
                <div class="boba-liquid" style="height: {fill_h}; background-color: {drink_color}; opacity: {sugar_op};">
                    {cheese_html}
                </div>
                <div class="topping-layer">{topping_html}</div>
            </div>
            <div style="margin-top: 25px; text-align: center;">
                <span class="spec-tag">Size {selected_size.split()[0]}</span>
                <span class="spec-tag">{SUGAR_LEVELS[selected_sugar]['label']}</span>
                <span class="spec-tag">{ICE_LEVELS[selected_ice]['label']}</span>
            </div>
        </div>
        """
        st.markdown(visual_html, unsafe_allow_html=True)

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
