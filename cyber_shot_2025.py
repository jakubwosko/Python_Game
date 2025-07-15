#################################################################################################
# Cyber Shot by Jakub Wosko
# version 1.06
# 3/2/2015
#
# comment: just wanted to learn Python. it turned out to be one of the most funny things :)
#################################################################################################

import pygame, sys, time, random, math
from pygame.locals import *
from copy import deepcopy
from math import sin, cos

pygame.init()
screen = pygame.display.set_mode((450, 550))
pygame.display.set_caption('CYBER SHOT')

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SNOW1 = (205,201,201)
SNOW2 = (139,137,137)

# 25 random colors for blocks
COLORS = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255),
    (0, 255, 255), (255, 128, 0), (128, 255, 0), (0, 128, 255), (255, 0, 128),
    (128, 0, 255), (255, 128, 128), (128, 255, 128), (128, 128, 255), (255, 255, 128),
    (255, 128, 255), (128, 255, 255), (192, 64, 64), (64, 192, 64), (64, 64, 192),
    (192, 192, 64), (192, 64, 192), (64, 192, 192), (128, 64, 192), (192, 128, 64)
]

screen.fill(WHITE)

def print_pause_message():
	# Clear center area for pause message
	pygame.draw.rect(screen, WHITE, (50, 180, 350, 120))
	
	# Pause message with black border for visibility
	font = pygame.font.SysFont("monospace", 60, bold=True)
	pause_msg = font.render("PAUSED", 1, (255, 0, 0))  # Red text
	msg_width = pause_msg.get_width()
	screen.blit(pause_msg, ((450 - msg_width) // 2, 200))
	
	# Instructions
	font = pygame.font.SysFont("monospace", 20)
	inst_msg = font.render("Press SPACE or P to resume", 1, (0, 0, 0))  # Black text
	msg_width = inst_msg.get_width()
	screen.blit(inst_msg, ((450 - msg_width) // 2, 260))

def print_score_hiscore_life(score,hiscore,life,power_mode=False,power_timer=0):
	# Clear top area including power mode message area
	pygame.draw.rect(screen, WHITE, (0,0,450,30))
	
	# Power mode message at the very top
	if power_mode:
		remaining = max(0, 10 - int(power_timer/200))  # Fixed calculation for game loop timing
		font_big = pygame.font.SysFont("monospace", 16, bold=True)
		power_msg = font_big.render("*** POWER MODE ACTIVE - " + str(remaining) + " SECONDS LEFT ***", 1, (0,255,0))
		msg_width = power_msg.get_width()
		screen.blit(power_msg, ((450 - msg_width) // 2, 2))  # Centered at top
	
	# Regular score display below power message
	font = pygame.font.SysFont("monospace", 13)
	scoretext=font.render("score:"+str(score), 1,(0,0,0))
	screen.blit(scoretext, (10, 18))
	scoretext=font.render("hiscore:"+str(hiscore), 1,(0,0,0))
	screen.blit(scoretext, (185, 18))
	textg=font.render("life:"+str(life), 1,(0,0,0))
	screen.blit(textg, (100, 18))
	
def print_gameover():
	font = pygame.font.SysFont("monospace", 50)
	textgm=font.render("GAME OVER", 1,(0,0,0))
	screen.blit(textgm, (90, 200))
	font = pygame.font.SysFont("monospace", 20)
	textgm=font.render("press any key", 1,(0,0,0))
	screen.blit(textgm, (135, 300))

def print_startgame():
	font = pygame.font.SysFont("monospace", 50)
	textgm=font.render("CYBER SHOT", 1,(0,0,0))
	screen.blit(textgm, (70, 200))
	font = pygame.font.SysFont("monospace", 15)
	textgm=font.render("press any key to start", 1,(0,0,0))
	screen.blit(textgm, (120, 300))
	pygame.display.update()

def print_speed_menu():
	screen.fill(WHITE)
	font = pygame.font.SysFont("monospace", 40)
	textgm=font.render("SELECT SPEED", 1,(0,0,0))
	screen.blit(textgm, (100, 150))
	
	font = pygame.font.SysFont("monospace", 20)
	textgm=font.render("1 - SLOW", 1,(0,0,0))
	screen.blit(textgm, (170, 220))
	textgm=font.render("2 - MEDIUM", 1,(0,0,0))
	screen.blit(textgm, (160, 260))
	textgm=font.render("3 - FAST", 1,(0,0,0))
	screen.blit(textgm, (170, 300))
	
	font = pygame.font.SysFont("monospace", 15)
	textgm=font.render("Press 1, 2, or 3", 1,(0,0,0))
	screen.blit(textgm, (150, 350))
	pygame.display.update()

def main_game(hiscore_in, game_speed):
	# Speed settings based on player choice
	if game_speed == 1:  # Slow
		SPEED = 0.005
		BALL_SPEED = 1
	elif game_speed == 2:  # Medium
		SPEED = 0.001
		BALL_SPEED = 2
	else:  # Fast
		SPEED = 0.0001
		BALL_SPEED = 3
	
	# start point with orientation, speed, score, etc...
	x,px,y,py=20,20,400,400
	orient_x,orient_y=1,-1
	bar,pbar=200,200
	life=3
	gameover=False
	myscore=0
	
	# Ball velocity components for angled movement
	ball_vel_x = BALL_SPEED
	ball_vel_y = -BALL_SPEED
	
	# Power-up system variables
	powerup_x = -100  # Off-screen initially
	powerup_y = -100
	powerup_prev_x = -100  # Previous position for clearing
	powerup_prev_y = -100
	powerup_active = False
	power_mode = False
	power_mode_timer = 0
	powerup_drop_timer = 0
	GREEN = (0, 255, 0)
	
	# Pause system variables
	paused = False
		
	#brics definition matrix with random colors (0-24 for color indices)
	def create_bricks():
		bricks = []
		for row in range(8):  # 8 rows now (5 original + 3 new)
			brick_row = []
			y_pos = 30 + row * 20
			for col in range(9):  # 9 columns
				x_pos = 1 + col * 50
				color_index = random.randint(0, 24)  # Random color from 25 colors
				brick_row.extend([color_index, x_pos, y_pos])
			bricks.append(brick_row)
		return bricks
	
	bricks2 = create_bricks()
	bricks_refresh = create_bricks()
		
	#################################################################################################
	# main_game() function main loop here
	#################################################################################################
	while True:
		#quit event and pause handling
		was_paused = paused  # Remember previous pause state
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_SPACE or event.key == K_p:
					paused = not paused  # Toggle pause
		
		# If paused, show pause message and skip game logic
		if paused:
			print_pause_message()
			pygame.display.update()
			time.sleep(0.1)  # Small delay to prevent excessive CPU usage
			continue
		
		# Clear pause message area when resuming from pause
		if was_paused and not paused:
			pygame.draw.rect(screen, WHITE, (50, 180, 350, 120))
		
		time.sleep (SPEED)
		
		# Power-up timer management (adjusted for actual game speed)
		powerup_drop_timer += 1
		if power_mode:
			power_mode_timer += 1
			if power_mode_timer > 2000:  # Approximately 10 seconds based on game speed
				power_mode = False
				power_mode_timer = 0
		
		# Drop power-up every 10 seconds (2000 game loops for testing, adjust as needed)
		if powerup_drop_timer > 2000 and not powerup_active:
			powerup_x = random.randint(50, 400)
			powerup_y = 30
			powerup_active = True
			powerup_drop_timer = 0
		
		# Move power-up down
		if powerup_active:
			powerup_prev_x, powerup_prev_y = powerup_x, powerup_y  # Store previous position
			powerup_y += 2
			if powerup_y > 550:  # Off screen
				powerup_active = False
		
		#ball position calculation & movement
		px, py = x, y
		x += ball_vel_x
		y += ball_vel_y
		
		#ball direction calculation & gameover
		if x>430:ball_vel_x = -abs(ball_vel_x)
		if x<20:ball_vel_x = abs(ball_vel_x)
		if y>530:
			ball_vel_y = -abs(ball_vel_y)
			life=life-1
			print_score_hiscore_life(myscore, hiscore_in, life)
			if life<=0:
				print_gameover()
				gameover=True
				
		if y<20:ball_vel_y = abs(ball_vel_y)
		
		#bar movement
		pygame.draw.rect(screen, WHITE, (pbar,450,75,10))
		pygame.draw.rect(screen, BLACK, (bar,450,75,10))
		
		# Power-up collision with paddle
		if powerup_active and powerup_y >= 450 and powerup_y <= 460 and powerup_x >= bar and powerup_x <= bar + 75:
			# Clear the power-up ball's current position before deactivating
			pygame.draw.circle(screen, WHITE, (int(powerup_x), int(powerup_y)), 12, 0)
			powerup_active = False
			power_mode = True
			power_mode_timer = 0
		
		#collision bar vs ball with 7-zone angle system
		if y >= 450 and y <= 460 and x >= bar and x <= bar + 75:
			# Divide paddle into 7 equal zones (75 pixels / 7 = ~10.7 pixels per zone)
			zone_width = 75.0 / 7.0
			hit_position = x - bar  # Position relative to left edge of paddle
			zone = int(hit_position / zone_width)
			
			# Ensure zone is within bounds (0-6)
			if zone < 0: zone = 0
			if zone > 6: zone = 6
			
			# Calculate new velocity components based on zone
			speed = (ball_vel_x**2 + ball_vel_y**2)**0.5  # Maintain speed
			
			# Direct angle-to-velocity mapping for each zone
			if zone == 0:  # 55° left
				ball_vel_x = -speed * cos(55 * 3.14159 / 180)
				ball_vel_y = -speed * sin(55 * 3.14159 / 180)
			elif zone == 1:  # 60° left
				ball_vel_x = -speed * cos(60 * 3.14159 / 180)
				ball_vel_y = -speed * sin(60 * 3.14159 / 180)
			elif zone == 2:  # 70° left
				ball_vel_x = -speed * cos(70 * 3.14159 / 180)
				ball_vel_y = -speed * sin(70 * 3.14159 / 180)
			elif zone == 3:  # 90° straight up
				ball_vel_x = 0
				ball_vel_y = -speed
			elif zone == 4:  # 110° right
				ball_vel_x = speed * cos(70 * 3.14159 / 180)  # 110° = 180° - 70°
				ball_vel_y = -speed * sin(70 * 3.14159 / 180)
			elif zone == 5:  # 130° right
				ball_vel_x = speed * cos(50 * 3.14159 / 180)  # 130° = 180° - 50°
				ball_vel_y = -speed * sin(50 * 3.14159 / 180)
			elif zone == 6:  # 135° right
				ball_vel_x = speed * cos(45 * 3.14159 / 180)  # 135° = 180° - 45°
				ball_vel_y = -speed * sin(45 * 3.14159 / 180)					
	
		#################################################################################################
		# BRICKS LOGIC
		#################################################################################################
		
		if y<=190:  # Extended range for 8 rows
			for tabY in range(0,8,1):  # 8 rows now
				for tabX in range(0,27,3):
					if y>=bricks2[tabY][tabX+2] and y<=bricks2[tabY][tabX+2]+20:
						if x>=bricks2[tabY][tabX+1] and x<=bricks2[tabY][tabX+1]+50:
							if bricks2[tabY][tabX] != 99:
								bricks2[tabY][tabX]=99
								myscore=myscore+1
								if not power_mode:
									ball_vel_y = abs(ball_vel_y)  # Normal bounce
								# In power mode, ball continues through blocks
		
		for tabY in range(0,8,1):  # 8 rows now
			for tabX in range(0,27,3):
				if bricks2[tabY][tabX] >= 0 and bricks2[tabY][tabX] <= 24:
					color = COLORS[bricks2[tabY][tabX]]
					pygame.draw.rect(screen, color, (bricks2[tabY][tabX+1],bricks2[tabY][tabX+2],50,20))
				if bricks2[tabY][tabX] == 99:
					pygame.draw.rect(screen, WHITE, (bricks2[tabY][tabX+1],bricks2[tabY][tabX+2],50,20))
		
		#################################################################################################			
		
		# Clear power-up previous position and draw new position
		if powerup_active:
			# Clear previous position (larger area to ensure complete clearing)
			pygame.draw.circle(screen, WHITE, (int(powerup_prev_x), int(powerup_prev_y)), 12, 0)
			# Draw current position
			pygame.draw.circle(screen, GREEN, (int(powerup_x), int(powerup_y)), 10, 0)
		
		#ball display (different color in power mode)
		pygame.draw.circle(screen, WHITE, (px,py),8,0)
		if power_mode:
			pygame.draw.circle(screen, GREEN, (x,y),7,0)  # Green ball in power mode
		else:
			pygame.draw.circle(screen, BLACK, (x,y),7,0)
							
		#keys for current state and position of the bar
		keys = pygame.key.get_pressed()
		if keys[K_LEFT]:
			if bar > 0:
				pbar,bar=bar,bar-3
		if keys[K_RIGHT]:
			if bar < 375:
				pbar,bar=bar,bar+3
		
		#print score hiscore and update screen			
		print_score_hiscore_life(myscore, hiscore_in, life, power_mode, power_mode_timer)
		pygame.display.update()
		
		#new stage 
		if myscore % 72 == 0:  # Updated for 8 rows * 9 columns = 72 blocks
			bricks2 = create_bricks()
		
		#gameover
		if gameover==True:
			return myscore		
		
def get_speed_choice():
	print_speed_menu()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					return 1  # Slow
				elif event.key == pygame.K_2:
					return 2  # Medium
				elif event.key == pygame.K_3:
					return 3  # Fast

######################################################################################
# MAIN
# GAME STARTS HERE
######################################################################################

hiscore=0
new_hiscore=0
first_time = True
print_startgame()

while True:
	if new_hiscore > hiscore:
		hiscore=new_hiscore
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if first_time:
				first_time = False
			# Always get speed choice after each game
			selected_speed = get_speed_choice()
			screen.fill(WHITE)
			new_hiscore = main_game(hiscore, selected_speed)
			
