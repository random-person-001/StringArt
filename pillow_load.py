import PIL.Image as Image
import PIL.ImageMath as Imgmath
import numpy as np

"""Note that the col methods are not used in the current implementation"""


"""
Load a png, and convert it into an np array of 32 bit unsigned floats of [0, 1]
where 0 was where there was black
"""


def get_normalized_img_2d_arr(fpath="test.png"):
    if not fpath.startswith('img/'):
        fpath = 'img/' + fpath
    with Image.open(fpath) as im:
        # perhaps look into Imgmath at some point?
        # change png into 32 bit unsigned float for each pixel
        im = im.convert("F")
        # im.show()
        a = np.asarray(im)
        # print(np.max(a))
        # print(a)
        normalized = a / np.max(a)  # usually 255, probably don't hardcode
        return normalized


"""
Given a 2d np array of unsigned floats in [0,1], seperate each of the columns
and stack them on top of each other to have one really really tall array.

As a side effect, invert the image, so that black is signal and white is 0
"""


def get_image_as_one_np_col(a):
    width = a.shape[0]
    a = 1 - a  # invert so that black is signal and white is 0
    cols = np.hsplit(a, width)  # create a bunch of vertical column arrays
    end = np.vstack(cols)  # put them together to make a very tall array
    return end


def load_img_as_col():
    normalized = get_normalized_img_2d_arr()
    return get_image_as_one_np_col(normalized)


"""
Do the inverse of get_image_as_one_np_col and get_normalized_img_2d_arr
such that given a really really tall 1d array column, split it up to reconstitute
a 2d array. Then make an image from that and show it.

As a side effect, invert the image, so 1 becomes black and 0 becomes white
"""


def convert_col_to_img(a):
    a = 1 - a
    cols = np.vsplit(a, INTERNAL_RES)
    end = np.hstack(cols)
    end *= 255  # todo make nonmagic number
    with Image.fromarray(end) as im:
        im.show()


def convert_2d_to_img(a):
    end = a * 255
    with Image.fromarray(end) as im:
        im.show()
        return im

def save_from_array(a, fname):
    end = a * 255
    with Image.fromarray(end) as im:
        im = im.convert('RGB')
        im.save(fname+'.png', 'PNG')



"""
target = load_img_as_col()
print(target)
convert_col_to_img(target)

"""
