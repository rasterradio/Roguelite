import libtcodpy as libtcod
import textwrap
from random import randint
 
#actual size of the window
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

#variables for GUI
BAR_WIDTH = 20
PANEL_HEIGHT = 1
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT
MSG_X = BAR_WIDTH + 2
MSG_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
MSG_HEIGHT = PANEL_HEIGHT - 1

FOV_ALGO = 0  #default FOV algorithm
FOV_LIGHT_WALLS = False  #light walls or not
LIGHT_RADIUS = 10

VIEWSTATE = "ascii"

color_dark_wall = libtcod.Color(0, 0, 100)
color_light_wall = libtcod.Color(130, 110, 50)
color_dark_ground = libtcod.Color(50, 50, 150)
color_light_ground = libtcod.Color(200, 180, 50) 
 
class Tile:
    #a tile of the map and its properties
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked

        #all tiles start unexplored
        self.explored = False
        #by default, if a tile is blocked, it also blocks sight
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight

#define combatants which enemies and player will inherit from. combatants will have anonymous functions which will run on defined events based on combat data
#event examples, event on low hp, event on low bullets, event on being hit 4 times in a row, event on hitting the player 4 times in a row, 
#event on the player taking out a gun, event on the enemy taking out a gun   
#event on the enemy dying
#event on the player dying
#combatant stats include hp, dmg, bullets, gun
# player and enemy choices are stored in the combat class, combat class also contains info that is printed to the screen,
#including player choices and current state of battle


class Combat:
    #a class containing logic necessary to run during the combat state
    def __init__(self, myself, enemy):
        self.player_results = read_grid_text('gridTextExample.txt', 3, 3)
        self.state = ""
        self.choices = []
        self.enemy = enemy
        self.myself = myself
        self.run()

    def determineIntent(self, enemy):
        return "fist"

    def run(self):
        myself = self.myself
        myself_result = "PLAYERRESULT"
        enemy = self.enemy
        enemy_result = "ENEMYRESULT"
        while True:
            print self.state
            if enemy.stagger > 0:
                enemy.stagger -= 1
            if myself.stagger > 0:
                myself.stagger -= 1

            print "---STATS---"
            print "bullets =" + str(myself.bullets)
            print "health =" + str(myself.hp) + "/" + str(myself.maxHp)  
            print "---OPTIONS---"
            print "fist"
            print "gun"
            print "fire"
            print "escape"
            print ""

            player_choice = raw_input("=>")
            if myself.stagger == 0:
                if player_choice == "fist":
                    enemy.hp -= myself.dmg

                if player_choice == "gun" and myself.gun:
                    myself.cocked = True
                    enemy.seeGun()

                if player_choice == "fire" and myself.cocked and myself.bullets > 0:
                    enemy.hp -= 4
                    enemy.stagger += 1
                    myself.bullets -= 1

            print myself_result

            enemy_choice = self.determineIntent(self.enemy)
            if enemy.stagger == 0:
                if enemy_choice == "fist":
                    myself.hp -= enemy.dmg

                if enemy_choice == "gun" and enemy.gun:
                    enemy.cocked = True
                    myself.seeGun()

                if enemy_choice == "fire" and enemy.gun and enemy.bullets > 0:
                    myself.hp -= 4
                    myself.stagger += 1
                    enemy.bullets -= 1

            print enemy_result

            if player.hp <= 0:
                game_state = 'dead'

            myself.update()
            enemy.update()

            if player_choice == "escape" and myself.stagger == 0:
                break
            if enemy_choice == "escape" and enemy.stagger == 0:
                break
            if enemy.dead:
                myself.bullets += enemy.bullets
                if myself.bullets > 6:
                    myself.bullets = 6
                myself.gun = myself.gun or enemy.gun
                break
class Script:
    def __init__(self, name=None, data=None, scripts=None, event=lambda:None):
        self.name = name
        self.data = data
        self.scripts = scripts
        self.event = event

    def __str__(self):
        return str(self.name)        

    def getChoice(self):
        self.choice = raw_input("=>")
        if not self.scripts.keys():
            return False
        if self.choice in self.scripts.keys():
            return True
        return False

    def run(self):
        while True:
            print
            print(self.data)
            print

            #render the screen
            VIEWSTATE = 'text'
            self.event()
            if self.scripts:
                for scr in self.scripts.values():
                    print(scr.name)
            if not self.getChoice():
                break
            if self.scripts:
                self = self.scripts.get(self.choice)     

#class Encounter:
    #encounter has to be just data
    #
    #encounter has a collection of objects which can be carried between landmarks to make the text events more variable
    #
    #encounter will likely need a subset of it's objects to be defined as combatants, since these objects will trigger the combat state
    
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
 
    def move(self, dx, dy):
        #move by the given amount, if the destination is not blocked
        if not map[self.x + dx][self.y + dy].blocked:
            self.x += dx
            self.y += dy
 
    def draw(self):
        #fade objects out of FOV
        if map[self.x][self.y].explored and not (libtcod.map_is_in_fov(fov_map, self.x, self.y)):
            libtcod.console_set_default_foreground(con, color_light_ground * libtcod.dark_gray)
            libtcod.console_put_char(con, self.lastX, self.lastY, self.char, libtcod.BKGND_NONE)

        if libtcod.map_is_in_fov(fov_map, self.x, self.y):
            libtcod.console_set_default_foreground(con, self.color)
            libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)
            self.lastX = self.x
            self.lastY = self.y

    def clear(self):
        #erase the character that represents this object
        libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)
        #if libtcod.map_is_in_fov(fov_map, self.x, self.y):
            #libtcod.console_put_char_ex(con, self.x, self.y, '.', libtcod.white, libtcod.dark_blue)

    def collide(self, object):
        if self.y == object.y and self.x == object.x:
            return True
        else:
            return False


class Combatant(Object):
    def __init__(self, x, y, char, hp, dmg, bullets, gun, halfHp, lowBullets, seeGun, water):
        Object.__init__(self, x, y, char)
        self.hp = hp
        self.maxHp = hp
        self.dmg = dmg
        self.bullets = bullets
        self.gun = gun
        self.dead = 0
        self.halfHp = halfHp
        self.lowBullets = lowBullets
        self.seeGun = seeGun
        self.water = water
        self.stagger = 0
        self.cocked = False

    def update(self):
        if self.hp < self.maxHp/2:
            self.halfHp()
        if self.bullets < 3 and self.gun:
            self.lowBullets()
        if self.hp <= 0:
            self.dead = True


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
                                 
def make_map():
    map_data = open('map.txt', 'r')

    x = 0
    y = -1
    for line in map_data:
        if y == -1 and line.find('x') != -1:
            global MAP_WIDTH
            MAP_WIDTH = int(line.split('x', 2)[0])
            global MAP_HEIGHT
            MAP_HEIGHT = int(line.split('x', 2)[1])

            global map
            map = [[Tile(False) for a in range(MAP_HEIGHT)] for b in range(MAP_WIDTH)]

        if y < MAP_HEIGHT and y >= 0:
            for char in line:
                if x < MAP_WIDTH:
                    if char == '_':
                        map[x][y] = Tile(False)
                    if char == 'X':
                        map[x][y] = Tile(True, True)
                x += 1
        x = 0
        y += 1

def read_grid_text(file, xRange, yRange):
    text_file = open(file, 'r')
    text_data = [["" for a in range(xRange)] for b in range(yRange)]
    x = 0
    y = 0
    for line in text_file:
        for word in line.split(';'):
            if x < xRange and y < yRange:
                text_data[x][y] = word
            x += 1
        x = 0
        y += 1

    return text_data

    #fill map with "unblocked" tiles
    #map = [[ Tile(False)
     #   for y in range(MAP_HEIGHT) ]
      #      for x in range(MAP_WIDTH) ]
 
    #place two pillars to test the map
    #map[30][22].blocked = True
    #map[30][22].block_sight = True
    #map[50][22].blocked = True
    #map[50][22].block_sight = True
    #map[11][15].block_sight = True

    map_data.close()

def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color):
    #render a bar (HP, experience, etc). first calculate the width of the bar
    bar_width = int(float(value) / maximum * total_width)
 
    #render the background first
    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)
 
    #now render the bar on top
    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)
 
    #finally, some centered text with the values
    libtcod.console_set_default_foreground(panel, libtcod.black)
    libtcod.console_print_ex(panel, x + total_width / 2, y, libtcod.BKGND_NONE, libtcod.CENTER,
        name + ': ' + str(value) + '/' + str(maximum))

def render_text():
    #blit the contents of "con" to the root console
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

    #prepare to render the GUI panel
    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

def render_ascii():
    global fov_map, color_dark_wall, color_light_wall
    global color_dark_ground, color_light_ground
    global fov_recompute
 
    if fov_recompute:
        #recompute FOV if needed (the player moved or something)
        fov_recompute = False
        #check to see if player is inside a forest/trees, later will need to be able to check if player is in forest or on mountain and adjust FOV
        if map[player.x][player.y].block_sight == True:
            libtcod.map_compute_fov(fov_map, player.x, player.y, LIGHT_RADIUS/2, FOV_LIGHT_WALLS, FOV_ALGO)
        else:
            libtcod.map_compute_fov(fov_map, player.x, player.y, LIGHT_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)
 
        #go through all tiles, and set their background color according to the FOV
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = map[x][y].block_sight
                if not visible:
                    if map[x][y].explored:
                        libtcod.console_set_char_background(con, x, y, libtcod.white, libtcod.BKGND_SET)
                    else:
                        #white FOV
                        libtcod.console_set_char_background(con, x, y, libtcod.white, libtcod.BKGND_SET)
                else:
                    #it's visible
                    if wall:
                        #libtcod.console_set_char_background(con, x, y, color_light_wall, libtcod.BKGND_SET )
                        libtcod.console_put_char_ex(con, x, y, '#', libtcod.black, libtcod.white)
                    else:
                        #libtcod.console_set_char_background(con, x, y, color_light_ground, libtcod.BKGND_SET )
                        libtcod.console_put_char_ex(con, x, y, '.', libtcod.grey, libtcod.white)
                    map[x][y].explored = True
    
    #draw all objects in the list except for the player, who appears over other objects so is drawn last
    for object in objects:
        if object != player:
            object.draw()
    player.draw()

    #blit the contents of "con" to the root console
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

    #prepare to render the GUI panel
    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    #print the game messages, one line at a time
    y = 1
    for (line, color) in game_msgs:
        libtcod.console_set_default_foreground(panel, color)
        libtcod.console_print_ex(panel, MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
        y += 1

    #show the player's stats
    #render_bar(1, 1, BAR_WIDTH, 'HP', player.hp, player.maxHp,
        #libtcod.light_red, libtcod.darker_red)

    #blit the contents of "panel" to the root console
    libtcod.console_blit(panel, 0, 0, SCREEN_WIDTH, PANEL_HEIGHT, 0, 0, PANEL_Y)

     #show the player's stats
    #libtcod.console_set_default_foreground(con, libtcod.black)
    #water = 10
    libtcod.console_print_ex(0, 1, SCREEN_HEIGHT - 2, libtcod.BKGND_NONE, libtcod.LEFT,
        'HP ' + str(player.hp) + '/' + str(player.maxHp))
    libtcod.console_print_ex(0, 15, SCREEN_HEIGHT - 2, libtcod.BKGND_NONE, libtcod.LEFT,
        str(player.bullets) + ' ' + 'Bullets')
    libtcod.console_print_ex(0, 29, SCREEN_HEIGHT - 2, libtcod.BKGND_NONE, libtcod.LEFT,
         'Water ' + str(player.water) + '/10')

def message(new_msg, color = libtcod.white):
    #split the message if necessary, among multiple lines
    new_msg_lines = textwrap.wrap(new_msg, MSG_WIDTH)
 
    for line in new_msg_lines:
        #if the buffer is full, remove the first line to make room for the new one
        if len(game_msgs) == MSG_HEIGHT:
            del game_msgs[0]
 
        #add the new line as a tuple, with the text and the color
        game_msgs.append( (line, color) )

def handle_mouse():
    mouse = libtcod.mouse_get_status()
    if mouse.lbutton:
        if mouse.cx == 0 and mouse.cy == 0:
            print "MOUSE" 

def handle_keys():
    global fov_recompute
 
    #key = libtcod.console_check_for_keypress()  #real-time
    key = libtcod.console_wait_for_keypress(True)  #turn-based
 
    if key.vk == libtcod.KEY_ENTER and key.lalt or key.vk == libtcod.KEY_ENTER and key.ralt:
        #Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    #if game_state == 'dead':
        #if key.vk != libtcod.KEY_NONE:
            #game_state == 'playing'
 
    elif key.vk == libtcod.KEY_ESCAPE:
        return True  #exit game

    if game_state == 'playing':
        #movement keys
        if libtcod.console_is_key_pressed(libtcod.KEY_UP):
            player.move(0, -1)
            fov_recompute = True
            #if player.x and player.y != house x and y or town x and y:
            player.water-=1
 
        elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
            player.move(0, 1)
            fov_recompute = True
            player.water-=1
 
        elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
            player.move(-1, 0)
            fov_recompute = True
            player.water-=1
 
        elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
            player.move(1, 0)
            fov_recompute = True
            player.water-=1

        #enable for thirst mechanic
        if player.water == 0:
            player_death(player)
 
def player_death(player):
    global game_state
    game_state = 'dead'
    libtcod.console_clear(0)
    libtcod.console_print_ex(0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, libtcod.BKGND_NONE, libtcod.CENTER, "The world fades.")
    libtcod.console_flush()

def intro():
    game_state = 'dead'
    libtcod.console_clear(0)
    libtcod.console_print_ex(0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 5, libtcod.BKGND_NONE, libtcod.CENTER, "ROGUELITE")
    libtcod.console_print_ex(0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, libtcod.BKGND_NONE, libtcod.CENTER, "This place is no longer safe, mi hijo. You must escape.")
    if randint(0,1) == 0:
        libtcod.console_print_ex(0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 5, libtcod.BKGND_NONE, libtcod.CENTER, "Created by Ian Colquhoun and Wilson Hodgson")
    else:
        libtcod.console_print_ex(0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 5, libtcod.BKGND_NONE, libtcod.CENTER, "Created by Wilson Hodgson and Ian Colquhoun")

    libtcod.console_flush()

 
#############################################
# Initialization & Main Loop
#############################################
 
libtcod.console_set_custom_font('lucida10x10_gs_tc.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'roguelite', False)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
panel = libtcod.console_new(SCREEN_WIDTH, PANEL_HEIGHT)

def handleHit():
    print("OWCH")

def handleLowAmmo():
    print("NoAmmo")

def handleSeeGun():
    print("YIKES")

player = Combatant(25, 23, '@', 20, 2, 6, True, handleHit, handleLowAmmo, handleSeeGun, 10)

tree = Object(11, 15, 't') #tree has to be grey, is there a way to make colours override default libtcod.black? Tree functions like non-object except for FOV, shouldn't have fade'

npc = Combatant(SCREEN_WIDTH/2 - 5, SCREEN_HEIGHT/2, '&', 20, 1, 0, False, handleHit, handleLowAmmo, handleSeeGun, 0)
 
def handleCombat():
    Combat(player, npc)

holeInMound = Script("a hole", "You reach inside the hole, you can't reach the end of the hole.", None, handleCombat)
discoverMound = Script("Atop the Mound", "on the plain, a two foot high vantage point can seem significant, until you view the hawk overhead.", {holeInMound.name:holeInMound})
holeInMound.scripts = {discoverMound.name:discoverMound}
mound = Landmark(player.x + 1, player.y + 2, '^', "Mound", [player], discoverMound)

#the list of objects with those two
objects = [npc, player, mound, tree]
 
#generate map (at this point it's not drawn to the screen)
make_map()
 
#create the FOV map, according to the generated map
fov_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
for y in range(MAP_HEIGHT):
    for x in range(MAP_WIDTH):
        libtcod.map_set_properties(fov_map, x, y, not map[x][y].block_sight, not map[x][y].blocked)
 
fov_recompute = True
game_state = 'playing'

#create the list of game messages and their colors, starts empty
game_msgs = []
start_game = False
#game_state = 'dead'
 
while not libtcod.console_is_window_closed():
    #render the screen
    if start_game == False:
        intro()
        if libtcod.console_wait_for_keypress(True).vk != libtcod.KEY_NONE:
            start_game = True
    if game_state != 'dead':
        #render_all()
        render_ascii()
        libtcod.console_flush()
 
    #erase all objects at their old locations, before they move
    for object in objects:
        object.clear()
 
    objects[2].update()
    if player.x == npc.x and player.y == npc.y:
        Combat(player, npc)
    #handle keys and exit game if needed
    if VIEWSTATE == 'ascii':
        exit = handle_keys()
    else:
        choice = handle_mouse()
    if exit:
        break