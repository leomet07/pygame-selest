import pygame
import os
pygame.init()
winh = 500
winw = winh
win = pygame.display.set_mode((winw, winh))
bg = pygame.image.load("src/bg.png")
char = pygame.image.load("src/potato.png")
monster = pygame.image.load("src/monster.png")
music = pygame.mixer.music.load('src/bgmusic.mp3')
pygame.mixer.music.play(-1)

class Enemy:
    def __init__(self, x , y):
        self.x = x
        self.y = y
        self.h = 24
        self.w = 24
        self.tickcount = 0

    def draw(self, win):
        global char
        global monster

        #pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.w, self.h))
        sprite = monster
        monster = pygame.transform.scale(sprite, (self.w, self.h))
        win.blit(monster, (self.x, self.y))


        #draw bullets
        # also render bullets
        for bullet in BULLETS:
            # darw bullet
            # USE ULLETS X TO DRAW
            pygame.draw.circle(win, (0,255,0), (bullet[0], bullet[1]), 5)

    def collide(self, bird):
        """
        returns if a point is colliding with the pipe
        :param bird: Bird object
        :return: Bool
        """

        # pixel perfect collision

        # collision isnt done with rects but with masks which follow the pixels of the sprite perfectly
        # checks if pixels are touching and not if the recs are touching
        # masks are 2d arrays of the pixels of the sprite and not the white stuuff that isnt the sprite
        # checks if ny pixel collides with another one
        bird_mask = bird.get_mask()


        bottom_mask = pygame.mask.from_surface(monster)

        # how far each mask is from the other

        bottom_offset = (self.x - bird.x, self.y + self.h - round(bird.y))

        # tells point of collision
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)


        if b_point :
            return True

        return False

    def launchbullets(self, player):
        print("Launching bullets")
        print("Bullets: " + str(len(BULLETS)))
        #bullet = ["playerx", "bottomofscreenY"]
        bullet = [player.x + 5, 480]
        BULLETS.append(bullet)
    def update(self, player):
        global BULLETS
        self.tickcount += 1
        if self.tickcount == 100:
            print("launch")
            self.tickcount = 0
            self.launchbullets(player)



        #move bullets

        #duplicate of bullets array as to not mess with for loop
        dupbullets = BULLETS
        deleted = 0
        for i in range(0,len(BULLETS) ):
            #print(i)
            #only move bullet up if its y is greater then the players
            #print(BULLETS[i - deleted][1])
            if 0 <= BULLETS[i - deleted][1]:
                #problem above
                #move bullet up by cham\nging its why
                #print("moving bullet up")
                BULLETS[i - deleted][1] -= 3
            else:
                dupbullets.pop(i)
                deleted += 1
            #print(BULLETS)

        BULLETS = dupbullets
        for bullet in BULLETS:
            #check for bullet collision
            if bullet[1] < player.y + player.h and  bullet[1] > player.y  :
                if bullet[0] > player.x and bullet[0] < player.x + player.w:
                    print("hit the bullet")
                    exit(0)
class Bullet:
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
class Player:
    def __init__(self, x, y):
        global char
        self.g = 2
        self.x = x
        self.y = y
        self.h = 24
        self.w = 24
        self.jumph = 110
        self.isJump = False
        self.jumpcount = 10
        self.img = char

    def draw(self, win):
        global char

        #pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.w, self.h))
        sprite = char
        char = pygame.transform.scale(sprite, (self.w, self.h))
        win.blit(char, (self.x, self.y))




    def update(self):

        #gravity conditions
        #print(self.y + self.h, self.x + self.w)

        allow = True
        for line in LINES:
            #print(not(self.y + self.h == line["xy"][1]  and self.x > line["xy"][0] and self.x < line["x2y2"][0] )  and self.y + self.h < 498)

            #print(not(self.y + self.h == line["xy"][1]  and self.x < line["x2y2"][0] and self.x > line["xy"][0] ) )

            if (allow):
                if not(not(self.y + self.h == line["xy"][1]  and self.x + (self.w/1) > line["xy"][0] and self.x < line["x2y2"][0] )  and self.y + self.h < 498):

                    allow =  False
                    #print("DISSALLOW")
        #print(allow)
        if allow:
            self.y += self.g

        #print("-----")

        #check for win condition
        line = LINES[0]
        if self.y + self.h == 70  and self.x + self.w > line["xy"][ 0] and self.x < line["x2y2"][ 0]:
            #if touching red line then game has been won

            print("win")
            exit(0)

    def get_mask(self):
        """
        gets the mask for the current image of the bird
        :return: None
        """
        # used for object collision
        return pygame.mask.from_surface(self.img)

    def jump(self):
        print("jump command retrieved")
        #if above ground then jump

        allow = False
        if self.y + self.h >= 498 :
            #only jump if line not in the way
            print("jump called")

            line = LINES[-1]

            equation = not (self.y + self.h - self.jumph < LINES[-1]["xy"][1] and self.x < line["x2y2"][ 0] and self.x + (self.w/2) > line["xy"][0])




            if equation:
                self.y -= self.jumph
                #print("pix")

        #if on a line jump if the line above is far away

        for i in range(0,len(LINES)):
            #print("line check")
            line = LINES[i]
            equation = True




            #print(equation)
            #HEHERE
            if  self.y + self.h == line["xy"][1] and self.x + self.w > line["xy"][ 0] and self.x < line["x2y2"][ 0]:
                if equation:
                    self.y -= self.jumph







LINES = [

{"xy": (166,70), "x2y2": (332,70) },
{"xy": (2,136), "x2y2": (196,136) },
{"xy": (255,190), "x2y2": (498,190) },
{"xy": (2,250), "x2y2": (200,250) },
{"xy": (260,310), "x2y2": (498,310) },
{"xy": (2,364), "x2y2": (206,364) },
    {"xy": (166,430), "x2y2": (332,430) }
]

BULLETS = []
player = Player(260, 460)
enemy = Enemy(30, 450)
run = True


pygame.display.set_caption('Selest')
background = pygame.Surface(win.get_size())
background.fill((0, 0, 0))


def update():
    player.update()


    win.blit(bg, (0, 0))
    #drawing after bg blip
    enemy.draw(win)
    player.draw(win)
    for i in range(0,len(LINES)):
        line = LINES[i]
        c1 = line["xy"]
        c2 = line["x2y2"]
        if i == 0:
            pygame.draw.line(win, (255, 0, 0), c1, c2)
            continue



        pygame.draw.line(win, (255, 255, 255),c1, c2)

    # win.blit(bg, (0, 0))
    pygame.display.update()

clock = pygame.time.Clock()
while run:
    clock.tick(30)
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        if player.x + player.w < ( winw- 5):
            player.x += 6
    if keys[pygame.K_LEFT]:
        if player.x > 2:

            player.x -= 6

    if keys[pygame.K_UP]:
        player.jump()
    for event in pygame.event.get():

        # wont throw an error if it quits.It thought player playerre quiting so it would quit.But now player arent so it works
        if event.type == pygame.QUIT:
            run = False

    collidestatus = enemy.collide(player)
    if collidestatus:
        print("Hit the monster")
        break
    enemy.update(player)
    player.update()
    update()

pygame.quit()
exit(0)