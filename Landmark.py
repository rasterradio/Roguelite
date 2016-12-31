from ObjectMod import Object

class Landmark(Object):
    #a location on the map that you can enter
    def __init__(self, x, y, char, name, objects, event):
        Object.__init__(self, x, y, char)
        self.name = name
        self.objects = objects
        self.event = event
        
    def update(self):
        for obj in self.objects:
            if Object.collide(self, obj):
                #run event if available
                self.event.run()

    #def visited(self):
        #if player.x == self.x and player.y == self.y:
            #return True
    #need code so that landmarks will fade once visited