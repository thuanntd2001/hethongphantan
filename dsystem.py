import socket
from datetime import datetime

class Server:
    def __init__(self, address = ("127.0.0.1", 6969)):
        self.address = address 
        self.waiting_clients = []
        self.licensed_client = None
        self.logs = []

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip

    def get_licensed_client(self):
        return self.licensed_client

    def config(self, address):
        self.address = address 

    def run(self,
            licensed_client_on_changed = None,
            waiting_clients_on_changed = None,
            logs_on_changed = None):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(self.address)
        s.listen(5)

        while True:
            conn, addr = s.accept()

            rev = conn.recv(1024)
            if rev == b"license":
                if self.licensed_client and self.licensed_client[0][0] == addr[0]:
                    conn.send(b"Yeu cau bi tu choi vi client chua duoc cap phep")
                    continue

                if self.waiting_clients == [] and self.licensed_client == None:
                    self.licensed_client = (addr, conn)
                    self.licensed_client[1].send(b"OK")
                    self.logs.append(("{} đã được cấp phép".format(self.licensed_client[0][0]), datetime.now()))

                    # Event
                    if logs_on_changed: logs_on_changed(self, ("{} đã được cấp phép".format(self.licensed_client[0][0]), datetime.now()))
                    if licensed_client_on_changed: licensed_client_on_changed(self, self.licensed_client)

                    continue

                self.waiting_clients.append((addr, conn))
                self.logs.append(("{} đã được thêm vào hàng đợi".format(addr[0]), datetime.now()))

                # Event
                if logs_on_changed: logs_on_changed(self, ("{} đã được thêm vào hàng đợi".format(addr[0]), datetime.now()))
                if waiting_clients_on_changed: waiting_clients_on_changed(self, self.waiting_clients)
            elif rev == b"release":
                if (self.licensed_client is None) or (self.licensed_client[0][0] != addr[0]):
                    conn.send(b"Yeu cau bi tu choi vi client chua duoc cap phep")
                    continue

                conn.send(b"OK")

                self.logs.append(("{} license đã bị thu hồi".format(self.licensed_client[0][0]), datetime.now()))
                # Event
                if logs_on_changed: logs_on_changed(self, ("{} license đã bị thu hồi".format(self.licensed_client[0][0]), datetime.now()))

                self.licensed_client = None
                # Event
                if licensed_client_on_changed: licensed_client_on_changed(self, self.licensed_client)

                if self.waiting_clients:
                    self.licensed_client = self.waiting_clients.pop(0)
                    self.licensed_client[1].send(b"OK")
                    self.logs.append(("{} đã bị thu hồi".format(self.licensed_client[0][0]), datetime.now()))

                    # Event
                    if logs_on_changed: logs_on_changed(self, ("{} đã bị thu hồi".format(self.licensed_client[0][0]), datetime.now()))
                    if licensed_client_on_changed: licensed_client_on_changed(self, self.licensed_client)
                    if waiting_clients_on_changed: waiting_clients_on_changed(self, self.waiting_clients)
            else:
                conn.send(b"yeu cau tu choi, vi '" + rev + "' khong ton tai")

        s.close()

class Client:
    def __init__(self, server_address = ("127.0.0.1", 6969)):
        self.server_address = server_address
        self.status = 0

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip

    def config(self, server_address):
        self.server_address = server_address

    def license(self):
        _status = self.status

        if self.status != 0:
            raise Exception("Yêu cầu bị từ chối vì vi phạm trạng thái!")

        self.status = 1

        res = self.__send_request(b"license")

        if res != b"OK":
            self.status = _status
            raise Exception(res.decode("utf-8"))

        self.status = 2

    def release(self):
        _status = self.status

        if self.status != 2:
            raise Exception("Yêu cầu bị từ chối vì vi phạm trạng thái!")

        self.status = 1

        res = self.__send_request(b"release")

        if res != b"OK":
            self.status = _status
            raise Exception(res.decode("utf-8"))

        self.status = 0

    def __send_request(self, data):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.connect(self.server_address)
        s.send(data)

        res = s.recv(1024)

        s.close()

        return res
