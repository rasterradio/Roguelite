import libtcodpy as libtcod
#has to do with not not completing roguelite
class Object:
    #this is a generic object: the player, a monster, an item, the stairs...
    #it's always represented by a character on screen.
    def __init__(self, x, y, char):
        self.x = x
        self.y = y
        self.char = char
        self.color = libtcod.black
        #self.fadedColor = color - libtcod.dark_gray
        self.lastX = self.x
        self.lastY = self.y
 
    def move(self, dx, dy, map):
        #move by the given amount, if the destination is not blocked
        if not map[self.x + dx][self.y + dy].blocked:
            self.x += dx
            self.y += dy

    def update(self):
        return True
 
    def draw(self, con, map, fov_map):
        #fade objects out of FOV
        if map[self.x][self.y].explored and not (libtcod.map_is_in_fov(fov_map, self.x, self.y)):
            libtcod.console_set_default_foreground(con, libtcod.dark_gray)
            libtcod.console_put_char(con, self.lastX, self.lastY, self.char, libtcod.BKGND_NONE)

        if libtcod.map_is_in_fov(fov_map, self.x, self.y):
            libtcod.console_set_default_foreground(con, self.color)
            libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)
            self.lastX = self.x
            self.lastY = self.y

    def clear(self, con):
        #erase the character that represents this object
        libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)
        #if libtcod.roguelite.map_is_in_fov(fov_roguelite.map, self.x, self.y):
            #libtcod.console_put_char_ex(roguelite.con, self.x, self.y, '.', libtcod.white, libtcod.dark_blue)

    def collide(self, object):
        if self.y == object.y and self.x == object.x:
            return True
        else:
            return False