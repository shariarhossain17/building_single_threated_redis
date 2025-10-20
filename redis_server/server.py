import select
import socket


class RedisServer:
    def __init__(self,host="localhost",port=6379):
        self.host=host
        self.port=port
        self.running=False
        self.client={}


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
                    [self.server_socket]+list(self.client.keys()),[],[],1.0
                )

                for sock in read:
                    print(f"sock is here {sock }")
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"event loop error {e}")

    
    def stop(self):
        self.server_socket.close()