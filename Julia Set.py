import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button #interactive buttons

#julia func
#c = complex num that defines the julia set
#z = complex nm being tested
def julia(c, z, max_iter):#computes whether a complex number z belongs to the Julia set for a given constant c.
    for i in range(max_iter):#max no of iter to determine if z escapes
        z = z * z + c #formula
        if abs(z) > 2:#if magnitude z>2 then it is in infinity
            return i # in that case, it returns i
    return max_iter #if z did not esscape within maxiter it is part of julia set


#julia set func
def julia_set(c, xmin, xmax, ymin, ymax, width, height, max_iter):#[xmin...=bounds of region][width,height = res of output image]
    r = np.linspace(xmin, xmax, width)
    i = np.linspace(ymin, ymax, height)
    z = r[:, None] + 1j * i[None, :] #r[],i[]=reshapes r to clmn vector,reshapes i to row vector
    #1j represents imaginary units
    iterations = np.vectorize(lambda z: julia(c, z, max_iter))(z)
    #applies the julia function to each element of the grid z using np.vectorize.
    #which is a convenience function for applying a scalar function to an array.
    return iterations #returns 2d array of iterations count

#plota julia set
def plot_julia(c, xmin, xmax, ymin, ymax, width=800, height=800, max_iter=256):
    dpi = 100
    img_width = width / dpi
    img_height = height / dpi

    fig, ax = plt.subplots(figsize=(img_width, img_height), dpi=dpi)
    julia_image = julia_set(c, xmin, xmax, ymin, ymax, width, height, max_iter)
    
    # Create a custom colormap: black for the inside, red for the outside
    cmap = plt.cm.hot  #Uses the "hot" colormap (red to yellow) for points that escape.
    cmap.set_under(color='black')  #Sets the color for points that do not escape (i.e., reach max_iter) to black.

    # Plot the Julia set
#im = ax.imshow(...): Displays the Julia set as an image.
#julia_image.T: Transposes the array to match the expected orientation.
#extent=(xmin, xmax, ymin, ymax): Sets the axis limits.
#cmap=cmap: Uses the custom colormap.
#origin='lower': Ensures the y-axis starts at the bottom.
#vmin=0.1, vmax=max_iter: Sets the range for the colormap.
#ax.set_facecolor('black'): Sets the background color of the plot to black.
#plt.title(...): Adds a title to the plot, showing the value of c.
#plt.xlabel(...), plt.ylabel(...): Adds labels for the x-axis (real part) and y-axis (imaginary part).
    im = ax.imshow(julia_image.T, extent=(xmin, xmax, ymin, ymax), cmap=cmap, origin='lower', vmin=0.1, vmax=max_iter)
    ax.set_facecolor('black')
    plt.title("Julia Set")
    plt.xlabel("Real(z)")
    plt.ylabel("Imaginery(z)")

    # Store the initial bounds for resetting
    initial_bounds = (xmin, xmax, ymin, ymax)

    # Function to update the plot
    def update_plot(new_xmin, new_xmax, new_ymin, new_ymax):
        nonlocal xmin, xmax, ymin, ymax
        xmin, xmax, ymin, ymax = new_xmin, new_xmax, new_ymin, new_ymax #recomputes the julia set for new bounds
        julia_image = julia_set(c, xmin, xmax, ymin, ymax, width, height, max_iter)
        im.set_data(julia_image.T)#updates image data
        im.set_extent((xmin, xmax, ymin, ymax))#updates axis limits
        plt.draw()#redraw

    # Function to handle mouse clicks (zoom in)
    def onclick(event):
        if event.inaxes == ax: #checks if click is inside the region
            xcenter, ycenter = event.xdata, event.ydata #coordinates of x nd y
            xrange = (xmax - xmin) / 4  # Zoom factor
            yrange = (ymax - ymin) / 4  # Zooms in by a factor of 4

            # Update the plot with new bounds
            update_plot(
                xcenter - xrange, xcenter + xrange,
                ycenter - yrange, ycenter + yrange
            )

    # Function to reset the plot to initial bounds
    def reset(event):
        update_plot(*initial_bounds)

    # Add a reset button
    ax_reset = plt.axes([0.81, 0.05, 0.1, 0.075])
    btn_reset = Button(ax_reset, 'Reset')
    btn_reset.on_clicked(reset)

    # Connect the click event to the handler
    fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()

# Parameters for the Julia set
c = complex(-0.7, 0.27015)  # Example value for c
xmin, xmax = -2, 2
ymin, ymax = -2, 2

# Initial view of the Julia set
plot_julia(c, xmin, xmax, ymin, ymax)
