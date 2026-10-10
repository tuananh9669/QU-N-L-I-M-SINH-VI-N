import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt

# Cố định random để bảng điểm không bị thay đổi liên tục mỗi khi tải lại trang web
random.seed(42)

# --- 1. XỬ LÝ DỮ LIỆU ---
ho_ten = ["Nguyễn Văn An", "Trần Thị Bình", "Lê Minh Cường", "Phạm Thị Dung", "Hoàng Văn Dũng",
          "Vũ Thị Hoa", "Đặng Minh Huy", "Bùi Thị Lan", "Đỗ Văn Nam", "Hồ Thị Phương"]

diem_chuyen_can = [random.randint(2, 10) for _ in range(len(ho_ten))]
diem_giua_ky = [random.randint(2, 10) for _ in range(len(ho_ten))]
diem_cuoi_ky = [random.randint(2, 10) for _ in range(len(ho_ten))]

df = pd.DataFrame({
    'Họ tên': ho_ten,
    'Chuyên cần': diem_chuyen_can,
    'Giữa kỳ': diem_giua_ky,
    'Cuối kỳ': diem_cuoi_ky
})

# Tính điểm tổng kết
df['Tổng kết'] = df['Chuyên cần'] * 0.2 + df['Giữa kỳ'] * 0.3 + df['Cuối kỳ'] * 0.5

# Thêm hàm và cột Xếp loại (yêu cầu của web)
def phan_loai(diem):
    if diem >= 8.5:
        return 'Giỏi'
    elif diem >= 7.0:
        return 'Khá'
    elif diem >= 5.0:
        return 'Trung bình'
    else:
        return 'Yếu'

df['Xếp loại'] = df['Tổng kết'].apply(phan_loai)


# --- 2. XÂY DỰNG GIAO DIỆN STREAMLIT ---
# Hiển thị tiêu đề
st.title("QUẢN LÝ ĐIỂM SINH VIÊN-")

# Hiển thị bảng điểm
st.subheader("1. Bảng điểm danh sách sinh viên")
st.dataframe(df, use_container_width=True)

# Hiển thị thống kê
st.subheader("2. Thống kê cơ bản")
diem_tb = df['Tổng kết'].mean()
vi_tri_max = df['Tổng kết'].idxmax()
vi_tri_min = df['Tổng kết'].idxmin()
so_sv_dat = (df['Tổng kết'] >= 5.0).sum()

st.write(f"- **Điểm trung bình của lớp:** {round(diem_tb, 2)}")
st.write(f"- **Sinh viên điểm cao nhất:** {df.loc[vi_tri_max, 'Họ tên']} ({df.loc[vi_tri_max, 'Tổng kết']} điểm)")
st.write(f"- **Sinh viên điểm thấp nhất:** {df.loc[vi_tri_min, 'Họ tên']} ({df.loc[vi_tri_min, 'Tổng kết']} điểm)")
st.write(f"- **Số sinh viên đạt (>= 5.0):** {so_sv_dat}")

# Tạo danh sách xổ xuống chọn sinh viên
st.subheader("3. Tra cứu chi tiết sinh viên")
sv_chon = st.selectbox("Chọn sinh viên để xem điểm:", df['Họ tên'])
info = df[df['Họ tên'] == sv_chon].iloc[0]

# Hiển thị thông tin sinh viên được chọn
st.info(
    f"**{info['Họ tên']}** - "
    f"Chuyên cần: {info['Chuyên cần']} | "
    f"Giữa kỳ: {info['Giữa kỳ']} | "
    f"Cuối kỳ: {info['Cuối kỳ']} 👉 "
    f"**Tổng kết: {info['Tổng kết']} ({info['Xếp loại']})**"
)

# Hiển thị biểu đồ cột
st.subheader("4. Biểu đồ điểm tổng kết")
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(df['Họ tên'], df['Tổng kết'], color='#4B8BBE', edgecolor='black')
ax.set_title('Biểu đồ Điểm Tổng Kết Của 10 Sinh Viên', fontsize=15, fontweight='bold')
ax.set_xlabel('Tên sinh viên', fontsize=12)
ax.set_ylabel('Điểm', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

st.pyplot(fig) # Lệnh của Streamlit để in đồ thị ra web

# Chân trang: Hiển thị tên và MSSV với kích thước nhỏ
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 12px; color: gray;'>"
    "Người tạo: Lê Công Tuấn Anh - MSSV: [033208005274]"
    "</p>", 
    unsafe_allow_html=True
)
