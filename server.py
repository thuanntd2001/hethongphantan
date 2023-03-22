from dsystem import Server
import socket
import threading

def run_server():
    server.run()

def do_waiting_clients():
    print("{:<24} {:<8}".format("Địa chỉ IP Máy chủ", "Cổng port kết nối"))
    for client in server.waiting_clients:
        print("{:<24} {:<8}".format(client[0][0], client[0][1]))

def do_licensed_client():
    print("Địa chỉ IP Máy chủ:", server.licensed_client[0][0])
    print("Cổng kết nối:", server.licensed_client[0][1])

def do_logs():
    for log in server.logs:
        print("{} - {}".format(log[1], log[0]))

host = "0.0.0.0"
port = 6969
server = Server((host, port))
thread = threading.Thread(target=run_server)
thread.start()

while True:
    com = input("##> ")
    if com == "Đang chờ clients":
        do_waiting_clients()
    elif com == "Clients đã đăng ký":
        do_licensed_client()
    elif com == "Đăng nhập":
        do_logs()
    elif com == "Thoát":
        exit()
    else:
        print("'{}' Không tìm thấy".format(com))
