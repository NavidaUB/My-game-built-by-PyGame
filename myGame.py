'''
Developed by Navid 
December 2020
'''
import pygame
import random
import math
pygame.init()

gameDisplay = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Navid's Game")

background = pygame.image.load('background.jpg')

player = pygame.image.load('player.png')
(playerWidth,playerHeight)=player.get_rect().size

redball= pygame.image.load('redball.png')
greenball = pygame.image.load('greenball.png')
blueball= pygame.image.load('blueball.png')
(ballWidth,ballHeight)=redball.get_rect().size
balls=[redball,greenball,blueball]

redbullet= pygame.image.load('redbullet.png')
greenbullet = pygame.image.load('greenbullet.png')
bluebullet= pygame.image.load('bluebullet.png')
(bulletWidth,bulletHeight)=redbullet.get_rect().size
bullets=[redbullet,greenbullet,bluebullet]

arrow=pygame.image.load('arrow.png')

magic = pygame.mixer.Sound('magic.wav')
wrong = pygame.mixer.Sound('wrong.wav')
welldone = pygame.mixer.Sound('welldone.wav')
shoot = pygame.mixer.Sound('shoot.wav')
bulletG = pygame.mixer.Sound('bullet.wav')
ballG = pygame.mixer.Sound('ball.wav')
music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

font = pygame.font.SysFont('comicsans', 40)
font2 = pygame.font.SysFont('comicsans', 80)

clock = pygame.time.Clock()

class myPlayer(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.width = playerWidth
        self.height = playerHeight
        self.arrow = arrow
        self.direction = 0
        self.rect = self.arrow.get_rect()
        self.rect.center = (self.x + self.width//2,self.y + self.height//2)
        self.collisionbox = (self.x , self.y , self.width, self.height)
        self.grab = False
        self.grabID =0 
        
    def show(self):
        self.aim()
        gameDisplay.blit(player,(self.x,self.y))
        gameDisplay.blit(self.arrow,self.rect)
        
    def aim(self):
        self.arrow=pygame.transform.rotate(arrow, self.direction)
        x, y = self.rect.center
        self.rect = self.arrow.get_rect()  
        self.rect.center = (self.x+ self.width//2, self.y+ self.height//2)      
        
class myBall(object):
    def __init__(self,x,y,speed,direction,colorID):
        self.x = x
        self.y = y
        self.width = ballWidth
        self.height = ballHeight
        self.speed = speed
        self.color=colorID
        self.direction=direction
        self.collisionbox = (self.x , self.y , self.width, self.height)
        self.visible = True
        
    def show(self):
        self.moving()
        gameDisplay.blit(balls[self.color],(self.x,self.y))
    
    def moving(self):
        
        if self.y - math.sin(self.direction)*self.speed < 80 or self.y - math.sin(self.direction)*self.speed  > 650:
            self.direction*=-1
        else:
            self.x += math.cos(self.direction)*self.speed 
            self.y -= math.sin(self.direction)*self.speed 
            self.collisionbox = (self.x , self.y , self.width, self.height)
                        
        if self.x + math.cos(self.direction)*self.speed  > 910 or self.x + math.cos(self.direction)*self.speed  < 340:
            self.direction=-self.direction + math.copysign(math.pi, math.sin(self.direction))
        else:
            self.x += math.cos(self.direction)*self.speed 
            self.y -= math.sin(self.direction)*self.speed 
            self.collisionbox = (self.x , self.y , self.width, self.height)
            
        self.x += math.cos(self.direction)*self.speed 
        self.y -= math.sin(self.direction)*self.speed 
        self.collisionbox = (self.x , self.y , self.width, self.height)
        
class myBullet(object):
    def __init__(self,x,y,speed,direction,colorID,player):
        self.x = x
        self.y = y
        self.width = bulletWidth
        self.height =bulletHeight
        self.speed = speed
        self.color=colorID
        self.direction=direction 
        self.collisionbox = (self.x , self.y , self.width, self.height)
        self.allowMovement = True
        self.player = player
        self.bulletID = 0
        self.captured = False
        self.visible = True
        
    def show(self):
        if self.allowMovement:
            self.moving()
        else:
            self.movingWith()            
        gameDisplay.blit(bullets[self.color],(self.x,self.y))
    
    def moving(self):  
        
        if self.y - math.sin(self.direction)*self.speed < 80 or self.y - math.sin(self.direction)*self.speed > 650:
            self.direction*=-1
        else:
            self.x += math.cos(self.direction)*self.speed
            self.y -= math.sin(self.direction)*self.speed
            self.collisionbox = (self.x , self.y , self.width, self.height)
            
        if self.x + math.cos(self.direction)*self.speed > 910 or self.x + math.cos(self.direction)*self.speed < 340:
            self.direction=-self.direction + math.copysign(math.pi, math.sin(self.direction))
        else:
            self.x += math.cos(self.direction)*self.speed
            self.y -= math.sin(self.direction)*self.speed
            self.collisionbox = (self.x , self.y , self.width, self.height)   
            
        self.x += math.cos(self.direction)*self.speed
        self.y -= math.sin(self.direction)*self.speed
        self.collisionbox = (self.x , self.y , self.width, self.height)
        
    def movingWith(self):
        self.x=self.player.x + self.player.width//2 -10
        self.y=self.player.y + self.player.height//2 -10
            
def ballGenerator():
    randomSpeed=random.uniform(0.7,1.5)
    randomColor=random.sample(range(0,3), 1)
    randomAngle=random.uniform(-1,1)*(math.pi/2)
    return myBall(340,365,randomSpeed,randomAngle,randomColor[0])

def bulletGenerator():
    randomSpeed=random.uniform(0.7,1.5)
    randomColor=random.sample(range(0,len(inGameBalls)), 1)
    randomAngle=random.uniform(-1,1)*(math.pi/2)
    return myBullet(910,365,randomSpeed,randomAngle,inGameBalls[randomColor[0]].color,currentPlayer)
    
def collision(obj1,obj2):
    collided=False
    condition1=(obj1.x + obj1.width > obj2.x) and (obj1.x < obj2.x +obj2.width)
    condition2=(obj1.x < obj2.x + obj2.width) and (obj1.x + obj1.width > obj2.x)
    condition3=(obj1.y < obj2.y + obj2.height) and (obj1.y + obj1.height > obj2.y)
    condition4=(obj1.y + obj1.height > obj2.y) and (obj1.y < obj2.y + obj2.height)
    if (condition1 and condition3) or (condition2 and condition3) or (condition2 and condition4) or (condition1 and condition4):
        collided = True
    else:
        collided = False
    return collided
    
def updateDisplay():
    gameDisplay.blit(background, (0,0))
    currentPlayer.show()
    
    for item in inGameBalls:
        if item.visible:
            item.show()
    for item in inGameBullets:
        if item.visible:
            item.show()
    text = font.render('Score: {}'.format(score), 1, (255,255,255))
    gameDisplay.blit(text, (580,30))
    if tempFlag2:
        text = font2.render('OOPS!'.format(score), 1, (255,0,0))
        gameDisplay.blit(text, (550,350))
        text = font2.render('   -2'.format(score), 1, (255,0,0))
        gameDisplay.blit(text, (550,400))
    if tempFlag3:
        text = font2.render('WELL DONE!', 1, (0,255,0))
        gameDisplay.blit(text, (450,350))
        text = font2.render('      +1'.format(score), 1, (0,255,0))
        gameDisplay.blit(text, (500,400))
        
    pygame.display.update()
    
currentPlayer=myPlayer(640,360)
setTimeBall=list(range(1000,100000,10000))
setTimeBullet=list(range(2000,100000,10000))
movingSpeed=7
aimSpeed = 5
shootSpeed = 3 
timeCounterBall=0
timeCounterBullet=0
checkpointTime = 0 
inGameBalls=[]
inGameBullets=[]
bulletID=0
score=0
tempFlag = False
tempFlag2 = False
tempFlag3 = False
playing = True

while playing:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
            
    pressedKeys = pygame.key.get_pressed()
    
    if pressedKeys[pygame.K_a]:
        if currentPlayer.x - playerWidth//2 - 305  > movingSpeed:
            currentPlayer.x -= movingSpeed
            currentPlayer.collisionbox = (currentPlayer.x , currentPlayer.y , currentPlayer.width, currentPlayer.height)
        
    if pressedKeys[pygame.K_d]:
        if -currentPlayer.x + playerWidth//2 + 855 > movingSpeed:
            currentPlayer.x += movingSpeed
            currentPlayer.collisionbox = (currentPlayer.x , currentPlayer.y , currentPlayer.width, currentPlayer.height)
        
    if pressedKeys[pygame.K_w]:
        if currentPlayer.y - playerHeight//2 - 45 > movingSpeed:
            currentPlayer.y -= movingSpeed
            currentPlayer.collisionbox = (currentPlayer.x , currentPlayer.y , currentPlayer.width, currentPlayer.height)
        
    if pressedKeys[pygame.K_s]:
        if -currentPlayer.y - playerHeight//2 + 655 > movingSpeed:
            currentPlayer.y += movingSpeed
            currentPlayer.collisionbox = (currentPlayer.x , currentPlayer.y , currentPlayer.width, currentPlayer.height)
            
    if pressedKeys[pygame.K_k]:
        currentPlayer.direction = (currentPlayer.direction - aimSpeed) % (360)
        
    if pressedKeys[pygame.K_j]:
        currentPlayer.direction = (currentPlayer.direction + aimSpeed) % (360)  
        
    if pressedKeys[pygame.K_SPACE]:    
        if currentPlayer.grab:
            inGameBullets[currentPlayer.grabID].direction = currentPlayer.direction * (2*math.pi / 360)
            inGameBullets[currentPlayer.grabID].speed = shootSpeed
            inGameBullets[currentPlayer.grabID].allowMovement = True
            checkpointTime = pygame.time.get_ticks()
            tempFlag = True
        
    if tempFlag:
        if pygame.time.get_ticks() - checkpointTime > 100:
           shoot.play()
           currentPlayer.grab =False
           tempFlag = False
    
    if pygame.time.get_ticks() > setTimeBall[timeCounterBall]:
        inGameBalls.append(ballGenerator())
        ballG.play()
        timeCounterBall += 1
        if timeCounterBall >= len(setTimeBall):
           timeCounterBall = 0
           additionalTime=pygame.time.get_ticks() + 2000
           setTimeBall=[ t + additionalTime for t in setTimeBall]          
        
    if pygame.time.get_ticks() > setTimeBullet[timeCounterBullet]: 
       inGameBullets.append(bulletGenerator())
       bulletG.play()
       inGameBullets[-1].bulletID=bulletID
       bulletID+=1
       timeCounterBullet += 1
       if timeCounterBullet >= len(setTimeBullet):
           timeCounterBullet = 0
           additionalTime = pygame.time.get_ticks() + 2000
           setTimeBullet = [ t + additionalTime for t in setTimeBullet]  
           
    for blt in inGameBullets:
        if not currentPlayer.grab and blt.visible:
            if collision(currentPlayer,blt):
                currentPlayer.grab =True
                magic.play()
                blt.allowMovement = False
                blt.captured = True
                blt.x = currentPlayer.x
                blt.y = currentPlayer.y
                currentPlayer.grabID = blt.bulletID
                               
    for bll in inGameBalls:
        if collision(currentPlayer,bll) and bll.visible:
            checkpointTime2 = pygame.time.get_ticks()
            tempFlag2=True
            
    if tempFlag2:       
        if pygame.time.get_ticks() - checkpointTime2 > 100:
            wrong.play()
            score-=2
            tempFlag2=False        
            
    for blt in inGameBullets:
        if not currentPlayer.grab:
            if blt.captured and blt.visible :
                for bll in inGameBalls:
                    if collision(blt,bll) and bll.visible and bll.color==blt.color:
                        blt.visible = False
                        bll.visible = False                    
                        checkpointTime3 = pygame.time.get_ticks()
                        tempFlag3 = True
                          
    if tempFlag3:
       if pygame.time.get_ticks() - checkpointTime3 > 150:
           welldone.play()
           score += 1 
           tempFlag3=False 
                   
    updateDisplay()
    
pygame.quit()