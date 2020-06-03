import socket
import threading
from time import sleep

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

from_server = client.recv(4040)
print(from_server.decode())


# Haandtere max antal beskeder der er tilladt at sende
def RMMessages():
    global mMessages
    sleep(1)
    mMessages = 0

# holder connection i live hvis option er true
def checkHeartbeat(client, lock):
    while True:
        sleep(3)
        lock.acquire()
        client.send("con-h 0x00".encode())
        lock.release()

def thread1(conn, lock):
    global mMessages
    mMessages = 0
    mNumber = 0

    while True:

        text = input()

        #Lock
        lock.acquire()
        conn.send(("msg-" + str(mNumber) + "=" + text).encode())
        lock.release()

        mMessages = mMessages + 1

        data = conn.recv(4040)
        from_server = data.decode()
        print(from_server)

        # Hvis server svarer med denne besked er connection lukket
        if from_server == "con-res 0xFE":
            conn.send("con-res 0xFF".encode())
            sleep(1)
            conn.close()
            print("Timeout")
            break

        # Tjekker om beskeder fra server følger protokol
        if not from_server.startswith("res-") and not ((mNumber - gettNumber(from_server)) == 1):
            conn.close()
            break


        # uddrager besked nummer fra server besked og returne det
        def gettNumber(from_server):
            global serverN
            if not from_server.startswith("com-0"):
                string = from_server.replace('res-', '', 1).replace('=', '', 1)
                numSearch = [int(i) for i in string.split() if i.isdigit()]
                serverN = numSearch[0]
                return int(serverN)







def start():

# tjekker server svar og connection fras client
if from_server.decode().startswith("com-0 accept"):
    client.send("com-0 accept".encode())

    threading.Thread(target=thread1, args=(client, lock)).start()
    threading.Thread(target=RMMessages).start()
    threading.Thread(target=heartbeat, args=(client,lock)).start()
else:
    client.close()


start()

