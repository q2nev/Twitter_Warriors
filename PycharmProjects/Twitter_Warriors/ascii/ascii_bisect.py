from PIL import Image, ImageStat
from bisect import bisect
import random
import sys
import pickle

def processImage(infile): #this file converts a gif to png and exports the first instance as foo0.png
    try:
        im = Image.open(infile)
        if infile[-4:]=='.jpg':
            return im
    except IOError:
        print "Cant load", infile
        sys.exit(1)
    i = 0
    mypalette = im.getpalette()
    try:
        while 1:
            im.putpalette(mypalette)
            new_im = Image.new("RGBA", im.size)
            new_im.paste(im)
            new_im.save('new'+str(i)+'.png')

            i += 1
            im.seek(im.tell() + 1)

    except EOFError:
        pass # end of sequence

def char_greydict():
    '''
    function takes in each image in a library and returns an average greyscale value for that image
    '''
    chars = dict()
    for i in range(32,126):
        im = Image.open('..//ascii//fonts//'+str(i)+'.png')
        im = im.convert("L")
        stat = ImageStat.Stat(im)
        chars[stat.mean[0]] = chr(i)

    return chars

def infile_give(gang):
    '''
    Input: .gif file
    Ouput: str representation of image in Ascii

    infile: path to image
    processImage: function convert gif to jpg

    '''
    im = Image.open('..//ascii//'+gang)

    #calculate image resize factors based on input image.
    im_w = im.size[0]
    im_h = im.size[1]
    new_w = 60*im_w/im_h

    #learn BILINEAR and ANTIALIAS
    im = im.convert("L")
    im = im.resize((new_w,10),Image.ANTIALIAS)
    min_lum, max_lum = im.getextrema()


    char_dict = char_greydict()
    ascii_list = char_dict.keys()
    #chars is dict of {char: greyscale value}
    ascii_list.sort()
    max_a = max(ascii_list)
    min_a = min(ascii_list)

    ascii_string=""

    for y in range(im.size[1]):
        for x in range(im.size[0]):
            l = im.getpixel((x,y))
            l=l*1.0*(max_a - min_a)/(max_lum-min_lum)
            ch_idx = bisect(ascii_list,l)
            max_idx = min(ch_idx, len(ascii_list)-1)
            min_idx = max(0, ch_idx - 1)
            if abs(ascii_list[max_idx] - l) < abs(ascii_list[min_idx] - l):
                ch_val = ascii_list[max_idx]
            else:
                ch_val = ascii_list[min_idx]
            ascii_string += char_dict[ch_val]

        ascii_string=ascii_string+"\n"
    print ascii_string



