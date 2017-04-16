from ObjectMod import Object
from HelperFunctions import MessageLog

class Combatant(Object):
    def __init__(self, x, y, char, hp, dmg, bullets, gun, halfHp, lowBullets, seeGun, water, maxWater, lowWater = lambda: None):
        Object.__init__(self, x, y, char)
        self.hp = hp
        self.maxHp = hp
        self.dmg = dmg
        self.bullets = bullets
        self.gun = gun
        self.halfHp = halfHp
        self.lowBullets = lowBullets
        self.lowWater = lowWater
        self.seeGun = seeGun
        self.water = water
        self.maxWater = maxWater
        self.staggerLevel = 0
        self.stagger = False
        self.cocked = False
        self.halfHpThreshold = False
        self.halfWaterThreshold = False

    def combat_update(self):
        if self.hp < self.maxHp/2 and self.halfHpThreshold == False:
            self.halfHpThreshold = True
            self.halfHp()
            self.stagger = True
        if self.cocked == True and self.stagger == True:
            self.cocked = False
        if self.bullets < 3 and self.gun:
            self.lowBullets()

    def update(self):
        Object.update(self)
        #if self.water < self.maxWater and self.halfWaterThreshold == False:
            #self.halfWaterThreshold = True
            #self.lowWater()
