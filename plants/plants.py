def tree(gen, forward=40, turn=0, width=0, colour=0):
    output = []
    if gen == 0:
        output.append((forward - (gen * 5), turn, 6, colour + 0))
    else:
        for i in range(2):
            output.append((forward - (gen * 5), (-10 + 20 * i), -2, colour + 0))
    return output


def grass(gen, forward=40, turn=0, width=0, colour=0):
    output = []
    if gen < 5:
        output.append((forward - 30, turn + gen * 2, -1, colour + 0))
    return output


def daisy(gen, forward=40, turn=0, width=0, colour=0):
    output = []
    if gen <= 5:
        output.append((forward - 20, turn + gen * 2, width, colour + 0))
    elif gen == 6:
        for i in range(18):
            output.append((forward - 15, turn + i * 20, width + 3, colour + 3))
    return output


def cyclamen(gen, forward=40, turn=0, width=0, colour=0):
    output = []
    if gen == 0:
        for i in range(3):
            output.append((forward - 20, turn - 10 + (i * 20), width, colour + 0))
    elif gen <= 4:
        output.append((forward - 20, turn - gen * 2, width, colour + 0))
    elif gen == 5:
        for i in range(7):
            output.append((forward - 15, (turn + i * 20) + 180, width + 3, colour + 2))
    return output


def foxglove(gen, forward=40, turn=0, width=0, colour=0):
    output = []
    if gen <= 1:
        output.append((forward - 20, turn + gen, width, colour + 0))
    elif gen == 2:
        output.append((forward - 20, turn + gen, width + 12, colour + 1))
    elif gen < 7:
        output.append((forward - 20, turn + gen, -gen / 2, colour + 1))
    return output