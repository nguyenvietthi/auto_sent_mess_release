import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import auto_sent_mess_fb
import threading
import mysql.connector
from time import sleep

status_string = dict()
status_string[0] = "Chưa Xử Lý"
status_string[1] = "Sai Mật Khẩu"
status_string[2] = "Đang Rải"
status_string[3] = "Bị Chặn"
status_string[4] = "Login Fail"
status_string[5] = "Couldn't send"
status_string[6] = "956 or 282"


def get_via(path):
    via_list = []
    f = open(path, "r")
    for via in f.read().split("\n"):
        via_list.append(via.split(" "))
    return via_list

def on_button_click():
    # Lấy dữ liệu từ các ô text box
    via_list = get_via(file_path_entry.get())
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="scan_page"
    )
    sql_updat = f"UPDATE via SET status = 0 WHERE via_id < {len(via_list)}"
    mycursor = mydb.cursor()
    mycursor.execute(sql_updat)
    mydb.commit()

    print(via_list)
    add_data_to_table(via_list)
    country    = text_boxes[0].get()
    key_word   = text_boxes[1].get()
    mess_text  = text_editor.get("1.0", tk.END)

    if(len(via_list) > 0 and country != "" and key_word != "" and mess_text != ""):
        # Hiển thị thông báo
        message_label.config(text="Dữ liệu đã được lấy thành công!", fg="green")
        threading.Thread(target=worker_thread, args=(via_list, country, key_word, mess_text)).start()
        threading.Thread(target=get_status, args=(via_list,)).start()
        button.configure(state="disabled", text="Mở tool khác, tắt cái này")
    else:
        message_label.config(text="Vui lòng nhập đủ thông tin", fg="red")

def on_closing():
    global should_exit
    should_exit = True
    root.destroy()

def update_message(message, color):
    message_label.config(text=message, fg=color)

def get_status(via_list):
    while(True):
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        database="scan_page"
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM via")
        myresult = mycursor.fetchall()
        print(myresult, len(myresult))
        tree.delete(*tree.get_children())

        for idx, via in enumerate(via_list):
            viatmp = list(via)
            viatmp.append(status_string[myresult[idx][1]])
            tree.insert('', 'end', values=viatmp)
        sleep(5)

def worker_thread(acc_list, country, key_word, mess_text):
    # Thực hiện công việc nặng nề ở đây
    print(country, key_word, mess_text)
    auto_sent_mess_fb.run_multi_acc(acc_list, country, key_word, mess_text)

    # Sau khi hoàn thành công việc, cập nhật thông báo trên GUI
    root.after(0, lambda: update_message("Công việc nặng nề đã hoàn thành!", "blue"))

def add_data_to_table(via_list):
    tree.delete(*tree.get_children())

    for via in via_list:
        viatmp = list(via)
        viatmp.append("Chưa Xử Lý")
        tree.insert('', 'end', values=viatmp)

def browse_file():
    # Hiển thị hộp thoại chọn file và lấy đường dẫn
    file_path = filedialog.askopenfilename()
    
    # Hiển thị đường dẫn lên Entry
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, file_path)

root = tk.Tk()
root.title("Auto send messages for Facebook")

# Tạo nút bấm
button = tk.Button(root, text="RUN AUTO", command=on_button_click)
button.grid(row=0, column=1, pady=10)

# Tạo 5 ô text box và nhãn tương ứng
text_boxes = []

label = tk.Label(root, text=f"Via File:")
label.grid(row=1, column=0, padx=5, pady=5)

file_path_entry = tk.Entry(root, width=50)
file_path_entry.grid(row=1, column=1, pady=5)

browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.grid(row=1, column=2, pady=5)

label = tk.Label(root, text=f"Country :")
label.grid(row=4, column=0, padx=5, pady=5)

text_box = tk.Entry(root, width=50)
text_box.grid(row=4, column=1, pady=5)
text_boxes.append(text_box)

label = tk.Label(root, text=f"Key Word :")
label.grid(row=5, column=0, padx=5, pady=5)

text_box = tk.Entry(root, width=50)
text_box.grid(row=5, column=1, pady=5)
text_boxes.append(text_box)

# Tạo ô soạn thảo văn bản và nhãn tương ứng
label_editor = tk.Label(root, text="Message:")
label_editor.grid(row=6, column=0, padx=5, pady=5)

text_editor = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=5)
text_editor.grid(row=6, column=1, pady=10)

# Khu vực thông báo
message_label = tk.Label(root, text="", fg="red")
message_label.grid(row=7, columnspan=2, pady=10)

# Tạo bảng
tree = ttk.Treeview(root, columns=('User Name', 'Password', "2FA", 'Trạng Thái'), show='headings', height=30)
tree.grid(row=8, columnspan=2, pady=10)

# Đặt tên cho các cột và đặt chiều rộng
columns = ['User Name', 'Password', '2FA', 'Trạng Thái']
column_widths = [150, 150, 250, 100]

for col, width in zip(columns, column_widths):
    tree.heading(col, text=col)
    tree.column(col, width=width)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
