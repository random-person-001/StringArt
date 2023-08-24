import numpy as np
import math
import time

import pillow_load
import mathy

IN_PYCHARM = False

# 4ish gb ram with 150 nails at 300x300 pixel inputs, but scales quadratically!!!!!
# global I_HAVE_MANY_GB_OF_RAM_IM_OK_WITH_USING_TO_MAKE_PROGRAM_GO_FASTER
I_HAVE_MANY_GB_OF_RAM_IM_OK_WITH_USING_TO_MAKE_PROGRAM_GO_FASTER = True

if IN_PYCHARM:
    from line_profiler_pycharm import profile
else:
    import cairo_visualize


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

target = pillow_load.get_normalized_img_2d_arr('bumble128.png')

R = target.shape[0]/2
NAILS = 180
STRING_COUNT = 1800
LINE_DARKNESS = 0.06
THETA_STEP = 2*math.pi / NAILS

COORDS = {n: (R+R*math.cos(n*THETA_STEP), R+R*math.sin(n*THETA_STEP)) for n in range(NAILS)}
path = []


def pregen_if_applicable():
    global I_HAVE_MANY_GB_OF_RAM_IM_OK_WITH_USING_TO_MAKE_PROGRAM_GO_FASTER
    if I_HAVE_MANY_GB_OF_RAM_IM_OK_WITH_USING_TO_MAKE_PROGRAM_GO_FASTER:
        chord_count = (NAILS * (NAILS-1)) / 2
        # chords * pixel/array size for each (width x width) * 4 bytes/px * convert to gb
        estimated_gb_ram = chord_count * (R*2)**2 * 4 / 1024 / 1024 / 1024
        print(f"Pregenning chords. Estimated ram usage: {estimated_gb_ram:.2f}GB")
        if estimated_gb_ram > 6:
            response = input("Are you really sure you are ok with this? To continue with the pregeneration, press y; any other key will revert to the other method. > ")
            if response != 'y' and response != 'Y':
                I_HAVE_MANY_GB_OF_RAM_IM_OK_WITH_USING_TO_MAKE_PROGRAM_GO_FASTER = False
                return                
        start_time = time.monotonic()
        mathy.pregen_chords(NAILS, COORDS, R, LINE_DARKNESS)
        print(f"Pregeneration of chords took {time.monotonic() - start_time:.3f} seconds")


    
# compare a prospective array state (from some candidate string path)
# and generate a scalar score for how good it is, compared to `target`
def calc_score(prospective):
    score = 0
    score = np.square(target - prospective).sum()
    return score
    
# @profile
def main():
    print('running!')
    pregen_if_applicable()

    if not I_HAVE_MANY_GB_OF_RAM_IM_OK_WITH_USING_TO_MAKE_PROGRAM_GO_FASTER:
        import PIL.Image
        import PIL.ImageDraw
        canvas = PIL.Image.new(mode="F", size=(int(R * 2), int(R * 2)), color=255)
        drawable = PIL.ImageDraw.Draw(canvas)
    else:
        canvas, drawable = None, None

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
                if I_HAVE_MANY_GB_OF_RAM_IM_OK_WITH_USING_TO_MAKE_PROGRAM_GO_FASTER:
                    overlay = mathy.add_darkness_from_line_pregen(start_nail, end_nail)
                else:
                    overlay = mathy.add_darkness_from_line(*COORDS[start_nail], *COORDS[end_nail], canvas, drawable, overlay, LINE_DARKNESS)
                #print(overlay)
                #print(jimmy)
                #print('\n\n')
                score = calc_score((jimmy)*(1-overlay))
                if score < best_score_this_round:
                    best_score_this_round = score
                    best_scoring_nail = end_nail
        # mutate jimmy
        #print(jimmy)
        #orig = jimmy.copy()
        #overlay.fill(0)
        
        if I_HAVE_MANY_GB_OF_RAM_IM_OK_WITH_USING_TO_MAKE_PROGRAM_GO_FASTER:
            overlay = mathy.add_darkness_from_line_pregen(start_nail, best_scoring_nail)
        else:
            overlay = mathy.add_darkness_from_line(*COORDS[start_nail], *COORDS[best_scoring_nail], canvas, drawable, overlay, LINE_DARKNESS)
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
    pillow_load.convert_2d_to_img(jimmy) 
    cairo_visualize.visualize_path(path, COORDS, 1600, fname='cairo-high-res')

if __name__ == '__main__':
    start_time = time.monotonic()
    main()
    print(f"Execution took {time.monotonic() - start_time:.3f} seconds")
