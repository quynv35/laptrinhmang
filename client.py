import socket

def upload_file(filename, server_ip):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, 9999))
    client.send(b'username')  # Gửi tên đăng nhập
    client.send(b'upload')     # Gửi yêu cầu upload
    client.send(filename.encode())
    with open(filename, 'rb') as f:
        data = f.read(1024)
        while data:
            client.send(data)
            data = f.read(1024)
    client.close()

def download_file(filename, server_ip):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, 9999))
    client.send(b'username')  # Gửi tên đăng nhập
    client.send(b'download')   # Gửi yêu cầu download
    client.send(filename.encode())
    with open('downloaded_' + filename, 'wb') as f:
        data = client.recv(1024)
        while data:
            f.write(data)
            data = client.recv(1024)
    client.close()

if __name__ == "__main__":
    # Thực hiện upload hoặc download
    upload_file('test.txt', 'localhost')
    download_file('test.txt', 'localhost')
