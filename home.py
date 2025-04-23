import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame



def open_game(root):
    pygame.mixer.music.pause()
    root.withdraw()  # Ẩn cửa sổ chính

    # Gọi hàm chạy game
    two_player = False
    import ChessMain as ch
    ch.main(two_player)

    # Khi cửa sổ game đóng, hiện lại cửa sổ chính
    root.deiconify()
    pygame.mixer.init()
    pygame.mixer.music.load("musics/cuestiones-119653.mp3")
    pygame.mixer.music.play(-1)

def open_game_2player(root):
    pygame.mixer.music.pause()
    root.withdraw()  # Ẩn cửa sổ chính
    two_player = True


    # Gọi hàm chạy game
    import ChessMain as ch
    ch.main(two_player)

    # Khi cửa sổ game đóng, hiện lại cửa sổ chính
    root.deiconify()
    pygame.mixer.init()
    pygame.mixer.music.load("musics/cuestiones-119653.mp3")
    pygame.mixer.music.play(-1)


def exit_game(root):
    root.quit()


def on_enter(e):
    e.widget.config(bg="#555", fg="white")

def on_leave(e):
    e.widget.config(bg="#222", fg="white")

def main():
    pygame.mixer.init()
    pygame.mixer.music.load("musics/cuestiones-119653.mp3")
    pygame.mixer.music.play(-1)

    root = tk.Tk()
    root.title("HOME")
    width, height = 500, 500
    screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
    x, y = (screen_width - width) // 2, (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.resizable(False, False)


    image_path = "images/anhhome.png"
    bg_image = Image.open(image_path).resize((500, 500), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)


    canvas = tk.Canvas(root, width=500, height=500, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")


    btn_style = {
        "font": ("Arial", 14, "bold"),
        "bg": "#222",
        "fg": "white",
        "bd": 3,
        "relief": "raised",
        "width": 12,
        "height": 1
    }


    btn_play = tk.Button(root, text="Play", command=lambda: open_game(root), **btn_style)
    btn_play.bind("<Enter>", on_enter)
    btn_play.bind("<Leave>", on_leave)


    btn_2play = tk.Button(root, text="2 Players",command=lambda : open_game_2player(root), **btn_style)
    btn_2play.bind("<Enter>", on_enter)
    btn_2play.bind("<Leave>", on_leave)


    btn_exit = tk.Button(root, text="Exit", command=lambda: exit_game(root), **btn_style)
    btn_exit.bind("<Enter>", on_enter)
    btn_exit.bind("<Leave>", on_leave)


    canvas.create_window(250, 200, window=btn_play)
    canvas.create_window(250, 250, window=btn_2play)
    canvas.create_window(250, 300, window=btn_exit)

    root.mainloop()
if __name__ == "__main__":
    main()