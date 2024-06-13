import os
import ftplib
from decouple import config

ftp_host = config('FTP_HOST', default='localhost')
ftp_user = config('FTP_USER', default='postgres')
ftp_pass = config('FTP_PASS', default='teste')
remote_dir = config('REMOTE_DIR', default='/')
local_dir = config('LOCAL_DIR', default='D:/')

def download_ftp_dir(ftp, remote_dir, local_dir):
    print(f"Acessando o diretório remoto: {remote_dir}")
    ftp.cwd(remote_dir)

    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    filelist = ftp.nlst()
    print(f"Arquivos e diretórios encontrados em {remote_dir}: {filelist}")

    for file in filelist:
        local_path = os.path.join(local_dir, file)
        remote_path = remote_dir + "/" + file

        try:
            ftp.cwd(remote_path)
            download_ftp_dir(ftp, remote_path, local_path)
            ftp.cwd("..")
        except ftplib.error_perm:
            if not os.path.exists(local_path):
                print(f"Baixando arquivo: {file}")
                with open(local_path, "wb") as f:
                    ftp.retrbinary("RETR " + file, f.write)
            else:
                print(f"O arquivo {file} já existe localmente. Pulando o download.")

def main():
    ftp = ftplib.FTP(ftp_host)
    ftp.login(ftp_user, ftp_pass)

    print(f"Conectado ao FTP: {ftp_host}")

    download_ftp_dir(ftp, remote_dir, local_dir)
    ftp.quit()

if __name__ == "__main__":
    main()
