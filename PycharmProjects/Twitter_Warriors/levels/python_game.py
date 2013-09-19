import game
import msvcrt
import ascii.ascii_bisect as ASC
import tweeters.twitter as TW
from start.initialize_game import battle
import sys, winsound

winsound.PlaySound('../start/canUdigit.wav', winsound.SND_FILENAME)

stops = dict()
player = None
current_stop=""


def main():
    # load game map
    with open("game.xml") as f:
        xml_file = f.read()

    success, g_map = game.obj_wrapper(xml_file)

    # construct rooms dict
    global stops
    for stop in g_map.stop:
        nomen = stop.attrs["nomen"]
        stops[nomen] = stop

    # initialize game
    global player
    player = g_map.player[0]

    # print intro
    intro = g_map.intro[0]
    print intro.desc[0].value

    print image_to_ascii(intro) # prints intro image

    stop = g_map.stop[0] # give initial stop

    # enter game loop
    while True:
        store_twitter = []

        describe(stop)


        if stop.attrs["nomen"]== "endgame": # use nomen here
            exit()
        # #start twitter game here
        # call_prompt = raw_input("What's your call against this mean muggin?!")
        #
        # hash_diff, at_diff = battle(stop.attrs["nomen"],call_prompt)
        # #return tuple of diff of ats and hashes
        # #currently battle function doesn't have unique call for each exit,item or stop specific keyword
        #
        #
        # if hash_diff <0 or at_diff<0: #breaks if either returns zero
        #     print "You're as dead as a doornail."
        #     exit()
        #
        # store_twitter.append(hash_diff,at_diff)
        # # call_difference
        # # a.)grabs the noun as the keyword in twitter for the move/item of the spot
        # #       -if the move/item does not have a keyword, return the same values for the player
        # # b.)grab the keyword

        command = raw_input(">")
        stop = process_command(stop, command)


def image_to_ascii(stop):
    image_path = str(stop.im[0].value).strip()
    ascii_string = ASC.infile_give(image_path)
    return ascii_string

def describe(stop):
    print stop.attrs["nomen"].upper(), "STATION"
    print stop.desc[0].value

def process_command(stop, command): #can also pass stop!
    exits, items = get_data(stop)
    verb, noun = parse(command)

    if verb == "go":
        ext = exits.get(noun)
        if ext:
            link = ext.attrs["link"]
            stop = stops[link]
            return stop
        else:
            print "You can't go there."
            return stop


    elif verb == "describe":
        ext = exits.get(noun)
        itm = exits.get(noun)
        if ext:
            print ext.desc[0].value
        elif itm:
            print itm.desc[0].value
        else:
            print "No such place."
        return stop
    #
    # elif verb == "describe":
    #     ext = exits.get(one_word_cmds[verb].split()[1])
    #     if ext:
    #         print ext.desc[0].value
    #         return stop
    #     else:
    #         print "What?"
    #         return stop

    else:
        print "unrecognized command"
        return stop


def get_data(stop): #can also pass stop and will have same result!
    exits = dict()
    for ext in stop.exit:
        nomen = ext.attrs["nomen"]
        dir = ext.attrs["dir"]
        exits[nomen] = ext
        exits[dir] = ext

    items = dict()
    for item in stop.item:
        nomen = item.attrs["nomen"]
        items[nomen] = item
    return exits, items

translate_verb = {"g" : "go",
                  "go" : "go",
                  "walk" : "go",
                  "get" : "go",
                  "jump" : "go",
                  "t" : "take",
                  "take" : "take",
                  "grab" : "take",
                  "describe" : "describe",
                  "desc":"describe",
                  "look":"describe"
                  }

translate_noun = {"n": "n",
                  "s": "s",
                  "e" : "e",
                  "w" : "w",
                  "u" : "u",
                  "up" : "u",
                  "surface":"u",
                  "d" : "d",
                  "down" : "d",
                  "north":"n",
                  "south": "s",
                  "east" : "e",
                  "west" : "w",
                  "across":"a",
                  "over":"a",
                  }

one_word_cmds = {"n" : "describe n",
                 "s" : "describe s",
                 "e" : "describe e",
                 "w" : "describe w",
                 "u" : "describe u",
                 "up": "describe u",
                 "d" : "describe d",
                 "off" :"describe outside",
                 "on":"describe on",
                 "around":"describe around"}

def parse(cmd):
    cmd = one_word_cmds.get(cmd, cmd)
    print cmd
    words = cmd.split()
    verb = words[0]
    verb = translate_verb.get(verb, "BAD_VERB")
    noun = " ".join(words[1:])
    noun = translate_noun.get(noun, noun)
    return verb, noun

main()