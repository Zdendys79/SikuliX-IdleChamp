import time
import sys
import math
import random
Settings.MoveMouseDelay = 0.1
#Settings.MinSimilarity = 0.8
Settings.ActionLogs=0
tc = time.clock()

def t(tx): #text zobrazený v logu
    global tc
    tc_old = tc
    tc = time.clock()
    print(str(round(tc - tc_old,1))+" "+tx)

images = {
    'back' : "1506712612259.png",
    'left' : "1506712658938.png",
    'right': "1506712696546.png",
    'ten'  : "1506713106664.png",  # Ten levels up
    'twfi' : '', # TwentyFive levels up
    'next' : "1506713166863.png",
    'logo' : "1506713410566.png",
    'gold' : "1506715446433.png",
    'slct' : "1506716349068.png"
        }

# List of Champions where ultimate attacks has been used.
champions = ['Bruenor','Celeste','Naieli','Stoki','Calliope','Asharra','Delina']


### Regions
scr = SCREEN
lt = scr.find(Pattern(images['logo']).similar(0.80)) # LeftTop corner of game window
pcs = Region(lt.x, lt.y + 26, 1280 , 720) # based on the game resolution
pcs.highlight(1)
pcs.setThrowException(False)
pcs.setAutoWaitTimeout(0.5)

lvls = Region(lt.x + 125, lt.y + 710, 1040 , 30) # Champion level buying buttons
lvls.highlight(1)
lvls.setThrowException(False)
lvls.setAutoWaitTimeout(1)

ulti = Region(lt.x + 200, lt.y + 551, 700 , 30) # ultimate attacks region
ulti.highlight(1)
ulti.setThrowException(False)
ulti.setAutoWaitTimeout(1)

txt = []
counters = { 'rounds' : 0, 'ultimates' : 0, 'clicks' : 0 }

while True:
    clck = False
    counters['rounds']+= 1
### 0. Pausing    
    wt = random.randint(10, 30)
    txt+= ["w(" + str(wt) + ")"]
    wait( wt )

### 1. Use random ultimate
    ch_key = random.choice(range(len(champions)))
    if ulti.exists(Pattern("ulti_"+champions[ch_key]+".png").similar(0.95)):
        ulti.click()
        counters['ultimates']+= 1
        wait(0.5)

### 2. Add clicking damage
    if False: ### Disable it for lot of Champions
#    if lvls.exists(images['ten']):
        pcs.click( Location(lt.x + 150, lt.y + 725 ) )
        wait(0.5)

### 3.0 Level up Champions
    if lvls.exists(images['ten']):
#    if False:
        clck = True
        lvls.click(lvls.getLastMatch())
        wait(0.5)
    ### 3.1 Add upgrade        
        if True:
            loc = Location(lvls.getLastMatch().x+50,lvls.getLastMatch().y+10)
            mouseMove(loc)
            lvls.click(loc)
            wait(1)
        ### 3.2 Select Champion path
            pcs.findAll(images['slct'])
            sel = pcs.getLastMatches()
            if sel is not None:
                sl = list(sel)
                pcs.click(random.choice(sl))
                wait(0.5)
        ### Print report
        txt+= ["Rounds : " + str(counters['rounds'])]
        txt+= ["Ultimates : " + str(counters['ultimates'])]
        txt+= ["Clicks : " + str(counters['clicks'])]
        txt+= ["LVL UP"]
        t(", ".join(txt))
        txt = []
        counters = { 'rounds' : 0, 'ultimates' : 0, 'clicks' : 0 }

### 3.3 Go to next area
        if random.randint(1, 3) == 3 and pcs.exists(images['next']):
            wait(180) # to refill ultimates
            pcs.click(pcs.getLastMatch())
            wait(1)
            txt+= ["NEXT"]

### 4. Collect golds around battlefield
#    if not clck:
    if False:
#        clck = True
        pcs.findAll(images['gold'])
        col = pcs.getLastMatches()
        if col is not None:
            cg = list(col)
            cg.sort(key = lambda m: (m.x*m.x)+(m.y*m.y))
            for c in cg:
                pcs.mouseMove(c)
    
### 5. Clicking on field - manual killing mobs
#    if not clck and random.randint(1, 3) == 3:
#    if not clck:
    if False:
        if pcs.exists(images['back']):
            loc = Location(pcs.getLastMatch().x + random.randint(-50,200),pcs.getLastMatch().y - random.randint(30,200))
            ccnt = random.randint(10, 40)
            counters['clicks']+= ccnt
            for x in range(0, ccnt):
                pcs.click(loc)