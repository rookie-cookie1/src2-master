import sys
import pygame
from PIL import Image
import os
from natsort import natsorted, ns
pygame.init()
WIDTH = 1280
HEIGHT = 720
attack = False
jump = False
land = False
frameList = [0, 0, 0, 4, -4]
finishedList = [True, True, True]
momentumDivisor = 4
facing = False #This boolean dictates wich direction loogey is facing
gravity = 1
inAir = True
class playerObject: #Creates the player controllable object
    def __init__(self, image, height, speed):
        global loogeyMeleeAttackList
        global loogeyWalkingList
        global loogeyJumpingList
        global jumpPower
        self.speed = speed
        self.image = image
        self.pos = image.get_rect().move(0, height)
        self.momentum = 0
        self.collideRect = pygame.Rect(self.pos.left, self.pos.bottom, 1, self.momentum)
        jumpPower = -24
        loogeyMeleeAttackList = []
        loogeyWalkingList = []
        loogeyJumpingList = []
        #These three FOR loops load the animation frames into the lists
        for frame in os.scandir('loogeyAnimations/loogeyMeleeAttack'):
            if frame.is_file():
                frame = pygame.image.load(frame).convert_alpha()
                loogeyMeleeAttackList.append(frame)
        for frame in os.scandir('loogeyAnimations/loogeyWalking'):
            if frame.is_file():
                frame = pygame.image.load(frame).convert_alpha()
                loogeyWalkingList.append(frame)
        for frame in os.scandir('loogeyAnimations/loogeyJumping'):
            if frame.is_file():
                frame = pygame.image.load(frame).convert_alpha()
                loogeyJumpingList.append(frame)

    #This move function activates functions via keypresses    
    def move(self, up = False, down = False, left = False, right = False, space = False):
        global attack
        global finished
        global facing
        global jump
        if right:
            facing = True
            self.pos.right += self.speed
            #Does the walk animation of loogey is not attacking
            if attack == False and jump == False:
                self.walk()
        if left:
            facing = False
            self.pos.right -= self.speed
            #Does the walk animation if loogey is not attacking
            if attack == False and jump == False:
                self.walk()
        if down:
            self.pos.top += self.speed
        if up:
            jump = True
        if space:
            attack = True
        #Do stuff
        if self.pos.right > WIDTH:
            self.pos.left = 0
        if self.pos.top > HEIGHT-SPRITE_HEIGHT:
            self.pos.top = 0
        if self.pos.right < SPRITE_WIDTH:
            self.pos.right = WIDTH
        if self.pos.top < 0:
            self.pos.top = HEIGHT-SPRITE_HEIGHT
    def attack(self):
        global tick
        global finishedList
        global attack
        global frameList
        if finishedList[0] == True:
            frameList[0] = 0
            finishedList[0] = False
        if frameList[0] < len(loogeyMeleeAttackList):
            frame = frameList[0]    
            imageframe = loogeyMeleeAttackList[frame]
            if facing == True:
                modified = pygame.transform.flip(imageframe, True, False)
                self.image = modified
            else:
                self.image = imageframe
            frameList[0] = frameList[0] + 1
        else:
            frameList[0] = 0
            attack = False
            finishedList[0] = True
    def jump(self):
        global tick 
        global inAir
        global frameList
        global facing
        global finishedList
        global momentumDivisor
        if inAir == False:
            inAir = True
            self.image = loogeyJumpingList[0]
            self.momentum = jumpPower
        else:
            if self.momentum <= 0:
                if finishedList[2] == True:
                    finishedList[2] = False
                    frameList[1] = 0
                    momentumDivisor = 4
                frame = frameList[1]
                if self.momentum == jumpPower + momentumDivisor and attack == False and frame < len(loogeyJumpingList):
                    if facing:
                        modified = pygame.transform.flip(loogeyJumpingList[frame], True, False)
                        self.image = modified
                    else:
                        self.image = loogeyJumpingList[frame]
                    frame = frame + 1
                    frameList[1] = frame
                    momentumDivisor = momentumDivisor + 4
                    
            else:
                frame = 0
                frameList[1] = frame
                finishedList[2] = True
                if facing:
                    modified = pygame.transform.flip(loogeyJumpingList[4], True, False)
                    self.image = modified
                else:
                    self.image = loogeyJumpingList[4]
                
    def land(self):
        global frameList
        global finishedList
        global land
        global facing
        if finishedList[1] == True:
            finishedList[1] = False
            frameList[3] = 4
        frame = frameList[3]
        if tick % 3 == 0:
            if frame < len(loogeyJumpingList):
                if facing:
                    modified = pygame.transform.flip(loogeyJumpingList[frame], True, False)
                    self.image = modified
                else:
                    self.image = loogeyJumpingList[frame]
                frame = frame + 1
                frameList[3] = frame
            else:
                frameList[3] = 4
                finishedList[1] = True
                land = False



    def walk(self):
        global tick
        global frameList
        frame = frameList[2]
        if tick % 3 == 0 and frameList[2] < len(loogeyWalkingList):
            imageframe = loogeyWalkingList[frame]
            if facing == True:
                modified = pygame.transform.flip(imageframe, True, False)
                self.image = modified
            else:
                self.image = imageframe
            frameList[2] = frameList[2] + 1
            if frameList[2] >= len(loogeyWalkingList):
                frameList[2] = 0
    def update(self):
        global land
        global inAir
        global jump
        halfwidth = self.pos.width/2
        if self.momentum < 0:
            newTop = self.pos.bottom +  self.momentum
            newHeight = self.momentum * -1
            self.collideRect.update(self.pos.left + halfwidth, newTop, 1, self.momentum)
        else:
            self.collideRect.update(self.pos.left + halfwidth, self.pos.bottom, 1, self.momentum)
        if inAir == True:
            self.momentum = self.momentum + gravity
            forwardPoint = self.pos.bottom + self.momentum
            halfSprite = self.pos.right - self.pos.left
            halfSprite = self.pos.left + halfSprite
            if floor.rect.colliderect(self.collideRect):
                self.pos.bottom = floor.rect.top + 12
                self.momentum = 0
                inAir = False
                jump = False
                land = True
            else:
                self.pos.bottom = self.pos.bottom + self.momentum
        else:
            self.momentum = 0
        if attack == True and tick % 3 == 0:
            self.attack()
        if jump == True and attack == False:
            self.jump()
        if land == True:
            self.land()
        
class gameObjectStatic:
    def __init__(self, color, width, height, posX, posY):
        self.color = color
        self.width = width
        self.height = height
        self.posX = posX
        self.posY = posY
        self.rect = pygame.Rect(self.posX, self.posY, self.width, self.height)
        
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

screen = pygame.display.set_mode((1280, 720)) #Creates the screen
clock = pygame.time.Clock()                   #get a pygame clock object
playerImgPG = pygame.image.load('loogeySprite.png').convert_alpha() #opens and converts the image
playerImgPil = Image.open('loogeySprite.png')
SPRITE_HEIGHT = playerImgPil.height
SPRITE_WIDTH = playerImgPil.width
background = pygame.image.load('ResizedGameMenu.png').convert() #Opens and converts the image
screen.blit(background, (0, 0)) #Creates the background
objects = []            #Object list
props = []              #The props list
player = playerObject(playerImgPG, 0, 5) #Creates the player object
floor = gameObjectStatic((3, 3, 3), WIDTH, 60, 0, 660)
props.append(floor)
tick = 0
while True: #Main game loop
    #This if block slows the attack animation down to 20fps and activates 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.blit(background, player.pos, player.pos)
    player.update()
    screen.blit(player.image, player.pos)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player.move(up=True)
    if keys[pygame.K_DOWN]:
        player.move(down=True)
    if keys[pygame.K_LEFT]:
        player.move(left=True)
    if keys[pygame.K_RIGHT]:
        player.move(right=True)
    if keys[pygame.K_SPACE]:
        player.move(space=True)
    floor.draw()
    pygame.display.update()
    clock.tick(60)
    tick = tick + 1
    if tick >= 60:
        tick = 0
    
    