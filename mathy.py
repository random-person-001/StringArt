import math
import numpy as np
import PIL.Image
import PIL.ImageDraw

from line_profiler_pycharm import profile

'''
A collection of math-heavy utility methods
'''




@profile
def add_darkness_from_line(nail_1_x, nail_1_y, nail_2_x, nail_2_y, canvas, drawable, output_arr, darkness):
    # zero it out
    canvas.paste(im=0, box=((0, 0, canvas.width, canvas.width)))

    # draw a fat, lighter line, and then a skinny stronger line. This is a jagged step dropoff instead of a linear one.
    width = canvas.width // 60
    fill = 127
    drawable.line(((nail_1_x, nail_1_y), (nail_2_x, nail_2_y)), fill=fill, width=width)
    width = canvas.width // 200
    fill = 255
    drawable.line(((nail_1_x, nail_1_y), (nail_2_x, nail_2_y)), fill=fill, width=width)

    output_arr = np.asarray(canvas)
    # print(output_arr)
    return output_arr * (darkness / 255)
    #
    # canvas.show()
    #return output_arr

