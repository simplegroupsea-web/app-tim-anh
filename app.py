import streamlit as st
import os
from PIL import Image

# Cấu hình giao diện trên điện thoại
st.set_page_config(page_title="Tra cứu Ảnh Sản Phẩm", page_icon="👗", layout="centered")

st.title("👗 Tìm Kiếm Ảnh Thời Trang")
st.markdown("Nhập tên sản phẩm hoặc **bấm biểu tượng Micro trên bàn phím điện thoại** để nói.")

# Ô nhập liệu tìm kiếm
search_query = st.text_input("Gõ tên sản phẩm:", placeholder="Ví dụ: áo thun đen...")

# Hàm tìm TẤT CẢ ảnh khớp từ khóa trong thư mục
def find_all_product_images(query):
    image_folder = "images"
    if not os.path.exists(image_folder):
        return []
    
    matched_images = []
    # Quét tất cả file trong thư mục images
    for filename in os.listdir(image_folder):
        name_without_ext = os.path.splitext(filename)[0].lower()
        # Nếu từ khóa có nằm trong tên file ảnh thì gom lại
        if query.lower().strip() in name_without_ext.replace("_", " "):
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
            img = Image.open(path)
            # Hiển thị ảnh luân phiên vào cột trái/phải
            with cols[i % 2]:
                st.image(img, use_container_width=True) 
    else:
        st.error("Không tìm thấy ảnh sản phẩm này trong kho. Vui lòng thử từ khóa khác!")