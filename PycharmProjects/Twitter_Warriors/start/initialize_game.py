'''
This code initializes the game.

http://www.stonegreasers.com/greaser/conclay.html


1. Prints Intro Text

2. Checks to see if they've played before via is_player function

3. Make New Player - initalizes new player with base code

4.


'''
import winsound, sys
from make_base_xml import Player
from make_boss import Boss
import tweeters.twitter as TW
import Q2API.xml.base_xml as BX
import string
import os


# winsound.PlaySound('canUdigit.wav', winsound.SND_FILENAME)

#player = Player()

def retweets(): #returns ats and hashes of most recent retweet
    tweets, ats, hashes= TW.recent_tweets(['RT'], 1)
    return tweets, ats, hashes

def play_game():
    player = Player()
    boss = Boss(player.get_level())
    while True:
        if player.get_hashes() <0 or player.get_ats() <0:  #this is the logic for losing
            print "Ain't nothin wrong with going out tough."
            # print game over ascii
            # print Warriors Ascii
            exit()

        if boss.get_ats() <0 or boss.get_hashes() <0:
            print "You have destroyed the ",boss.name,"!"
            print "The", boss.name, "left behind a new weapon!"
            print "A sledge hammer!"
            print "Drive the bus?(B) Or battle some more?! (Q)"

        print player.get_location_text()

        play = raw_input('>> ')
        #turn if statements into options dictionary?!
        #for move in options:

        if play == 'C':
            print "What's the new call fly brother?!"
            new_call = raw_input( ">> ")
            player.update_call(str(new_call))
        elif play == 'L':
            print player.get_location_text()
        elif play == 'I':
            #this gives current inventory
            print "Current Hashes: ", player.get_hashes()
            print "Current Holler-Ats: ", player.get_ats()
            print "Current Health: ", player.get_health()

        elif play == 'RT':
            battle()
            print player.get_location()
            player.update_location(str(int(player.get_location())+1))
        elif play == 'options':

            pass

        elif play =="J":
            player_ats = player.get_call()[1]
            player_hashes = player.get_hashes()

            battle(player_ats,player_hashes)

        elif play == 'start' or play == 'restart':
            player = Player()
        #
        elif play == 'save':
        #   pass
            player.update_health(player.get_health()-boss.get_ats()-boss.get_hashes())
            #save to users xml file...
            player.save_xml_file()
        #
        else:
            print "Whatchu sayin punk!"


def battle(boss_kw, call_prompt):
    boss_ats = retweets()[1]
    boss_hashes = retweets()[2]
    player_ats = TW.recent_tweets([call_prompt],1)[1]
    player_hashes = TW.recent_tweets([call_prompt],1)[2]
    ats_diff = player_ats - boss_ats
    hashes_diff = player_hashes - boss_hashes
    if boss_ats == player_ats:
        if player_hashes == boss_hashes:
            print "It's a draw!"

        elif player_hashes > boss_hashes:
            print "You smoked them out!"

        elif boss_hashes > player_hashes:
            print "They smoked you out!"
            print "You lose", hashes_diff, "of your stash."

    elif boss_ats > player_ats:
        if player_hashes == boss_hashes:

            print "They're packing the same hashes!"
            print "Run brother, run!!"

        elif player_hashes > boss_hashes:
            print "They got a big crew, but you smoked them out!"
            print "Add the difference to your stack! And roll on back!"
        elif boss_hashes > player_hashes:
            print "They smoked you out! And you couldn't fight!"
            print "And you lose", ats_diff,"of your holler @s."
            print "You lose", hashes_diff, "of your stash."

    elif boss_ats < player_ats:
        print "You out hollered them. You mad tweeter, you!"
        if player_hashes == boss_hashes:
            print "You sly mother. You beat that turkey!"

        elif player_hashes > boss_hashes:
            print "You smoked them out, too!"

        elif boss_ats > player_ats:
            print "They smoked you out!"
            print "You lose", hashes_diff, "of your stash."
    return ats_diff, hashes_diff

    #player.update_location(player.get_location+1)
#play_game()