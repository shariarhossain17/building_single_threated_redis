import select
import socket


class RedisServer:
    def __init__(self,host="localhost",port=6379):
        self.host=host
        self.port=port
        self.running=False
        self.clients={}


    def start(self):
        self.server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.server_socket.bind((self.host,self.port))
        self.server_socket.listen()
        self.server_socket.setblocking(False)
        self.running=True
        print(f"redis style server running on {self.host}:{self.port}")
        self._event_loop()

    def _event_loop(self):
        while self.running:
            try:
                read,_,_=select.select(
                    [self.server_socket]+list(self.clients.keys()),[],[],1.0
                )
                for sock in read:
                    if sock is self.server_socket:
                        self.accept_client()
                    else:
                        self.handle_client(sock)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"event loop error {e}")
    def accept_client(self):
            client,addr=self.server_socket.accept()
            client.setblocking(False)
            self.clients[client]={"addr":addr,"buffer":b""}
            client.send(b"+ok\r\n")
    def handle_client(self,client):
        try:
            data=client.recv(1024)
            if not data:
                self._disconnect_client(client)
                return
            self.clients[client]["buffer"]+=data
            self._process_buffer(client)
        except ConnectionError:
            self._disconnect_client(client)
    

    def _process_buffer(self,client):
        buffer=self.clients[client]["buffer"]
        print(buffer)
        while b"\n" in buffer:
            command,buffer=buffer.split(b"\n",1)
            if command:
                response=b"hello\r\n"
                client.send(response)
    def _disconnect_client(self,client):
        client.close()
        self.clients.pop(client,None)
    
        
       

    
    def stop(self):
        self.server_socket.close()