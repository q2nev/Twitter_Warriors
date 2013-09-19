import twitter as TW

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