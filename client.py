from dsystem import Client

def do_license():
    try:
        print("Wating for reponse...")
        client.license()
        print("Ok")
    except Exception as ex:
        print(ex)

def do_release():
    try:
       print("Wating for reponse...")
       client.release()
       print("Ok")
    except Exception as ex:
        print(ex)

def do_config():
    host = input("Host: ")
    port = int(input("Port: "))
    client.config((host, port))

def do_status():
    states = {0: 'Nothing', 1: 'Wating', 2: 'Licensed'}
    print(states[client.status])

def do_configs():
    print("Host:", client.server_address[0])
    print("Port:", client.server_address[1])

host = input("Host: ")
port = int(input("Port: "))

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
        print("'{}' not found".format(com))
