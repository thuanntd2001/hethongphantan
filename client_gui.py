import tkinter as tk
import tkinter.messagebox as messagebox
from tooltip import ToolTip
from dsystem import Client
import socket
import threading

def refresh_status_label():
    states = {0: 'Chưa có gì', 1: 'Đang đợi', 2: 'Đã cho phép'}
    status_label.config(text="Trạng thái: " + states[client.status])

def close_button_click():
    window.destroy()

def __license():
    try:
        host = host_text.get("1.0", 'end-1c')
        port = int(port_text.get("1.0", 'end-1c'))
        client.config((host, port))
        status_label.config(text="Trạng thái: Đang đợi ...")
        client.license()
    except Exception:
        messagebox.showerror(title="Lỗi", message=str("Yêu cầu không hợp lệ"))

    refresh_status_label()

def __release():
    try:
        host = host_text.get("1.0", 'end-1c')
        port = int(port_text.get("1.0", 'end-1c'))
        client.config((host, port))
        status_label.config(text="Trạng thái: Đang đợi ...")
        client.release()
    except Exception:
        messagebox.showerror(title="Lỗi", message=str("Yêu cầu không hợp lệ"))

    refresh_status_label()

def license_button_click():
    global thread
    if (thread.is_alive()):
        messagebox.showerror(title="Lỗi", message="Từ chối yêu cầu, đang đợi phản hồi từ máy chủ")
        return

    thread = threading.Thread(target=__license)
    thread.start()

def release_button_click():
    global thread
    if (thread.is_alive()):
        messagebox.showerror(title="Lỗi", message="Từ chối yêu cầu, đang đợi phản hồi từ máy chủ")
        return

    thread = threading.Thread(target=__release)
    thread.start()

client = Client()
thread = threading.Thread()

# Gui
window = tk.Tk()
window.title("Máy khách | " + client.get_ip())
window.geometry('400x300')

# Input Host
host_label = tk.Label(text="Máy chủ")
host_text = tk.Text(height=1)

# Input Port
port_label = tk.Label(text="Cổng")
port_text = tk.Text(height=1)

# Request button
license_button = tk.Button(text="Yêu cầu truy cập", width=16, command=license_button_click)

# Request button
release_button = tk.Button(text="Ngưng truy cập", width=16, command=release_button_click)

# Close button
close_button = tk.Button(text="Đóng", width=16, command=close_button_click)

# Status label
status_label = tk.Label(text="Trạng thái: Chưa có gì")

host_label.pack(padx=5, anchor="w")
host_text.pack(padx=5, pady=5)
port_label.pack(padx=5, anchor="w")
port_text.pack(padx=5, pady=5)

license_button.pack(padx=5, pady=5)
release_button.pack(padx=5, pady=5)
close_button.pack(padx=5, pady=5)

status_label.pack(side=tk.BOTTOM, padx=5, pady=5)

window.mainloop()
