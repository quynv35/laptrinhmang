import socket
import threading
import sqlite3
import os

# Khởi tạo cơ sở dữ liệu
def init_db():
    conn = sqlite3.connect('file_sharing.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS logs (username TEXT, action TEXT, filename TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
    conn.commit()
    conn.close()

def help():
    menu = """
    Dang ki: register <username> <password>
    Dang nhap: login <username> <password>
    Download: download <filename>
    Upload: upload <filename>"""
    return menu

# Hàm xử lý đăng ký
def register_user(username, password):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Hàm xử lý đăng nhập
def login_user(username, password):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

# Hàm xử lý client
def handle_client(client_socket):
    action = client_socket.recv(1024).decode("utf-8").strip()

    if action not in ["register", "login", "help","download", "upload"]:
        client_socket.send(b"Command not found !")
        client_socket.send(help().encode("utf-8"))
        client_socket.close()
        return

    if action == 'register':
        username = client_socket.recv(1024).decode()
        password = client_socket.recv(1024).decode()
        if register_user(username, password):
            client_socket.send(b'Success')
        else:
            client_socket.send(b'Username already exists')

    elif action == 'login':
        username = client_socket.recv(1024).decode()
        password = client_socket.recv(1024).decode()
        if login_user(username, password):
            client_socket.send(b'Success')
        else:
            client_socket.send(b'Invalid credentials')
        return  # Kết thúc xử lý nếu không đăng nhập thành công

    username = client_socket.recv(1024).decode()
    action = client_socket.recv(1024).decode()

    if action == 'upload':
        filename = client_socket.recv(1024).decode()
        with open(filename, 'wb') as f:
            data = client_socket.recv(1024)
            while data:
                f.write(data)
                data = client_socket.recv(1024)
        log_action(username, 'upload', filename)
    elif action == 'download':
        filename = client_socket.recv(1024).decode()
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                data = f.read(1024)
                while data:
                    client_socket.send(data)
                    data = f.read(1024)
            log_action(username, 'download', filename)
    elif action == 'help':
        pass
    else:
        pass
    client_socket.close()

# Ghi nhật ký
def log_action(username, action, filename):
    conn = sqlite3.connect('file_sharing.db')
    c = conn.cursor()
    c.execute('INSERT INTO logs (username, action, filename) VALUES (?, ?, ?)', (username, action, filename))
    conn.commit()
    conn.close()

# Chạy server
def start_server():
    init_db()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("Server is listening...")
    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
