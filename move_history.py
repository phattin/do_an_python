import tkinter as tk
from tkinter import scrolledtext

class MoveHistoryWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Lịch sử nước đi")
        self.root.geometry("250x500+180+80")
        self.root.overrideredirect(True)  # Ẩn thanh tiêu đề gốc

        self.is_collapsed = False  # Trạng thái thu gọn

        # Thanh tiêu đề tùy chỉnh
        title_bar = tk.Frame(self.root, bg="gray", relief='raised', bd=2)
        title_bar.pack(fill=tk.X)

        # Nút thu gọn/mở rộng
        self.toggle_btn = tk.Label(title_bar, text="⏵", bg="gray", fg="white", cursor="hand2", font=("Arial", 12))
        self.toggle_btn.pack(side=tk.RIGHT, padx=5)
        self.toggle_btn.bind("<Button-1>", lambda e: self.toggle_body())

        # Tiêu đề
        title_label = tk.Label(title_bar, text=" Lịch sử nước đi", bg="gray", fg="white", font=("Consolas", 10, "bold"))
        title_label.pack(side=tk.LEFT, padx=5)

        # Kéo cửa sổ
        def start_move(event):
            self.x = event.x
            self.y = event.y

        def do_move(event):
            x = event.x_root - self.x
            y = event.y_root - self.y
            self.root.geometry(f"+{x}+{y}")

        title_bar.bind("<Button-1>", start_move)
        title_bar.bind("<B1-Motion>", do_move)

        # Vùng hiển thị nước đi
        self.body_frame = tk.Frame(self.root)
        self.body_frame.pack(fill=tk.BOTH, expand=True)

        self.history_box = scrolledtext.ScrolledText(self.body_frame, width=30, height=30, font=("Consolas", 10))
        self.history_box.pack(padx=10, pady=10)

    def toggle_body(self):
        if self.is_collapsed:
            self.body_frame.pack(fill=tk.BOTH, expand=True)
            self.toggle_btn.config(text="⏵")
            self.root.geometry("250x500+180+80")
        else:
            self.body_frame.forget()
            self.toggle_btn.config(text="⏷")  # Đổi hướng mũi tên khi gấp
            self.root.geometry("250x50+180+80")
        self.is_collapsed = not self.is_collapsed

    def add_move(self, move_str, move):
        color = "Trắng" if move.pieceMoved.startswith("w") else "Đen"
        self.history_box.insert(tk.END, f" {move_str}\n")
        self.history_box.see(tk.END)

    def remove_last_move(self):
        """Xoá nước đi cuối cùng khỏi hộp văn bản."""
        history = self.history_box.get("1.0", tk.END).strip().split("\n")
        if history:
            self.history_box.delete("1.0", tk.END)  
            new_history = history[:-1]  
            for line in new_history:
                self.history_box.insert(tk.END, line + "\n")
            self.history_box.see(tk.END)
    #move_window.remove_last_move() xóa cuối

    def update(self):
        self.root.update()
