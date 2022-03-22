#%%
import matplotlib.pyplot as plt
import numpy as np
#%%
def f(x, y, t):
    return t * np.sin(x) + np.random.randn() * np.cos(t * y)

def plot3D(f, t=1):
    nx, ny = (100, 100)
    x = np.linspace(-10, 10, nx)
    y = np.linspace(-10, 10, ny)
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y, t)
    fig = plt.figure(figsize=(12, 8))
    ax = plt.axes(projection='3d')
    ax.view_init(40, 35)
    ax.contour3D(X, Y, Z, 200, cmap='jet')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z');

#%%
plot3D(f, t=1)

#%%

#%%
