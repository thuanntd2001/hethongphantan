import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from tooltip import ToolTip
from dsystem import Server
import socket
import threading

def close_button_click():
    window.destroy()

def licensed_client_on_changed(server, client):
    if client == None:
       
        licensed_client_label.config(text="Clients được cấp phép: Chưa có ai" ,font=("Arial", 8, "bold"), fg="black", bg="white")
        return

    licensed_client_label.config(text="Clients được cấp phép: " + client[0][0],font=("Arial", 8, "bold"), fg="black", bg="white")

def waiting_clients_on_changed(server, waiting_list):
    for i in waiting_clients_list.get_children():
        waiting_clients_list.delete(i)

    for client in waiting_list:
        waiting_clients_list.insert(parent='', index='end', text='', values=(client[0][0], str(client[0][1])))

def logs_on_changed(server, log):
    logs_list.insert(parent='', index='end', text='', values=(log[0], str(log[1])))


def run_server():
    server.run(waiting_clients_on_changed=waiting_clients_on_changed,
            licensed_client_on_changed=licensed_client_on_changed,
            logs_on_changed=logs_on_changed)

host = "0.0.0.0"
port = 6969
server = Server((host, port))
thread = threading.Thread(target=run_server)
thread.start()

# Gui
window = tk.Tk()
window.title("Máy chủ")
window.geometry('800x625')
window.configure(bg="green")
# XIN CHÀO
hello_client_label= tk.Label(text="Xin chào máy chủ: " + server.get_ip(), font=("Arial", 18), fg="blue", bg="yellow")
#  licensed_client label
licensed_client_label = tk.Label(text="Clients được cấp phép: Chưa có ai",font=("Arial", 8, "bold"), fg="black", bg="white")

#  Waiting clients label
waiting_clients_label = tk.Label(text="Đang chờ Clients",font=("Arial", 10, "bold"), bg="pink")

# Waiting clients
waiting_clients_list = ttk.Treeview()
waiting_clients_list['columns'] = ("Địa chỉ IP", "Cổng port")

waiting_clients_list.column("#0", width=0, stretch=tk.NO)
waiting_clients_list.column("Địa chỉ IP", anchor=tk.CENTER, width=380)
waiting_clients_list.column("Cổng port", anchor=tk.CENTER, width=180)

waiting_clients_list.heading("#0", text="", anchor=tk.CENTER)
waiting_clients_list.heading("Địa chỉ IP", text="Địa chỉ IP", anchor=tk.CENTER)
waiting_clients_list.heading("Cổng port",text="Cổng port", anchor=tk.CENTER)

# Logs label
logs_label = tk.Label(text="Được cấp phép ",font=("Arial", 10, "bold"), bg="pink")

# Waiting clients
logs_list = ttk.Treeview()
logs_list['columns'] = ("Được cấp phép", "Thời gian")

logs_list.column("#0", width=0, stretch=tk.NO)
logs_list.column("Được cấp phép", anchor=tk.CENTER, width=400)
logs_list.column("Thời gian", anchor=tk.CENTER, width=160)

logs_list.heading("#0", text="", anchor=tk.CENTER)
logs_list.heading("Được cấp phép", text="Được cấp phép", anchor=tk.CENTER)
logs_list.heading("Thời gian",text="Thời gian", anchor=tk.CENTER)

# Close button
close_button = tk.Button(text="Đóng", font=("Arial", 10, "bold"), width=20, command=close_button_click, bg="red", fg="white")

# Info label
info_label = tk.Label(text="Máy chủ: " + server.get_ip() + " | Cổng Port: 6969")

hello_client_label.pack(padx=50, anchor="center")
licensed_client_label.pack(padx=300, anchor="w")
logs_label.pack(padx=5, anchor="w")
logs_list.pack()
waiting_clients_label.pack(padx=5, anchor="w")
waiting_clients_list.pack()
close_button.pack(padx=5, pady=5)
info_label.pack(side=tk.BOTTOM, padx=5, pady=5)

window.mainloop()
