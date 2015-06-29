import pygame
from config import *

class vector(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def add(self, vector2):
        self.x += vector2.x
        self.y += vector2.y
        
class player(object):
    def __init__(self, x, y):
        self.score = 0
        self.speed = 0  # holds current speed. Use constant PADDLESPEED when neccessary
        self.rect = pygame.Rect(x, y, 15, 100) 
        self.rect.centery = HEIGHT / 2
    
    def paddle_movt(self, direction):
        
        if direction == 'up':
            if self.rect.top - PADDLESPEED < TOP:
                self.rect.top = TOP
                self.speed = 0
            else:
                self.rect.top -= PADDLESPEED
                self.speed = -PADDLESPEED
        elif direction == 'down':
            if self.rect.bottom + PADDLESPEED > BOTTOM:
                self.rect.bottom = BOTTOM
                self.speed = 0
            else:
                self.rect.bottom += PADDLESPEED
                self.speed = PADDLESPEED
        else:
            self.speed = 0
    
    def is_moving(self):
        if self.speed:
            return True
        
    def update_score(self):
        self.score += 1
        
    def center(self):
        self.rect.centery = HEIGHT / 2

class ball(object):
    def __init__(self, delta): 
        self.delta = delta  # delta is the velocity vector
        self.rect = pygame.Rect(WIDTH / 2, HEIGHT / 2, 20, 20) 
    # critical case: what happens when player and ball move. collision doesn't take that into account
    def collision(self, player1, player2,sndflag): 
        
        if self.rect.top + self.delta.y <= TOP or self.rect.bottom + self.delta.y >= BOTTOM: 
            self.delta.y = -self.delta.y
            sndflag.append(True)
    
        if (self.rect.right + self.delta.x) >= player2.rect.left:  # right side
            if (self.rect.bottom + self.delta.y) >= (player2.rect.top  + player2.speed) and (self.rect.top + self.delta.y) <= (player2.rect.bottom + player2.speed) :
                self.delta.x = -XDAMPING * self.delta.x
                if player2.is_moving():
                    self.delta.y += YDAMPING * player2.speed
            sndflag.append(True)
                    
        elif (self.rect.left + self.delta.x) <= player1.rect.right:  # left side
            if (self.rect.bottom + self.delta.y) >= (player1.rect.top  + player1.speed) and (self.rect.top + self.delta.y) <= (player1.rect.bottom) + (player1.speed) :
                self.delta.x = -XDAMPING * self.delta.x
                if player2.is_moving:
                    self.delta.y += YDAMPING * player1.speed
            sndflag.append(True)
        
        if self.rect.right >= RIGHT:
            self.reset(1, player1)#if ball goes right, increase player1score
            self.reset(0, player2) #reset without changing score
        elif self.rect.left <= LEFT: #if ball goes left, increase player2score
            self.reset(2, player2)
            self.reset(0, player1)
        
    
    def reset(self, i, player):  # remember to add a proper win screen
        pygame.time.delay(300)
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.delta.y = BALLSPEED[1]
        if i==0:
            player.center()
            player.speed=0
        elif i == 1:
            player.update_score()
            player.center()
            player.speed = 0
            self.delta.x = BALLSPEED[0]
        else:
            player.update_score()
            player.center()
            player.speed = 0
            self.delta.x = -BALLSPEED[0]


    def update(self):
        self.rect.move_ip(self.delta.x, self.delta.y)
