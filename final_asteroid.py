#CAMERON WATTS#
#COMP PROG#
#3 16 19#

import pygame, sys, math

from pygame.locals import *
from tkinter import *
from tkinter import ttk
import random, time


pygame.mixer.pre_init(44100, 16, 1, 4096)
pygame.init()
clock = pygame.time.Clock()


"""COLORS"""
BLUE = (0, 0, 255)
NEW_GRAY = (65,65,65)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
AQUA = (0, 255, 255)
MAGENTA = (255, 0, 255)
PURPLE = (128, 0, 128)
SPACE = (20,20,40)
""""""


"""VARIABLES"""
lasers = []
asteroids = []
temp_value_laser = 0
temp_value_asteroid = 0
temp_key = ''
""""""


"""SCREEN"""
window_width = 1450
window_height = 700
screen = pygame.display.set_mode((window_width, window_height))
player_zone = pygame.Rect(1400,0,100,700)
""""""


"""CLASSES"""
class Entity(pygame.sprite.Sprite):
   """Inherited by any object in the game."""

   def __init__(self, x, y, width, height):
       pygame.sprite.Sprite.__init__(self)

       self.x = x
       self.y = y
       self.width = width
       self.height = height

       self.rect = pygame.Rect(self.x, self.y, self.width, self.height)



class Player(Entity):
   # The player controlled Paddle

   def __init__(self, x, y, width, height, angle, moving, laser, bomb, score, high_score, lives):
       super(Player, self).__init__(x, y, width, height)

       self.angle = angle
       self.image = pygame.image.load("spaceship.png")
       self.image_copy = self.image.copy() #very important, is used for rotating the image without screwing up the quality of it

       self.moving = moving
       self.laser = laser
       self.bomb = bomb #stats that are edited ingame
       self.score = score
       self.high_score = high_score
       self.lives = lives
       
   def Move(self, key):
      """MOVES PLAYER"""
      self.rect = self.image.get_rect(center=self.rect.center)
      if (key == pygame.K_LEFT):
         self.angle += 5
         if self.angle > 350: #had problems with 360, and 180* so i just made it impossible to get to that angle#
            self.angle = 10
         if self.angle > 170:
            self.angle = 170
         self.image = pygame.transform.rotate(self.image_copy, self.angle) #rotates image#
         return self.image.get_rect #returns new image#
         
      if (key == pygame.K_RIGHT):
         self.angle -= 10
         if self.angle < 10:
            self.angle = 10
         if self.angle > 170: #same thing as above#
            self.angle = 170
            
         self.image = pygame.transform.rotate(self.image_copy, self.angle)
         return self.image.get_rect
      
player = Player(1350, window_height / 2, 0, 0, 0, False, False, 2, 0, 0, 3)  #player



class Asteroid():
   def __init__(self,x,y,width,height,speed):
       self.x = x
       self.y = y
       self.width = width
       self.height = height
       self.speed = speed


       
class Laser():
   def __init__(self,x,y,width,height,angle,speed):
      self.x = x
      self.y = y
      self.width = width
      self.height = height
      self.angle = angle
      self.speed = speed



def high_score_define():
   global player
   file = open ('high_score.txt','r')
   x = file.read()
   player.high_score = int(x)




high_score_define()
for i in range(10):
    asteroids.append(Asteroid(0,random.randint(0, 645), 75,75, 1))
   


      
def explosion():
   theme1 = pygame.mixer.Sound('EXPLOSION.wav')
   theme1.set_volume(100)
   theme1.play(0)



def score_keep():
   global score, scoreBox, live, liveBox, bomb, bombBox, high_score, high_scoreBox
   font = pygame.font.Font('Comic Sans MS.ttf', 30)
    
   score = font.render('SCORE: ' +str(player.score)+ '', True, WHITE, BLACK)
   high_score = font.render('HIGH SCORE: ' +str(player.high_score)+ '', True, WHITE, BLACK)
   live = font.render('LIVES: ' +str(player.lives)+ '', True, WHITE, BLACK)
   bomb = font.render('BOMBS: ' +str(player.bomb)+ '', True, WHITE, BLACK)

   high_scoreBox = high_score.get_rect()
   high_scoreBox.center = (550,20)
   scoreBox = score.get_rect() 
   scoreBox.center = (875,20)
   liveBox = score.get_rect() 
   liveBox.center = (200,20)
   bombBox = score.get_rect() 
   bombBox.center = (1200,20)



def default():
   global player, laser, angle, temp_value_laser, temp_value_asteroid, lasers, asteroids
   #defaults that gets reset every round#
   asteroids = []
   lasers = []
   temp_value_laser = 0
   temp_value_asteroid = 0
   laser = False
   player.lives = 3
   player.score = 0
   player.bombs = 2
   player_zone = pygame.Rect(1400,0,100,700)


def game():
   global laser, temp_value_laser, temp_value_asteroid, asteroids, temp_key
   while True:
   #===========================================================#
      """SETS BUTTON INPUTS"""
      score_keep()
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
         if event.type == pygame.KEYDOWN:
            if event.key == K_LSHIFT:
               if player.bomb > 0: #bomb#
                  for value in asteroids:
                     player.score += 100
                  asteroids = []
                  player.bomb -= 1
                  explosion()
            if event.key == K_SPACE:
               player.laser = True #tells program that the person is holding down the space bar#
            if event.key == K_LEFT or event.key == K_RIGHT:
               player.moving = True #tells program that the person is moving#
               temp_key = event.key
            
         if event.type == pygame.KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
               player.moving = False #player is no longer moving#
            if event.key == K_SPACE:
               player.laser = False #player is no longer holding down space#
   #===========================================================#
               

               
   #===========================================================#
      """CHECKS BUTTON INPUTS"""       
      if player.moving == True: #moves the player if moving is true
         player.Move(temp_key)
      
      if player.laser == True: #couldn't get a formula to work, so I just hard coded in where to append the laser for all positions#
         if temp_value_laser == 0:
            if player.angle == 0 or player.angle == 5:
               lasers.append(Laser(1320 - ((player.angle - 10)/2),window_height / 2 - 52,35,35,player.angle,13))
            if player.angle == 10 or player.angle == 15:
               lasers.append(Laser(1320 - ((player.angle - 10)/2),window_height / 2 - 52 + 1,35,35,player.angle,5))
            if player.angle == 20 or player.angle == 25:
               lasers.append(Laser(1320 - ((player.angle - 10)/2),window_height / 2 - 52 + 4,35,35,player.angle,5))
            if player.angle == 30 or player.angle == 35:
               lasers.append(Laser(1320 - ((player.angle - 10)/2),window_height / 2 - 52 + 7,35,35,player.angle,6))
            if player.angle == 40 or player.angle == 45:
               lasers.append(Laser(1320 - ((player.angle - 10)/2),window_height / 2 - 52 + 10,35,35,player.angle,7))
            if player.angle == 50 or player.angle == 55:
               lasers.append(Laser(1320 - ((player.angle - 10)/2),window_height / 2 - 52 + 13,35,35,player.angle,7))
            if player.angle == 60 or player.angle == 65:
               lasers.append(Laser(1320 - ((player.angle - 10)/2),window_height / 2 - 52 + 17,35,35,player.angle,6))
            if player.angle == 70 or player.angle == 75:
               lasers.append(Laser(1320 - ((player.angle - 10)/2),window_height / 2 - 52 + 20,35,35,player.angle,5))
            if player.angle == 80 or player.angle == 85:
               lasers.append(Laser(1320 - ((player.angle - 10)/2),window_height / 2 - 52 + 31,35,35,player.angle,5))
            if player.angle == 90 or player.angle == 95:
               lasers.append(Laser(1320 - ((player.angle - 10)/2),window_height / 2 - 52 + 38,35,35,player.angle,15.333))

            if player.angle == 100 or player.angle == 105:
               lasers.append(Laser(1320 + ((player.angle - 110)/2),window_height / 2 - 52 + 38 + 1,35,35,player.angle,5))
            if player.angle == 110 or player.angle == 115:
               lasers.append(Laser(1320 + ((player.angle - 110)/2),window_height / 2 - 52 + 38 + 4,35,35,player.angle,5))
            if player.angle == 120 or player.angle == 125:
               lasers.append(Laser(1320 + ((player.angle - 110)/2),window_height / 2 - 52 + 38 + 7,35,35,player.angle,6))
            if player.angle == 130 or player.angle == 135:
               lasers.append(Laser(1320 + ((player.angle - 110)/2),window_height / 2 - 52 + 38 + 10,35,35,player.angle,7))
            if player.angle == 140 or player.angle == 145:
               lasers.append(Laser(1320 + ((player.angle - 110)/2),window_height / 2 - 52 + 38 + 13,35,35,player.angle,7))
            if player.angle == 150 or player.angle == 155:
               lasers.append(Laser(1320 + ((player.angle - 110)/2),window_height / 2 - 52 + 38 + 17,35,35,player.angle,6))
            if player.angle == 160 or player.angle == 165:
               lasers.append(Laser(1320 + ((player.angle - 110)/2),window_height / 2 - 52 + 38 + 20,35,35,player.angle,5))
            if player.angle == 170 or player.angle == 175:
               lasers.append(Laser(1320 + ((player.angle - 110)/2),window_height / 2 - 52 + 38 + 31,35,35,player.angle,5))
            if player.angle == 180:
               lasers.append(Laser(1320 + ((player.angle - 110)/2),window_height / 2 - 52 + 38 + 31,35,35,player.angle,15.333))
      #===========================================================#


               
      #===========================================================#
         """CALCULATIONS"""
            
      for value in lasers:
         if player.angle != 0:
            if value.angle == 90:
               value.y -= 0
               value.x -= value.speed
            if value.angle < 90 and value.angle != 0:
               temp = (((math.cos(175)) * value.angle) / 10) #calculates which direction laser goes based on player angle#
               value.y -= value.speed
               value.x -= temp * value.speed
            if value.angle > 90 and  value.angle < 180 and value.angle != 90:
               temp = (((math.cos(175)) * ((value.angle - 180) * -1) / 10))
               value.y += value.speed
               value.x -= temp * value.speed
      #===========================================================#
               
         for value2 in asteroids:
            if pygame.Rect(value2.x,value2.y,value2.width,value2.height).colliderect(pygame.Rect(value.x,value.y,value.width,value.height)): #if laser touches asteroid, gives player points
               player.score += 100
               try:
                  if value in lasers:
                     lasers.remove(value) #removes laser#
               except:
                  pass
               explosion()
               asteroids.remove(value2) #removes asteroid
         if value.x > 1450 or value.y > 700 or value.x < 0 or value.y < 0: #if laser goes off screen#
            try:
               lasers.remove(value)
            except:
               pass
      #===========================================================#


            
      #===========================================================#
      """COOLDOWNS"""
      temp_value_laser += 1 #cooldown for the laser#
      if temp_value_laser > 14:
         temp_value_laser = 0
            
      temp_value_asteroid += 1 #cooldown for asteroid spawning#
      if temp_value_asteroid > 20:
         asteroids.append(Asteroid(0,random.randint(0, 645), 75,75, 1 + ((player.score / 100) * .001)))
         temp_value_asteroid = 0
         
      for value in asteroids: #if asteroid gets passed a certain point, player loses a life#
         if pygame.Rect(value.x,value.y,value.width,value.height).colliderect(player_zone):
            player.lives -=1
            asteroids.remove(value)
         value.x += value.speed #slowly increases speed over time#
      #===========================================================#




      #===========================================================#
      """SCREEN UPDATE"""
      pygame.display.flip()

      screen.fill(SPACE)
      screen.blit(player.image ,(player.rect[0],player.rect[1]))
      screen.blit(score, scoreBox)  #updates screen#
      screen.blit(high_score, high_scoreBox)
      screen.blit(live, liveBox)
      screen.blit(bomb, bombBox)
      
      for value in lasers:
         pygame.draw.rect(screen,RED, (value.x,value.y,value.width,value.height))

      for value in asteroids:
         pygame.draw.rect(screen,NEW_GRAY, (value.x,value.y,value.width,value.height))
      #===========================================================#


         
      #===========================================================#
      """ENDGAME CHECK"""
      if player.score > player.high_score:
         player.high_score = player.score
      pygame.display.update()
      clock.tick(10000)

      if player.lives < 1: 
         pygame.display.update()
         clock.tick(10000)
         time.sleep(2)
         file = open('high_score.txt','w') #changes highscore once player dies#
         file.write(str(player.high_score))
         file.close()
         default()
         menu() #then goes back to the menu#
      #===========================================================#
def menu():
   """MAIN MENU"""
   global player, temp_value_laser, temp_value_asteroid, laser, moving
   default()
   font = pygame.font.Font('Comic Sans MS.ttf', 50)
   
   screen.fill(SPACE)
   
   new_game = font.render('New Game', True, WHITE,NEW_GRAY) #creates everything seen on the menu#
   quitt = font.render('Quit', True, WHITE,NEW_GRAY)
   instructions = font.render('Instructions', True, WHITE, NEW_GRAY)
   
   new_gameBox = new_game.get_rect()               
   new_gameBox.center = (200,30)
   
   quittBox = quitt.get_rect() 
   quittBox.center = (650,30)
   
   instructionsBox = instructions.get_rect() 
   instructionsBox.center = (1200,30)

   
   while True:
      default()
      for event in pygame.event.get():
         if event.type == pygame.MOUSEBUTTONDOWN:
            position = event.pos
            if pygame.Rect(position[0],position[1],0,0).colliderect(new_gameBox): #if the person presses newgame#
               game()
            if pygame.Rect(position[0],position[1],0,0).colliderect(quittBox):#if the person presses quit#
               pygame.quit()
               sys.exit()
            if pygame.Rect(position[0],position[1],0,0).colliderect(instructionsBox):#if the person presses instructions#
               instructions_view()

            
      pygame.draw.rect(screen,NEW_GRAY,(0,0,1450,67))
      screen.blit(new_game, new_gameBox) #updates screen#
      screen.blit(quitt, quittBox)
      screen.blit(instructions, instructionsBox)

      
      pygame.display.update()
      clock.tick(10000)


def instructions_view():
   """TKINTER POPUP"""
   #I didn't feel like doing much work for the instructions, so I just did a tkinter popup
   root = Tk()
   root.geometry("200x200")
   instructions_label = Label(root, text="""INSTRUCTIONS:\nLeft [<]
Right [>]
Fire [Space]
Bomb [left shift]""")
   instructions_label.grid(column=0,row=0)
   root.mainloop()

   
menu()
      
       
