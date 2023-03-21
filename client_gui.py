import tkinter as tk
import tkinter.messagebox as messagebox
from tooltip import ToolTip
from dsystem import Client
import socket
import threading

def refresh_status_label():
    states = {0: 'Nothing', 1: 'Wating', 2: 'Licensed'}
    status_label.config(text="Status: " + states[client.status])

def close_button_click():
    window.destroy()

def __license():
    try:
        host = host_text.get("1.0", 'end-1c')
        port = int(port_text.get("1.0", 'end-1c'))
        client.config((host, port))
        status_label.config(text="Status: Wating")
        client.license()
    except Exception as ex:
        messagebox.showerror(title="Error", message=str(ex))

    refresh_status_label()

def __release():
    try:
        host = host_text.get("1.0", 'end-1c')
        port = int(port_text.get("1.0", 'end-1c'))
        client.config((host, port))
        status_label.config(text="Status: Wating")
        client.release()
    except Exception as ex:
        messagebox.showerror(title="Error", message=str(ex))

    refresh_status_label()

def license_button_click():
    global thread
    if (thread.is_alive()):
        messagebox.showerror(title="Error", message="Request denied, due to waiting for response from the server")
        return

    thread = threading.Thread(target=__license)
    thread.start()

def release_button_click():
    global thread
    if (thread.is_alive()):
        messagebox.showerror(title="Error", message="Request denied, due to waiting for response from the server")
        return

    thread = threading.Thread(target=__release)
    thread.start()

client = Client()
thread = threading.Thread()

# Gui
window = tk.Tk()
window.title("Client | " + client.get_ip())
window.geometry('400x300')

# Input Host
host_label = tk.Label(text="Host")
host_text = tk.Text(height=1)

# Input Port
port_label = tk.Label(text="Port")
port_text = tk.Text(height=1)

# Request button
license_button = tk.Button(text="License", width=16, command=license_button_click)

# Request button
release_button = tk.Button(text="Release", width=16, command=release_button_click)

# Close button
close_button = tk.Button(text="Close", width=16, command=close_button_click)

# Status label
status_label = tk.Label(text="Status: Nothing")

host_label.pack(padx=5, anchor="w")
host_text.pack(padx=5, pady=5)
port_label.pack(padx=5, anchor="w")
port_text.pack(padx=5, pady=5)

license_button.pack(padx=5, pady=5)
release_button.pack(padx=5, pady=5)
close_button.pack(padx=5, pady=5)

status_label.pack(side=tk.BOTTOM, padx=5, pady=5)

window.mainloop()
