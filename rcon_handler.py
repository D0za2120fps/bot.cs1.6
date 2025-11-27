# utils/rcon_handler.py
import socket
from config import RCON_PASS

class RCONHandler:
    def __init__(self, host='193.19.119.166', port=8888):
        self.host = host
        self.port = port
        self.password = R2013dkwdm3

    def send_command(self, command):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            msg = f"\xff\xff\xff\xffrcon {self.password} {command}\n".encode()
            s.sendto(msg, (self.host, self.port))
            s.close()
        except Exception as e:
            print("Ошибка RCON:", e)

    def reload_admins(self):
        self.send_command("amx_reloadadmins")
