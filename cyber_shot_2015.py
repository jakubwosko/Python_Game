#################################################################################################
# Cyber Shot by Jakub Wosko
# version 1.06
# 3/2/2015
#
# comment: just wanted to learn Python. it turned out to be one of the most funny things :)
#################################################################################################

import pygame, sys, time
from pygame.locals import *
from copy import deepcopy

pygame.init()
screen = pygame.display.set_mode((450, 550))
pygame.display.set_caption('CYBER SHOT')

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SNOW1 = (205,201,201)
SNOW2 = (139,137,137)

screen.fill(WHITE)

def print_score_hiscore_life(score,hiscore,life):
	pygame.draw.rect(screen, WHITE, (10,8,300,15))
	font = pygame.font.SysFont("monospace", 13)
	scoretext=font.render("score:"+str(score), 1,(0,0,0))
	screen.blit(scoretext, (10, 8))
	scoretext=font.render("hiscore:"+str(hiscore), 1,(0,0,0))
	screen.blit(scoretext, (185, 8))
	textg=font.render("life:"+str(life), 1,(0,0,0))
	screen.blit(textg, (100, 8))
	
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

def main_game(hiscore_in):
	# start point with orientation, speed, score, etc...
	x,px,y,py=20,20,130,130
	orient_x,orient_y=1,1
	bar,pbar=200,200
	life=3
	gameover=False
	myscore=0
	SPEED=0.001
		
	#brics definition matrx 
	
	bricks2 = [[1,1,30,2,51,30,1,101,30,2,151,30,1,201,30,2,251,30,1,301,30,2,351,30,1,401,30],
	           [2,1,50,1,51,50,2,101,50,1,151,50,2,201,50,1,251,50,2,301,50,1,351,50,2,401,50],
	           [1,1,70,2,51,70,1,101,70,2,151,70,1,201,70,2,251,70,1,301,70,2,351,70,1,401,70],
	           [2,1,90,1,51,90,2,101,90,1,151,90,2,201,90,1,251,90,2,301,90,1,351,90,2,401,90],
	           [1,1,110,2,51,110,1,101,110,2,151,110,1,201,110,2,251,110,1,301,110,2,351,110,1,401,110]]
	
	bricks_refresh = [[1,1,30,2,51,30,1,101,30,2,151,30,1,201,30,2,251,30,1,301,30,2,351,30,1,401,30],
	           [2,1,50,1,51,50,2,101,50,1,151,50,2,201,50,1,251,50,2,301,50,1,351,50,2,401,50],
	           [1,1,70,2,51,70,1,101,70,2,151,70,1,201,70,2,251,70,1,301,70,2,351,70,1,401,70],
	           [2,1,90,1,51,90,2,101,90,1,151,90,2,201,90,1,251,90,2,301,90,1,351,90,2,401,90],
	           [1,1,110,2,51,110,1,101,110,2,151,110,1,201,110,2,251,110,1,301,110,2,351,110,1,401,110]]
		
	#################################################################################################
	# main_game() function main loop here
	#################################################################################################
	while True:
		time.sleep (SPEED)
		
		#ball position calculation & movement
		if orient_x==1:px,x=x,x+1
		if orient_x==-1:px,x=x,x-1
		if orient_y==1:py,y=y,y+1
		if orient_y==-1:py,y=y,y-1
		
		#ball direction calculation	& gameover
		if x>430:orient_x=-1
		if x<20:orient_x=1
		if y>530:
			orient_y=-1
			life=life-1
			print_score_hiscore_life(myscore, hiscore_in, life)
			if life<=0:
				print_gameover()
				gameover=True
				
				
		if y<20:orient_y=1
		
		#bar movement
		pygame.draw.rect(screen, WHITE, (pbar,450,50,10))
		pygame.draw.rect(screen, BLACK, (bar,450,50,10))
		
		#collision bar vs ball with direction
		if y==450:
			if x>=bar and x<=bar+25:
				orient_y=-1
				orient_x=-1
			if x>=bar+26 and x<=bar+50:
				orient_y=-1
				orient_x=1					
	
		#################################################################################################
		# BRICKS LOGIC
		#################################################################################################
		
		if y<=130:
			for tabY in range(0,5,1):
				for tabX in range(0,27,3):
					if y>=bricks2[tabY][tabX+2] and y<=bricks2[tabY][tabX+2]+20:
						if x>=bricks2[tabY][tabX+1] and x<=bricks2[tabY][tabX+1]+50:
							if bricks2[tabY][tabX] != 99:
								bricks2[tabY][tabX]=99
								orient_y=1
								myscore=myscore+1;
		
		for tabY in range(0,5,1):
			for tabX in range(0,27,3):
				if bricks2[tabY][tabX] == 1:
					pygame.draw.rect(screen, SNOW1, (bricks2[tabY][tabX+1],bricks2[tabY][tabX+2],50,20))
				if bricks2[tabY][tabX] == 2:
					pygame.draw.rect(screen, BLACK, (bricks2[tabY][tabX+1],bricks2[tabY][tabX+2],50,20))
				if bricks2[tabY][tabX] == 99:
					pygame.draw.rect(screen, WHITE, (bricks2[tabY][tabX+1],bricks2[tabY][tabX+2],50,20))
		
		#################################################################################################			
		
		#ball display
		pygame.draw.circle(screen, WHITE, (px,py),8,0)
		pygame.draw.circle(screen, BLACK, (x,y),7,0)
							
		#print score hiscore and update screen			
		print_score_hiscore_life(myscore, hiscore_in, life)
		pygame.display.update()
		
		#quit event
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			
		#keys for current state and position of the bar
		keys = pygame.key.get_pressed()
		if keys[K_LEFT]:
			if bar > 0:
				pbar,bar=bar,bar-3
		if keys[K_RIGHT]:
			if bar < 400:
				pbar,bar=bar,bar+3
		
		#new stage 
		if myscore % 45 == 0:
			bricks2 = deepcopy(bricks_refresh)
		
		#gameover
		if gameover==True:
			return myscore		
		
######################################################################################
# MAIN
# GAME STARTS HERE
######################################################################################

hiscore=0
new_hiscore=0
print_startgame()

while True:
	if new_hiscore > hiscore:
		hiscore=new_hiscore
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			screen.fill(WHITE)
			new_hiscore = main_game(hiscore)
			
