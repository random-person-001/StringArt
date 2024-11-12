import numpy as np
import math
import time

import pillow_load
import mathy


"""
TWEAK ME!

Using more nails than `pixel width of input image / 2` is generally superflous I think
"""
NAILS = 187
STRING_COUNT = 4200
LINE_DARKNESS = 0.03  # this is based on real world values, through trial and error
TARGET_FILENAME = "rfe2-185.png"
ENABLE_PROFILER = False

# 4ish gb ram with 150 nails at 300x300 pixel inputs, but scales quadratically!!!!!
# Memory - O(pixels^2 * nails^2)
# This doubles speed at 128x128px with 150 nails and 1800 strings, and will make an
# even greater impact with more strings
# global I_HAVE_MANY_GB_OF_RAM_IM_OK_WITH_USING_TO_MAKE_PROGRAM_GO_FASTER
I_HAVE_MANY_GB_OF_RAM_IM_OK_WITH_USING_TO_MAKE_PROGRAM_GO_FASTER = True
"""
End of tweak me area
3700 strings -> line darkness = 0.03


"""


if ENABLE_PROFILER:  # aka we're in pycharm
    from line_profiler_pycharm import profile
else:
    import cairo_visualize


""" Procedure:
load black and white image (could crop outside circle but I don't think
that matters) - this is our Reference

Create a list that holds the indicies of the points we've been to

If the user has indicated they have a lot of ram available and are interested
  in speeding up the algorithm, we will pregenerate some stuff. Specifically, the
  raster representation [numpy array] of every possible chord. Doing it only once, 
  at the beginning, means we go much faster for when we draw lots of lines. 

Create a raster of same pixel dimensions as reference, all white. Whenever
  we find the best line from a nail and want to move on to the next one now,
  we update this raster to be darker along the chord we just drew. Call this 
  raster `Jimmy`

To determine where the next line is drawn from this peg, test each potential
connection:
    - add the potential line to Jimmy (but dont save as Jimmy). Some math close to 
      subtracting Jimmy from the Reference is used for a score, and we run with the 
      potential line that has the best (lowest) score

"""

# default coordinate systems origin:
#  pillow: top left
#  cairo: top left
# so when viewing any intermediate data, invert the y! (y=resolution-y)

target = pillow_load.get_normalized_img_2d_arr(TARGET_FILENAME)
R = target.shape[0] / 2

THETA_STEP = 2 * math.pi / NAILS
COORDS = {
    n: (R + R * math.cos(n * THETA_STEP), R + R * math.sin(n * THETA_STEP))
    for n in range(NAILS)
}
path = []  # this is the sequence of nail indicies to connect that create our end image


def pregen_if_applicable():
    """
    Pregenerates the raster representations of every possible chord combination, if user has opted
    to enable this, which can help speed execution.

    SIDE EFFECTS: This halts execution and requires user confirmation if the estimated RAM usage will
    be at a potentially hazardous level
    Also prints out some nice info about what it's doing.
    :return:
    """
    global I_HAVE_MANY_GB_OF_RAM_IM_OK_WITH_USING_TO_MAKE_PROGRAM_GO_FASTER
    if I_HAVE_MANY_GB_OF_RAM_IM_OK_WITH_USING_TO_MAKE_PROGRAM_GO_FASTER:
        chord_count = (NAILS * (NAILS - 1)) / 2
        # chords * pixel/array size for each (width x width) * 4 bytes/px * convert to gb
        estimated_gb_ram = chord_count * (R * 2) ** 2 * 4 / 1024 / 1024 / 1024
        print(
            f"Pregenning {int(chord_count)} chords. Estimated ram usage: {estimated_gb_ram:.2f}GB"
        )
        if estimated_gb_ram > 6:
            response = input(
                "Are you really sure you are ok with this? To continue with the pregeneration, press y; any other key will revert to the other method. > "
            )
            if response != "y" and response != "Y":
                I_HAVE_MANY_GB_OF_RAM_IM_OK_WITH_USING_TO_MAKE_PROGRAM_GO_FASTER = False
                return
        start_time = time.monotonic()
        mathy.pregen_chords(NAILS, COORDS, R, LINE_DARKNESS)
        print(
            f"Pregeneration of chords took {time.monotonic() - start_time:.3f} seconds"
        )


def calc_score(prospective):
    """
    :param prospective: numpy array to compare to the target image/array
    :return: a scalar indicating how far the prospective state is from our target. Lower is better.
    """
    return np.square(target - prospective).sum()


#  @profile
def main():
    print("running!")
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

    jimmy = np.ones(target.shape, dtype="float32")
    overlay = np.ones(target.shape, dtype="float32")
    start_nail = 0
    path.append(start_nail)

    loop_start_time = time.monotonic()

    for i in range(STRING_COUNT):
        if i % 256 == 0:
            print(f"Progress: {i/STRING_COUNT:2.0%}")
            if i == 256*2:
                elapsed_s = time.monotonic() - loop_start_time
                print(f"Estimated time remaining: {STRING_COUNT/i * elapsed_s:2.0f} seconds")
        best_score_this_round = target.shape[0] ** 3  # an arbitrarily high number
        best_scoring_nail = 0
        for end_nail in range(NAILS):
            if end_nail == start_nail:
                pass
            else:
                # mutate the overlay array
                if I_HAVE_MANY_GB_OF_RAM_IM_OK_WITH_USING_TO_MAKE_PROGRAM_GO_FASTER:
                    overlay = mathy.add_darkness_from_line_pregen(start_nail, end_nail)
                else:
                    overlay = mathy.add_darkness_from_line(
                        *COORDS[start_nail],
                        *COORDS[end_nail],
                        canvas,
                        drawable,
                        overlay,
                        LINE_DARKNESS,
                    )
                # print(overlay)
                # print(jimmy)
                # print('\n\n')
                score = calc_score(jimmy * (1 - overlay))
                if score < best_score_this_round:
                    best_score_this_round = score
                    best_scoring_nail = end_nail

        if I_HAVE_MANY_GB_OF_RAM_IM_OK_WITH_USING_TO_MAKE_PROGRAM_GO_FASTER:
            overlay = mathy.add_darkness_from_line_pregen(start_nail, best_scoring_nail)
        else:
            overlay = mathy.add_darkness_from_line(
                *COORDS[start_nail],
                *COORDS[best_scoring_nail],
                canvas,
                drawable,
                overlay,
                LINE_DARKNESS,
            )
        jimmy = jimmy * (1 - overlay)
        # print(jimmy)
        path.append(best_scoring_nail)
        # print(best_scoring_nail)
        start_nail = best_scoring_nail

    print(path)
    
    def fname(info1):
        return f"img/{TARGET_FILENAME}-stringed-{NAILS}-nails-{STRING_COUNT}-strings-{LINE_DARKNESS}-darkness-{info1}"
    pillow_load.save_from_array(jimmy, fname('jimmy'))  # what the algorithm thought it acheived
    if not ENABLE_PROFILER:
        cairo_visualize.visualize_path(path, COORDS, 1600, fname("string-detail"))  # high rez


if __name__ == "__main__":
    start_time = time.monotonic()
    main()
    print(f"Execution took {time.monotonic() - start_time:.3f} seconds")
    # del mathy.pregenned_chords
    total_length = mathy.get_total_string_length(path, COORDS) / R  # now length is in terms of circle radii
    feet_to_meters = 0.3048
    # a 3000 yd cone/spool of Overlocker/Overlocking thread is on the order of $10 or less!
    print(f"With a two-foot diameter circle, this would take {total_length/feet_to_meters:.0f} meters of string")
