from random import randint
#this is the offending line, can't self reference roguelite
from HelperFunctions import read_grid_text
from HelperFunctions import MessageLog
import os
import libtcodpy as libtcod

class Combat:
	def __init__(self, myself, enemy, con):
		self.player_results_fist = read_grid_text('playerFistStagger.txt', 11, 1)
		self.enemy_results_fist = read_grid_text('enemyFistStagger.txt', 11, 1)
		self.player_results_death = read_grid_text('playerDeathStagger.txt', 5, 1)
		self.state = ""
		self.choices = []
		self.enemy = enemy
		self.myself = myself
		self.con = con
		self.run()

	def run(self):
		clear = lambda: os.system('CLS')
		myself = self.myself
		con = self.con
		messages = MessageLog()
		myself_result = "PLAYERESULT"
		enemy = self.enemy
		enemy_result = "ENEMYRESULT"
		deathLevel = 0
		messages.display("The shriveled man holds your bags in his hand.\n\n")
		while True:
			libtcod.console_clear(0)
			#messages.display( "Health = " + str(myself.hp) + "/" + str(myself.maxHp) + "\n\n" )
			#messages.display( "Health = " + str(enemy.hp) + "/" + str(enemy.maxHp) + "\n\n" )
			#messages.display( "-----OPTIONS-----\n\n")
			messages.display( "Fist")
			messages.display( "Leave")
			messages.display( "\n\n")

			player_choice = messages.get_console_input().lower()
			if player_choice == "fist":
				enemy.staggerLevel += 1
				enemy.hp -= 1
				if enemy.hp > 0:
					myself_result = self.player_results_fist[enemy.staggerLevel][myself.staggerLevel]
				else:
					if enemy.hp > -4:
						deathLevel +=1
					myself_result = self.player_results_death[deathLevel][myself.staggerLevel]

			if player_choice == "leave" and enemy.hp > 0:
				myself_result = "Not without the water."
			if player_choice == "leave" and enemy.hp <= 0:
				messages.display("You pull the flask from his clothing. He doesn't move.\n")
				messages.display("Leave\n\n")
				player_choice2 = messages.get_console_input().lower()
				if player_choice2 == "leave":
					break

			if enemy.hp > 0:
				#enemy_result = list of enemy reactions
				enemy_result = self.enemy_results_fist[enemy.staggerLevel][myself.staggerLevel]
			else:
				enemy_result = ""
					
			#clear()
			#messages.display ("-----VAGRANT-----")

			messages.display( myself_result)
			messages.display("\n")
			messages.display( enemy_result)
			messages.display("\n")
