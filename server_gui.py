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
        licensed_client_label.config(text="Licensed client: No-one")
        return

    licensed_client_label.config(text="Licensed client: " + client[0][0])

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
window.title("Server")
window.geometry('600x700')

#  licensed_client label
licensed_client_label = tk.Label(text="Licensed client: No-one")

#  Waiting clients label
waiting_clients_label = tk.Label(text="Wating clients:")

# Waiting clients
waiting_clients_list = ttk.Treeview()
waiting_clients_list['columns'] = ("IP", "Port")

waiting_clients_list.column("#0", width=0, stretch=tk.NO)
waiting_clients_list.column("IP", anchor=tk.CENTER, width=380)
waiting_clients_list.column("Port", anchor=tk.CENTER, width=180)

waiting_clients_list.heading("#0", text="", anchor=tk.CENTER)
waiting_clients_list.heading("IP", text="IP", anchor=tk.CENTER)
waiting_clients_list.heading("Port",text="Port", anchor=tk.CENTER)

# Logs label
logs_label = tk.Label(text="Logs:")

# Waiting clients
logs_list = ttk.Treeview()
logs_list['columns'] = ("Log", "Time")

logs_list.column("#0", width=0, stretch=tk.NO)
logs_list.column("Log", anchor=tk.CENTER, width=380)
logs_list.column("Time", anchor=tk.CENTER, width=180)

logs_list.heading("#0", text="", anchor=tk.CENTER)
logs_list.heading("Log", text="Log", anchor=tk.CENTER)
logs_list.heading("Time",text="Time", anchor=tk.CENTER)

# Close button
close_button = tk.Button(text="Close", width=16, command=close_button_click)

# Info label
info_label = tk.Label(text="Host: " + server.get_ip() + " | Port: 6969")

licensed_client_label.pack(padx=5, anchor="w")
logs_label.pack(padx=5, anchor="w")
logs_list.pack()
waiting_clients_label.pack(padx=5, anchor="w")
waiting_clients_list.pack()
close_button.pack(padx=5, pady=5)
info_label.pack(side=tk.BOTTOM, padx=5, pady=5)

window.mainloop()
