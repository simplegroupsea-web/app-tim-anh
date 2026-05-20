import streamlit as st
import os
from PIL import Image

# Cấu hình giao diện trên điện thoại (Đã đổi icon áo thun và tên tab)
st.set_page_config(page_title="Tra cứu Ảnh Phong Boutique", page_icon="👕", layout="centered")

# Đổi tiêu đề chính của app
st.title("👕 Tìm Kiếm Ảnh Thời Trang Phong Boutique")

# Markdown hướng dẫn người dùng bấm vào micro trên bàn phím
st.markdown("Nhập tên sản phẩm hoặc **bấm biểu tượng Micro trên bàn phím điện thoại** để nói.")

# Khung hướng dẫn chi tiết dành riêng cho điện thoại Samsung
st.info("📱 **Mẹo cho người dùng điện thoại Samsung:**\n\nNếu app không nhận diện được Tiếng Việt, với điện thoại Samsung tìm mục: **Bàn Phím Samsung** (thường là biểu tượng bánh răng ⚙️ trên bàn phím luôn) ➔ chọn mục **'Nhập bằng giọng nói'** ➔ chọn mục **'Nhập bằng giọng nói của Google'**.")

# Ô nhập liệu tìm kiếm (Text Input)
search_query = st.text_input("Gõ tên sản phẩm:", placeholder="Ví dụ: áo thun đen...")

# Hàm tìm TẤT CẢ ảnh khớp từ khóa trong thư mục images
def find_all_product_images(query):
    image_folder = "images"
    if not os.path.exists(image_folder):
        return []
    
    matched_images = []
    # Quét tất cả file trong thư mục images
    for filename in os.listdir(image_folder):
        # Chuyển tên file về chữ thường để so sánh
        name_without_ext = os.path.splitext(filename)[0].lower()
        # Chuyển đổi dấu gạch ngang/gạch dưới thành khoảng trắng trong tên file để dễ khớp
        normalized_filename = name_without_ext.replace("_", " ").replace("-", " ")
        
        # Nếu từ khóa có nằm trong tên file ảnh
        if query.lower().strip() in normalized_filename:
            matched_images.append(os.path.join(image_folder, filename))
            
    return matched_images

# Xử lý khi người dùng nhập thông tin
if search_query:
    image_paths = find_all_product_images(search_query)
    
    if len(image_paths) > 0:
        st.success(f"Đã tìm thấy **{len(image_paths)}** ảnh khớp với: **{search_query}**")
        
        # Chia giao diện thành 2 cột để hiển thị ảnh gọn gàng hơn
        cols = st.columns(2)
        
        for i, path in enumerate(image_paths):
            # Mở và hiển thị ảnh
            img = Image.open(path)
            # Hiển thị ảnh luân phiên vào cột trái/phải
            with cols[i % 2]:
                st.image(img, use_container_width=True) 
    else:
        st.error(f"Không tìm thấy ảnh sản phẩm cho từ khóa: **{search_query}**. Vui lòng thử từ khóa khác!")
