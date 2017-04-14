from ObjectMod import Object
from HelperFunctions import MessageLog

class Landmark(Object):
    #a location on the map that you can enter
    def __init__(self, x, y, char, name, objects, event):
        Object.__init__(self, x, y, char)
        self.name = name
        self.objects = objects
        self.event = event
        self.messages = MessageLog()

    def update(self):
        for obj in self.objects:
            if Object.collide(self, obj):
                #run event if available
                self.event.messages = MessageLog()
                self.event.run(self.messages)

    def follow(self, target, map):
        if (self.x != target.x or self.y != target.y):
            dx = target.x - self.x
            dy = target.y - self.y
            if (dx) : dx = dx / abs(dx)
            if (dy) : dy = dy / abs(dy)
            self.move(dx, dy, map)
    #def visited(self):
        #if player.x == self.x and player.y == self.y:
            #return True
    #need code so that landmarks will fade once visited
