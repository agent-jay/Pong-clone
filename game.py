
import pygame, sys
from pygame.locals import *
from config import *
from objects import *

class Scene(object):
    def __init__(self):  # problem is that this constructor is overriden. hence pause doesnt exist.so use super()
        self.pause = False
    def keyboard_handler(self):
        pass  # raise a bloody error!!
    def update(self):
        pass
    def render(self):
        pass  # raise not implemented error instead. figure out how
    def game_quit(self):
        pygame.mixer.quit()
        pygame.quit()
        sys.exit()
    def play_sound(self):
        self.sound.play(0) #play the sound once
    def draw_grid(self, width, height, color):
        a = width / LINESH  # draw vertical lines
        for i in list(xrange(LINESH))[1:]:
            pygame.draw.line(self.surface , color, (a * i, 0), (a * i, height), 1)
        a = height / LINESV  # draw horizontal lines
        for i in list(xrange(LINESV))[1:]:
            pygame.draw.line(self.surface , color, (0, a * i), (width, a * i), 1)
        pygame.draw.line(self.surface , color , (width * .5, 0), (width * .5, height), 4)  # DRAW HALFLINE
        pygame.draw.lines(self.surface , WHITE, True, BOUNDARY, 4)  # DRAW BOUNDARY
        


class Game_Scene(Scene):  # the class containing the actual game. 
    
    def __init__(self, surface):
        super(Game_Scene, self).__init__()
        self.player1 = player(4, HEIGHT * .5)  # INITAIALIZE X,Y FOR BOTH PLAYERS
        self.player2 = player(WIDTH - 19, HEIGHT * .5)
        self.delta = vector(BALLSPEED[0], BALLSPEED[1])
        self.ball = ball(self.delta)
        self.surface = surface
        self.sound= pygame.mixer.Sound('bounce1.wav')
        #pygame.key.set_repeat(10, 10)   #doing this is dangerous. might enable it when infact simply creating a new game object that wont immediately be processed
        
    def draw_hud(self):
        fontObj = pygame.font.SysFont('Arial.ttf', 28)
        textSurfaceObj = fontObj.render(str(self.player1.score), True, WHITE)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.topright = (WIDTH * .476, HEIGHT * .0714)
        self.surface.blit(textSurfaceObj, textRectObj)
        textSurfaceObj = fontObj.render(str(self.player2.score), True, WHITE)
        textRectObj.topleft = (WIDTH * .524, HEIGHT * .0714)
        self.surface.blit(textSurfaceObj, textRectObj)
    
    def keyboard_handler1(self, events):
        self.player1.paddle_movt('stationary')  # THIS ENSURES THAT IF NO KEY IS PRESSED BALL IS GIVEN 0 SPEED
        self.player2.paddle_movt('stationary')
        for event in events:  # event handling. later insert into update function
            if event.type == QUIT:
                self.game_quit()  # consider making it part of the class. common to both levels. so inherit?
            elif event.type == KEYDOWN:  # implement key pressed not just keydown
                if event.key == K_UP:
                    self.player2.paddle_movt('up')
                elif event.key == K_DOWN:
                    self.player2.paddle_movt('down')
                elif event.key == K_w:
                    self.player1.paddle_movt('up')
                elif event.key == K_s:
                    self.player1.paddle_movt('down')
                elif event.key == K_ESCAPE:
                    global manager
                    self.pause = True
                    manager.tmp = self
                    manager.prep_next(Menu_Scene(self.surface))  # tells that the next game scene should be the menu.consider using handler function
                    return  # return control immediately
                
    def keyboard_handler(self, events):
        self.player1.paddle_movt('stationary')  # THIS ENSURES THAT IF NO KEY IS PRESSED BALL IS GIVEN 0 SPEED
        self.player2.paddle_movt('stationary')
        for event in events:  # event handling. later insert into update function
            if event.type == QUIT:
               self.game_quit()

        events = pygame.key.get_pressed()        
        if events[K_UP]:
            self.player2.paddle_movt('up')
        if events[K_DOWN]:
            self.player2.paddle_movt('down')
        if events[K_w]:
            self.player1.paddle_movt('up')
        if events[K_s]:
            self.player1.paddle_movt('down')
        if events[K_ESCAPE]:
            global manager
            self.pause = True
            manager.tmp = self
            manager.prep_next(Menu_Scene(self.surface))  # tells that the next game scene should be the menu.
            return
        #pygame.event.clear()
    
    def win_check(self):
        global manager
        wintext=[]
        if self.player1.score == WINREQ:
            wintext='Player 1 Wins'
        elif self.player2.score == WINREQ:
            wintext= 'Player 2 Wins'
        if wintext:
            fontObj = pygame.font.SysFont('Arial.ttf', 70)
            textSurfaceObj = fontObj.render(wintext, True, WHITE)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (WIDTH /2 , HEIGHT /2)
            self.surface.blit(textSurfaceObj, textRectObj)
            pygame.display.update()
            pygame.time.wait(2000)
            manager.prep_next(Menu_Scene(self.surface))
            manager.tmp = None
                 
    def update(self):
        self.keyboard_handler(pygame.event.get())
        sndflag=[]
        self.ball.collision(self.player1, self.player2,sndflag)
        if sndflag:
            self.play_sound()
        self.ball.update()
        self.win_check()
        
    def render(self):
        self.surface.fill((0, 0, 0))
        self.draw_grid(WIDTH, HEIGHT, GRAY)
        pygame.draw.rect(self.surface, WHITE, self.player1.rect)
        pygame.draw.rect(self.surface, WHITE, self.player2.rect)
        pygame.draw.rect(self.surface, WHITE, self.ball.rect)
        self.draw_hud()
        pygame.display.update()  
    
class Menu_Scene(Scene):
    def __init__(self, surface):
        super(Menu_Scene, self).__init__()
        self.text = ['Pong*','Start Game', 'Resume', 'Quit']
        self.select = 1
        self.surface = surface
        self.sound= pygame.mixer.Sound('select.wav')
        pygame.key.set_repeat()  # disables keyheld events
        
    def keyboard_handler(self, events, sndflag):
        global manager
        for event in events:
            if event.type == QUIT:
                self.game_quit()
            elif event.type == KEYDOWN:
                if event.key == K_UP or event.key== K_w:
                    if self.select != 1:
                        self.select -= 1
                    sndflag.append(True)
                elif event.key == K_DOWN or event.key== K_s:
                    if self.select != len(self.text) - 1 :
                        self.select += 1
                    sndflag.append(True)
                elif event.key == K_RETURN:
                    if self.select == 1:  # start new game
                        manager.prep_next(Game_Scene(self.surface))
                        return
                    elif self.select == 2:  # resume
                        manager.resume()
                    elif self.select == 3:  # quit
                        self.game_quit()
                elif event.key == K_ESCAPE:
                    manager.resume()
                    return

    def update(self):
        sndflag=[]
        self.keyboard_handler(pygame.event.get(),sndflag)
        if sndflag:
            self.play_sound()
        
    def draw(self):  #very very ugly function. Sorry :D. 
        global manager
        fontObj = pygame.font.SysFont('Arial.ttf', 100)
        for i in range(len(self.text)):
            textSurfaceObj = fontObj.render(str(self.text[i]), True, WHITE)
            if i==0:
                fontObj1 = pygame.font.SysFont('Arial.ttf', 130)
                textSurfaceObj = fontObj1.render(str(self.text[i]), True, WHITE)
            if i == 2:  # darken resume game when there is nothin to resume
                if manager.tmp == None:
                    textSurfaceObj = fontObj.render(str(self.text[i]), True, BRIGHTGRAY)
            textRectObj = textSurfaceObj.get_rect()
            if i==0:
                textRectObj.midtop = (WIDTH * .5, 50)
            else:
                textRectObj.midtop = (WIDTH * .5, i * 100 + 80)
            self.surface.blit(textSurfaceObj, textRectObj)
            if i == self.select:
                pygame.draw.rect(self.surface, WHITE, textRectObj, 1)        
        
    def render(self):
        self.surface.fill((0, 0, 0))
        self.draw_grid(WIDTH, HEIGHT, DARKGRAY)
        self.draw()
        pygame.display.update()    

class State_handler(object):
    def __init__(self, surface):
        self.surface = surface
        self.current = Menu_Scene(self.surface)
        self.next = None  # for now
        self.tmp = None  # used for holding paused game states
    
    def prep_next(self, state):
        self.next = state
        pygame.event.clear()  # flushes event queue so that esc isnt repeatedly executed
    
    def resume(self):
        if self.tmp != None:
            self.next = self.tmp
            pygame.event.clear()
            #pygame.key.set_repeat(10, 10)
        
    def switch(self):
        self.current = self.next
        pygame.event.clear()
    
def main():
    global manager  # figure out how to remove the global variable
    pygame.init()
    fpsclock = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT),FULLSCREEN)
    manager = State_handler(DISPLAYSURF)

    while True:
        manager.next = manager.current
        manager.current.update()
        manager.current.render()
        if manager.next != manager.current:  # if the next state has been modified in the game loop and is not the same state as it is currently
            manager.switch()
        fpsclock.tick(FPS)

if __name__ == '__main__':
    main()
