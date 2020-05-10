import socket

def recvall(sock):
    data = ""
    while not data.endswith("\r\n"):
        data = data + sock.recv(1).decode()
    return data

def game(sockIPv4):
    reply = recvall(sockIPv4)
    print(reply)

sockIPv4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sockIPv4.connect(("127.0.0.1", 1234))

    gameFound = False

    while not gameFound:
        reply = recvall(sockIPv4)
        if reply == "GAME_CREATED\r\n":
            print("Awaiting for second player...")
        elif reply == "PLAYER_FOUND\r\n" or reply == "GAME_FOUND\r\n":
            if reply == "PLAYER_FOUND\r\n":
                print("Second player joined the game!")
                gameFound = True
            elif reply == "GAME_FOUND\r\n":
                print("You've found a game!")
                gameFound = True
        elif reply == "RECONNECT\r\n":
            sockIPv4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sockIPv4.connect(("127.0.0.1", 1234))

    if gameFound:
        game(sockIPv4)


except Exception as e:
    print("Connection failed %s" % e)
finally:
    sockIPv4.close()
