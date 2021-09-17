"""
Week 1 practice project template for Python Data Visualization
Load a county-level PNG map of the USA and draw it using matplotlib
"""

import matplotlib.pyplot as plt

# Houston location

USA_SVG_SIZE = [555, 352]
HOUSTON_POS = [302, 280]


def draw_USA_map(map_name):
    """
    Given the name of a PNG map of the USA (specified as a string),
    draw this map using matplotlib
    """

    # Load map image, note that using 'rb'option in open() is critical since png files are binary
    with open(map_name, 'rb') as f:
        map_img = plt.imread(f)

    #  Get dimensions of USA map image
    y_length, x_length, num_band = map_img.shape
    print(y_length, x_length, num_band)

    # Optional code to resize plot as fixed size figure -
    DPI = 80.0                  # adjust this constant to resize your plot
    xinch = x_length / DPI
    yinch = y_length / DPI
    plt.figure(figsize=(xinch,yinch))

    # Plot USA map
    plt.imshow(map_img)

    # Plot green scatter point in center of map
    x_center = x_length/2
    y_center = y_length/2
    plt.scatter(
        x=x_center,
        y=y_center,
        s=100,
        c='Green'
    )

    # Plot red scatter point on Houston, Tx - include code that rescale coordinates for larger PNG files
    x_pos = HOUSTON_POS[0] / USA_SVG_SIZE[0] * x_length
    y_pos = HOUSTON_POS[1] / USA_SVG_SIZE[1] * y_length
    plt.scatter(
        x=x_pos,
        y=y_pos,
        s=100,
        c='red'
    )

    plt.show()


# draw_USA_map("USA_Counties_555x352.png")
draw_USA_map("USA_Counties_1000x634.png")
