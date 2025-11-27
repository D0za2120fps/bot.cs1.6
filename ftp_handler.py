# utils/ftp_handler.py
from ftplib import FTP
from config import FTP_HOST, FTP_USER, FTP_PASS, USERS_INI_PATH

class FTPHandler:
    def __init__(self):
        self.host = FTP_HOST
        self.user = FTP_USER
        self.password = FTP_PASS
        self.path = USERS_INI_PATH

    def add_user(self, nick, password, flags):
        ftp = FTP(self.host)
        ftp.login(self.user, self.password)
        # Скачать файл
        lines = []
        with open("users_temp.ini", "wb") as f:
            ftp.retrbinary(f"RETR {self.path}", f.write)
        with open("users_temp.ini", "r") as f:
            lines = f.readlines()
        # Добавить нового пользователя
        lines.append(f'"{nick}" "{password}" "{flags}" "a"\n')
        # Загрузить обратно
        with open("users_temp.ini", "w") as f:
            f.writelines(lines)
        with open("users_temp.ini", "rb") as f:
            ftp.storbinary(f"STOR {self.path}", f)
        ftp.quit()
