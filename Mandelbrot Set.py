import numpy as np #numerical computations
import matplotlib.pyplot as plt #visualizations
from matplotlib.widgets import Button #interactive buttons in plot

# manderbrot func
def mandelbrot(c, max_iter):#complex number & max iter
    z = np.zeros_like(c, dtype=np.complex128)#initialized as an array of zeros with the same shape as c
    #datatype:complex128 specifies dtype as complex num with 128 bit floating point
    mandelbrot_mask = np.ones_like(c, dtype=bool)# boolean array initialized to True.
    #keeps track of which points are still being iterated(magnitude <= to 2).
    iterations = np.zeros_like(c, dtype=int)#number of iterations it takes for each point to escape the Mandelbrot set.


    for i in range(max_iter):
        z[mandelbrot_mask] = z[mandelbrot_mask] * z[mandelbrot_mask] + c[mandelbrot_mask] #updates z using
#zn+1=zn**2+(for points that are still being iterated ,where mandelbrot_mask is True).
        mask = np.abs(z) <= 2 #checks points with magnitude <=2
        iterations += mandelbrot_mask #increments the iteration count for points that are still being iterated.
        mandelbrot_mask &= mask #updates the mask to exclude points that have escaped (their magnitude exceeds 2).

    return iterations # no of iterations took for each point to escape ms

#manderbrotset func
def mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter): #generates ms with real (x) and imaginery (y) values
    #[width,height = res of output image]
    r = np.linspace(xmin, xmax, width) #array of real nums using linspace
    i = np.linspace(ymin, ymax, height) #array of imag nums using linspace
    c = r[:, None] + 1j * i[None, :]# creates 2d grid of complex nums(combining real and imag parts)
    ##r[],i[]=reshapes r to clmn vector,reshapes i to row vector
    #1j represents imaginary units
    return mandelbrot(c, max_iter)

#plotting func
def plot_mandelbrot(xmin, xmax, ymin, ymax, width=800, height=800, max_iter=256):
    dpi = 100 #dots per inch (determines resolution)
    img_width = width / dpi #calculates size of the plot in inches based on given width and height in pixels.
    img_height = height / dpi

    fig, ax = plt.subplots(figsize=(img_width, img_height), dpi=dpi)#creates a figure and axis for the plot.
    mandelbrot_image = mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter)#func call to compute ms set
    im = ax.imshow(mandelbrot_image.T, extent=(xmin, xmax, ymin, ymax), cmap='hot', origin='lower')
    #imshow displays the image of ms set
    #T transposes the array to match the orientation
    #extent sets the limits
    #cmap for colorma-Uses the "hot" colormap (red to yellow) for points that escape.
    #orgin ensures y axis starts at the bottom 
    ax.set_facecolor('black') #bg color
    plt.title("Mandelbrot Set") #title
    plt.xlabel("Real numbers")#xaxis
    plt.ylabel("Imaginary numbers")#yaxis

    # Store the initial bounds for resetting later
    initial_bounds = (xmin, xmax, ymin, ymax)

    # Func to update the plot
    def update_plot(new_xmin, new_xmax, new_ymin, new_ymax):#updates plot with new bounds
        nonlocal xmin, xmax, ymin, ymax #nonlocal is used to modify the outer function's variables
        xmin, xmax, ymin, ymax = new_xmin, new_xmax, new_ymin, new_ymax
        mandelbrot_image = mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter) #ecomputes the set for the new bounds.
        im.set_data(mandelbrot_image.T)#Updates the image data
        im.set_extent((xmin, xmax, ymin, ymax))#Updates the axis limits
        plt.draw()#ms is recomputed for new bounds, the image and axis limits are updated(redraws the plot)

    # Func to handle mouse clicks (zoom in)
    def onclick(event):
        if event.inaxes == ax:#Checks if the click is within the plot area.
            xcenter, ycenter = event.xdata, event.ydata #Gets the coordinates of the click.
            xrange = (xmax - xmin) / 4  # Zoom factor
            yrange = (ymax - ymin) / 4  #zooms in by a factor of 4

            # Update the plot with new bounds
            update_plot(
                xcenter - xrange, xcenter + xrange,
                ycenter - yrange, ycenter + yrange
            )

    # Func to reset the plot to initial bounds
    def reset(event):
          update_plot(*initial_bounds)

     # Add a reset button
    ax_reset = plt.axes([0.81, 0.05, 0.1, 0.075])#creates new axis for reset button
    btn_reset = Button(ax_reset, 'Reset')#creates button
    btn_reset.on_clicked(reset)#links the btn to the reset func


    fig.canvas.mpl_connect('button_press_event', onclick)#links the onclick function to mouse click events.
    plt.show()

# Initial view of the Mandelbrot set
plot_mandelbrot(-2.0, 1.0, -1.5, 1.5)
