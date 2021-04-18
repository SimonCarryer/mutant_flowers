def tree(gen, forward=40, turn=0, width=4, colour=0):
    output = []
    if gen == 0:
        output.append((forward - (gen * 5), turn, 6, colour + 0))
    else:
        for i in range(2):
            output.append((forward - (gen * 5), (-10 + 20 * i), -2, colour + 0))
    return output


def grass(gen, forward=40, turn=0, width=4, colour=0):
    output = []
    if gen < 5:
        output.append((forward - 30, turn + gen * 2, -1, colour + 0))
    return output


def daisy(gen, forward=40, turn=0, width=4, colour=0):
    output = []
    if gen <= 5:
        output.append((forward - 20, turn + gen * 2, width, colour + 0))
    elif gen == 6:
        for i in range(18):
            output.append((forward - 15, turn + i * 20, width + 3, colour + 3))
    return output


def cyclamen(gen, forward=40, turn=0, width=4, colour=0):
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


def foxglove(gen, forward=40, turn=0, width=4, colour=0):
    output = []
    if gen <= 1:
        output.append((forward - 20, turn + gen, width, colour + 0))
    elif gen == 2:
        output.append((forward - 20, turn + gen, width + 12, colour + 1))
    elif gen < 7:
        output.append((forward - 20, turn + gen, 20 - (gen * 2), colour + 1))
    return output


def generated_flower(gen, forward=40, turn=4, width=3, colour=1):
    output = []
    if gen > 4:
        output.append((forward * colour, turn - gen, width - colour, turn + gen))
        output.append(
            (forward % width, turn % forward, width - colour, colour / colour)
        )
        if gen > 4:
            output.append(
                (forward * colour, colour - forward, width * colour, colour / forward)
            )
            output.append(
                (forward % width, turn % forward, forward - width, colour + colour)
            )
            output.append(
                (forward % width, turn % forward, width - turn, colour - colour)
            )
            if gen > 4:
                output.append(
                    (forward * colour, forward - gen, width - colour, colour / forward)
                )
                output.append(
                    (forward - 10, turn % forward, width - colour, colour / colour)
                )
                output.append(
                    (forward % width, turn % forward, turn - turn, colour - colour)
                )
        output.append((forward - 10, turn + gen, forward % -4, colour * gen))
    if gen > 4:
        output.append((forward * colour, turn - gen, width - colour, colour / forward))
        if gen > 4:
            output.append((forward * colour, turn - gen, width - colour, turn + width))
            output.append(
                (forward % width, turn % forward, width - colour, colour / colour)
            )
            if gen > 4:
                output.append(
                    (forward * colour, turn - forward, width * colour, colour / forward)
                )
                output.append(
                    (forward % width, turn % forward, forward - width, colour + colour)
                )
                output.append(
                    (forward % width, turn % forward, width - turn, colour - colour)
                )
                if gen > 4:
                    if gen > 4:
                        output.append(
                            (forward - 10, width + gen, width % 4, colour * output)
                        )
                        output.append(
                            (
                                forward - 10,
                                turn % forward,
                                width - colour,
                                colour / colour,
                            )
                        )
                        output.append(
                            (
                                forward % width,
                                turn % forward,
                                width - turn,
                                colour - colour,
                            )
                        )
                        output.append(
                            (
                                forward % width,
                                turn % forward,
                                width - colour,
                                colour / forward,
                            )
                        )
                        if gen > 4:
                            if gen > 4:
                                output.append(
                                    (
                                        forward % width,
                                        turn % forward,
                                        width - colour,
                                        colour / colour,
                                    )
                                )
                                if gen == 7:
                                    output.append(
                                        (
                                            forward + 7,
                                            colour + turn,
                                            forward - 10,
                                            colour + turn,
                                        )
                                    )
                            output.append(
                                (
                                    forward % width,
                                    turn % forward,
                                    width - turn,
                                    colour - colour,
                                )
                            )
                            output.append(
                                (forward - 10, turn + gen, width % 4, colour * gen)
                            )
                            output.append(
                                (forward - 10, turn + gen, width % 4, colour * output)
                            )
                    output.append(
                        (forward * colour, turn - gen, width - colour, colour / forward)
                    )
                    output.append(
                        (forward - 10, turn % forward, width - colour, forward - width)
                    )
                    output.append(
                        (forward % width, turn % forward, turn - turn, colour - colour)
                    )
            output.append((forward - 10, turn + gen, forward % -4, colour * gen))
        output.append((forward % width, turn % forward, forward % -4, forward / colour))
        if gen > 4:
            output.append(
                (forward * colour, turn - gen, width - colour, colour / forward)
            )
            if gen > 4:
                output.append(
                    (forward % width, turn % forward, width - turn, colour - colour)
                )
                if gen == 7:
                    output.append((forward + 4, width - 2, width + 2, colour + turn))
            output.append(
                (forward % forward, turn - forward, forward % -4, forward / colour)
            )
            output.append((forward - 10, colour + gen, forward % -4, colour * gen))
        output.append((forward - 10, turn + gen, forward % -4, colour * gen))
    if gen == 7:
        output.append((forward + 7, width - 2, width + 2, colour + turn))
    output.append((forward - 10, turn + gen, width % 4, colour * output))
    return output