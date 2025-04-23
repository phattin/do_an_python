from PIL import Image
import pygame as p

for i in range(1, 87 + 1):
    img=Image.open(f"transfer/transfer ({i}).png")
    img.save(f"transfer1/transfer1 ({i}).png", icc_profile=None)
print("Đã xử lý xong ảnh. File mới: output.png")
