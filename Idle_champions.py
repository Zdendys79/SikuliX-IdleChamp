import time
import random
import pprint
import datetime
# pylint: disable=invalid-name
Settings.MoveMouseDelay = 0
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
        Smaže počítadla až na LVL_UP
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

# counters = {'rounds' : 0, 'bonus' : 0, 'ultimates' : 0, 'clicks' : 0, 'lvl_up' : 0}
txt = []
tc = time.clock()
counters = Counters()

images = {
    'back' : "1506712612259.png",
    'left' : "1506712658938.png",
    'right': "1506712696546.png",
    'ten'  : "1506713106664.png",  # Ten levels up
    'next' : "1506713166863.png",
    'logo' : "1506713410566.png",
    'gold' : "1506715446433.png",
    'slct' : "1506716349068.png"
    }

# List of Champions where ultimate attacks has been used.
champions = ['Bruenor', 'Celeste', 'Naieli', 'Stoki', 'Calliope', 'Asharra', 'Minsc', 'Delina']

bonuses = ['stone', 'gnome']

use = {
    'pausing' : False,
    'bonuses' : True,
    'ultimates' : True,
    'upgrade_clicking' : False, # disable it for lot of Champions
    'clicking' : False,
    'level_up' : 'ten',
    'upgrades' : True,
    'next_area' : 5, # goto next area each X levelups
    'collect_gold' : True
    }


### Regions
scr = SCREEN
lt = scr.find(Pattern(images['logo']).similar(0.80)) # LeftTop corner of game window

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

def resetValues():
    global txt, tc
    counters.reset()
    txt = []
    tc = time.clock()

def printReport(timecounter, text):
    text += ["LVL UP"]
    text += [pprint.saferepr(counters.echo())]
    strtime = "{:0>8}".format(datetime.timedelta(seconds=round(time.clock() - timecounter, 1)))
    print(strtime + " " + ", ".join(text))
    resetValues()

def findBonus():
    for b in bonuses:
        bonus_picture = "bonus_"+b+".png" 
        if  bone.exists(Pattern(bonus_picture).similar(0.75)):
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
        return Location(x, y)
    else:
        return False

### sranda začíná
resetValues()

while True:
    clck = False
    counters.addRound()

### Pausing    
    if use['pausing']:
        wait(random.randint(3, 12))

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
    if lvls.exists(images[use['level_up']]):
        lvls.click(lvls.getLastMatch())
        clck = True
        wait(0.5)

### .1 Add upgrade        
        if use['upgrades']:
            loc = Location(lvls.getLastMatch().x + 50, lvls.getLastMatch().y + 10)
            mouseMove(loc)
            lvls.click(loc)
            wait(1)

### .1.0 Select Champion path
            pcs.findAll(images['slct'])
            sel = pcs.getLastMatches()
            if sel is not None:
                pcs.click(random.choice(list(sel)))
                wait(0.5)

### .2 Go to next area
        counters.addLvl()
        if (counters.lvl_ups % use['next_area']) == 0 and pcs.exists(images['next']):
            wait(120) # to refill some ultimates
            pcs.click()
            wait(1)
            txt += ["NEXT AREA"]

### .3 Print report
        printReport(tc, txt)

### Collect golds around battlefield
    if use['collect_gold']:
        pcs.findAll(images['gold'])
        col = pcs.getLastMatches()
        if col is not None:
            cg = list(col)
            cg.sort(key=lambda m: (m.x*m.x)+(m.y*m.y))
            for c in cg:
                pcs.mouseMove(c)
    
### Clicking on field - manual killing mobs
    loc = goOut()
    if use['clicking'] and bool(loc):
        clickcount = random.randint(10, 40)
        counters.addClick(clickcount)
        for _ in range(clickcount):
            pcs.click(loc)