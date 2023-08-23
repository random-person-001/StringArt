import numpy as np
import math

import pillow_load
import mathy
# import cairo_visualize

from line_profiler_pycharm import profile

''' Procedure:
load bw 1000px wide image (potentially crop outside circle but I don't think
that matters) - this is our Reference

Create a list that holds the indicies of the points we've been to
Create a raster of same pixel dimensions as reference, all white. Whenever
  we find the best line from a nail and want to move on to the next one now,
  we update this raster with how we're looking now. Call it Jimmy

To determine where the next line is drawn from this peg, test each potential
connection:
    - add the potential line to Jimmy (but dont save as Jimmy). Subtract
      Jimmy from the Reference for a score, and run with the potential
      line that has the best (lowest) score

Calculating score:
currently dumb and slow, to improve. Measures how far apart the images are
'''

# default coordinate systems origin:
#  pillow: top left
#  cairo: top left
# so when viewing intermediate data, invert the y! (y=resolution-y)

target = pillow_load.get_normalized_img_2d_arr('test4.png')

R = target.shape[0]/2
NAILS = 99
STRING_COUNT = 600
LINE_DARKNESS = 0.1
THETA_STEP = 2*math.pi / NAILS

COORDS = {n: (R+R*math.cos(n*THETA_STEP), R+R*math.sin(n*THETA_STEP)) for n in range(NAILS)}
path = []

# compare a prospective array state (from some candidate string path)
# and generate a scalar score for how good it is, compared to `target`
def calc_score(prospective):
    score = 0
    score = np.square(target - prospective).sum()
    return score
    

def main():
    print('running!')
    # Meet jimmy. jimmy is how our solution is looking so far. Every time
    # we find a chord we determine is best, we add its result into jimmy,
    # and then move along testing the next potential chord candidates

    jimmy = np.ones(target.shape, dtype='float32')
    overlay = np.ones(target.shape, dtype='float32')
    start_nail = 0
    path.append(start_nail)

    for i in range(STRING_COUNT):
        best_score_this_round = target.shape[0]**3 # an arbitrarily high number
        best_scoring_nail = 0
        for end_nail in range(NAILS):
            #overlay.fill(0)
            if end_nail == start_nail:
                pass
            else:
                # mutate the overlay array
                mathy.add_darkness_from_line(*COORDS[start_nail], *COORDS[end_nail], overlay, LINE_DARKNESS)
                # print(overlay)
                score = calc_score((jimmy)*(1-overlay))
                if score < best_score_this_round:
                    best_score_this_round = score
                    best_scoring_nail = end_nail
        # mutate jimmy
        #print(jimmy)
        #orig = jimmy.copy()
        #overlay.fill(0)
        mathy.add_darkness_from_line(*COORDS[start_nail], *COORDS[best_scoring_nail], overlay, LINE_DARKNESS)
        jimmy = jimmy*(1-overlay)
        #print(jimmy)
        #print(jimmy == orig)
        path.append(best_scoring_nail)
        #print(best_scoring_nail)
        start_nail = best_scoring_nail

    print(path)
    print('\n last overlay=')
    print(overlay)
    print('\n target=')
    print(target)
    print('\n jimmy=')
    print(jimmy)
    cairo_visualize.visualize_path(path, COORDS, target.shape[0], fname='cairo-low-res')
    pillow_load.convert_2d_to_img(jimmy) # invert so black is where we drew and white is where we didn't
    cairo_visualize.visualize_path(path, COORDS, 1600, fname='cairo-high-res')

if __name__ == '__main__':
    main()