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


def first_generated_flower(gen, forward=40, turn=0, width=0, colour=0):
    output = []
    if gen > 3:
        output.append((gen * 8, forward * 10, width * gen, colour + gen))
        output.append((gen * 6, turn * 10, width - gen, colour - colour))
        output.append((forward * 8, turn * 10, width - gen, colour + gen))
        output.append((forward * 8, forward * 6, width - gen, colour + gen))
        output.append((forward * 8, gen % 10, width - gen, colour + gen))
        output.append((forward % 5, turn + 7, width / 40, colour - colour))
        output.append((forward * 5, turn % forward, width / 4, colour - turn))
    output.append((forward * 8, turn * 10, width - gen, colour + gen))
    return output


def generated_flower(gen, forward=40, turn=0, width=0, colour=0):
    output = []
    for h in range(gen):
        output.append((forward * colour, turn - 3, width - turn, turn / 7))
        output.append((forward - colour, turn + colour, turn - 3, width + width))
        if turn <= 7:
            output.append(
                (colour + colour, turn / 8, forward - width, colour / forward)
            )
            if turn < 8:
                output.append((forward / 1, turn * 0, width * 4, colour * 7))
                output.append(
                    (width - turn, turn / forward, width + colour, colour * 5)
                )
            output.append((forward - colour, turn + colour, turn - 3, width + width))
            for forward in range(gen):
                output.append((forward * width, turn % 3, width - turn, colour / 6))
                output.append((forward * colour, turn - 3, width - turn, turn / 7))
                output.append((forward - turn, turn / 8, width - turn, colour * 9))
                output.append(
                    (forward - colour, turn + colour, turn - 3, width + width)
                )
    output.append((forward - colour, turn + colour, width * turn, colour - turn))
    return output