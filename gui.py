import tkinter as tk
from tkinter import scrolledtext
import auto_sent_mess_fb
import threading

def on_button_click():
    # Lấy dữ liệu từ các ô text box
    user_name  = text_boxes[0].get()
    pass_word  = text_boxes[1].get()
    secret_2fa = text_boxes[2].get()
    country    = text_boxes[3].get()
    key_word  = text_boxes[4].get()
    mess_text  = text_editor.get("1.0", tk.END)

    if(user_name != "" and pass_word != "" and secret_2fa != "" and country != "" and key_word != "" and mess_text != ""):
        # Hiển thị thông báo
        message_label.config(text="Dữ liệu đã được lấy thành công!", fg="green")
        threading.Thread(target=worker_thread, args=(user_name, pass_word, secret_2fa, country, key_word, mess_text,)).start()
    else:
        message_label.config(text="Vui lòng nhập đủ thông tin", fg="red")

# Hàm chạy khi bạn đóng cửa sổ
def on_closing():
    global should_exit
    should_exit = True
    root.destroy()

def update_message(message, color):
    # Cập nhật thông báo trên GUI
    message_label.config(text=message, fg=color)

def worker_thread(user_name, pass_word, secret_2fa, country, key_word, mess_text):
    # Thực hiện công việc nặng nề ở đây
    print("ASdasdasdasdas", user_name, pass_word, secret_2fa, country, key_word, mess_text)
    auto_sent_mess_fb.run_auto(user_name, pass_word, secret_2fa, country, key_word, mess_text)

    # Sau khi hoàn thành công việc, cập nhật thông báo trên GUI
    root.after(0, lambda: update_message("Công việc nặng nề đã hoàn thành!", "blue"))

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Auto send messages for Facebook")

# Tạo nút bấm
button = tk.Button(root, text="RUN AUTO", command=on_button_click)
button.grid(row=0, column=1, pady=10)

# Tạo 5 ô text box và nhãn tương ứng
text_boxes = []

label = tk.Label(root, text=f"User Name:")
label.grid(row=1, column=0, padx=5, pady=5)

text_box = tk.Entry(root, width=50)  # Đặt chiều rộng của ô text box
text_box.grid(row=1, column=1, pady=5)
text_boxes.append(text_box)

label = tk.Label(root, text=f"Pass Word:")
label.grid(row=2, column=0, padx=5, pady=5)

text_box = tk.Entry(root, width=50)  # Đặt chiều rộng của ô text box
text_box.grid(row=2, column=1, pady=5)
text_boxes.append(text_box)

label = tk.Label(root, text=f"2FA Secret :")
label.grid(row=3, column=0, padx=5, pady=5)

text_box = tk.Entry(root, width=50)  # Đặt chiều rộng của ô text box
text_box.grid(row=3, column=1, pady=5)
text_boxes.append(text_box)

label = tk.Label(root, text=f"Country :")
label.grid(row=4, column=0, padx=5, pady=5)

text_box = tk.Entry(root, width=50)  # Đặt chiều rộng của ô text box
text_box.grid(row=4, column=1, pady=5)
text_boxes.append(text_box)

label = tk.Label(root, text=f"Key Word :")
label.grid(row=5, column=0, padx=5, pady=5)

text_box = tk.Entry(root, width=50)  # Đặt chiều rộng của ô text box
text_box.grid(row=5, column=1, pady=5)
text_boxes.append(text_box)

# Tạo ô soạn thảo văn bản và nhãn tương ứng
label_editor = tk.Label(root, text="Message:")
label_editor.grid(row=6, column=0, padx=5, pady=5)

text_editor = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=20)
text_editor.grid(row=6, column=1, pady=10)

# Khu vực thông báo
message_label = tk.Label(root, text="", fg="red")
message_label.grid(row=7, columnspan=2, pady=10)

# Chạy vòng lặp chính của GUI
root.mainloop()
