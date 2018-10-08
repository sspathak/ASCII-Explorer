import pygame
from time import sleep
import reader
import random
import sys

pygame.init()
def frame (screen):
    frame1=pygame.display.set_mode((100,100))

def update ():
    global rate 
    global lvlS
    global lvlE
    global x 
    global y
    global pause
    global canjump
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            looping = False
            pygame.display.quit()
            quit()
        elif event.type == 2:
            if event.key==32:
                if pause==True:
                    pause=False
                elif pause==False:
                    pause==True
                    update()
            elif event.key == 273: #up
                if canjump:
                    global iterate
                    iterate=True
                    rate = -3.5  
                    canjump=False #jump
            elif event.key == 276:#left
                control(["add","l"])
            elif event.key == 275: #right
                control(["add","r"])
            elif event.key == 274:
                recover()

            else:
                print event.key
        elif event.type == 3:
            global srate
            if event.key == 275:#right
                if srate>0:
                    srate=0
                control(["remove","r"])
            elif event.key == 276:#left
                if srate<0:
                    srate=0
                control(["remove","l"])
        if iterate:
            global itercount
            itercount+=1
    move()
def stringer(ar):
    tempStr=""
    for i in ar:
        tempStr=tempStr+i
    return tempStr

def move():
    global permitr
    global permitl
    global y
    global x
    global rate
    global width
    global srate
    if controlstack[-1]=="r" and permitr:
        srate=1
        x=x+int(srate)
    elif controlstack[-1]=="l" and permitl:
        srate=-1
        x=x+int(srate)
    y=y+int(rate)
    global itercount
    if rate<0 and itercount%4==0:
        rate=rate+0.5 #jump
    else:
        rate=rate+0.5
        global iterate
        iterate=False
        global itercount
        itercount=0
    if rate >=3.5:
        rate = 2.5
    if srate>2:
        srate=2
    elif srate<-2:
        srate=-2
    if y<=0:
        y=2
    elif y >= ground:
        y=ground+1
        rate=-1
        canjump=True
    objGen([[[0,0],[0,0]]])
def framePrint (frame):
    stage=" ________________________________________________ \n"
    for i in range(len(frame)):
        stage=stage+frame[i]+"\n"
    print stage + "\n ________________________________________________ \n"


def track(action):
    global tracker
    global backup
    if action[0]=="register":
        tracker.append([action[1],action[2],action[3],action[4]])
        if not(len(tracker) <21):
            tracker.pop(0)
    elif action[0]=="recover":
        backup=True
        tracker.pop()
        a=tracker.pop()
        return a
def slowprint(x):
    print "\n"
    for i in range(len(x)):
        if i+1 != x:
            sys.stdout.write(x[i])

            sleep(0.03)
        else:
            print "a"
    sleep(1)
class character:
    charskin=[["[","*"," "," ","*","]"],["["," ","_","_"," ","]"]]
    def __init__(self):
        pass
    def validate(self):
        print '''
____ _  _ ___ _  _ ____ _  _ ___ _ ____ ____ ___ _ _  _ ____ 
|__| |  |  |  |__| |___ |\ |  |  | |    |__|  |  | |\ | | __ 
|  | |__|  |  |  | |___ | \|  |  | |___ |  |  |  | | \| |__] 
                                                             ''' + "\n"+ "                "+stringer(character.charskin[0]) + "\n" + "                "+stringer(character.charskin[1])

        for i in character.charskin:
            for j in i:
                if j=="M" or j=="." or len(i)!=6:
                    print j
                    print'''
                         __      __              
| |\ | \  /  /\  |    | |  \    /__` |__/ | |\ | 
| | \|  \/  /~~\ |___ | |__/    .__/ |  \ | | \| 
                                                 '''
                    sleep(0.5)
                    slowprint ("AVOID USING 'M', '.', OR MORE THAN 6 LETTERS ")
                    slowprint ("SWITCHING TO CHARACTER EDIT MODE. ")
                    return False
        return True

    def create(self):
        i=0
        j=0

        slowprint("NOW SELECT THE COMMAND WINDOW TO CREATE YOUR CHARACTER SKIN ")
        tempskin=[["[","*"," "," ","*","]"],["["," ","_","_"," ","]"]]
        for i in range(2):
            tempskin[i]=raw_input("enter 6 ASCII characters of your choice : ")
        temp=[[],[]]
        for j in range(len(tempskin)):
            for k in tempskin[j]:
                temp[j].append(k)
        tempskin=temp
        character.charskin=tempskin
        if self.validate():
            slowprint ("SKIN VALIDATED ")
            slowprint("NOW SELECT THE PYGAME WINDOW AND PRESS UP OR DOWN ARROW KEY ")
            print ""
            return



def frameGen(frame):
    global width
    global rate
    global y
    global x
    global ground
    global lvl
    global lvlE
    try:
        collision(frame,x,y)
    except IndexError:
        rate=-1
    track(["register",x,y,lvlS,lvlE])

    
        #the code below places the character on the frame
    frameline=list(frame[y])
    for i in range(6):
        frameline[x+i]=character.charskin[0][i]
    frame[y]=stringer(frameline)
    frameline=list(frame[y+1])    
    for i in range(6):
        frameline[x+i]=character.charskin[1][i]
    frame[y+1]=stringer(frameline)

    framePrint(frame)
    sleep(0.03)

def recover():
    global x
    global y
    global lvlS
    global lvlE
    global rate
    r=track(["recover"])
    x=r[0]
    y=r[1]
    lvlS=r[2]
    lvlE=r[3]
    rate=0
    objGen(0)

def control(key):
    global controlstack
    global srate
    if key[0]=="add":
        controlstack.append(key[1])
    if key[0]=="remove":
        controlstack.remove(key[1])




def collision(frame,x1,y1):
    global width 
    global rate
    global y
    global ground
    global x
    global backup
    global permitl
    global permitr
    global lvlS
    global lvlE
    global srate
    global lvlcomplete
    global gameover
    global canjump
    contact0=list(frame[y1-2])
    contact1=list(frame[y1-1])
    contact2=list(frame[y1  ])
    contact3=list(frame[y1+1])
    contact4=list(frame[y1+2])
    contact5=list(frame[y1+3])    
    if ((contact4[x1]=="M" and contact4[x1+5]=="M")  and (contact1[x1]=="M" and contact1[x1+5]=="M") and ((contact0[x1]=="M" or contact0[x1+5]=="M") or (contact3[x1-1]=="M"or contact3[x1+6]=="M"))): #and (contact3[x1-1]=="M" and contact3[x1+6]=="M")
        recover()
    elif ((contact4[x1]==" " and contact4[x1+5]==" ") and (contact2[x1-1]=="M" and contact2[x1+6]=="M") and (contact1[x1]=="M" and contact1[x1+5]=="M")):
        recover()
        print "thiz is buggy :("
    elif ((contact1[x1+1]=="M" and contact4[x1+1]=="M")or(contact1[x1+2]=="M" and contact4[x1+2]=="M")or(contact1[x1+3]=="M" and contact4[x1+3]=="M")or(contact1[x1+4]=="M" and contact4[x1+4]=="M")):
        recover()
    elif (( contact3[x1-1]=="M" and contact4[x1+6]==" ") or( contact3[x1+6]=="M" and contact4[x1-1]==" ")) and (contact4[x1]=="M" or contact4[x1+5]=="M"):
        rate=-1
    elif (contact4[x1]=="M" or contact4[x1+5]=="M")  and ((contact3[x1-1]=="M" and contact3[x1+6]=="M") or (contact2[x1-1]=="M" and contact3[x1+6]=="M")): #and (contact3[x1-1]=="M" and contact3[x1+6]=="M")
        rate=-1
        y-=1
    elif contact4[x1]=="M" or contact4[x1+5]=="M":
        ground=y-1
        rate=-1
        canjump=True
    else:
        ground = 40
    if contact2[x1-1]=="M" or contact3[x1-1]=="M":
        permitl=False
        if srate<0:
            srate=0
    else:
        permitl=True
    if contact1[x1]=="M" or contact1[x1+5]=="M":
        pass
    if contact2[x1+6]=="M" and contact3[x1+6]=="M":
        permitr=False
        if srate>0:
            srate=0
    else:
        permitr=True
    if gameover:
        gameoverP()
    elif lvlcomplete:
        lvlcompleteP()
    if (contact1[x1]=="." or contact1[x1+5]=="." or contact2[x-1]=="." or contact2[x1+6]=="." or contact3[x-1]=="." or contact3[x1+6]=="." or contact4[x1]=="." or contact4[x1+5]=="."):
        gameover=True
    if (contact1[x1]=="|" or contact1[x1+5]=="|" or contact2[x-1]=="|" or contact2[x1+6]=="|" or contact3[x-1]=="|" or contact3[x1+6]=="|" or contact4[x1]=="|" or contact4[x1+5]=="|"):
        lvlcomplete=True


def gameoverP():
    sleep(0.5)
    print "\n \n \n \n \n \n \n \n \n \n "
    print " _______  _______  __   __  _______    _______  __   __  _______  ______   \n|       ||   _   ||  |_|  ||       |  |       ||  | |  ||       ||    _ |  \n|    ___||  |_|  ||       ||    ___|  |   _   ||  |_|  ||    ___||   | ||  \n|   | __ |       ||       ||   |___   |  | |  ||       ||   |___ |   |_||_ \n|   ||  ||       ||       ||    ___|  |  |_|  ||       ||    ___||    __  |\n|   |_| ||   _   || ||_|| ||   |___   |       | |     | |   |___ |   |  | |\n|_______||__| |__||_|   |_||_______|  |_______|  |___|  |_______||___|  |_|"
    slowprint("\n \n \n \n \n \n \n \n \n \n \n \n \n \n ")
    sleep(1)
    initialize()
    home()
    #quit()
def lvlcompleteP():
    for i in range (15):
        print "\n"
        sleep(0.2)
        slowprint ("\n \n \n \n \n \n \n \n \n \n ")
        print '''                   __       ___________    ____  _______  __                     
                  |  |     |   ____\   \  /   / |   ____||  |                    
                  |  |     |  |__   \   \/   /  |  |__   |  |                    
                  |  |     |   __|   \      /   |   __|  |  |                    
                  |  `----.|  |____   \    /    |  |____ |  `----.               
                  |_______||_______|   \__/     |_______||_______|               
                                                                                 
  ______   ______   .___  ___. .______    __       _______ .___________. _______ 
 /      | /  __  \  |   \/   | |   _  \  |  |     |   ____||           ||   ____|
|  ,----'|  |  |  | |  \  /  | |  |_)  | |  |     |  |__   `---|  |----`|  |__   
|  |     |  |  |  | |  |\/|  | |   ___/  |  |     |   __|      |  |     |   __|  
|  `----.|  `--'  | |  |  |  | |  |      |  `----.|  |____     |  |     |  |____ 
 \______| \______/  |__|  |__| | _|      |_______||_______|    |__|     |_______|
                                                                                 '''
        slowprint("\n \n \n \n \n \n \n \n \n \n \n \n \n \n ")
        quit()
    for i in range (15):
        print "\n"
        sleep(0.2)
        initialize()
        return

def objGen(coords):
    global width
    global frame1
    global loaded
    global lvlload
    
    if loaded==False:
        frame1=[" "*width]*43
        tempStr=""
        scroll()
        frame1=reader.reader(scroll())
    frameGen(frame1)
    
def scroll():
    global width
    global x
    global lvlS
    global lvlE
    if x>30 and lvlE<395:
        x=30
        lvlS+=1
        lvlE+=1
    elif x<30 and lvlS>1:
        x=30
        lvlS-=1
        lvlE-=1
    return [lvlS,lvlE,42]


def mainloop():
    global looping
    while looping:
        update()


def mainmenu():
    global selected
    play2='''
  ___    ___                                                                                     
/\  _`\ /\_ \                                                                                    
\ \ \L\ \//\ \      __     __  __                                                                
 \ \ ,__/ \ \ \   /'__`\  /\ \/\ \                                                               
  \ \ \/   \_\ \_/\ \L\.\_\ \ \_\ \                                                              
   \ \_\   /\____\ \__/.\_\\\\/`____ \                                                             
    \/_/   \/____/\/__/\/_/ `/___/> \                                                            
                               /\___/                                                            
                               \/__/   
                               '''
    inst2='''
 ______                   __                           __                                        
/\__  _\                 /\ \__                       /\ \__  __                                 
\/_/\ \/     ___     ____\ \ ,_\  _ __   __  __    ___\ \ ,_\/\_\    ___     ___     ____        
   \ \ \   /' _ `\  /',__\\\\ \ \/ /\`'__\/\ \/\ \  /'___\ \ \/\/\ \  / __`\ /' _ `\  /',__\       
    \_\ \__/\ \/\ \/\__, `\\\\ \ \_\ \ \/ \ \ \_\ \/\ \__/\ \ \_\ \ \/\ \L\ \/\ \/\ \/\__, `\      
    /\_____\ \_\ \_\/\____/ \ \__\\\\ \_\  \ \____/\ \____\\\\ \__\\\\ \_\ \____/\ \_\ \_\/\____/      
    \/_____/\/_/\/_/\/___/   \/__/ \/_/   \/___/  \/____/ \/__/ \/_/\/___/  \/_/\/_/\/___/       
                                                                                                 '''
    charedit2='''
      __                                      __                                 __      __      
     /\ \                                    /\ \__                             /\ \  __/\ \__   
  ___\ \ \___      __     _ __    __      ___\ \ ,_\    __   _ __          __   \_\ \/\_\ \ ,_\  
 /'___\ \  _ `\  /'__`\  /\`'__\/'__`\   /'___\ \ \/  /'__`\/\`'__\      /'__`\ /'_` \/\ \ \ \/  
/\ \__/\ \ \ \ \/\ \L\.\_\ \ \//\ \L\.\_/\ \__/\ \ \_/\  __/\ \ \/      /\  __//\ \L\ \ \ \ \ \_ 
\ \____\\\\ \_\ \_\ \__/.\_\\\\ \_\\\\ \__/.\_\ \____\\\\ \__\ \____\\\\ \_\      \ \____\ \___,_\ \_\ \__\\
 \/____/ \/_/\/_/\/__/\/_/ \/_/ \/__/\/_/\/____/ \/__/\/____/ \/_/       \/____/\/__,_ /\/_/\/__/
                                                                                                 '''
    exit2='''
                 __                                                                              
              __/\ \__                                                                           
   __   __  _/\_\ \ ,_\                                                                          
 /'__`\/\ \/'\/\ \ \ \/                                                                          
/\  __/\/>  </\ \ \ \ \_                                                                         
\ \____\/\_/\_\\\\ \_\ \__\                                                                        
 \/____/\//\/_/ \/_/\/__/                                                                        
    '''
    play1='''
 ____  __     ___  _  _                                                           
 || \\\\ ||    // \\\\ \\\\//                                                           
 ||_// ||    ||=||  )/                                                            
 ||    ||__| || || //                                                             
                              '''
    inst1='''
 __ __  __  __  ______ ____  __ __   ___ ______ __   ___   __  __  __             
 || ||\ || (( \ | || | || \\\\ || ||  //   | || | ||  // \\\\  ||\ || (( \            
 || ||\\\\||  \\\\    ||   ||_// || || ((      ||   || ((   )) ||\\\\||  \\\\             
 || || \|| \_))   ||   || \\\\ \\\\_//  \\\\__   ||   ||  \\\\_//  || \|| \_))            
                                                                                '''
    charedit1='''
   ___ __  __  ___  ____   ___    ___ ______  ____ ____      ____ ____   __ ______
  //   ||  || // \\\\ || \\\\ // \\\\  //   | || | ||    || \\\\    ||    || \\\\  || | || |
 ((    ||==|| ||=|| ||_// ||=|| ((      ||   ||==  ||_//    ||==  ||  )) ||   ||  
  \\\\__ ||  || || || || \\\\ || ||  \\\\__   ||   ||___ || \\\\    ||___ ||_//  ||   ||  
                                               '''
    exit1='''
  ____ _   _ __ ______                                                            
 ||    \\\\ // || | || |                                                            
 ||==   )X(  ||   ||                                                              
 ||___ // \\\\ ||   ||                                                              
                       '''                                                                                          
    while True:
        hear=listen()
        sleep(0.1)
        if hear==274:
            if selected<4:
                selected+=1
        elif hear==273:
            if selected>1:
                selected-=1
        elif hear==13:
            return selected
        else:
            continue
        print "\n"*20
        if selected==1:
            print play2 +inst1 +charedit1 +exit1
        elif selected==2:
            print play1 +inst2 +charedit1 +exit1
        elif selected==3:
            print play1 +inst1 +charedit2 +exit1
        elif selected==4: 
            print play1 +inst1 +charedit1 +exit2
        print "\n"*20





def home():
    sleep(0.1)
    global skin 
    global x
    global y
    global lvlS
    global lvlE
    global width
    global ch
    x=8
    rate=-1
    y=8
    lvlS=1
    lvlE=width
    for event in pygame.event.get():
        sleep(0.3)
        if event.type == pygame.QUIT:
            looping = False
            pygame.display.quit()
            quit()
    ch=mainmenu()
    if ch==1:#1
        mainloop()
    elif ch==2:
        slowprint ("Instructions: ")
        slowprint (" ***** please select the PYGAME WINDOW ***** \n ***** or else the keys will NOT work ***** ")
        slowprint (" Controls ........... ARROW KEYS. ")
        slowprint (" PAUSE .............. SPACEBAR ")
        slowprint (" RESUME ............. SPACEBAR ")
        slowprint (" Enjoy the game! (Press any key) ") 
    elif ch==3:
        skin.create()
    elif ch==4:
        looping = False
        pygame.display.quit()
        quit()

def listen():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            looping = False
            pygame.display.quit()
            quit()
        elif event.type == 2:
            return event.key   

#main

def initialize():
    global controlstack
    global y
    global rate
    global x
    global width
    global loaded
    global frame1
    global ground
    global lvlload
    global lvlS
    global lvlE
    global tracker
    global backup
    global permitr
    global permitl
    global looping
    global pause
    global srate
    global iterate
    global itercount
    global skin
    global lvlcomplete
    global gameover
    global dj
    global ch
    global selected
    global canjump
    canjump=True
    selected=0
    ch=0
    dj=True
    gameover=False
    lvlcomplete=False
    iterate=False
    itercount=0
    srate=0
    pause=False
    controlstack=["n",]
    backup=False
    permitr=True
    permitl=False
    lvlS=1
    lvlload=[0,0]     #just to initialize as list
    ground=30
    frame1=""
    loaded=False
    width=75 
    x=8
    rate=-1
    y=8
    frame("")
    looping = True
    lvlE=width
    tracker=[[8,8,lvlS,lvlE]]*100 #tracks 10 previous coordinates
    skin=character()

global controlstack
global y
global rate
global x
global width
global loaded
global frame1
global ground
global lvlload
global lvlS
global selected
global lvlE
global tracker
global backup
global permitr
global permitl
global looping
global pause
global srate
global iterate
global itercount
global skin
global gameover
global lvlcomplete
global dj
global ch
global canjump
initialize()
while True:
    home()
