import os
from ftplib import FTP, error_perm


class FtpClient:
    def __init__(self, addr: str, port: int, user: str, passwd: str):
        self.addr = addr
        self.port = port
        self.user = user
        self.passwd = passwd

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self._ftp.close()

    def connect(self):
        self._ftp = FTP()
        self._ftp.connect(self.addr, self.port)
        self._ftp.login(self.user, self.passwd)

    def _traverse(self, depth=0):
        level = {}
        for entry in (path for path in self._ftp.nlst() if path not in ('.', '..')):
            try:
                self._ftp.cwd(entry)
                level[entry] = self._traverse(depth + 1)
                self._ftp.cwd('..')
            except error_perm:
                level[entry] = {}
        return level

    def retrfs(self):
        return self._traverse()

    def upload(self, src: str, dst: str):
        name = src.split('/')[-1]
        with open(src, 'rb') as file:
            self._ftp.cwd(dst)
            self._ftp.storbinary('STOR ' + name, file)
            self._ftp.cwd('/')

    def download(self, src: str, dst: str):
        name = src.split('/')[-1]
        srcdir = '/'.join(src.split('/')[:-1])
        with open(os.path.join(dst, name), 'wb') as file:
            self._ftp.cwd(srcdir)
            self._ftp.retrbinary('RETR ' + name, file.write)
            self._ftp.cwd('/')

    def quit(self):
        self._ftp.quit()
