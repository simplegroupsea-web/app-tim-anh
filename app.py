import streamlit as st
import os
from PIL import Image
# Nhập thư viện Micro và Nhận diện giọng nói
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
from io import BytesIO

# Cấu hình giao diện trên điện thoại
st.set_page_config(page_title="Tra cứu Ảnh Sản Phẩm", page_icon="👗", layout="centered")

st.title("👗 Tìm Kiếm Ảnh Thời Trang")

# --- PHẦN 1: TÍCH HỢP NÚT MICRO TỰ ĐỘNG ---
st.markdown("---")
st.markdown("### 🎙️ Nhập bằng giọng nói (Google)")
st.markdown("Bấm nút 'Bấm để nói' bên dưới, nói tên sản phẩm (Tiếng Việt) và đợi trong giây giây để hệ thống tự nhập.")

# Biến để lưu kết quả giọng nói
spoken_text = ""

# Tạo nút Micro. Ngôn ngữ được cố định là vi-VN (Tiếng Việt)
audio = mic_recorder(
    start_prompt="👉 Bấm để nói",
    stop_prompt="⏹️ Bấm để dừng",
    key='recorder',
    use_container_width=True,
    language='vi-VN' # Cố định ngôn ngữ
)

# Xử lý khi có dữ liệu âm thanh
if audio:
    with st.spinner("Đang nhận diện giọng nói..."):
        try:
            # Lấy dữ liệu âm thanh từ trình duyệt
            audio_bytes = audio['bytes']
            
            # Khởi tạo bộ nhận diện
            r = sr.Recognizer()
            
            # Đọc dữ liệu âm thanh
            audio_file = BytesIO(audio_bytes)
            with sr.AudioFile(audio_file) as source:
                audio_data = r.record(source)
            
            # Gửi lên Google Speech Recognition API để chuyển thành văn bản
            # Cố định ngôn ngữ tiếng Việt (vi-VN)
            spoken_text = r.recognize_google(audio_data, language='vi-VN')
            st.success(f"🤖 Google nghe được: **{spoken_text}**")
            
        except sr.UnknownValueError:
            st.error("🤖 Google không nghe rõ. Vui lòng thử lại gần micro hơn!")
        except sr.RequestError as e:
            st.error(f"🤖 Lỗi kết nối dịch vụ Google: {e}")
        except Exception as e:
            st.error(f"⚠️ Đã có lỗi xảy ra: {e}")
            
st.markdown("---")


# --- PHẦN 2: LOGIC TÌM KIẾM ẢNH ---

# Ô nhập liệu tìm kiếm (sẽ tự điền nếu có giọng nói)
# Nếu spoken_text có giá trị, nó sẽ được dùng làm giá trị mặc định cho ô input
search_query = st.text_input("Gõ tên sản phẩm:", value=spoken_text, placeholder="Ví dụ: áo thun đen...")

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