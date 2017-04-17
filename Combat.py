from random import randint
#this is the offending line, can't self reference roguelite
from HelperFunctions import read_grid_text
from HelperFunctions import MessageLog
import os
import libtcodpy as libtcod

class Combat:
    #a class containing logic necessary to run during the combat state
    def __init__(self, myself, enemy, con):
        self.player_results_fist = read_grid_text('playerFistStagger.txt', 4, 4)
        self.player_results_gun = read_grid_text('playerGunStagger.txt', 4, 1)
        self.player_results_fire = read_grid_text('playerFireStagger.txt', 4, 1)
        self.player_results_escape = read_grid_text('playerEscapeStagger.txt', 4, 4)
        self.enemy_results_fist = read_grid_text('enemyFistStagger.txt', 4, 3)
        self.enemy_results_gun = read_grid_text('enemyGunStagger.txt', 4, 1)
        self.enemy_results_fire = read_grid_text('enemyFireStagger.txt', 4, 4)
        self.state = ""
        self.choices = []
        self.enemy = enemy
        self.myself = myself
        self.con = con
        self.run()

    def determineIntent(self, enemy):
            if randint(0,1) == 1 and enemy.bullets > 0 and enemy.cocked == False or enemy.cocked == True:
                return "gun"
            else:
                return "fist"

    def run(self):
        os.system('CLS')
        myself = self.myself
        con = self.con
        messages = MessageLog()
        myself_result = "PLAYERESULT"
        enemy = self.enemy
        enemy_result = "ENEMYRESULT"
        enemy_choice = ""
        while True:
            if myself.stagger == True:
                myself_result = ""
            if enemy.stagger == True:
                enemy_result = ""

            if myself.stagger == False:
                messages.display("------STATS------\n\n")
                messages.display(("Bullets = " + str(myself.bullets)))
                messages.display( "Health = " + str(myself.hp) + "/" + str(myself.maxHp) + "\n\n" )
                #messages.display( "Enemy health = " + str(enemy.hp) + "/" + str(enemy.maxHp) + "\n")
                #messages.display( "Enemy stagger = " + str(enemy_choice) + "\n")
                messages.display( "-----OPTIONS-----\n\n")
                messages.display( "Fist")
                messages.display( "Gun")
                messages.display( "Escape")
                messages.display( "\n\n")

                player_choice = messages.get_console_input().lower()
                if player_choice == "fist":
                    if myself.cocked == True:
                        myself.cocked = False
                    enemy.hp -= myself.dmg
                    if enemy.hp > 0:    
                        myself_result = self.player_results_fist[enemy.staggerLevel][myself.staggerLevel]
                    else:
                        myself_result = "You drive your boot down, the vibrations of the snapping of bone and sinew rushing up your leg to meet your spine."

                if player_choice == "gun" and myself.cocked == True and myself.bullets > 0:
                    if enemy.hp > 0:
                        enemy.hp -= 4
                        enemy.stagger = True
                        if enemy.staggerLevel < 3:
                            enemy.staggerLevel += 1
                        myself.bullets -= 1
                        myself_result = self.player_results_fire[enemy.staggerLevel][0]
                    else:
                        myself_result = "You fire a shot into the crimson mulch."

                if player_choice == "gun" and myself.cocked and myself.bullets == 0:
                    myself_result = "You pull the trigger. Nothing. No shells left."
               
                if player_choice == "gun" and myself.cocked == False:
                    myself.cocked = True
                    if enemy.hp > 0:
                        myself_result = self.player_results_gun[enemy.staggerLevel][0]
                    else:
                        myself_result =  "You pull out your gun."

            if player_choice == "escape" and enemy.hp > 0:
                myself_result = self.player_results_escape[enemy.staggerLevel][myself.staggerLevel]
                if myself.cocked == True:
                    myself.cocked = False
                myself_result = self.player_results_escape[enemy.staggerLevel][myself.staggerLevel]
                if enemy.stagger == True:
                    messages.get_console_input()
		    break
            if player_choice == "escape" and enemy.hp <= 0:
                myself.bullets += enemy.bullets
                if enemy.bullets > 0:
                    messages.display( "You ruffle through his coat, collecting his bullets.")
                    if myself.bullets > 6:
                        myself.bullets = 6
                    myself.gun = myself.gun or enemy.gun
                    messages.get_console_input()
		    break
                else:
                    break
                    
                os.system('CLS')
                messages.display( ("------ROJO-------"))

            if myself.stagger == True:
                messages.display( "------STATS------\n")
                messages.display( "Bullets = " + str(myself.bullets))
                messages.display( "Health = " + str(myself.hp) + "/" + str(myself.maxHp) + "\n" )
                messages.display( "Enemy health = " + str(enemy.hp) + "/" + str(enemy.maxHp) + "\n")
                messages.display( "----STAGGERED----\n")
                messages.display( "You focus on drowning out the pain. Inhale. Exhale.")
                player_choice = messages.get_console_input()
                myself_result = ""
                enemy_result = ""
                os.system('CLS')
            myself.stagger = False

            if myself_result != "":
                messages.display( myself_result)

            if enemy.stagger == False and enemy.hp > 0:
                enemy_choice = self.determineIntent(self.enemy)
                if enemy_choice == "fist":
                    myself.hp -= enemy.dmg
                    #if canFistStaggerEnemy == True and player.hp < player.maxHp/2:
                            #player.stagger = True
                            #canFistStaggerEnemy = False
                            #player.staggerLevel += 1
                    enemy_result = self.enemy_results_fist[enemy.staggerLevel][myself.staggerLevel]

                if enemy_choice == "gun" and enemy.cocked == True and enemy.bullets > 0:
                    myself.hp -= 4
                    myself.stagger = True
                    if myself.staggerLevel < 3:
                        myself.staggerLevel += 1
                    enemy.bullets -= 1
                    enemy_result = self.enemy_results_fire[enemy.staggerLevel][myself.staggerLevel]
                    
                if enemy_choice == "gun" and enemy.cocked == False:
                    enemy.cocked = True
                    enemy_result = self.enemy_results_gun[enemy.staggerLevel][0]
            
            if enemy.stagger == True and enemy.hp > 0:
                enemy_result = "Huffing, he climbs back to his feet."
            if enemy.hp <= 0:
                enemy_result = ""

            if enemy_result != "":
                messages.display( enemy_result)
            enemy.stagger = False

            if myself.hp <= 0:
                game_state = 'dead'
                libtcod.console_clear(0)
                libtcod.console_print_ex(0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, libtcod.BKGND_NONE, libtcod.CENTER, "The world fades.")
                os.system('CLS')
                messages.display( ("------ROJO-------"))
                messages.display( "Re-launch the game to find the Republic again.")
                libtcod.console_flush()
                break
            else:
                myself.combat_update()
                enemy.combat_update()
