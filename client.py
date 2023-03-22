from dsystem import Client

def do_license():
    try:
        print("Đợi phản hồi từ máy chủ...")
        client.license()
        print("Ok")
    except Exception as ex:
        print(ex)

def do_release():
    try:
       print("Đợi phản hồi từ máy chủ...")
       client.release()
       print("Ok")
    except Exception as ex:
        print(ex)

def do_config():
    host = input("Máy chủ: ")
    port = int(input("Cổng: "))
    client.config((host, port))

def do_status():
    states = {0: 'Chưa có gì', 1: 'Đang đợi', 2: 'Đã cho phép'}
    print(states[client.status])

def do_configs():
    print("Máy chủ:", client.server_address[0])
    print("Cổng:", client.server_address[1])

host = input("Máy chủ: ")
port = int(input("Cổng: "))

status = 0
client = Client((host, port))

while True:
    com = input("##> ")
    if com == "license":
        do_license()
    elif com == "release":
        do_release()
    elif com == "config":
        do_config()
    elif com == "status":
        do_status()
    elif com == "configs":
        do_configs()
    elif com == "exit":
        exit()
    else:
        print("'{}' không tìm thấy".format(com))
