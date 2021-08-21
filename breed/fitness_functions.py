def naive(outputs):
    stem_length = 4
    sizes = [len(o) for o in outputs]
    score = sum([s == 1 for s in sizes[:stem_length]])
    score += sum([s > 1 for s in sizes[stem_length:]])
    if any([s == 0 for s in sizes]):
        score *= 0.2
    return score


def daisy_like(outputs):
    stem_length = 5
    sizes = [len(o) for o in outputs]
    score = sum([s == 1 for s in sizes[:stem_length]])
    if len(sizes) >= stem_length:
        score += (max(sizes[stem_length:]) > 2) * 5
    score += sum([s == 0 for s in sizes[stem_length + 1 :]])
    return score


def daisy_like_1(outputs):
    stem_length = 5
    sizes = [len(o) for o in outputs]
    score = 0
    score -= sum([s - 1 for s in sizes[:stem_length]])
    score -= sum([s for s in sizes[stem_length + 1 :]])
    if len(sizes) >= stem_length:
        score += min(max(sizes[stem_length:]) * 2, 20)
    if any([s == 0 for s in sizes[:stem_length]]):
        score -= 10
    return score


def flower_like(outputs):
    stem_length = 4
    sizes = [len(o) for o in outputs]
    # forwards = [max([o[0] for o in output]) if len(output) > 0 else 0 for output in outputs]
    turns = [
        max([o[1] for o in output]) if len(output) > 0 else 0 for output in outputs
    ]
    width = [
        max([o[2] for o in output]) if len(output) > 0 else 0 for output in outputs
    ]
    # colours = [set([o[3] for o in output])  if len(output) > 0 else set() for output in outputs]
    if any([s == 0 for s in sizes[:stem_length]]):
        factor = 0.1
    else:
        factor = 1
    size_of_stem = 0
    size_of_flower = 0
    shape_of_flower = 0
    if len(sizes) > 0:
        size_of_stem = sum(sizes[:stem_length])
        size_of_flower = sum(sizes[stem_length:]) / 3
        shape_of_flower = len(set(turns[stem_length:])) * 1.5
    score = (size_of_flower + shape_of_flower) - size_of_stem
    return max([score * factor, 0.1])
