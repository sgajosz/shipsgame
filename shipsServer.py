import socket
import threading

def recvall(sock):
    data = ""
    while not data.endswith("\r\n"):
        data = data + sock.recv(1).decode()
    return data

def sendToPlayer(player1, player2, command):
    try:
        player1.sendall(command.encode())
        return True
    except Exception as e:
        player2.sendall("SECOND_PLAYER_LEFT_GAME\r\n".encode())
        return False

def checkIfShipSank(ships, row, column):
    sank = True
    if row != 0 and ships[row-1][column] == "1":
        sank = False
    elif row != 9 and ships[row+1][column] == "1":
        sank = False
    elif column != 0 and ships[row][column-1] == "1":
        sank = False
    elif column != 9 and ships[row][column+1] == "1":
        sank = False

    if not sank:
        return sank

    if (row != 0 and ships[row - 1][column] == "X") or (row != 9 and ships[row + 1][column] == "X"):
        x = 1
        while row - x >= 0:
            if ships[row - x][column] == "1":
                return False
            if ships[row - x][column] == "0" or ships[row - x][column] == "*":
                break
            x += 1
        x = 1
        while row + x <= 9:
            if ships[row + x][column] == "1":
                return False
            if ships[row + x][column] == "0" or ships[row + x][column] == "*":
                break
            x += 1

    elif (column != 0 and ships[row][column-1] == "X") or (column != 9 and ships[row][column+1] == "X"):
        x = 1
        while column - x >= 0:
            if ships[row][column-x] == "1":
                return False
            if ships[row][column-x] == "0" or ships[row][column-x] == "*":
                break
            x += 1
        x = 1
        while column + x <= 9:
            if ships[row][column+x] == "1":
                return False
            if ships[row][column+x] == "0" or ships[row][column+x] == "*":
                break
            x += 1

    return sank


def insert(text, character, index):
    return text[:index] + character + text[index+1:]


def game(playerOneConnection, playerTwoConnection):
    logFile = open("server.log", "a")
    info = "Game between " + playerOneConnection[1][0] + " and " + playerTwoConnection[1][0] + " has started\n"
    logFile.write(info)

    if not sendToPlayer(playerOneConnection[0], playerTwoConnection[0], "Game started!\r\n"):
        logFile.write(playerOneConnection[1][0] + "has left the game\n")
        logFile.close()
        return
    if not sendToPlayer(playerTwoConnection[0], playerOneConnection[0], "Game started!\r\n"):
        logFile.write(playerTwoConnection[1][0] + "has left the game\n")
        logFile.close()
        return

    if not sendToPlayer(playerOneConnection[0], playerTwoConnection[0], "PLACE_YOUR_SHIPS\r\n"):
        logFile.write(playerOneConnection[1][0] + "has left the game\n")
        logFile.close()
        return
    if not sendToPlayer(playerTwoConnection[0], playerOneConnection[0], "PLACE_YOUR_SHIPS\r\n"):
        logFile.write(playerTwoConnection[1][0] + "has left the game\n")
        logFile.close()
        return

    playerOnePlacedShips = False
    playerTwoPlacedShips = False
    while not playerOnePlacedShips or not playerTwoPlacedShips:
        try:
            reply = recvall(playerOneConnection[0])
        except Exception as e:
            logFile.write(playerOneConnection[1][0] + "has left the game\n")
            logFile.close()
            playerTwoConnection[0].sendall("END_OF_GAME\r\n".encode())
            return
        if "PLACED_SHIPS " in reply and len(reply) == 125:
            print(playerOneConnection[1][0] + ' ' + reply)
            playerOneShips = reply.split(" ")[1].split(".")
            playerOnePlacedShips = True
        elif reply == "KEYBOARD_INTERRUPT\r\n":
            logFile.write(playerOneConnection[1][0] + " has left the game\n")
            logFile.close()
            playerTwoConnection[0].sendall("END_OF_GAME\r\n".encode())
            return
        else:
            if not sendToPlayer(playerOneConnection[0], playerTwoConnection[0], "ERROR_PLACE_YOUR_SHIPS\r\n"):
                logFile.write(playerOneConnection[1][0] + "has left the game\n")
                logFile.close()
                return

        try:
            reply = recvall(playerTwoConnection[0])
        except Exception as e:
            logFile.write(playerTwoConnection[1][0] + "has left the game\n")
            logFile.close()
            playerOneConnection.sendall("END_OF_GAME\r\n".encode())
            return
        if "PLACED_SHIPS " in reply and len(reply) == 125:
            print(playerTwoConnection[1][0] + ' ' + reply)
            playerTwoShips = reply.split(" ")[1].split(".")
            playerTwoPlacedShips = True
        elif reply == "KEYBOARD_INTERRUPT\r\n":
            logFile.write(playerTwoConnection[1][0] + " has left the game\n")
            logFile.close()
            playerOneConnection[0].sendall("END_OF_GAME\r\n".encode())
            return
        else:
            if not sendToPlayer(playerTwoConnection[0], playerOneConnection[0], "ERROR_PLACE_YOUR_SHIPS\r\n"):
                logFile.write(playerTwoConnection[1][0] + "has left the game\n")
                logFile.close()
                return

    playerOneShipsCount = 0
    playerTwoShipsCount = 0
    end = False

    while True:
        if not sendToPlayer(playerOneConnection[0], playerTwoConnection[0], "YOUR_TURN\r\n"):
            logFile.write(playerOneConnection[1][0] + "has left the game\n")
            logFile.close()
            return
        if not sendToPlayer(playerTwoConnection[0], playerOneConnection[0], "SECOND_PLAYER_TURN\r\n"):
            logFile.write(playerTwoConnection[1][0] + "has left the game\n")
            logFile.close()
            return

        while True:
            try:
                reply = recvall(playerOneConnection[0])
            except Exception as e:
                logFile.write(playerOneConnection[1][0] + "has left the game\n")
                logFile.close()
                playerTwoConnection[0].sendall("END_OF_GAME\r\n".encode())
                return
            if reply.startswith("SHOOT ") and len(reply) == 10:
                shot = reply[6:8]
                row = ord(shot[0].upper()) - 65
                column = int(shot[1])
                if row >= 0 and row <= 9 and column >= 0 and column <= 9:
                    break
            elif reply == "KEYBOARD_INTERRUPT\r\n":
                logFile.write(playerOneConnection[1][0] + " has left the game\n")
                logFile.close()
                playerTwoConnection[0].sendall("END_OF_GAME\r\n".encode())
                return
            if not sendToPlayer(playerOneConnection[0], playerTwoConnection[0], "SYNTAX_ERROR\r\n"):
                logFile.write(playerOneConnection[1][0] + "has left the game\n")
                logFile.close()
                return

        print(reply)
        info = playerOneConnection[1][0] + " has shot into the field " + shot + " of player " + playerTwoConnection[1][0]
        print(info)
        logFile.write(info)

        if playerTwoShips[row][column] == "1":
            playerTwoShips[row] = insert(playerTwoShips[row], "X", column)
            sank = checkIfShipSank(playerTwoShips, row, column)
            if sank:
                message1 = "HIT_AND_SANK"
                message2 = "HIT_AND_SANK " + shot
                playerTwoShipsCount += 1
            else:
                message1 = "HIT"
                message2 = "HIT " + shot
        else:
            playerTwoShips[row] = insert(playerTwoShips[row], "*", column)
            message1 = "MISHIT"
            message2 = "MISHIT " + shot

        if playerTwoShipsCount == 10:
            message1 += " WIN"
            message2 += " DEFEAT"
            info = playerOneConnection[1][0] + " has won the game against player " + playerTwoConnection[1][0] + "\n"
            print(info)
            logFile.write(info)
            end = True
        else:
            info = message1 + "\n"
            print(info)
            logFile.write(info)

        if not sendToPlayer(playerOneConnection[0], playerTwoConnection[0], message1+"\r\n"):
            logFile.write(playerOneConnection[1][0] + "has left the game\n")
            logFile.close()
            return
        if not sendToPlayer(playerTwoConnection[0], playerOneConnection[0], message2+"\r\n"):
            logFile.write(playerTwoConnection[1][0] + "has left the game\n")
            logFile.close()
            return

        if end:
            break

        if not sendToPlayer(playerTwoConnection[0], playerOneConnection[0], "YOUR_TURN\r\n"):
            logFile.write(playerTwoConnection[1][0] + "has left the game\n")
            logFile.close()
            return

        if not sendToPlayer(playerOneConnection[0], playerTwoConnection[0], "SECOND_PLAYER_TURN\r\n"):
            logFile.write(playerOneConnection[1][0] + "has left the game\n")
            logFile.close()
            return

        while True:
            try:
                reply = recvall(playerTwoConnection[0])
            except Exception as e:
                logFile.write(playerTwoConnection[1][0] + "has left the game\n")
                logFile.close()
                playerOneConnection[0].sendall("END_OF_GAME\r\n".encode())
                return
            if reply.startswith("SHOOT ") and len(reply) == 10:
                shot = reply[6:8]
                row = ord(shot[0].upper()) - 65
                column = int(shot[1])
                if row >= 0 and row <= 9 and column >= 0 and column <= 9:
                    break
            elif reply == "KEYBOARD_INTERRUPT\r\n":
                logFile.write(playerTwoConnection[1][0] + " has left the game\n")
                logFile.close()
                playerOneConnection[0].sendall("END_OF_GAME\r\n".encode())
                return
            if not sendToPlayer(playerTwoConnection[0], playerOneConnection[0], "SYNTAX_ERROR\r\n"):
                logFile.write(playerTwoConnection[1][0] + "has left the game\n")
                logFile.close()
                return

        print(reply)
        info = playerTwoConnection[1][0] + " has shot into the field " + shot + " of player " + playerOneConnection[1][0]
        logFile.write(info)
        print(info)

        if playerOneShips[row][column] == "1":
            playerOneShips[row] = insert(playerOneShips[row], "X", column)
            sank = checkIfShipSank(playerOneShips, row, column)
            if sank:
                message1 = "HIT_AND_SANK"
                message2 = "HIT_AND_SANK " + shot
                playerOneShipsCount += 1
            else:
                message1 = "HIT"
                message2 = "HIT " + shot
        else:
            playerOneShips[row] = insert(playerOneShips[row], "*", column)
            message1 = "MISHIT"
            message2 = "MISHIT " + shot

        if playerOneShipsCount == 10:
            message1 += " WIN"
            message2 += " DEFEAT"
            info = playerTwoConnection[1][0] + " has won the game against of player " + playerOneConnection[1][0] + "\n"
            print(info)
            logFile.write(info)
            end = True
        else:
            info = message1 + "\n"
            print(info)
            logFile.write(info)

        if not sendToPlayer(playerTwoConnection[0], playerOneConnection[0], message1+"\r\n"):
            logFile.write(playerTwoConnection[1][0] + "has left the game\n")
            logFile.close()
            return
        if not sendToPlayer(playerOneConnection[0], playerTwoConnection[0], message2+"\r\n"):
            logFile.write(playerOneConnection[1][0] + "has left the game\n")
            logFile.close()
            return

        if end:
            break

    info = "Game between " + playerOneConnection[1][0] + " and " + playerTwoConnection[1][0] + " has ended\n"
    logFile.write(info)
    print(info)
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
