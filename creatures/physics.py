import numpy as np


def normalise_vector(a, axis=-1, order=2):
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2 == 0] = 1
    return (a / np.expand_dims(l2, axis))[0]


def magnitude_vector(vector):
    return np.linalg.norm(vector)


def distance_between_points(current, target):
    return np.linalg.norm(target - current)
