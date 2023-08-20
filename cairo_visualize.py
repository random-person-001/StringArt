import cairo
import random
import math

# cairo coordinates start in top left, and going down and right is positive

        
def visualize_path(path, coords, resolution, fname='stringartrender.png'):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, resolution, resolution)
    ctx = cairo.Context(surface)
    #ctx.scale(2*radius, 2*radius)

    # occasionally we want to render at a higher rez than the input picture
    scale = resolution / coords[0][0] 
    coords = {i: (coords[i][0]*scale, coords[i][1]*scale) for i in range(len(coords))}

    # ctx.save()
    ctx.set_source_rgba(1, 1, 1, 1)
    ctx.paint()
    # ctx.restore()

    ctx.set_source_rgba(0,0,0,.2)
    ctx.set_line_width(2)

    previous_point = coords[0]
    ctx.move_to(*coords[0])
    for point in path:
        x = coords[point][0]
        y = coords[point][1]
        ctx.move_to(*previous_point)
        ctx.line_to(x,y)
        ctx.stroke()
        #print(x)
        previous_point = x,y
    # ctx.close_path()
    # ctx.show_page()
    print("Image built, now saving")
    surface.write_to_png(fname+'.png')
    print("png saved")

'''
# make a random drawing
if __name__ == '__main__':
    NAILS = 300
    THETA_STEP = 2*math.pi / NAILS
    R=800
    STRING_COUNT = 500
    COORDS = {n: (R+R*math.cos(n*THETA_STEP), R+R*math.sin(n*THETA_STEP)) for n in range(NAILS)}
    path = []
    for i in range(STRING_COUNT
                   ):
        path.append(random.randrange(0, NAILS))
    visualize_path(path, COORDS, R)
'''

# draw a specific path
if __name__ == '__main__':
    path = [0, 48, 76, 45, 93, 33, 89, 56, 12, 57, 14, 64, 35, 32, 35, 32, 67, 24, 75, 24, 75, 24, 75, 24, 75, 24, 75, 0, 17, 82, 17, 82, 17, 82, 17, 82, 17, 9, 68, 65, 1, 98, 1, 98, 1, 98, 1, 98, 1, 71, 28, 71, 28, 50, 48, 20, 55, 54, 55, 23, 76, 23, 76, 23, 43, 39, 37, 36, 37, 36, 37, 36, 37, 36, 63, 61, 16, 10, 14, 85, 89, 91, 89, 88, 11, 88, 11, 88, 11, 88, 11, 88, 11, 88, 11, 50, 21, 78, 21, 78, 21, 78, 21, 78, 21, 78, 21, 78, 21, 78, 21, 78, 21, 78, 21, 78, 21, 78, 21, 78, 21, 78, 21, 51, 56, 59, 97, 2, 68, 4, 69, 30, 69, 30, 69, 30, 69, 30, 69, 30, 69, 30, 69, 30, 69, 30, 69, 30, 69, 30, 69, 30, 69, 30, 69, 30, 69, 30, 69, 16, 17, 82, 17, 82, 17, 82, 17, 82, 17, 82, 17, 82, 17, 82, 17, 82, 17, 82, 17, 82, 17, 50, 48, 43, 44, 43, 44, 43, 39, 42, 40, 41, 40, 41, 40, 41, 40, 41, 40, 41, 40, 41, 40, 41, 40, 35, 32, 30, 69, 30, 69, 5, 61, 57, 58, 57, 96, 3, 96, 3, 96, 3, 96, 3, 96, 3, 96, 3, 96, 3, 96, 3, 71, 28, 71, 28, 71, 28, 71, 28, 71, 28, 71, 17, 82, 17, 82, 17, 82, 17, 82, 17, 82, 17, 82, 17, 82, 17, 51, 21, 78, 21, 78, 21, 78, 21, 78, 21, 78, 21, 78, 21, 78, 21, 52, 22, 52, 22, 17, 82, 17, 82, 17, 18, 81, 18, 81, 18, 81, 18, 81, 18, 81, 18, 81, 18, 81, 18, 81, 18, 81, 18, 81, 18, 81, 18, 81, 18, 81, 95, 94, 95, 94, 59, 56, 57, 58, 57, 58, 57, 58, 57, 21, 78, 21, 78, 21, 78, 21, 78, 21, 78, 21, 78, 21, 18, 81, 18, 81, 18, 81, 18, 81, 91, 95, 94, 95, 94, 95, 4, 21, 78, 21, 78, 21, 50, 25, 74, 25, 74, 25, 74, 25, 74, 25, 74, 25, 74, 25, 74, 25, 74, 25, 74, 25, 49, 25, 74, 25, 74, 25, 49, 48, 43, 39, 37, 36, 37, 36, 37, 36, 37, 36, 37, 36, 63, 60, 96, 3, 96, 3, 96, 3, 96, 3, 96, 3, 96, 3, 16, 10, 14, 85, 14, 11, 88, 11, 88, 11, 88, 11, 88, 11, 88, 11, 88, 11, 88, 11, 88, 11, 88, 11, 88, 11, 88, 11, 88, 11, 13, 12, 13, 67, 1, 98, 1, 98, 1, 98, 1, 68, 18, 81, 18, 81, 18, 81, 18, 81, 18, 81, 18, 81, 18, 81, 18, 81, 18, 81, 18, 81, 18, 81, 18, 81, 18, 81, 18, 81, 18, 81, 18, 81, 18, 81, 18, 81, 18, 81, 18, 81]
    NAILS = 99
    STRING_COUNT = 500
    LINE_DARKNESS = 0.1
    THETA_STEP = 2*math.pi / NAILS
    R = 1600
    COORDS = {n: (R+R*math.cos(n*THETA_STEP), R+R*math.sin(n*THETA_STEP)) for n in range(NAILS)}
    visualize_path(path, COORDS, R)
