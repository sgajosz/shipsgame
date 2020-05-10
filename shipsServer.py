import socket
import threading

def recvall(sock):
    data = ""
    while not data.endswith("\r\n"):
        data = data + sock.recv(1).decode()
    return data

def game(playerOneConnection, playerTwoConnection):
    logFile = open("server.log", "a")
    info = "Game between " + playerOneConnection[1][0] + " and " + playerTwoConnection[1][0] + " has started\n"
    logFile.write(info)
    playerOneConnection[0].sendall("Game started!\r\n".encode())
    playerTwoConnection[0].sendall("Game started!\r\n".encode())
    info = "Game between " + playerOneConnection[1][0] + " and " + playerTwoConnection[1][0] + " has ended\n"
    logFile.write(info)
    playerOneConnection[0].close()
    playerTwoConnection[0].close()
    logFile.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind(("127.0.0.1", 1234))
sock.listen(10)

gamesInProgress = []

while True:
    try:
        logFile = open("server.log", "a")
        playerOneConnection = sock.accept()
        info = playerOneConnection[1][0] + " joined the server\n"
        print(info)
        logFile.write(info)

        playerOneConnection[0].sendall("GAME_CREATED\r\n".encode())
        playerTwoConnection = sock.accept()
        info = playerTwoConnection[1][0] + " joined the server\n"
        print(info)
        logFile.write(info)
    except socket.error as e:
        print("Connection error occured")

    try:
        playerOneConnection[0].sendall("PLAYER_FOUND\r\n".encode())
    except socket.error as e:
        playerTwoConnection[0].sendall("RECONNECT\r\n".encode())
        info = playerOneConnection[1][0] + " has left the game\n"
        logFile.write(info)
        logFile.close()
        continue

    try:
        playerTwoConnection[0].sendall("GAME_FOUND\r\n".encode())
    except socket.error as e:
        print("Connection error occured")

    newGame = threading.Thread(target=game, args=(playerOneConnection, playerTwoConnection))
    gamesInProgress.append(newGame)
    newGame.start()
    logFile.close()
    break
