import math

from line_profiler_pycharm import profile

'''
A collection of math-heavy utility methods
'''

@profile
def x_intersect_of_lines(pixel_x, pixel_y, line_start_x, line_start_y, slope):
    # x1, y1 are the pixel
    x1, y1 = pixel_x, pixel_y
    # x2, y2 are a point on the prospective line. This line has the slope `m`
    x2, y2 = line_start_x, line_start_y
    m = slope
    # return (1+slope**2)**-1 * (pixel_y + slope**2 + slope*( pixel_y - line_start_y + line_start_x))
    if slope != 'inf':
        return (x2*m**2 + m*y1 - m*y2 + x1) / (m**2+1)
    return line_start_x
    

# pixel x and y are start corner (bottom left)
@profile
def line_distance_from_pixel(pixel_x, pixel_y, line_start_x, line_start_y, line_slope):
    # get a point-slope form from the pixle, and
    # get an equation for the line, and
    # set the y coords to be equal, solve for x
    x = x_intersect_of_lines(pixel_x, pixel_y, line_start_x, line_start_y, line_slope)

    # in this space, we allow for a shallow tangent line to extend past the outside of the
    # circle. The closest point on that line will be beyond either of its endpoints, and
    # the pixel distance will calculate based on that flawed false distance.
    # Effects on a large picture should be minimal, but this yeilds strange artefacts
    # on small images, and drawing outside the circle.
    
    if line_slope == 'inf':
        return abs(pixel_x - line_start_x)
    
    # y-y1 = m(x-x1), point-slope form
    # this completes our knowledge of x,y of the point on the line that is closest to the pixel
    y = line_start_y + line_slope*(x-line_start_x)
    if abs(x-line_start_x) < 0.000000001: # imprecisions kill this. Would polar graphs work better?
        y = pixel_y
    # measure distance between pixel and that intersection point
    # pythag time
    # dist**2 = deltaX**2 + deltaY**2
    dist = ( (x-(pixel_x))**2 + (y-(pixel_y))**2 )**0.5
    return dist

@profile
def line_darkness_at(line_darkness, distance):
    # a trapazoid, with a radius of 0.5 about distance=0, and output within that radius equal to LINE_DARKNESS
    # between the edge of that plateau and a distance of 1 further, there is a linear dropoff
    # before being 0 everywhere else
    if distance <= 0.5:
        return line_darkness
    elif 0.5 < distance and distance < 1.5:
        return -1*line_darkness * (distance-1.5)
    else:
        return 0

@profile
def add_darkness_from_line(nail_1_x, nail_1_y, nail_2_x, nail_2_y, output_arr, darkness):
    if nail_2_x - nail_1_x == 0:
        line_slope = 'inf' 
    else:
        line_slope = (nail_2_y - nail_1_y) / (nail_2_x - nail_1_x)

    # orig = output_arr.copy()
    for pixel_y in range(output_arr.shape[0]): 
        for pixel_x in range(output_arr.shape[1]):
            output_arr[pixel_y][pixel_x] = line_darkness_at(darkness, line_distance_from_pixel(pixel_x, pixel_y, nail_1_x, nail_1_y, line_slope))
    # print(orig == output_arr)
        
