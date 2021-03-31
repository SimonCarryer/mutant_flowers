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


def flower(gen, forward=40, turn=0, width=0, colour=0):
    output = []
    if gen <= 5:
        output.append((forward - 20, turn + gen * 2, width, colour + 0))
    elif gen == 6:
        for i in range(18):
            output.append((forward - 15, turn + i * 20, width + 3, colour + 2))
    return output
