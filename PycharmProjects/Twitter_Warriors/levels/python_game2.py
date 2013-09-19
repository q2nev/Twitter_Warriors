import game
import ascii_diff as ASC
from battle import battle
import msvcrt
import os
import time
import pygame.mixer as mix
import string
import Q2API.xml.mk_class as MK


stops = dict()
fights = dict()
items = dict()
finds = dict()
sounds= dict() #keep track of which sounds have been played
asciis = dict()
#initialize dicts to keep track of stops,
#  and items by attributes

#initialize hashes and ats

def main():
    global g_map
     #keep track of which images have been printed

    # load game map
    with open("..//levels//game.xml") as f:
        xml_file = f.read()

    success, g_map = game.obj_wrapper(xml_file)

    # construct stops dict
    global stops
    for stop in g_map.stop:
        nomen = stop.attrs["nomen"]
        stops[nomen] = stop

    global player
    player = g_map.player[0]

    # give initial stop
    stop = g_map.stop[0]
    # enter game loop
    while True:

        #prints current stop description, image, sound
        describe(stop)

        command = raw_input(">")
        #returns next stop, prints various things via command
        stop = process_command(stop, command)
        #process command includes:

def image_to_ascii(stop):
    img= str(stop.attrs["im"]).strip(string.whitespace)
    img_txt = img[:-4]+'.txt'
    if img in os.listdir('../ascii/'):
        if img_txt in os.listdir('../ascii/'):
            with open(img_txt) as f:
                lines = f.readlines()
                for line in lines:
                    print line
                    time.sleep(2)

        elif img[-4:] == '.jpg' or img[-4:] == '.jpeg':
            ascii_string = ASC.image_diff('../ascii/'+img)
            with open(img[:-4]+'.txt','w') as fin:
                fin.write(ascii_string)

            for line in ascii_string:
                print line
                time.sleep(2)
        else:
            pass

def play_music(stop):
    #sound_delay = str(stop.attrs["delay"]).strip(string.whitespace)
    mix.init()
    sound_file = str(stop.attrs["sd"]).strip(string.whitespace)
    if sounds.get(sound_file,False) == True:
        return
    else:
        sounds[sound_file] = True
        sound = mix.Sound(sound_file)
        sound.play(maxtime=25000)

def describe(stop):

    print stop.attrs["nomen"].upper(), "STATION"
    print stop.desc[0].value

    play_music(stop)
    #image_to_ascii(stop)


def process_command(stop, command): #can also pass stop!
    '''
    1. Parse Command
    2. Get Items and places from Command
    3. Handles Twitter Battle
    - Twitter Game play : if desc or stop, or item contains name in fight dict.

    '''
    global finds

    places, items, fights = get_data(stop)
    verb, noun = parse(command)

    if verb == "go":
        pl = places.get(noun)
        if pl:
            link = pl.attrs["link"]
            stop = stops[link]
        else:
            print "You can't go there."

    elif verb == "describe":
        boss_kw = noun
        pl = places.get(noun)
        itm = places.get(noun)

        if boss_kw == "around":
            for pl in stop.place:
                for des in pl.desc:
                    print "\n\t"+"Place description:", des.value,
                    print "\n\t"+"Name for place:", des.attrs["nomen"]
                    print "\n\t"+"direction for place:", des.attrs["dir"]
                    print "_____________________________________"

            for itm in stop.item:
                for des in itm.desc:
                    print "\n\t"+"item description:", des.value
                    print "\n\t"+"Name for item:",des.attrs["nomen"]
                    print "\n\t"+"direction for item:",des.attrs["dir"]
                    print "_____________________________________"

        elif fights.get(boss_kw) == 'true' :
            #this loops checks to
            if finds.get(boss_kw,False):
                print "You already Twitter Battled the", boss_kw.upper(),"!"

            else:
                hashes, ats = twitter_data(boss_kw)
                print "You now have", hashes,"ounces of hash"
                print "And",ats, "holler-ats!"
                finds[boss_kw] = hashes,ats

        elif pl:
            print pl.desc[0].value

        elif itm:
            print itm.desc[0].value

    elif verb == "load":
        games = os.listdir("..//save")
        if games:
            for i, file_name in enumerate(games):
                print str(i) + "\t" + file_name.split(".")[0]
                choice = raw_input("choose a game or type 'N' for a new game\n>")
                if choice not in ["N", "n", "new", "NEW"]:
                    try:
                        game_file = "saved_games\\" + games[int(choice)]
                    except:
                        print "WHAT?"
                else:
                    return 'game.xml'
        else:
            return 'game.xml'

    elif verb == "save":
        stop_nomen = g_map.stop.attrs["nomen"]
        player.attrs["stop"] = str(stop_nomen)
        save_file = raw_input("enter a name for the save file>")
        game_data = g_map.flatten_self()
        with open("saved_games\\" + save_file + ".xml", "w") as f:
            f.write(game_data)
            print "game saved!"
        return stop

    elif verb == "exit":
        exit()

    elif verb =="get":
        pass

    else:
        print "unrecognized command"
    return stop

def twitter_data(boss_kw):
    global hashes
    global ats

    print "It's a glare from", boss_kw
    call_prompt = raw_input("What's your call against this mean muggin?!")

    #start twitter game here
    hash_diff, at_diff = battle(boss_kw,call_prompt)
    #return tuple of diff of ats and hashes
    # call_difference
    # a.)grabs the noun as the keyword in twitter for the move/item of the spot
    #       -if the move/item does not have a keyword, return the same values for the player
    # b.)grab the keyword

    finds[boss_kw] = hash_diff,at_diff

    hashes += hash_diff
    ats += at_diff

    if hashes <0 or ats<0: #breaks if either returns zero
        print "You're as dead as a doornail."
        print "Would you like to restart?"
        restart = raw_input(">>")
        while True:
            if restart =="Y":
                return main()
            elif restart == "N":
                exit()
            else:
                print "Unknown command"
                continue
    return hashes,ats

def get_data(stop): #can also pass stop and will have same result!
    places = dict()
    fights = dict()
    items = dict()
    for pl in stop.place:
        nomen = pl.attrs["nomen"]
        dir = pl.attrs["dir"]
        fight = pl.attrs["fight"]
        places[nomen] = pl
        places[dir] = pl
        fights[nomen] = fight

    for itm in stop.item:
        nomen = itm.attrs["nomen"]
        fight = itm.attrs["fight"]
        items[nomen] = itm
        fights[nomen] = fight

    return places, items, fights

translate_verb = {"g" : "go","go" : "go","walk" : "go","get" : "go","jump" : "go",
                  "t" : "take", "take" : "take","grab" : "take",
                  "l":"describe","look":"describe","describe" : "describe","desc":"describe",
                  "current":"cur","cur":"cur","give":"cur"
                  }

translate_noun = {"n": "n","north":"n",
                  "s": "s","south": "s",
                  "e" : "e","east" : "e",
                  "w" : "w","west" : "w",
                  "u" : "u", "up" : "u","surface":"u",
                  "d" : "d", "down" : "d",
                  "a" : "a","across":"a","over":"a","cross":"a",
                  "i":"i","h":"i", "inventory":"i",
                  }

one_word_cmds = {"n" : "describe n","s" : "describe s","e" : "describe e","w" : "describe w",
                 "u" : "describe u","up": "describe u",
                 "d" : "describe d",
                 "off" :"describe outside",
                 "on":"describe on",
                 "l":"load","load":"load",
                 "current": "describe around","now": "describe around","around":"describe around",
                 "i":"give inventory","h":"give inventory",
                 "rules":"give rules","next": "go start","begin":"go start","start":"go start",
                 }

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