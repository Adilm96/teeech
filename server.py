import socket
import threading
from time import sleep

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def timeout():
    global clientTO
    while True:
        sleep(4)

        if f_client("con-h 0x00"):  # resetter connection, hvis client har enabled heartbeat
            clientTO = False

        print(" timeout " + str(clientTO))

        # clientTO == True: sendes connection reset besked
        # clientTo == False: sæt til True og sleep i 4 sek.
        if clientTO:
            connection.send(("con-res 0x0FE").encode())
        else:
            clientTO = True

def thread1():
    global clientTO
    global f_client
    f_client = ''
    mNumber = 1
    handshake = False

    while True:
        data = conn.recv(4040)
        clientTO = True

        from_client = data.decode()
        print(from_client)

        # tjekker om inkommende beskeder bryder protokol og om connection er nødt til at være lukket
        if not from_client.startswith("msg-0"):
            clientTO = False
            #Tjekker om timeout
            if from_client == "con-res 0xFF":
                conn.close()
                print("connection timeouted")
                break
            #tjekker om beskeder bryder protokol
            if not from_client.startswith("com-0") and not from_client.startswith("com-h 0x00") and ((mNumber - gettNumber(from_client)) !=1):
                conn.close()
                break

        if not handshake:
            if from_client.startswith("com-0") and not from_client.startswith("com-0 accept") and int(from_client[7:9]) in range(0,256):
                clientTO = False
                conn.send(("com-0 accept" + socket.gethostbyname(socket.gethostname())).encode())

            if from_client == "com-0 accept":
                clientTO = False
                handshake = True

            # Tjekker efter korrekt besked nummer og svarer client
            if from_client.startswith("msg-") and ((mNumber - gettNumber(from_client)) == 1):
                clientTO = False
                conn.send(("res-" + str(mNumber) + "=Im Server").encode())
                mNumber = mNumber+2

            from_client = ''

def gettNumber(from_client):
    global clNumber
    if not from_client.startswith("com-0"):
        string = from_client.replace('msg-', '', 1).replace('=', ' ', 1)
        numSearch = [int(i) for i in string.split() if i.isdigit()]
        clNumber = numSearch[0]
        return int(clNumber)


def start():
    server.listen(4)
    print(f"server is listening on {SERVER}")
    while True:
       global conn
       conn, addr = server.accept()
       threading.Thread(target=timeout).start()
       threading.Thread(target=thread1).start()



print("server is starting...")

start()
