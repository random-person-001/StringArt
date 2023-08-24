import math
import numpy as np
import PIL.Image
import PIL.ImageDraw

# from line_profiler_pycharm import profile

'''
A collection of math-heavy utility methods
'''

pregenned_chords = dict()

def pregen_chords(nails, coords, r, line_darkness):
    # populate my dict `pregenned_chords` with every key `(start nail, end nail)` and corresponding
    # value `numpy array of the overlay made from that`
    import PIL.Image
    import PIL.ImageDraw
    canvas = PIL.Image.new(mode="F", size=(int(r * 2), int(r * 2)), color=255)
    drawable = PIL.ImageDraw.Draw(canvas)

    for start_nail in range(nails):
        for end_nail in range(nails):
            if start_nail < end_nail and (start_nail, end_nail) not in pregenned_chords:
                # zero out our canvas
                canvas.paste(im=0, box=(0, 0, canvas.width, canvas.width))

                # draw a fat, lighter line, and then a skinny stronger line. This is a jagged step dropoff instead of a linear one.
                width = canvas.width // 60
                fill = 127
                drawable.line((coords[start_nail], coords[end_nail]), fill=fill, width=width)
                width = canvas.width // 200
                fill = 255
                drawable.line((coords[start_nail], coords[end_nail]), fill=fill, width=width)
                output_arr = np.asarray(canvas)
                pregenned_chords[(start_nail, end_nail)] = output_arr * (line_darkness / 255)


def add_darkness_from_line_pregen(start_nail, end_nail):
    if end_nail < start_nail:
        # reorder cuz we only store them in ascending order; the other half is redundant
        start_nail, end_nail = end_nail, start_nail
    return pregenned_chords[(start_nail, end_nail)]

# @profile
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

