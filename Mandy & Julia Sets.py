import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# Julia set function
def julia(c, z, max_iter):
    for i in range(max_iter):
        z = z * z + c
        if abs(z) > 2:
            return i
    return max_iter

def julia_set(c, xmin, xmax, ymin, ymax, width, height, max_iter):
    r = np.linspace(xmin, xmax, width)
    i = np.linspace(ymin, ymax, height)
    z = r[:, None] + 1j * i[None, :]
    iterations = np.vectorize(lambda z: julia(c, z, max_iter))(z)
    return iterations

# Mandelbrot set function
def mandelbrot(c, max_iter):
    z = np.zeros_like(c, dtype=np.complex128)
    mandelbrot_mask = np.ones_like(c, dtype=bool)
    iterations = np.zeros_like(c, dtype=int)

    for i in range(max_iter):
        z[mandelbrot_mask] = z[mandelbrot_mask] * z[mandelbrot_mask] + c[mandelbrot_mask]
        mask = np.abs(z) <= 2
        iterations += mandelbrot_mask
        mandelbrot_mask &= mask

    return iterations

def mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter):
    r = np.linspace(xmin, xmax, width)
    i = np.linspace(ymin, ymax, height)
    c = r[:, None] + 1j * i[None, :]
    return mandelbrot(c, max_iter)

# Plotting function
def plot_mandelbrot_and_julia(xmin, xmax, ymin, ymax, width=800, height=800, max_iter=256):
    dpi = 100
    img_width = width / dpi
    img_height = height / dpi

    # Create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(img_width * 2, img_height), dpi=dpi)
    fig.subplots_adjust(wspace=0.3)  # Adjust space between subplots

    # Plot Mandelbrot set
    mandelbrot_image = mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter)
    im1 = ax1.imshow(mandelbrot_image.T, extent=(xmin, xmax, ymin, ymax), cmap='hot', origin='lower')
    ax1.set_facecolor('black')
    ax1.set_title("Mandelbrot Set")
    ax1.set_xlabel("Real numbers")
    ax1.set_ylabel("Imaginary numbers")

    # Initialize Julia set plot
    julia_image = np.zeros((height, width), dtype=int)
    im2 = ax2.imshow(julia_image.T, extent=(-2, 2, -2, 2), cmap='hot', origin='lower', vmin=0.1, vmax=max_iter)
    ax2.set_facecolor('black')
    ax2.set_title("Julia Set")
    ax2.set_xlabel("Real(z)")
    ax2.set_ylabel("Imaginary(z)")

    # Store initial bounds for resetting
    initial_bounds = (xmin, xmax, ymin, ymax)

    # Function to update Mandelbrot set
    def update_mandelbrot(new_xmin, new_xmax, new_ymin, new_ymax):
        nonlocal xmin, xmax, ymin, ymax
        xmin, xmax, ymin, ymax = new_xmin, new_xmax, new_ymin, new_ymax
        mandelbrot_image = mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter)
        im1.set_data(mandelbrot_image.T)
        im1.set_extent((xmin, xmax, ymin, ymax))
        plt.draw()

    # Function to update Julia set
    def update_julia(c):
        julia_image = julia_set(c, -2, 2, -2, 2, width, height, max_iter)
        im2.set_data(julia_image.T)
        im2.set_extent((-2, 2, -2, 2))
        ax2.set_title(f"Julia Set for c = {c:.4f} + {c.imag:.4f}i")
        plt.draw()

    # Function to handle mouse clicks (zoom in)
    def onclick(event):
        if event.inaxes == ax1:  # Check if click is within the Mandelbrot set
            xcenter, ycenter = event.xdata, event.ydata
            xrange = (xmax - xmin) / 4  # Zoom factor
            yrange = (ymax - ymin) / 4

            # Update Mandelbrot set with new bounds
            update_mandelbrot(
                xcenter - xrange, xcenter + xrange,
                ycenter - yrange, ycenter + yrange
            )

    # Function to handle mouse motion (update Julia set)
    def on_motion(event):
        if event.inaxes == ax1:  # Check if mouse is over the Mandelbrot set
            c = complex(event.xdata, event.ydata)
            update_julia(c)

    # Function to reset the plot to initial bounds
    def reset(event):
        update_mandelbrot(*initial_bounds)
        update_julia(complex(-0.7, 0.27015))  # Reset Julia set to default

    # Add a reset button
    ax_reset = plt.axes([0.81, 0.05, 0.1, 0.075])
    btn_reset = Button(ax_reset, 'Reset')
    btn_reset.on_clicked(reset)

    # Connect the click and motion events to the handlers
    fig.canvas.mpl_connect('button_press_event', onclick)
    fig.canvas.mpl_connect('motion_notify_event', on_motion)

    plt.show()

# Initial view of the Mandelbrot set and Julia set
plot_mandelbrot_and_julia(-2.0, 1.0, -1.5, 1.5)
