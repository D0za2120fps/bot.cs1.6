import socket
from config import RCON_HOST, RCON_PORT, RCON_PASS

class RCONHandler:
    def send_command(self, command):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            msg = f"\xff\xff\xff\xffrcon {RCON_PASS} {command}\n".encode()
            s.sendto(msg, (RCON_HOST, RCON_PORT))
            s.close()
        except Exception as e:
            print("Ошибка RCON:", e)

    def reload_admins(self):
        self.send_command("amx_reloadadmins")
