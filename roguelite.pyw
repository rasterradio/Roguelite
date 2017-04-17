import libtcodpy as libtcod
import textwrap
from random import randint
import os
from math import sqrt
from time import *
#import Tile
#import Combat
#import Script
#import Object
#import Landmark
#import Combatant

from Tile import *
from Combat import *
from Script import *
from ObjectMod import Object
from Landmark import *
from Combatant import *
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
LIGHT_RADIUS = 50

VIEWSTATE = "ascii"
steps = 0
global enemyEncounter
enemyEncounter = False
color_dark_wall = libtcod.Color(0, 0, 100)
color_light_wall = libtcod.Color(130, 110, 50)
color_dark_ground = libtcod.Color(50, 50, 150)
color_light_ground = libtcod.Color(200, 180, 50)

def getNearest(obj, objects):
    list = sorted(objects, key= lambda item: abs(sqrt((obj.x - item.x)**2 + (obj.y - item.y)**2)))
    return list[1]

def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color):
    #render a bar (HP, experience, etc). first calculate the width of the bar
    bar_width = int(float(value) / maximum * total_width)

    #render the background first
    libtcod.con
    sole_set_default_background(panel, back_color)
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
                        libtcod.console_put_char_ex(con, x, y, '#', libtcod.black, libtcod.black)
                    else:
                        #libtcod.console_set_char_background(con, x, y, color_light_ground, libtcod.BKGND_SET )
                        libtcod.console_put_char_ex(con, x, y, '.', libtcod.grey, libtcod.white)
                    map[x][y].explored = True

    #draw all objects in the list except for the player, who appears over other objects so is drawn last
    for object in objects:
        if object != player:
            object.draw(con, map, fov_map)
    player.draw(con, map, fov_map)

    #blit the contents of "con" to the root console
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

    #prepare to render the GUI panel
    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    #print the game messages, one line at a time
    y = 1
    for (line, color) in game_msgs:
        libtcod.console_set_default_foreground(panel, color)
        libtcod.console_print(panel, MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
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
        'Health ' + str(player.hp) + '/' + str(player.maxHp))
    libtcod.console_print_ex(0, 15, SCREEN_HEIGHT - 2, libtcod.BKGND_NONE, libtcod.LEFT,
        str(player.bullets) + ' ' + 'Bullets')
    libtcod.console_print_ex(0, 29, SCREEN_HEIGHT - 2, libtcod.BKGND_NONE, libtcod.LEFT,
        'Water ' + str(player.water) + '/' + str(player.maxWater))

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
            player.move(0, -1, map)
            fov_recompute = True
            #if player.x == town.x and player.y == town.y or player.x == town1 and player.y == town1.y:
            player.water-=1

        elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
            player.move(0, 1, map)
            fov_recompute = True
            player.water-=1

        elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
            player.move(-1, 0, map)
            fov_recompute = True
            player.water-=1

        elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
            player.move(1, 0, map)
            fov_recompute = True
            if player.maxWater == 40:
                player.water-=2
            else:
                player.water-=1

        #enable for thirst mechanic
        #if player.water == 0:
            #player_death(player)

def player_death(player):
    global game_state
    game_state = 'dead'
    libtcod.console_clear(0)
    libtcod.console_print_ex(0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, libtcod.BKGND_NONE, libtcod.CENTER, "The world fades.")
    os.system('CLS')
    print ("----VAGRANT-----")
    print "Re-launch the game to thirst again."
    libtcod.console_flush()

def intro():
    os.system('CLS')
    print ("----VAGRANT-----")
    game_state = 'dead'
    libtcod.console_clear(0)
    libtcod.console_print_ex(0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 5, libtcod.BKGND_NONE, libtcod.CENTER, "VAGRANT")
    libtcod.console_print_ex(0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, libtcod.BKGND_NONE, libtcod.CENTER, "You are thirsty.")
    if randint(0,1) == 0:
        libtcod.console_print_ex(0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 5, libtcod.BKGND_NONE, libtcod.CENTER, "Created by Ian Colquhoun and Wilson Hodgson")
    else:
        libtcod.console_print_ex(0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 5, libtcod.BKGND_NONE, libtcod.CENTER, "Created by Wilson Hodgson and Ian Colquhoun")
    libtcod.console_flush()

def ending():
    game_state = 'dead'
    libtcod.console_clear(0)
    libtcod.console_print_ex(0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 5, libtcod.BKGND_NONE, libtcod.CENTER, "END")
    #libtcod.console_print_ex(0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, libtcod.BKGND_NONE, libtcod.CENTER, "Mi hijo, you have found the Republic. Pray that it will last.")
    if randint(0,1) == 0:
        libtcod.console_print_ex(0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 5, libtcod.BKGND_NONE, libtcod.CENTER, "Created by Ian Colquhoun and Wilson Hodgson")
    else:
        libtcod.console_print_ex(0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 5, libtcod.BKGND_NONE, libtcod.CENTER, "Created by Wilson Hodgson and Ian Colquhoun")
    libtcod.console_flush()

def make_object_map(objects):
    omap_data = open('landmarks.txt', 'r')

    x = 0
    y = -1
    for line in omap_data:
        if y < MAP_HEIGHT and y >= 0:
            for char in line:
                if x < MAP_WIDTH:
                    if char != '_':
                        objects.append(Object(x, y, char))
                x += 1
        x = 0
        y += 1

    omap_data.close()

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
                    if char == 'V':
                        map[x][y] = Tile(False, True)
                x += 1
        x = 0
        y += 1

    map_data.close()

#############################################
# Initialization & Main Loop
#############################################

libtcod.console_set_custom_font('lucida10x10_gs_tc.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'VAGRANT', False)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
panel = libtcod.console_new(SCREEN_WIDTH, PANEL_HEIGHT)
pony = False

def handleLow():
    return None

def handleLowAmmo():
    print("")

def handleSeeGun():
    print("")

def handleLowWater():
    if player.maxWater == 40:
            if player.water == 20:
                shootPony = Script("Shoot", "You kept your eyes closed and tried to drown out the sound.\nYou saddle her gear and carry on.", ponyDead)
                resistPony = Script("Carry on", "Can't spare the bullet. You spur her forward.")
                ponyThirst = Script("ponyThirst", "The pony moves in ragged breaths. There is not enough water for the two of you.")
                ponyThirst.connect(shootPony)
                ponyThirst.connect(resistPony)
                ponyThirst.messages = MessageLog()
                ponyThirst.run(ponyThirst.messages)

            if player.water == 10:
                leavePony = Script("leavePony", "The pony falls to her knees. She cannot go on.\nOn foot, you turn to see her being covered by the sandy wind.", ponyDead)
                leavePony.messages = MessageLog()
                leavePony.run(leavePony.messages)

def enemySpawn():
    nearest = getNearest(player, objects)
    distanceToNearest = sqrt((player.x - nearest.x)**2 + (player.y - nearest.y)**2)
    print(nearest.char)
    print(" ")
    print(nearest.x)
    print(nearest.y)
    print(" ")

    #if distanceToNearest > 4 and enemyEncounter == True :
    if enemyEncounter == True :
        print("distance greater and rand hit")
        distanceFromPlayer = randint(0,1)
        if distanceFromPlayer == 0 : distanceFromPlayer -= 1
        distanceFromPlayer = distanceFromPlayer*4
        enemyX = player.x + distanceFromPlayer
        enemyY = player.y + distanceFromPlayer
        enemy = Combatant(enemyX, enemyY, '&', 10, 1, 3, True, handleLow, handleLowAmmo, handleSeeGun, 3, 10, lambda:None)
        def onUpdate() :
            if (steps % 3 == 0): enemy.avoid(player, map)
            if(enemy.x == player.x and enemy.y == player.y):
                objects.remove(enemy)
        enemy.onUpdate = onUpdate
        global enemyEncounter
        enemyEncounter = False
        return enemy

def handleCombat():
    npc = Combatant(-1, -1, '&', 10, 1, 1, False, handleLow, handleLowAmmo, handleSeeGun, 0) #for some reason gunshots by enemy fire every bullet, killing player instantly. need to fix
    Combat(player, npc, con)

def refillWater():
    player.water = player.maxWater

def refillPartialWater():
    player.water = 9

def lightSleep():
    if player.hp >= 10:
        player.hp = 20
    else:
        player.hp = 10

def deepSleep():
    player.hp = 20

def landmarkVisit():
    player.water += 1

def handleEnding():
    ending()

def boughtPony():
    pony = True
    player.maxWater = 40

def ponyDead():
    pony = False

player = Combatant(10, 20, '@', 10, 2, 2, True, handleLow, handleLowAmmo, handleSeeGun, 10, 20, handleLowWater)

dryWellWater = Script("Drink", "You filter a small pool of water from the dark mud.", refillPartialWater)
houseWater = Script("Drink", "You draw water from the well.\nThere's enough in the waterskin to last several days in the wild.", refillWater)
houseSleep = Script("Sleep", "You take shelter for the night.\nProtection from the elements helps to heal shallow wounds.\n", lightSleep)
houseSafeSearch = Script("Enter", "A quick search through the house shows it to be ransacked.\nBut there is still some water in the well and a cot upstairs.", lambda: None, {houseWater.name:houseWater, houseSleep.name:houseSleep})
houseAttack = Script("Attack", "", handleCombat)
houseEnemySearch = Script("Search", "Peeking into the den, you find a young man in uniform burning books\nto make a fire.\nHe turns around and grits his teeth. Mira, es un poco Rojo.", lambda: None, {houseAttack.name:houseAttack})
if player.hp < 10 and player.hp > 0:
    houseWater.scripts = {houseSleep.name:houseSleep}
if player.water < 10 and player.water > 0:
    houseSleep.scripts = {houseWater.name:houseWater}

discoverHouse1 = Script("Leave", "An old house sets on the hill, the paint yellowed and flaking.\nThe door hangs open.", lambda: None, {houseSafeSearch.name:houseSafeSearch})
discoverHouse2 = Script("Leave", "An old house sets on the hill, the paint yellowed and flaking.\nThe door hangs open.", lambda: None, {houseEnemySearch.name:houseEnemySearch})
discoverHouse3 = Script("Leave", "A clay hut with a straw roof, surrounded by a stone fence.\nNo light comes from inside.", lambda:None, {houseSafeSearch.name:houseSafeSearch})
discoverHouse4 = Script("Leave", "A clay hut with a straw roof, surrounded by a stone fence.\nNo light comes from inside.", lambda: None, {houseEnemySearch.name:houseEnemySearch})

townWater = Script("Drink", "You dip your waterskin into the well.\nThere's enough there to last twelve days in the wild.", refillWater)
townSleep = Script("Sleep", "You spend the night at an inn.\nThe good food and warm bed help heal old wounds.", deepSleep)
townSafe = Script("", "You step out of the alley and back into the street.\nPeople crowd aroud a well, filling buckets. An inn sits across the mercado.", lambda: None, {houseWater.name:townWater, houseSleep.name:townSleep})

#discoverTown1 = Script("Leave", "A crumbling parish. Young boys kick a ball aroud the courtyard while\nnuns shovel hay. The wooden cross has been covered by a Falangist banner.", lambda: None, {townEnemy.name:townEnemy})
#discoverTown2 = Script("Leave", "A small community of farmers. Trucks circle the town and soldiers are stationed\noutside of clay huts. Staying here could be dangerous.", lambda: None, {townEnemy.name:townEnemy})
discoverBorder = Script("Sanctuary", "A large set of iron gates. A soldier in red greets you and motions to the others.\nThe gates open.", handleEnding)

buyPony = Script("Purchase", "You load the horse with bags and lead her back into the market.\nA strong back means extra space to carry water.", boughtPony)
townPony = Script("Shop", "A man guides you into a large, smoky tent. He has horses for sale.", lambda:None, {buyPony.name:buyPony})#, discoverTown.name:discoverTown})
discoverTown = Script("Return", "You step into a bazaar. Women balance pots on their heads and children push\nthrough the crowd.", lambda:None, {townPony.name:townPony, townWater.name:townWater, townSleep.name:townSleep})

discoverWell = Script("Well", "A well. The earth has cracked and dried against the clay ridge.", lambda:None, {houseWater.name:houseWater})
discoverWell2 = Script("Well", "The stones around the well have been burned and bashed,\nleaking sunlight into its basin.")
discoverWell2.connect(dryWellWater)


def setEncounter():
    global enemyEncounter
    enemyEncounter = True
caveWake = Script("Wake", "You jump out of sleep. Your flask is gone. A figure is running over a dune.", setEncounter)
caveSleep = Script("Sleep", "You tune out the howling of the wind and drift off.")
caveWater = Script("Drink", "You pool together some moisure in your hands and transfer it to your flask.", refillPartialWater)
discoverCave = Script("Return", "The wind grows fierce. You take shelter in the cave for the night.")
discoverCave.connect(caveWater)
discoverCave.connect(caveSleep)
caveWater.connect(discoverCave)
caveSleep.connect(caveWake)

town = Landmark(34, 23, 'T', "Town", [player], discoverTown)
well = Landmark(18, 21, 'W', "Well", [player], discoverWell)
well2 = Landmark(60, 14, 'W', "Well", [player], discoverWell2)
cave = Landmark(50, 15, 'C', "Cave", [player], discoverCave)

#house = Landmark(39, 21, 'H', "House", [player], discoverHouse1)
#house1 = Landmark(32, 18, 'H', "House", [player], discoverHouse4)
#house2 = Landmark(51, 24, 'H', "House", [player], discoverHouse2)

#tree= Object(17, 15, 't')
#tree1= Object(18, 15, 't')
#tree2= Object(19, 15, 't')
#tree3= Object(20, 15, 't')
#tree4= Object(21, 15, 't')
#tree5= Object(22, 15, 't')
#tree6= Object(23, 15, 't')
#tree7= Object(17, 14, 't')
#tree8= Object(18, 14, 't')
#tree9= Object(19, 14, 't')
#tree10= Object(20, 14, 't')
#tree11= Object(21, 14, 't')
#tree12= Object(22, 14, 't')
#tree13= Object(23, 14, 't')
#tree14= Object(18, 15, 't')
#tree15= Object(18, 15, 't')
#tree16= Object(18, 15, 't')
#tree17= Object(18, 15, 't')
#tree18= Object(18, 15, 't')
#tree19= Object(18, 15, 't')
#tree20= Object(18, 15, 't')
#tree21= Object(18, 15, 't')
#tree22= Object(18, 15, 't')
#tree23= Object(18, 15, 't')
#tree24= Object(18, 15, 't')
#tree25= Object(18, 15, 't')
#tree26= Object(18, 15, 't')
#tree27= Object(18, 15, 't')
#tree28= Object(18, 15, 't')

npc = Combatant(-1, -1, '&', 20, 1, 0, False, handleLow, handleLowAmmo, handleSeeGun, 0, 0)

#border = Landmark(35, 11, 'B', "Border", [player], discoverBorder)
#border1 = Landmark(36, 11, 'B', "Border", [player], discoverBorder)
#border2 = Landmark(37, 11, 'B', "Border", [player], discoverBorder)
#border3= Landmark(38, 11, 'B', "Border", [player], discoverBorder)
#border4= Landmark(39, 11, 'B', "Border", [player], discoverBorder)
#border5= Landmark(40, 11, 'B', "Border", [player], discoverBorder)
#border6= Landmark(41, 11, 'B', "Border", [player], discoverBorder)
#border7= Landmark(42, 11, 'B', "Border", [player], discoverBorder)
#border8= Landmark(43, 11, 'B', "Border", [player], discoverBorder)
#border9= Landmark(44, 11, 'B', "Border", [player], discoverBorder)
#border10= Landmark(45, 11, 'B', "Border", [player], discoverBorder)

townPony.connect(discoverTown)
buyPony.connect(discoverTown)

#townAttack.connect(townSafe)
#houseAttack.connect(houseSafeSearch)

#the list of objects with those two
objects = [player, well, town, well2, cave]

#generate map (at this point it's not drawn to the screen)
make_map()
make_object_map(objects)

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
    #combat = Combat(player,npc)
    if start_game == False:
        intro()
        if libtcod.console_wait_for_keypress(True).vk != libtcod.KEY_NONE:
            start_game = True
    #erase all objects at their old locations, before they move
    for object in objects:
        object.clear(con)
        object.update()
    #well.follow(player, map)
    loui = enemySpawn()
    if loui != None:
        objects.append(loui)
        loui.follow(player, map)
    if game_state != 'dead':
        #render_all()
        render_ascii()
        libtcod.console_flush()

    #objects[3].update()
    if player.x == npc.x and player.y == npc.y:
        Combat(player, npc, con)

    #if player.x == house.x and player.y == house.y:
        #houseChoice = randint(0,3)
        #player.water += 1

    #handle keys and exit game if needed
    if VIEWSTATE == 'ascii':
        exit = handle_keys()
    else:
        choice = handle_mouse()
    if exit:
        break
    steps += 1
