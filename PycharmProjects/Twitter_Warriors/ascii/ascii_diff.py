'''
1. Make Dict of Images for each character
2. Take in Image to Convert
    - take in image piece.
3. Run image piece against char dict with smallest difference.
4. Print char image with smallest difference to console.

'''
from PIL import Image, ImageChops, ImageStat, ImageOps

def resize_image(im):
    '''
    this takes in an image and blows it up so that it will fit an 80 character string
    '''
    im_w = im.size[0]
    im_h = im.size[1]

    new_im_height = (im_h * 400)/im_w
    new_height_rem = new_im_height%12
    new_im_height = new_im_height - new_height_rem

    im = ImageOps.fit(im,(400, new_im_height),Image.ANTIALIAS)
    return im

def char_dict():
    '''
    takes char images and appends them to
    '''
    chars = dict()
    for i in range(32,127):
        im = Image.open('..//ascii//fonts//'+str(i)+'.png')
        im = im.convert("L")
        chars[i] = im
    return chars

def image_list(file):
    im = Image.open(file)

    im = resize_image(im)
    im = im.convert("L")

    im = ImageOps.autocontrast(im)
    im = ImageOps.equalize(im)

    images = []
    yo = 0
    for y in range(im.size[1]/12):
        xo = 0
        for x in range(im.size[0]/8):
            image_piece = im.crop((xo,yo,8*(x+1),12*(y+1)))

            images.append(image_piece)

            xo += 8
        yo +=12
    return images

def image_diff(filename):
    image_string = ""
    i = 0
    for im in image_list(filename):

        current_key = 2
        chars = char_dict()

        diff_old = 5000
        for key, char_im in chars.iteritems():
            #print key
            diff_im = ImageChops.difference(im,char_im)
            stat_im = ImageStat.Stat(diff_im)

            diff_var = stat_im.mean[0]

            if diff_var < diff_old:
                diff_old = diff_var
                current_key = key
        #print chr(current_key)
        image_string += chr(current_key)
        i+=1
        if i == 50:
            i=0
            image_string += "\n"
    return image_string

