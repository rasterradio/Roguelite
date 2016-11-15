import libtcodpy as libtcod
 
#actual size of the window
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
 
#size of the map
MAP_WIDTH = 80
MAP_HEIGHT = 45

 
color_dark_wall = libtcod.Color(0, 0, 100)
color_dark_ground = libtcod.Color(50, 50, 150)
 
 
class Tile:
    #a tile of the map and its properties
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked
 
        #by default, if a tile is blocked, it also blocks sight
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight
		
class Combat:
	#a class containing logic necessary to run during the combat state
		
class Script:
	#a script/ or story (basically an event) is a class that contains logic necessary for running a Landmark in the text adventure state,
	#or a landmark and its encounter in text adventure state
		
class Encounter:
	#encounter has to be just data
	#
	#encounter has a collection of objects which can be carried between landmarks to make the text events more variable
	#
	#encounter will likely need a subset of it's objects to be defined as combatants, since these objects will trigger the combat state
 
 class Landmark(Object):
	#a location on the map that you can enter
	def __init__(self, x, y, char, color, name, objects, event)
		Object.__init__(self, x, y, char, color)
		self.name = name
		self.objects = objects
		self.event = event
		
	def update(self):
		for object in objects
			if Object.collide(self, object)
				#run event if available
				self.runEvent(self)
								
					
	
	
class Object:
    #this is a generic object: the player, a monster, an item, the stairs...
    #it's always represented by a character on screen.
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
 
    def move(self, dx, dy):
        #move by the given amount, if the destination is not blocked
        if not map[self.x + dx][self.y + dy].blocked:
            self.x += dx
            self.y += dy
 
	def update(self):
		for object in objects
			if collide(self, object)
			######Do something
 
    def draw(self):
        #set the color and then draw the character that represents this object at its position
        libtcod.console_set_default_foreground(con, self.color)
        libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)
 
    def clear(self):
        #erase the character that represents this object
        libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)
 
	def collide(self, object)
		if self.y == object.y and self.x == object.x:
			return True
		else return False
 
def make_map():
    global map
 
    #fill map with "unblocked" tiles
    map = [[ Tile(False)
        for y in range(MAP_HEIGHT) ]
            for x in range(MAP_WIDTH) ]
 
    #place two pillars to test the map
    map[30][22].blocked = True
    map[30][22].block_sight = True
    map[50][22].blocked = True
    map[50][22].block_sight = True
 
 
def render_all():
    global color_light_wall
    global color_light_ground
 
    #go through all tiles, and set their background color
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            wall = map[x][y].block_sight
            if wall:
                libtcod.console_set_char_background(con, x, y, color_dark_wall, libtcod.BKGND_SET )
            else:
                libtcod.console_set_char_background(con, x, y, color_dark_ground, libtcod.BKGND_SET )
 
    #draw all objects in the list
    for object in objects:
        object.draw()
 
    #blit the contents of "con" to the root console
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
 
def handle_keys():
    #key = libtcod.console_check_for_keypress()  #real-time
    key = libtcod.console_wait_for_keypress(True)  #turn-based
 
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        #Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
 
    elif key.vk == libtcod.KEY_ESCAPE:
        return True  #exit game
 
    #movement keys
    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        player.move(0, -1)
 
    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        player.move(0, 1)
 
    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        player.move(-1, 0)
 
    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        player.move(1, 0)
 
 
#############################################
# Initialization & Main Loop
#############################################
 
libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Roguelite', False)

con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
 
#create object representing the player
player = Object(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, '@', libtcod.white)
 
#create an NPC
npc = Object(SCREEN_WIDTH/2 - 5, SCREEN_HEIGHT/2, '@', libtcod.yellow)
 
#the list of objects with those two
objects = [npc, player]
 
#generate map (at this point it's not drawn to the screen)
make_map()
 
 
while not libtcod.console_is_window_closed():
 
    #render the screen
    render_all()
 
    libtcod.console_flush()
 
    #erase all objects at their old locations, before they move
    for object in objects:
        object.clear()
 
    #handle keys and exit game if needed
    exit = handle_keys()
    if exit:
        break
		
raw_input("PRESS ENTER")