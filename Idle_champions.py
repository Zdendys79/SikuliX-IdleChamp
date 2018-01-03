# 
import time
import random
import pprint
import datetime
# pylint: disable=invalid-name
Settings.MoveMouseDelay = 0.1
#Settings.MinSimilarity = 0.8
Settings.ActionLogs = 0

class Counters:
    """
    Definice počítadel
    """
    def __init__(self):
        self.rounds = 0
        self.bonuses = 0
        self.ultimates = 0
        self.clicks = 0
        self.lvl_ups = 0

    def reset(self):
        """
        Smaže počítadla až na lvl_ups
        """
        self.rounds = 0
        self.bonuses = 0
        self.ultimates = 0
        self.clicks = 0

    def addRound(self, rnd=1):
        self.rounds += rnd

    def addBonus(self, bonus=1):
        self.bonuses += bonus

    def addUltimate(self, ultimate=1):
        self.ultimates += ultimate

    def addClick(self, click=1):
        self.clicks += click

    def addLvl(self, lvl=1):
        self.lvl_ups += lvl

    def echo(self):
        return [self.rounds, self.bonuses, self.ultimates, self.clicks, self.lvl_ups]

def makeReg(x, y, w, h, highlight_time=2, throw_exception=False, auto_wait_timeout=1):
    """
    Definice regionů
    """
    reg = Region(x, y, w, h)
    reg.highlight(highlight_time)
    reg.setThrowException(throw_exception)
    reg.setAutoWaitTimeout(auto_wait_timeout)
    return(reg)
        
# counters = {'rounds' : 0, 'bonus' : 0, 'ultimates' : 0, 'clicks' : 0, 'lvl_up' : 0}
txt = []
tc = time.clock()
counters = Counters()
unlocked_list_x = []

images = {
    'back' : "1506712612259.png",
    'left' : "1506712658938.png",
    'right': "1506712696546.png",
    'ten'  : "1506713106664.png",  # Ten levels up (switch left bottom button to 10)
    'xxv'  : ".png",  # 25 levels up (switch left bottom button to 25)
    'upg'  : ".png",  # Upgrade levels up (switch left bottom button to Upg)   
    'next' : "1506713166863.png",
    'logo' : "1514991346441.png",
#    "1506713410566.png",
    'golds' : "1506715446433.png",
    'slct' : "1506716349068.png",
    'unlocked' : "unlocked.png",
    'gold' : "gold.png"
    }

# List of Champions where ultimate attacks has been used.
champions = ['Bruenor', 'Celeste', 'Nayeli', 'Stoki', 'Calliope', 'Asharra', 'Minsc', 'Delina', 'Makos', 'Tyril']

bonuses = ['stone', 'gnome']

use = {
    'pausing' : [5, 15], # delay on each loop between x<=>y [in seconds]
    'bonuses' : False,
    'ultimates' : True,
    'upgrade_clicking' : False, # disable it for lot of Champions or 'gold' lvlups
    'clicking' :  [2, 5],
#    'level_up' : False,
#    'level_up' : 'ten',
    'level_up' : 'gold',
    'upgrades' : True,
    'next_area' : 4, # goto next area each X levelups
    'collect_golds' : False
    }


### Regions
lt = SCREEN.find(Pattern(images['logo']).similar(0.80)) # LeftTop corner of game window

pcs = makeReg(lt.x, lt.y + 26, 1280, 720) # Game window based on the game resolution
bone = makeReg(lt.x, lt.y + 125, 1280, 200) # Bonuses line
ulti = makeReg(lt.x + 200, lt.y + 551, 700, 30) # Champions ultimate attack buttons
lvls = makeReg(lt.x + 125, lt.y + 710, 1040, 30) # Champions levels buying buttons

#if use['clicking'][0] > 0:
#    lvls = makeReg(lt.x + 125, lt.y + 710, 1040, 30) # Champions levels buying buttons
#else:
#    lvls = makeReg(lt.x + 225, lt.y + 710, 940, 30) # Champions levels buying buttons
lvlx = makeReg(lt.x + 125, lt.y + 693, 1040, 16) # Champions actual levels

"""
pcs = Region(lt.x, lt.y + 26, 1280, 720) # Game window based on the game resolution
pcs.highlight(1)
pcs.setThrowException(False)
pcs.setAutoWaitTimeout(0.5)

ulti = Region(lt.x + 200, lt.y + 551, 700, 30) # Champions ultimate attack buttons
ulti.highlight(1)
ulti.setThrowException(False)
ulti.setAutoWaitTimeout(1)

bone = Region(lt.x, lt.y + 125, 1280, 130) # Bonuses line
bone.highlight(1)
bone.setThrowException(False)
bone.setAutoWaitTimeout(1)

lvls = Region(lt.x + 125, lt.y + 710, 1040, 30) # Champions levels buying buttons
lvls.highlight(1)
lvls.setThrowException(False)
lvls.setAutoWaitTimeout(1)
"""

def resetValues():
    global txt, tc
    counters.reset()
    txt = []
    tc = time.clock()

def printReport(timecounter, text):
    text += [pprint.saferepr(counters.echo())]
    strtime = "{:0>8}".format(datetime.timedelta(seconds=round(time.clock() - timecounter, 0)))
    print(strtime + " " + ", ".join(text))
    resetValues()

def findBonus():
    for b in bonuses:
        bonus_picture = "bonus_"+b+".png"
        if  bone.exists(Pattern(bonus_picture).similar(0.75).targetOffset(-5, 5)):
            bone.click()
            counters.addBonus()

def useUltimate():
    ultimate_picture = "ulti_"+champions[random.choice(range(len(champions)))]+".png"
    if  ulti.exists(Pattern(ultimate_picture).similar(0.95)):
        ulti.click()
        counters.addUltimate()
        wait(0.5)
        pcs.mouseMove(goOut())

def goOut():
    if pcs.exists(images['back']): #find backpack
        x = pcs.getLastMatch().x + random.randint(-50, 200)
        y = pcs.getLastMatch().y - random.randint(30, 200)
        lo = Location(x, y)
    else:
        lo = False
    return lo

def searchUnlocked():
    global unlocked_list_x
    lvlx.findAll(images['unlocked'])
    unlocked_list_x = []
    unl = lvlx.getLastMatches()
    if unl is not None:
        for u in unl:
            unlocked_list_x += [u.x]
    printReport(tc, ["Nalezeno "+str(len(unlocked_list_x))+" odemcenych hrdinu."])

### sranda začíná
resetValues()
#searchUnlocked()

while True:
    clck = False
    counters.addRound()

### Pausing
    if use['pausing'][0] > 0:
        wait(random.randint(use['pausing'][0], use['pausing'][1]))

### Bonuses collecting
    if use['bonuses']:
        findBonus()

### Use random ultimate
    if use['ultimates']:
        useUltimate()

### Buy "Click damage"
    if use['upgrade_clicking'] and lvls.exists(images['ten']):
        pcs.click(Location(lt.x + 150, lt.y + 725))
        wait(0.5)

### .0 Level up Champions
    if bool(use['level_up']) and lvls.exists(Pattern(images[use['level_up']]).similar(0.99)):
#        if not bool(Counters.rounds%5): # every x cycles
#            searchUnlocked()
        lvls.click(lvls.getLastMatch())
        clck = True
        wait(0.5)

### .1 Add upgrade
#        if use['upgrades']:
#            loc = Location(lvls.getLastMatch().x + 80, lvls.getLastMatch().y + 10)
#            mouseMove(loc)
#            lvls.click(loc)
#            wait(1)

### .1.0 Select Champion path
        pcs.findAll(images['slct'])
        sel = pcs.getLastMatches()
        if sel is not None:
            pcs.click(random.choice(list(sel)))
            wait(0.5)

### .2 Go to next area
        counters.addLvl()
        if (counters.lvl_ups % use['next_area']) == 0 and bone.exists(images['next']):
#            wait(120) # to refill some ultimates
            bone.click()
            wait(1)
            txt += ["NEXT AREA"]

### .3 Print report
        printReport(tc, txt)

### Collect golds around battlefield
    if use['collect_golds']:
        pcs.findAll(images['golds'])
        col = pcs.getLastMatches()
        if col is not None:
            cg = list(col)
            cg.sort(key=lambda m: (m.x*m.x)+(m.y*m.y))
            for c in cg:
                pcs.mouseMove(c)

### Clicking on field - manual killing mobs
    loc = goOut()
    if use['clicking'][0] > 0 and bool(loc):
        clickcount = random.randint(use['clicking'][0], use['clicking'][1])
        counters.addClick(clickcount)
        for _ in range(clickcount):
            pcs.click(loc)
