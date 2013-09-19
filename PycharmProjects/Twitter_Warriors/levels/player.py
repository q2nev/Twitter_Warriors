import Q2API.xml.base_xml as BX
import Q2API.xml.mk_class as MC
import os
import string
import start.current_user
import levels.turnbullacs as TB
import tweeters.twitter as TW


class Player(object):
    def __init__(self,username ="new",password="",dummy = ''):
        #username default is new and password is empty string for check
        self.username = username
        self.is_player()
        #dummy = self.tweet(

    def is_player(self):
        '''
        checks whether new user is a player or not
        '''
        new = raw_input(">> Have you played Twitter Warriors before? (Y/N)")
        self.username = raw_input(">> What's your username warrior?")
        if new == 'Y':
            print "Great! Let's pull in your game!"
            if self.check_for_file_duplicates():
                #still need to check for pwd here...
                self.make_player_xml()
            else:
                print "Couldn't find your file!"
                return self.is_player()
        elif new == 'N':
            if self.check_for_file_duplicates():
                print "That name is already in use!"
                self.is_player()
            else:
                self.make_player_xml()
                self.make_class()
        else:
            raw_input(">> Improper Input")
            self.is_player()

    def check_for_file_duplicates(self):
        '''
        checks if file in saved folder
        '''
        os.chdir('..//save')
        for name in os.listdir(os.getcwd()):
            if name[:-4] == self.username:
                return True
        return False

    def make_player_xml(self,stop="",call = "",saved_ats = 0, saved_hashes = 0, location = 0, health = 100,):
        '''
        Uses Q2API.xml.base_xml to make initial xml file for user in below format
        <Username>
            <Finds>
            </Finds>
            <Stop>
            </Stop>
            <SavedHashes>
            </SavedHashes>
            <SavedAts>
            </SavedAts>
        </Username>
        '''
        current_stop = BX.XMLNode('Stop',None,stop,[])
        saved_hashes = BX.XMLNode('SavedHashes',None,1,[])
        saved_ats = BX.XMLNode('SavedAts',None,1,[])
        inventory = BX.XMLNode('Inventory',None,None,[saved_ats,saved_hashes,health])
        username = BX.XMLNode('Username',None,None,[current_stop,inventory,password])
        #it's not saving properly for first attribute...
        self.save_xml_file(username.flatten_self())   #saves flattened self
        return self.save_xml_to_current_xml(username.flatten_self())

    def save_xml_file(self,xml):
        '''
        takes in xml document and saves to username xml
        '''
        file = xml
        fout = open('..//save//'+str(self.username)+'.xml','w')
        fout.write(file)
        fout.close()

    def save_xml_to_current_xml(self,xml):
        '''
        Writes to current xml file
        '''
        file = xml
        fout = open('..//start//current_user.xml','w')
        fout.write(file)
        fout.close()

    def make_class(self):
        '''
        uses mk_class from Q2API
        '''
        current_user = MC.generate_class('..//start//current_user.xml')
        return current_user

    def make_class2(self):
        for level in os.listdir("../levels"):
            if level[-4:] == '.xml' and level[:-4] == str(self.get_level()):
                current_level = MC.generate_class('..//levels//'+str(level))
                return current_level

    def make_level_class(self):
        current_level = MC.generate_class('..//levels//'+str(self.get_level())+'.xml')
        return current_level

    def tweet(self, keyword, moves = 10):
        return TW.recent_tweets([str(keyword)], 10)

    def get_location(self):
        with open('..//start//current_user.xml') as fin:
            x_file = fin.read()
        success, user = start.current_user.obj_wrapper(x_file)
        if success:
            #print user.Location[0].value
            return str(user.Location[0].value)
        else:
            print "getloc Failure."

    def new_call(self):
        print "What's our new call brother?!"
        call = raw_input('>> ')
        return call

    def get_level(self):
        with open('..//start//current_user.xml') as f:
            x_file = f.read()
        success, current = start.current_user.obj_wrapper(x_file)
        if success:
            #print current.Username.Level[0].value
            print current.Level[0].value
            return current.Level[0].value
        else:
            print "getlev Failure."

    def get_hashes(self):
        with open('..//start//current_user.xml') as fin:
            x_file = fin.read()
        success, user = start.current_user.obj_wrapper(x_file)
        if success:
            # print user.Inventory[0].SavedHashes[0].value
            return int(user.Inventory[0].SavedHashes[0].value)
        else:
            print "Failure at get hashes."

    def get_ats(self):
        '''
        This grabs a users ats from their inventory via current_user.py and prints it to the console
        '''
        with open('..//start//current_user.xml') as fin:
            x_file = fin.read()
        success, user = start.current_user.obj_wrapper(x_file)
        if success:
            #print user.Inventory[0].SavedAts[0].value
            return int(user.Inventory[0].SavedAts[0].value)
        else:
            print "Failure at get ats."

    def get_health(self):
        '''
        This grabs a users health from current_user.py
        '''
        with open('..//start//current_user.xml') as fin:
            x_file = fin.read()
        success, user = start.current_user.obj_wrapper(x_file)
        if success:
            print user.Inventory[0].Health[0].value
        else:
            print "Failure at health."

    def get_call(self):
        with open('..//start//current_user.xml') as fin:
            x_file = fin.read()
        success, user = start.current_user.obj_wrapper(x_file)
        if success:
            print str(user.Call[0].value)
        else:
            print "Failure at get call."

    def get_location_text(self):
        with open('..//levels//turnbullacs.xml') as fin:
            xml_file = fin.read()
        success_gang, gang = TB.obj_wrapper(xml_file)
        if success_gang:
            print 'done'
            loc = self.get_location()
            if int(gang.spot[int(loc)].intro[0].attrs['location']) == int(self.get_location()):
                print "found match"
                return gang.spot[int(loc)].intro[0].value
            else:
                print "work on syntax for location text"
        else:
            print "Failure at get location text."

    def update_call(self, new_value): #this uses the Twitter API to give us our hash_count and Tweet_Count
        password = BX.XMLNode('Password',None,self.password,[])
        current_call = BX.XMLNode('Call',None,new_value,[])
        current_level = BX.XMLNode('Level',None,self.get_level,[])
        current_location = BX.XMLNode('Location',None,self.get_location(),[])
        health = BX.XMLNode('Health',None,self.get_health(),[])
        saved_hashes = BX.XMLNode('SavedHashes',None,self.get_hashes,[])
        saved_ats = BX.XMLNode('SavedAts',None,self.get_ats(),[])
        inventory = BX.XMLNode('Inventory',None,None,[saved_ats,saved_hashes,health])
        user = BX.XMLNode(self.username,None,None,[current_call,current_level,current_location,inventory,password])
        # self.save_xml_file(user.flatten_self())   #saves flattened self
        self.save_xml_to_current_xml(user.flatten_self())
        self.make_class()
        return user.flatten_self()

    def update_location(self,new_value):
        password = BX.XMLNode('Password',None,self.password,[])
        current_call = BX.XMLNode('Call',None,self.get_call(),[])
        current_level = BX.XMLNode('Level',None,self.get_level(),[])
        current_location = BX.XMLNode('Location',None,new_value,[])
        health = BX.XMLNode('Health',None,self.get_health(),[])
        saved_hashes = BX.XMLNode('SavedHashes',None,self.get_hashes(),[])
        saved_ats = BX.XMLNode('SavedAts',None,self.get_ats(),[])
        inventory = BX.XMLNode('Inventory',None,None,[saved_ats,saved_hashes,health])
        user = BX.XMLNode(self.username,None,None,[current_call,current_level,current_location,inventory,password])
        # self.save_xml_file(user.flatten_self())   #saves flattened self
        self.save_xml_to_current_xml(user.flatten_self())
        self.make_class()
        return user.flatten_self()

    def update_level(self,new_value):
        password = BX.XMLNode('Password',None,self.password,[])
        current_call = BX.XMLNode('Call',None,self.get_call(),[])
        current_level = BX.XMLNode('Level',None,self.get_level(),[])
        current_location = BX.XMLNode('Location',None,new_value,[])
        health = BX.XMLNode('Health',None,self.get_health(),[])
        saved_hashes = BX.XMLNode('SavedHashes',None,self.get_hashes(),[])
        saved_ats = BX.XMLNode('SavedAts',None,self.get_ats(),[])
        inventory = BX.XMLNode('Inventory',None,None,[saved_ats,saved_hashes,health])
        user = BX.XMLNode(self.username,None,None,[current_call,current_level,current_location,inventory,password])
        # self.save_xml_file(user.flatten_self())   #saves flattened self
        self.save_xml_to_current_xml(user.flatten_self())
        self.make_class()
        return user.flatten_self()
        pass

    def update_hashes(self,new_value):
        password = BX.XMLNode('Password',None,self.password,[])
        current_call = BX.XMLNode('Call',None,self.get_call(),[])
        current_level = BX.XMLNode('Level',None,self.get_level(),[])
        current_location = BX.XMLNode('Location',None,self.get_location(),[])
        health = BX.XMLNode('Health',None,self.get_health(),[])
        saved_hashes = BX.XMLNode('SavedHashes',None,new_value,[])
        saved_ats = BX.XMLNode('SavedAts',None,self.get_ats(),[])
        inventory = BX.XMLNode('Inventory',None,None,[saved_ats,saved_hashes,health])
        user = BX.XMLNode(self.username,None,None,[current_call,current_level,current_location,inventory,password])
        # self.save_xml_file(user.flatten_self())   #saves flattened self
        self.save_xml_to_current_xml(user.flatten_self())
        self.make_class()
        return user.flatten_self()

    def update_ats(self,new_value):
        password = BX.XMLNode('Password',None,self.password,[])
        current_call = BX.XMLNode('Call',None,self.get_call(),[])
        current_level = BX.XMLNode('Level',None,self.get_level(),[])
        current_location = BX.XMLNode('Location',None,self.get_location(),[])
        health = BX.XMLNode('Health',None,self.get_health(),[])
        saved_hashes = BX.XMLNode('SavedHashes',None,self.get_hashes(),[])
        saved_ats = BX.XMLNode('SavedAts',None,new_value,[])
        inventory = BX.XMLNode('Inventory',None,None,[saved_ats,saved_hashes,health])
        user = BX.XMLNode(self.username,None,None,[current_call,current_level,current_location,inventory,password])
        # self.save_xml_file(user.flatten_self())   #saves flattened self
        self.save_xml_to_current_xml(user.flatten_self())
        self.make_class()
        return user.flatten_self()

    def update_health(self,new_value):
        password = BX.XMLNode('Password',None,self.password,[])
        current_call = BX.XMLNode('Call',None,self.get_call(),[])
        current_level = BX.XMLNode('Level',None,self.get_level(),[])
        current_location = BX.XMLNode('Location',None,self.get_location(),[])
        health = BX.XMLNode('Health',None,new_value,[])
        saved_hashes = BX.XMLNode('SavedHashes',None,self.get_hashes(),[])
        saved_ats = BX.XMLNode('SavedAts',None,self.get_ats(),[])
        inventory = BX.XMLNode('Inventory',None,None,[saved_ats,saved_hashes,health])
        user = BX.XMLNode(self.username,None,None,[current_call,current_level,current_location,inventory,password])
        # self.save_xml_file(user.flatten_self())   #saves flattened self
        self.save_xml_to_current_xml(user.flatten_self())
        self.make_class()
        return user.flatten_self()
