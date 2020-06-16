import socket

def recvall(sock):
    data = ""
    while not data.endswith("\r\n"):
        data = data + sock.recv(1).decode()
    return data

def printCurrentBoard(ships):
    currentLetter = 'A'
    print("     ", end="")
    for i in range(0, 10):
        print(str(i) + "    ", end="")
    print('')

    for i in range(0, 10):
        for j in range(0, 10):
            if j == 0:
                print(currentLetter + "    ", end="")
                currentLetter = chr(ord(currentLetter) + 1)
            print(str(ships[i][j]) + "    ", end="")
        print('')

    print("0 - not ship field")
    print("1 - ship filed")
    print("X - hit ship/part of the ship")
    print("* - mishit")


def placeShips():
    ships = [[], [], [], [], [], [], [], [], [], []]
    for i in range(0, 10):
        for j in range(0, 10):
            ships[i].append(0)

    printCurrentBoard(ships)

    fourMastOk = False
    while not fourMastOk:
        print("Place your fourmast ship(ex: A1 A2 A3 A4):", end="")
        fourMastPosition = input()

        fourMastPosition = fourMastPosition.split(' ')
        inRange = False

        try:
            for i in fourMastPosition:
                row = ord(i[0].upper()) - 65
                column = int(i[1])
                if row >= 0 and row <= 9 and column >= 0 and column <= 9:
                    inRange = True

            if len(fourMastPosition) == 4 and inRange:
                fourMastPosition = sorted(fourMastPosition)
                if fourMastPosition[0][0] == fourMastPosition[1][0] and fourMastPosition[1][0] == fourMastPosition[2][0] and fourMastPosition[2][0] == fourMastPosition[3][0]:
                    first = int(fourMastPosition[0][1])
                    second = int(fourMastPosition[1][1])
                    third = int(fourMastPosition[2][1])
                    fourth = int(fourMastPosition[3][1])
                    if fourth == third + 1 and third == second + 1 and second == first + 1:
                        fourMastOk = True
                elif fourMastPosition[0][1] == fourMastPosition[1][1] and fourMastPosition[1][1] == fourMastPosition[2][1] and fourMastPosition[2][1] == fourMastPosition[3][1]:
                    first = ord(fourMastPosition[0][0])
                    second = ord(fourMastPosition[1][0])
                    third = ord(fourMastPosition[2][0])
                    fourth = ord(fourMastPosition[3][0])
                    if fourth == third + 1 and third == second + 1 and second == first + 1:
                        fourMastOk = True
        except Exception as e:
            pass

        if not fourMastOk:
            print("Incorrect input!")
        else:
            for i in fourMastPosition:
                ships[ord(i[0].upper()) - 65][int(i[1])] = 1

        printCurrentBoard(ships)

    threeMastOkCounter = 0
    while threeMastOkCounter != 2:
        if threeMastOkCounter < 0:
            threeMastOkCounter = 0
        threeMastOk = False
        if threeMastOkCounter == 0:
            print("Place your first threemast ship(ex: A1 A2 A3):", end="")
        elif threeMastOkCounter:
            print("Place your second threemast ship(ex: A1 A2 A3):", end="")
        threeMastPosition = input()
        threeMastPosition = threeMastPosition.split(' ')
        inRange = False

        try:
            for i in threeMastPosition:
                row = ord(i[0].upper()) - 65
                column = int(i[1])
                if row >= 0 and row <= 9 and column >= 0 and column <= 9:
                    inRange = True

            if len(threeMastPosition) == 3 and inRange:
                threeMastPosition = sorted(threeMastPosition)
                if threeMastPosition[0][0] == threeMastPosition[1][0] and threeMastPosition[1][0] == threeMastPosition[2][0]:
                    first = int(threeMastPosition[0][1])
                    second = int(threeMastPosition[1][1])
                    third = int(threeMastPosition[2][1])
                    if third == second + 1 and second == first + 1:
                        threeMastOkCounter += 1
                        threeMastOk = True
                elif threeMastPosition[0][1] == threeMastPosition[1][1] and threeMastPosition[1][1] == threeMastPosition[2][1]:
                    first = ord(threeMastPosition[0][0])
                    second = ord(threeMastPosition[1][0])
                    third = ord(threeMastPosition[2][0])
                    if third == second + 1 and second == first + 1:
                        threeMastOkCounter += 1
                        threeMastOk = True

            for i in threeMastPosition:
                row = ord(i[0].upper()) - 65
                column = int(i[1])
                if ships[row][column] == 1:
                    threeMastOkCounter -= 1
                    threeMastOk = False
                elif row != 0 and ships[row - 1][column] == 1:
                    threeMastOkCounter -= 1
                    threeMastOk = False
                elif row != 9 and ships[row + 1][column] == 1:
                    threeMastOkCounter -= 1
                    threeMastOk = False
                elif column != 0 and ships[row][column -1] == 1:
                    threeMastOkCounter -= 1
                    threeMastOk = False
                elif column != 9 and ships[row][column + 1] == 1:
                    threeMastOkCounter -= 1
                    threeMastOk = False
        except Exception as e:
            pass

        if not threeMastOk:
            print("Incorrect input!")
        else:
            for i in threeMastPosition:
                ships[ord(i[0].upper()) - 65][int(i[1])] = 1

        printCurrentBoard(ships)

    twoMastOkCounter = 0

    while twoMastOkCounter != 3:
        twoMastOk = False
        if twoMastOkCounter < 0:
            twoMastOkCounter = 0
        if twoMastOkCounter == 0:
            print("Place your first twomast ship(ex: A1 A2):", end="")
        elif twoMastOkCounter == 1:
            print("Place your second twomast ship(ex: A1 A2):", end="")
        elif twoMastOkCounter == 2:
            print("Place your thrid twomast ship(ex: A1 A2):", end="")
        twoMastPosition = input()
        twoMastPosition = twoMastPosition.split(' ')
        inRange = False

        try:
            for i in twoMastPosition:
                row = ord(i[0].upper()) - 65
                column = int(i[1])
                if row >= 0 and row <= 9 and column >= 0 and column <= 9:
                    inRange = True

            if len(twoMastPosition) == 2 and inRange:
                twoMastPosition = sorted(twoMastPosition)
                if twoMastPosition[0][0] == twoMastPosition[1][0]:
                    first = int(twoMastPosition[0][1])
                    second = int(twoMastPosition[1][1])
                    if second == first + 1:
                        twoMastOkCounter += 1
                        twoMastOk = True
                elif twoMastPosition[0][1] == twoMastPosition[1][1]:
                    first = ord(twoMastPosition[0][0])
                    second = ord(twoMastPosition[1][0])
                    if second == first + 1:
                        twoMastOkCounter += 1
                        twoMastOk = True

                for i in twoMastPosition:
                    row = ord(i[0].upper()) - 65
                    column = int(i[1])
                    if ships[row][column] == 1:
                        twoMastOkCounter -= 1
                        twoMastOk = False
                    elif row != 0 and ships[row - 1][column] == 1:
                        twoMastOkCounter -= 1
                        twoMastOk = False
                    elif row != 9 and ships[row + 1][column] == 1:
                        twoMastOkCounter -= 1
                        twoMastOk = False
                    elif column != 0 and ships[row][column -1] == 1:
                        twoMastOkCounter -= 1
                        twoMastOk = False
                    elif column != 9 and ships[row][column + 1] == 1:
                        twoMastOkCounter -= 1
                        twoMastOk = False
        except Exception as e:
            pass

        if not twoMastOk:
            print("Incorrect input!")
        else:
            for i in twoMastPosition:
                ships[ord(i[0].upper()) - 65][int(i[1])] = 1

        printCurrentBoard(ships)

    oneMastOkCounter = 0
    while oneMastOkCounter != 4:
        oneMastOk = False
        if oneMastOkCounter < 0:
            oneMastOkCounter = 0
        if oneMastOkCounter == 0:
            print("Place your first onemast ship(ex: A1):", end="")
        elif oneMastOkCounter == 1:
            print("Place your second onemast ship(ex: A1):", end="")
        elif oneMastOkCounter == 2:
            print("Place your thrid onemast ship(ex: A1):", end="")
        elif oneMastOkCounter == 3:
            print("Place your fourth onemast ship(ex: A1):", end="")
        oneMastPosition = input()
        inRange = False

        try:
            if len(oneMastPosition) != 2:
                raise Exception()
            row = ord(oneMastPosition[0].upper()) - 65
            column = int(oneMastPosition[1])
            if row >= 0 and row <= 9 and column >= 0 and column <= 9:
                inRange = True

            if len(oneMastPosition) == 2 and inRange:
                oneMastOkCounter += 1
                oneMastOk = True

            row = ord(oneMastPosition[0].upper()) - 65
            column = int(oneMastPosition[1])
            if ships[row][column] == 1:
                oneMastOkCounter -= 1
                oneMastOk = False
            elif row != 0 and ships[row - 1][column] == 1:
                oneMastOkCounter -= 1
                oneMastOk = False
            elif row != 9 and ships[row + 1][column] == 1:
                oneMastOkCounter -= 1
                oneMastOk = False
            elif column != 0 and ships[row][column -1] == 1:
                oneMastOkCounter -= 1
                oneMastOk = False
            elif column != 9 and ships[row][column + 1] == 1:
                oneMastOkCounter -= 1
                oneMastOk = False

        except Exception as e:
            print(e)

        if not oneMastOk:
            print("Incorrect input!")
        else:
            ships[ord(oneMastPosition[0].upper()) - 65][int(oneMastPosition[1])] = 1

        printCurrentBoard(ships)

    return ships


def game(sockIPv4):
    try:
        reply = recvall(sockIPv4)
        if reply == "SECOND_PLAYER_LEFT_GAME\r\n":
            print("Second player left game! You win!")
            return
        print(reply)

        reply = recvall(sockIPv4)
        if reply == "SECOND_PLAYER_LEFT_GAME\r\n":
            print("Second player left game! You win!")
            return
        if reply == "PLACE_YOUR_SHIPS\r\n":
            ships = placeShips()

        message = "PLACED_SHIPS "
        for row in ships:
            for column in row:
                message += str(column)
            message += "."
        message += "\r\n"
        sockIPv4.send(message.encode())
        print("Waiting for the second player...")

        enemysShips = [[], [], [], [], [], [], [], [], [], []]
        for i in range(0, 10):
            for j in range(0, 10):
                enemysShips[i].append(0)

        while True:
            reply = recvall(sockIPv4)
            if reply == "SECOND_PLAYER_LEFT_GAME\r\n":
                print("Second player left game! You win!")
                return

            if reply == "YOUR_TURN\r\n":
                print("It's your turn to shoot.")
                correctField = False
                while not correctField:
                    print("Second player's ships")
                    printCurrentBoard(enemysShips)
                    print("Choose field(ex: A1): ", end="")
                    shot = input()
                    try:
                        row = ord(shot[0].upper()) - 65
                        column = int(shot[1])
                    except Exception as e:
                        print("Incorrect input!")
                        continue

                    if row >= 0 and row <= 9 and column >= 0 and column <= 9 and len(shot) == 2:
                        correctField = True
                    else:
                        print("Incorrect input!")
                        continue
                    if enemysShips[row][column] == "X" or enemysShips[row][column] == "*":
                        print("You have already shot into this field.")
                        correctField = False
                message = "SHOOT " + shot + "\r\n"
                sockIPv4.sendall(message.encode())

                reply = recvall(sockIPv4)
                mark = ""
                if reply == "SECOND_PLAYER_LEFT_GAME\r\n":
                    print("Second player left game! You win!")
                    return
                elif reply == "HIT\r\n":
                    print("You hit part of the opponent's ship.")
                    mark = "X"
                elif reply == "HIT_AND_SANK\r\n":
                    print("You sank opponent's ship.")
                    mark = "X"
                elif reply == "MISHIT\r\n":
                    print("You missed opponent's ship.")
                    mark = "*"
                elif "WIN" in reply:
                    print("You win!")
                    printCurrentBoard(enemysShips)
                    break
                enemysShips[row][column] = mark
                print("Second player's ships")
                printCurrentBoard(enemysShips)
                print("Second player's turn.")
            elif reply == "SECOND_PLAYER_TURN\r\n":
                print("Waiting for second player's hit...")
                reply = recvall(sockIPv4)
                mark = ""
                if reply == "SECOND_PLAYER_LEFT_GAME\r\n":
                    print("Second player left game! You win!")
                    return
                elif "DEFEAT" in reply:
                    print("You lost!")
                    printCurrentBoard(ships)
                    break
                elif reply.startswith("HIT_AND_SANK "):
                    print("Second player shot into field " + reply[13:15] + " and sank your ship.")
                    shot = reply[13:15]
                    mark = "X"
                elif reply.startswith("MISHIT "):
                    print("Second player shot into " + reply[7:9])
                    shot = reply[7:9]
                    mark = "*"
                elif reply.startswith("HIT "):
                    print("Second player hit your ship in field " + reply[4:6])
                    shot = reply[4:6]
                    mark = "X"
                row = ord(shot[0].upper()) - 65
                column = int(shot[1])
                ships[row][column] = mark
                print("Your ships")
                printCurrentBoard(ships)
    except (KeyboardInterrupt, SystemExit):
        sockIPv4.sendall("KEYBOARD_INTERRUPT\r\n".encode())
        print("\nYou ended the game")

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
            sockIPv4.close()
            sockIPv4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sockIPv4.connect(("127.0.0.1", 1234))

    if gameFound:
        game(sockIPv4)


except socket.error as e:
    print("Connection failed %s" % e)
finally:
    sockIPv4.close()
