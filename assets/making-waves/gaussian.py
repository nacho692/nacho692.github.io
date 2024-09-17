import numpy as np

def gaussian2d(x, y, sig):
    return np.exp(-(x**2 + y**2) / (2 * sig**2)) / (2 * np.pi * sig**2)


def gaussian2d_kernel(size, sig):
    kernel = np.fromfunction(lambda x, y: gaussian2d(x - size // 2, y - size // 2, sig), (size, size))
    kernel *= 1/np.min(kernel)
    return np.round(kernel, 0)

kernel = gaussian2d_kernel(5, 0.9)
print(kernel, np.sum(kernel))