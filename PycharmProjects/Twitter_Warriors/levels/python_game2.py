import game
import tweeters.twitter as TW
import ascii_diff as ASC
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
battles = dict()
#initialize dicts to keep track of stops,
#  and items by attributes

#initialize hashes and ats
g_map = None
hashes = 20
ats = 20

def load_game(game_file):
    '''
    this function opens a player that has a saved game
    '''
    with open(game_file) as f:
        xml_file = f.read()

    success, p_map = game.obj_wrapper(xml_file)
    #call player map here because we are not altering most of the file.

    if not success:
        print "Failure to wrap object."
        exit()

    global player #only need player from file
    global stops #grab dict from main file so that we can call current stop from nomen attribute

    player = p_map.player[0]

    nomen = player.attrs["stop"] #grab stop from player's xml file and return for game play
    stop = stops[nomen]

    return stop

def load_ats_hashes(game_file):
    global ats
    global hashes
    with open('../save/'+game_file) as f:
        xml_file = f.read()

    success, p_map = game.obj_wrapper(xml_file)
    #call player map here because we are not altering most of the file.

    if not success:
        print "Failure to wrap object."
        exit()

    global player #only need player from file

    player = p_map.player[0]

    ats = player.attrs["ats"] #grab stop from player's xml file and return for game play
    hashes = player.attrs["hashes"]

    return ats,hashes

def main():
    global g_map
     #keep track of which images have been printed

    # load game map
    with open("..//levels//game.xml") as f:
        xml_file = f.read()

    success, g_map = game.obj_wrapper(xml_file) #turn into python object via Q2API
    if not success:
        print "Failure to wrap object. Try running mk_class again."
        exit()

    # construct stops dict
    global stops

    for stop in g_map.stop:
        nomen = stop.attrs["nomen"]
        stops[nomen] = stop

    global battles
    for scenario in g_map.scenario: #
        ats = scenario.attrs['ats']
        hashes = scenario.attrs['hashes']
        battles[(ats,hashes)] = scenario

    global player
    player = g_map.player[0]

    # give initial stop
    stop = g_map.stop[0]
    # enter game loop
    while True:
        #prints current stop description, image, sound etc.
        describe(stop)

        command = raw_input(">")
        #returns next stop, prints various things via command
        stop = process_command(stop, command)


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

def describe(stop,mute=False,desc_num=0):
    # print the name of the current station
    if mute == False:
        print stop.attrs["nomen"].upper(), "STATION"
        print stop.desc[desc_num].value
    #plays the current stations music
    play_music(stop)

    #image_to_ascii(stop)
    return stop

def process_command(stop, command): #can also pass stop!
    '''
    1. Parse Command
    2. Get Items and places from Command
    3. Handles Twitter Battle
    - Twitter Game play : if desc or stop, or item contains name in fight dict.

    '''
    global finds
    global hashes
    global ats

    places, items, fights = get_data(stop)
    verb, noun = parse(command)
    # print verb
    # print len(verb)
    # print type(verb)

    # print noun
    # print len(noun)
    # print type(noun)
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
            print "Not everybody's trying to hustle a hustler!"
            print pl.desc[0].value

        elif itm:
            print "Grab it!"
            print itm.desc[0].value

    elif verb == "load": #loads game from save directory
        games = os.listdir("..//save")
        if games:
            save_count = 0
            for i, file_name in enumerate(games): #prints the players
                if file_name.split(".")[1]=='.xml':
                    print str(i) + "\t" + file_name.split(".")[0]
                    save_count +=1
            if save_count > 0:

                print "Choose a game by its number, or type new for new game.\n"
                choice = raw_input(">>")
                if choice not in ["N", "n", "new", "NEW"]:
                    try:
                        game_file = "..\\save\\" + games[int(choice)]
                    except:
                        print "WHAT?"

            else:
                print "Could not find any saved games"
                game_file = 'game.xml'
        else:
            game_file = 'game.xml'
        return load_game(game_file)

    elif verb == "score":
        games = os.listdir("../save/")
        save_count = 0
        for i, file_name in enumerate(games): #prints the players
            if file_name[-4:]=='.xml':
                try:
                    print str(i) + "\t" + file_name.split(".")[0]
                except:
                    print "couldn't print game"
                try:
                    print "Ats:",load_ats_hashes(file_name)[0]  + "\t" + "Hashes:",load_ats_hashes(file_name)[1]
                except:
                    print "couldn't find scores"
            save_count += 1
        if save_count == 0:
            print "No saved games!"
            return stop
        return stop

    elif verb =="cur":
        print "Hashes:", hashes
        print "Ats:",ats
        return stop

    elif verb == "save":
        #save_file: name to save file at via raw_input
        stop_nomen = stop.attrs["nomen"]
        player.attrs["stop"] = str(stop_nomen)

        player.attrs["hashes"] = hashes
        player.attrs["ats"] = ats


        save_file = raw_input("enter a name for the save file>")
        #file = open("../save/" + save_file + ".xml", "w+")
        game_data = g_map.flatten_self()
        with open("..\\save\\" + save_file + ".xml", "w+") as f:
            f.write(game_data)
            print "game saved!"
        print "Continue game ? (Y/N) (Pressing N will put exit the game!)"
        continue_game = raw_input('>>')
        if continue_game == "Y":
            return stop
        elif continue_game == "N":
            print "OK!"
            exit()
        else:
            print "Unrecognized command, I'll just let you keep playing!"

        return stop

    elif verb =="restart":
        print "Restart game? (Y/N)"
        restart_game = raw_input('')
        if restart_game == "Y":
            return main()
        elif restart_game == "N":
            print "OK!"
            exit()
        else:
            print "Unrecognized command, I'll just let you keep playing!"
    elif verb =="how":
        print g_map.stop[0].item[0].desc[0].value
        return stop

    elif verb == "exit":
        print "Do you want to save your game? (Y,N)?"
        save_file = raw_input('>>')
        if save_file == "Y":
            process_command(stop,'save')
        elif save_file == "N":
            print "OK!"
            exit()
        else:
            print "What?! (Exit Prompt Error)"
            process_command(stop,'exit')


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
    #maybe use get function here to define

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
                  "current":"cur","cur":"cur","give":"cur",
                  "load":"load","start":"start","save":"save",
                  "how":"how","help":"how",
                  "exit":"exit",
                  "score":"score"
                  }

translate_noun = {"n": "n","north":"n",
                  "s": "s","south": "s",
                  "e" : "e","east" : "e",
                  "w" : "w","west" : "w",
                  "u" : "u", "up" : "u","surface":"u",
                  "d" : "d", "down" : "d",
                  "a" : "a","across":"a","over":"a","cross":"a",
                  "i":"i","h":"i", "inventory":"i",
                  "board":"board"
                  }

one_word_cmds = {"n" : "describe n","s" : "describe s","e" : "describe e","w" : "describe w",
                 "u" : "describe u","up": "describe u",
                 "d" : "describe d",
                 "off" :"describe outside",
                 "on":"describe on",
                 "l":"load game","load":"load game",
                 "current": "describe around","now": "describe around","around":"describe around",
                 "i":"cur inventory","h":"cur inventory",
                 "rules":"how to","how":"how to","help":"how to",
                 "next": "go start","begin":"go start","start":"go start",
                 "score":"score board",
                 "commands":"commands",
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

def retweets(): #returns ats and hashes of most recent retweet
    tweets, ats, hashes= TW.recent_tweets(['RT'], 1)
    return tweets, ats, hashes

def battle(boss_kw, call_prompt):
    boss_ats = retweets()[1]
    boss_hashes = retweets()[2]
    player_ats = TW.recent_tweets([call_prompt],1)[1]
    player_hashes = TW.recent_tweets([call_prompt],1)[2]
    ats_diff = player_ats - boss_ats
    hashes_diff = player_hashes - boss_hashes
    print "Hash from battle:", hashes_diff
    print "Holler-Ats from battle:",ats_diff
    if ats_diff > 0:
        ats_winner = 'player'
    elif ats_diff == 0:
        ats_winner = 'equal'
    else:
        ats_winner = 'boss'

    if hashes_diff >0:
        hashes_winner = 'player'
    elif hashes_diff ==0:
        hashes_winner = 'equal'
    else:
        hashes_winner = 'boss'
    print battles[(ats_winner,hashes_winner)].desc[0].value
    return hashes_diff, ats_diff

main()