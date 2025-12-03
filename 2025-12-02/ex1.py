import math

def cosine_lr(lr_max, lr_min, T_max, t):
    """Calculate the learning rate using cosine annealing.

    Args:
        lr_max (float): Maximum learning rate.
        lr_min (float): Minimum learning rate.
        T_max (int): Total number of iterations.
        t (int): Current iteration.

    Returns:
        float: The calculated learning rate.
    """
    return lr_min + 0.5 * (lr_max - lr_min) * (1 + math.cos(math.pi * t / T_max))