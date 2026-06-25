import streamlit as st
import os
from PIL import Image

# Cấu hình giao diện trên điện thoại
st.set_page_config(page_title="Tra cứu Ảnh Phong Boutique", page_icon="👕", layout="centered")

# Đổi tiêu đề chính của app
st.title("👕 Tìm Kiếm Ảnh Thời Trang Phong Boutique")

# Markdown hướng dẫn người dùng bấm vào micro trên bàn phím
st.markdown("Nhập tên sản phẩm hoặc **bấm biểu tượng Micro trên bàn phím điện thoại** để nói.")

# Khung hướng dẫn chi tiết dành riêng cho điện thoại Samsung
st.info("📱 **Mẹo cho người dùng điện thoại Samsung:**\n\nNếu app không nhận diện được Tiếng Việt, với điện thoại Samsung tìm mục: **Bàn Phím Samsung** (thường là biểu tượng bánh răng ⚙️ trên bàn phím luôn) ➔ chọn mục **'Nhập bằng giọng nói'** ➔ chọn mục **'Nhập bằng giọng nói của Google'**.")

# Ô nhập liệu tìm kiếm (Text Input)
search_query = st.text_input("Gõ tên sản phẩm:", placeholder="Ví dụ: áo thun đen...")

# Hàm tìm TẤT CẢ ảnh khớp từ khóa ở cả THƯ MỤC GỐC và THƯ MỤC IMAGES
def find_all_product_images(query):
    # Khai báo các thư mục cần quét ảnh (Dấu "." là ngoài gốc, "images" là folder trong)
    folders_to_scan = [".", "images"]
    matched_images = []
    
    for image_folder in folders_to_scan:
        # Nếu thư mục tồn tại thì mới quét
        if os.path.exists(image_folder):
            for filename in os.listdir(image_folder):
                # Chỉ lấy các file ảnh
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    # Chuyển tên file về chữ thường để so sánh
                    name_without_ext = os.path.splitext(filename)[0].lower()
                    # Chuyển đổi dấu gạch ngang/gạch dưới thành khoảng trắng
                    normalized_filename = name_without_ext.replace("_", " ").replace("-", " ")
                    
                    # Nếu từ khóa có nằm trong tên file ảnh
                    if query.lower().strip() in normalized_filename:
                        full_path = os.path.join(image_folder, filename)
                        # Tránh trùng lặp ảnh nếu bạn lỡ up cùng 1 file ở cả trong lẫn ngoài
                        if full_path not in matched_images:
                            matched_images.append(full_path)
            
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
