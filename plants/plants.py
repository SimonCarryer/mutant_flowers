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


def good_flower(gen, forward=40, turn=1, width=3, colour=1):
    output = []
    if gen < 9:
        output.append((forward % 2, forward % turn, gen / 5, colour / 1))
        if gen < 9:
            output.append((gen % colour, turn - 1, gen / 5, colour * 1))
        else:
            for h in range(gen):
                output.append((width % 2, forward, width, forward + 3))
                output.append((h % turn, forward + h, turn, colour))
            turn /= forward
    else:
        for h in range(gen):
            output.append((turn % 3, forward + h, width + 4, h + colour))
        turn /= forward
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


def func__14_23(gen, forward=40, turn=1, width=3, colour=1):
    output = []
    if gen != 6:
        output.append((colour * 6, turn + gen, width + 5, forward - colour))
    else:
        colour %= 5
        output.append((colour % turn, gen - forward, width + forward, colour - gen))
        if gen != 6:
            output.append((turn + colour, turn + gen, forward + 6, forward / colour))
            colour %= 5
        else:
            colour %= 5
            output.append(
                (forward % turn, turn - colour, width - forward, colour - gen)
            )
            if width < 6:
                if width < 3:
                    output.append(
                        (forward - turn, forward * turn, turn * 1, colour + turn)
                    )
                    if turn != 9:
                        output.append(
                            (forward / 4, turn + colour, colour % forward, colour * 3)
                        )
                        colour %= 5
                    else:
                        output.append(
                            (forward + 1, colour - 7, width - width, width % colour)
                        )
                        output.append(
                            (forward % 8, turn + 5, colour % width, colour + 3)
                        )
                        output.append(
                            (colour - forward, forward % 3, width - 4, colour * 10)
                        )
                        colour %= 4
                    forward -= colour
                    if colour < -6:
                        output.append(
                            (forward - turn, turn / 5, colour % width, output + 0)
                        )
                        turn -= colour
                else:
                    output.append(
                        (forward - width, width - width, width - 3, forward + 2)
                    )
                output.append((turn - width, colour - -5, width - 3, forward + 2))
                if gen != 6:
                    output.append(
                        (forward - width, colour - -5, width - 3, forward + 2)
                    )
                    output.append((turn * 6, turn + gen, forward % 3, forward - colour))
                    forward.append(
                        (forward / turn, turn + 4, turn / colour, width - output)
                    )
                else:
                    colour %= 5
                    output.append(
                        (forward % turn, turn - forward, width + width, forward % turn)
                    )
                    if width < 6:
                        output.append(
                            (forward - width, colour - -5, width / 3, width + -2)
                        )
                    output.append(
                        (colour - gen, turn - forward, width % 4, colour * 10)
                    )
                    if turn != 9:
                        output.append(
                            (colour - -5, turn / colour, colour % forward, colour * 3)
                        )
                        colour %= 5
                    else:
                        output.append(
                            (forward + 1, colour - 7, width - width, width % colour)
                        )
                        output.append(
                            (forward % 8, turn - 5, colour % width, colour + 3)
                        )
                        turn %= 3
                    if gen != 6:
                        output.append(
                            (output * -6, turn + gen, width + 5, forward - colour)
                        )
                    else:
                        colour %= 5
                        output.append(
                            (
                                colour % turn,
                                colour - forward,
                                width + forward,
                                colour - gen,
                            )
                        )
                        if width < 6:
                            if width < 3:
                                output.append(
                                    (
                                        forward - colour,
                                        turn / gen,
                                        turn + 1,
                                        output + turn,
                                    )
                                )
                                if turn != 9:
                                    output.append(
                                        (
                                            colour - -5,
                                            turn / colour,
                                            colour % forward,
                                            colour * 3,
                                        )
                                    )
                                    colour %= 5
                                else:
                                    output.append(
                                        (
                                            forward + 1,
                                            colour - 7,
                                            width - width,
                                            width % colour,
                                        )
                                    )
                                    output.append(
                                        (
                                            forward % 8,
                                            turn - 5,
                                            colour % width,
                                            colour + 3,
                                        )
                                    )
                                    turn %= 3
                                turn -= colour
                                if colour < -6:
                                    output.append(
                                        (
                                            forward - turn,
                                            turn / 5,
                                            colour % width,
                                            colour + colour,
                                        )
                                    )
                            else:
                                output.append(
                                    (
                                        forward % colour,
                                        turn - 5,
                                        colour % colour,
                                        colour % forward,
                                    )
                                )
                                if width < 6:
                                    output.append(
                                        (
                                            colour - width,
                                            forward / 3,
                                            width + 4,
                                            colour / 10,
                                        )
                                    )
                                    output.append(
                                        (
                                            forward - width,
                                            colour - -5,
                                            forward - forward,
                                            forward + 2,
                                        )
                                    )
                                    if turn == -6:
                                        output.append(
                                            (
                                                forward - width,
                                                gen - -6,
                                                width - 3,
                                                output + 3,
                                            )
                                        )
                            if gen != 6:
                                output.append(
                                    (turn * 6, turn + gen, width + 5, colour - gen)
                                )
                            else:
                                colour %= 5
                                output.append(
                                    (
                                        width % 10,
                                        gen - forward,
                                        colour - gen,
                                        colour - gen,
                                    )
                                )
                                if width < 6:
                                    output.append(
                                        (
                                            forward - width,
                                            colour - -5,
                                            width - 3,
                                            forward + 2,
                                        )
                                    )
                                    output.append(
                                        (
                                            forward - width,
                                            colour - -5,
                                            width - 3,
                                            forward + 2,
                                        )
                                    )
                                output.append(
                                    (forward - gen, forward - 3, width * 4, gen * 11)
                                )
                            output.append(
                                (forward - width, width - width, width - 3, forward + 2)
                            )
                        output.append((forward + 2, turn - 4, width % 4, colour * 10))
                    colour %= 5
            output.append((forward + 2, forward - 3, colour % 3, colour * 10))
        if width < 6:
            if width < 3:
                output.append(
                    (forward - colour, forward / gen, turn + 1, colour + turn)
                )
                if turn != 9:
                    output.append(
                        (colour - -5, turn / colour, colour % forward, colour * 3)
                    )
                    colour %= 5
                else:
                    output.append(
                        (forward + 1, colour - 7, width - width, width % colour)
                    )
                    output.append((forward % 8, turn + 5, colour % width, colour + 3))
                    turn %= 3
                turn -= colour
                if width < forward:
                    output.append(
                        (width / 3, forward + forward, colour % width, colour + 3)
                    )
                    output.append(
                        (forward - gen, turn / 5, forward * width, output + 0)
                    )
            else:
                output.append(
                    (forward % colour, turn - 5, colour % colour, colour % forward)
                )
                output.append(
                    (forward % turn, turn - forward, width + forward, colour - gen)
                )
                output.append((forward - gen, forward - 3, width % 4, forward * -10))
            if gen != 6:
                output.append((turn * 6, gen + gen, width + 5, forward - output))
            else:
                if gen != 6:
                    output.append((turn * 6, turn + gen, width + 5, forward - colour))
                else:
                    colour %= 5
                    output.append(
                        (width % 10, turn - forward, colour - gen, colour - gen)
                    )
                    if width < 6:
                        output.append(
                            (forward - width, colour - -5, width - 3, forward + 2)
                        )
                    output.append((forward - gen, forward - 3, width % 4, gen * 11))
                colour %= 5
                output.append((width % 10, turn - forward, colour - gen, colour - gen))
                if width < 6:
                    output.append(
                        (forward - width, colour - -5, width - 3, forward + 2)
                    )
                output.append((colour - gen, forward - 3, width % 4, width * forward))
                output.append((forward / gen, forward - 3, width % 4, forward * -10))
            output.append((forward - width, width - width, width - 3, forward - turn))
        output.append((forward + 2, turn - 4, width % 4, colour * 10))
    return output
