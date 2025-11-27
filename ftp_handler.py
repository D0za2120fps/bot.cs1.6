from ftplib import FTP
from config import FTP_HOST, FTP_USER, FTP_PASS, USERS_INI_PATH

class FTPHandler:
    def add_user(self, nick, password, flags):
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        with open("users_temp.ini", "wb") as f:
            ftp.retrbinary(f"RETR {USERS_INI_PATH}", f.write)
        with open("users_temp.ini", "r") as f:
            lines = f.readlines()
        lines.append(f'"{nick}" "{password}" "{flags}" "a"\n')
        with open("users_temp.ini", "w") as f:
            f.writelines(lines)
        with open("users_temp.ini", "rb") as f:
            ftp.storbinary(f"STOR {USERS_INI_PATH}", f)
        ftp.quit()
