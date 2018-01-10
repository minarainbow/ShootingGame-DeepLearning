import pygame
import random
from time import sleep
from Bat import Bat
from Fire import Fire
import time

FPS = 60

WHITE = (255, 255, 255)
RED = (255, 0, 0)
pad_width = 400
pad_height = 400

# Model Size
aircraft_width = 53
aircraft_height = 33
bat_width = 56
bat_height = 28
fireball_width = 56
fireball_height = 24
fireball2_width = 34
fireball2_height = 24

# Game Speed
FLIGHT_SPEED = 4
BAT_SPEED = 6
FIRE_SPEED = 6
BACKGROUND_SPEED = 2


pygame.init()
FPSCLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((pad_width, pad_height))
pygame.display.set_caption('Flight')

 # draw sprites
aircraft = pygame.image.load('game/images/plane.png')
background1 = pygame.image.load('game/images/background.png')
background2 = background1.copy()
bat = pygame.image.load('game/images/bat.png')
fireball = pygame.image.load('game/images/fireball.png')

class GameState:
    def __init__(self):
        self.score = self.playerIndex = self.loopIter = 0
        self.playerx = int(pad_width * 0.07)
        self.playery = int((pad_height - aircraft_height) / 2)

        self.bat = []
        self.fire = []

        for i in range(3):
            newBat = getRandomBat()
            newFire = getRandomFire()
            new_batmap = {'x': newBat['x'], 'y': newBat['y'],}
            new_firemap = {'x': newFire['x'], 'y': newFire['y']}
            self.bat.append(new_batmap)
            self.fire.append(new_firemap)

        self.Up = False
        self.Down = False

    def frame_step(self, input_actions):

        pygame.event.pump()

        reward = 0.1
        terminal = False

        if sum(input_actions) != 1:
            raise ValueError('Multiple input actions!')

        # input_actions[0] == 1: do nothing
        # input_actions[1] == 1: monster up
        # input_actions[2] == 1: monster down
        if input_actions[1] == 1:
            self.Up = True

        if input_actions[2] == 1:
            self.Down = True


        # actions of aircraft
        if self.Up:
            self.playery -= FLIGHT_SPEED
            self.Up = False
        if  self.Down:
            self.playery += FLIGHT_SPEED
            self.Down = False

        
        #  limit aircraft's movement to be able to move only in the screen.
        if self.playery < 0:
            self.playery = 0
        elif self.playery + aircraft_height > pad_height:
            self.playery = pad_height - aircraft_height

         # check for score and reward
        playerMidPos = self.playerx + aircraft_width / 2
        for b in self.bat:            
            batMidPos = b['x'] + bat_width / 2
            if batMidPos <= playerMidPos < batMidPos + 4:
                self.score += 1
                #SOUNDS['point'].play()
                reward = 1
        for f in self.fire:
            fireMidPos = f['x'] + fireball_width / 2
            if fireMidPos <= playerMidPos < fireMidPos + 4:
                self.score += 1
                #SOUNDS['point'].play()
                reward = 1


        # Fire / Bat Movement
        for b, f in zip(self.bat, self.fire):
            b['x'] -= BAT_SPEED
            f['x'] -= FIRE_SPEED

        # remove first bat if its out of the screen
        # and add new bat in list
        if self.bat[0]['x'] < -bat_width:
            newBat = getRandomBat()
            self.bat.pop(0)
            self.bat.append(newBat)

        # remove first fire if its out of the screen
        # and add new fire in list
        if self.fire[0]['x'] < -fireball_width:
            newFire = getRandomBat()
            self.fire.append(newFire)
            self.fire.pop(0)

        # check if crash here
        isCrash= checkCrash({'x': self.playerx, 'y': self.playery},
                            self.bat, self.fire)
        if isCrash:
            #SOUNDS['hit'].play()
            #SOUNDS['die'].play()
            terminal = True
            self.__init__()
            reward = -1

        SCREEN.fill(WHITE)
        SCREEN.blit(background1, (0, 0))

        for b in self.bat:
            SCREEN.blit(bat, (b['x'], b['y']))

        for f in self.fire:
            SCREEN.blit(fireball, (f['x'], f['y']))


        # print score so player overlaps the score
        # showScore(self.score)
        SCREEN.blit(aircraft,
                    (self.playerx, self.playery))

        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        #print self.upperPipes[0]['y'] + PIPE_HEIGHT - int(BASEY * 0.2)
        return image_data, reward, terminal

def getRandomBat():
    """returns a randomly generated pipe"""
    # y of gap between upper and lower pipe
    batX = random.randint(pad_width, 2 * pad_width)
    batY = random.randint(0, pad_height - bat_height)

    return {'x': batX, 'y': batY, }

def getRandomFire():
    """returns a randomly generated pipe"""
    # y of gap between upper and lower pipe
    fireX = random.randint(pad_width, 2 * pad_width)
    fireY = random.randint(0, pad_height - fireball_height)

    return {'x': fireX, 'y': fireY}


def checkCrash(aircraft, bats, fires):
    for bat in bats:
        if ((aircraft['x'] + aircraft_width > bat['x'] + 5)
            and (aircraft['x'] < bat['x']+ bat_width)):
            if ((aircraft['y'] + 5 < bat['y'] + bat_height)
                and (aircraft['y'] + aircraft_height > bat['y'] + 5)):
                return True
    for fire in fires:
        if ((aircraft['x'] + aircraft_width  > fire['x'] + 5)
            and (aircraft['x'] < fire['x'] + fireball_width)):
            if ((aircraft['y'] + 5 < fire['y']+ fireball_height ) 
                and (aircraft['y'] + aircraft_height > fire['y'] + 5)):
                return True
    return False



