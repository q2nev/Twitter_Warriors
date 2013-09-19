import tweeters.twitter as TW
from xml.dom.minidom import parse
import random
import Q2API.xml.base_xml as BX
import Q2API.xml.mk_class as MC
import start.boss as CB
import levels.game as GM


class Boss(object):
    '''
    Boss object
    name: used to define the file to load
    keyword: is the keyword for the given gang -- can be inserted into level if desired
    moves: one less than the amount of tweets for the user. Defaulted to 10.

    tweet_count: generates integer for tweets left(for counting purposes tweets must match up with user)
    at_count: ats given the keyword for the Boss
    hashes_count: hashes given the keyword for the Boss.
    write_boss_xml: rewrites boss xml
    '''
    def __init__(self,name,keyword="",moves=10):
        self.name = name
        #print self.name
        self.keyword = 'bus'
        self.moves = moves
        #self.keyword = self.pull_boss_keyword()
        self.initial_write_boss_xml()
        self.make_boss_class()


    def pull_boss_keyword(self):
        with open('..//levels//turnbullacs.xml') as fin:
            xml_file = fin.read()
        success, boss = GM.obj_wrapper(xml_file)
        if success:
            return boss.spot[0].keyword[0].value
        else:
            print "Failure pull boss keyword."

    def tweet(self):
        return TW.term_tweet([str(self.keyword)], 10)

    def initial_write_boss_xml(self):
        twitter_tuple = self.tweet()
        try:
            tws = BX.XMLNode('tweet_count',None,twitter_tuple[0],[])
            ats = BX.XMLNode('at_count',None,twitter_tuple[1],[])
            hashes = BX.XMLNode('hash_count',None,twitter_tuple[2],[])
        except:
            print ""
            tws = BX.XMLNode('tweet_count',None,0,[])
            ats = BX.XMLNode('at_count',None,0,[])
            hashes = BX.XMLNode('hash_count',None,0,[])
        current_boss = BX.XMLNode('boss_'+str(self.name),None,None,[tws,ats,hashes])
        current_boss = current_boss.flatten_self()
        self.save_boss_xml(current_boss)
        return

    def save_boss_xml(self,xml):
        '''
        Takes in flattened boss xml file and outputs it to boss.xml file
        '''
        fout = open('..//start//boss.xml','w')
        fout.write(xml)
        fout.close()
        return

    def make_boss_class(self):
        boss = MC.generate_class('..//start//boss.xml')
        return boss

    def get_ats(self):
        with open('..//start//boss.xml') as fin:
            xml_file = fin.read()
        success, b = CB.obj_wrapper(xml_file)
        if success:
            return int(b.at_count[0].value)
        else:
            print "Failure."

    def get_hashes(self):
        with open('..//start//boss.xml') as fin:
            xml_file = fin.read()
        success, b = CB.obj_wrapper(xml_file)
        if success:
            return int(b.hash_count[0].value)
        else:
            print "Failure."

    def get_tws(self):
        with open('..//start//boss.xml') as fin:
            xml_file = fin.read()
        success, b = CB.obj_wrapper(xml_file)
        if success:
            return int(b.tweet_count[0].value)
        else:
            print "Failure."

    def choose_ats(self):
        if self.get_ats() ==0:
            return None
        else:
            print self.get_ats()
            print type(self.get_ats())
            choice_ats = range(self.get_ats())
            num_ats = random.choice(choice_ats)
            return num_ats

    def update_ats(self, new_value):
        tws = BX.XMLNode('tweet_count',None,self.get_tws(),[])
        ats = BX.XMLNode('at_count',None,new_value,[])
        hashes = BX.XMLNode('hash_count',None,self.get_hashes(),[])
        current_boss = BX.XMLNode('boss_'+str(self.name),None,None,[tws,ats,hashes])
        current_boss = current_boss.flatten_self()
        self.save_boss_xml(current_boss)
        return

    def update_ats2(self,new_value):
        #try flatten method later
        pass

    def update_hashes(self, new_value):
        tws = BX.XMLNode('tweet_count',None,self.get_tws(),[])
        ats = BX.XMLNode('at_count',None,self.get_ats(),[])
        hashes = BX.XMLNode('hash_count',None,new_value,[])
        current_boss = BX.XMLNode('boss_'+str(self.name),None,None,[tws,ats,hashes])
        current_boss = current_boss.flatten_self()
        self.save_boss_xml(current_boss)
