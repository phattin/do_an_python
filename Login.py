import tkinter as tk
from tkinter import messagebox
import mysql.connector
from PIL import Image, ImageTk
import home as h


# Kết nối MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="users_db"
)
cursor = conn.cursor()

# Hàm kiểm tra đăng nhập
def login():
    username = entry_username.get().strip()
    password = entry_password.get().strip()

    if not username or not password:
        messagebox.showerror("Lỗi", "Tên đăng nhập và mật khẩu không được để trống!")
        return

    query = "SELECT * FROM users WHERE user_name=%s AND pass=%s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()

    if user:
        messagebox.showinfo("Thành công", "Đăng nhập thành công!")
        root.destroy()
        open_home()
    else:
        messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu!")

# Hàm đăng ký
def register():
    username = entry_username.get().strip()
    password = entry_password.get().strip()

    if not username or not password:
        messagebox.showerror("Lỗi", "Tên đăng nhập và mật khẩu không được để trống!")
        return

    try:
        query = "INSERT INTO users (user_name, pass) VALUES (%s, %s)"
        cursor.execute(query, (username, password))
        conn.commit()
        messagebox.showinfo("Thành công", "Đăng ký thành công! Hãy đăng nhập.")
    except mysql.connector.IntegrityError:
        messagebox.showerror("Lỗi", "Tên người dùng đã tồn tại!")

def open_home():
    h.main()

# Cấu hình cửa sổ
root = tk.Tk()
root.title("Đăng nhập")
width = 500
height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - width) // 2
y = (screen_height - height) // 2
root.geometry(f"{width}x{height}+{x}+{y}")
root.resizable(False, False)

# Load ảnh nền
image_path = "images/anhnen.png"
bg_image = Image.open(image_path)
bg_image = bg_image.resize((500, 500), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Hiển thị ảnh nền trên canvas
canvas = tk.Canvas(root, width=500, height=500, highlightthickness=0)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Vẽ chữ lên canvas
canvas.create_text(180, 180, text="Tên đăng nhập:", font=("Arial", 14), fill="white", anchor="e")
canvas.create_text(180, 230, text="Mật khẩu:", font=("Arial", 14), fill="white", anchor="e")

# Tạo ô nhập liệu (trong suốt)
entry_username = tk.Entry(root, font=("Arial", 14), fg="white", insertbackground="white", bg="#222222", highlightthickness=0, bd=0)
entry_password = tk.Entry(root, font=("Arial", 14), fg="white", insertbackground="white", bg="#222222", highlightthickness=0, bd=0, show="*")

# Đặt ô nhập lên canvas
canvas.create_window(200, 180, window=entry_username, width=200, height=30, anchor="w")
canvas.create_window(200, 230, window=entry_password, width=200, height=30, anchor="w")

# Nút đăng nhập và đăng ký
btn_login = tk.Button(root, text="Đăng nhập", font=("Arial", 12), command=login)
btn_register = tk.Button(root, text="Đăng ký", font=("Arial", 12), command=register)

canvas.create_window(250, 280, window=btn_login, width=100, height=30)
canvas.create_window(250, 320, window=btn_register, width=100, height=30)

root.mainloop()

cursor.close()
conn.close()
