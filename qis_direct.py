import socket, time
from quarchpy.qis import isQisRunning, startLocalQis

if not isQisRunning():
    startLocalQis()
    time.sleep(8)

s = socket.create_connection(("127.0.0.1", 9722), timeout=10)
time.sleep(1)

def cmd(c):
    s.sendall((c + "\r\n").encode())
    time.sleep(1.5)
    try:
        return s.recv(65536).decode(errors="replace")
    except Exception as e:
        return f"(no reply: {e})"

print("LIST:", cmd("$list"))
print("SCAN:", cmd("$scan"))
print("LIST2:", cmd("$list"))
s.close()

