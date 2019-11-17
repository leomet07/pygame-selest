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
pygame.font.init() # you have to call this at the start,
                   # if you want to use this module.
comicsans = pygame.font.SysFont('Comic Sans MS', 30)

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

        sprite = monster
        monster = pygame.transform.scale(sprite, (self.w, self.h))
        #draw the monster
        win.blit(monster, (self.x, self.y))




        #draw bullets
        for bullet in BULLETS:
            #draw the current bullet
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
        b_point = False
        #print(bird.y, self.y)
        if bird.x <= self.x + self.w and bird.x >= self.x :

            if bird.y >= self.y  and bird.y <= self.y + self.h:
                print("hit")
                b_point = True




        return b_point

    def launchbullets(self, player):
        #print("Launching bullets")
        #print("Bullets: " + str(len(BULLETS)))

        bullet = [player.x + 5, 480]
        BULLETS.append(bullet)
    def update(self, player):
        global run
        global BULLETS
        self.tickcount += 1
        if self.tickcount == 75:
            #print("launch")
            self.tickcount = 0
            self.launchbullets(player)




        #duplicate of bullets array as to not mess with for loop
        dupbullets = BULLETS
        deleted = 0
        for i in range(0,len(BULLETS) ):
            if 0 <= BULLETS[i - deleted][1]:
                BULLETS[i - deleted][1] -= 9
            else:
                dupbullets.pop(i)
                deleted += 1



        #drawing of the bullets
        BULLETS = dupbullets
        for bullet in BULLETS:
            #check for bullet collision
            if bullet[1] < player.y + player.h and  bullet[1] > player.y  :
                if bullet[0] > player.x and bullet[0] < player.x + player.w:

                    #LET PLAYER LIVE IF TOUCHING THE GROUND
                    if player.y + player.h != 498:
                        print("hit the bullet")
                        run = False


        #move towards player upward
        if self.y + self.h> player.y + player.h:
            #move monster up if player is above
            self.y -= 1

        if self.y < player.y :
            #move monster down if player is below
            self.y += 1

        if self.x  <= player.x  :
            #move monster right if player is right
            self.x += 1

        if self.x + self.w > player.x  :
            #move monster left if player is left
            self.x -= 1

class Player:
    def __init__(self, x, y):
        #char is the character sprite
        global char
        self.g = 2
        self.x = x
        self.y = y
        self.h = 24
        self.w = 24
        self.jumph = 20
        self.isJump = False
        self.jumpcount = 10
        self.img = char
        self.upwardvel = 0

        #calculates total amount of pixels flown up
        testjumph = self.jumph
        self.totaljumph = 0
        while testjumph != 0:
            self.totaljumph += testjumph
            testjumph -= 2
            #subtracting 2 to simulate gravity



    def draw(self, win):
        global char
        #pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.w, self.h))
        sprite = char
        char = pygame.transform.scale(sprite, (self.w, self.h))
        win.blit(char, (self.x, self.y))




    def update(self):
        global current_level
        global enemy
        #making the level a global var
        global LINES
        global run
        global winstatus
        global game_update

        #gravity conditions
        #print(self.y + self.h, self.x + self.w)

        allow = True
        #gravity is allowed if not standing on a line
        for line in LINES:
            #if already standing on a line, dont check for standing on others
            if (allow):
                #checking if touching line
                if not(not(self.y + self.h == line["xy"][1]  and self.x + (self.w/1) > line["xy"][0] and self.x < line["x2y2"][0] )  and self.y + self.h < 498):

                    allow =  False


        if allow:
            self.y += self.g

        #print("-----")

        #getting the top line
        #print("Length f lines" + str(len(LINES)))
        line = LINES[0]
        # check for win condition
        if self.y + self.h == 70  and self.x + self.w > line["xy"][ 0] and self.x < line["x2y2"][ 0]:
            #if touching red line then game has been won

            print("win")

            current_level +=1

            data = []
            with open('level.json') as json_file:
                data = json.load(json_file)

                #if last level quit, otherwise continue loading
                if len(data) > current_level :
                    LINES = []
                    print(data[current_level]["level"])
                    LINES = data[current_level]["level"]
                else:
                    print("victory")
                    winstatus = True
                    game_update = False

            #ressting the player and enemypos
            self.x = 400
            self.y = 460
            enemy.y = 460
            enemy.x = 50



        #moving player up if the  upward vel is positive(exists)
        self.y -= self.upwardvel

        #the jump gets slower towards the peak so the jump amount is lowered if it isnt zero.
        if self.upwardvel > 0:
            self.upwardvel -= 2



    def jump(self):

        #if above ground(floor) then jump

        allow = False
        if self.y + self.h >= 498 :

            #lauprint("jump called")

            line = LINES[-1]
            # only jump if the bottom platform is not in the way
            equation = not (self.y + self.h - self.totaljumph < LINES[-1]["xy"][1] and self.x < line["x2y2"][ 0] and self.x + (self.w/2) > line["xy"][0])

            if equation:
                self.upwardvel += self.jumph


        #if on a line jump
        for i in range(0,len(LINES)):
            #get the current line being cycled to
            line = LINES[i]

            #check if standing on a line
            if self.y + self.h == line["xy"][1] and self.x + self.w > line["xy"][ 0] and self.x < line["x2y2"][ 0]:

                self.upwardvel += self.jumph







import json
LINES = []
data = []
current_level = 0
#loading in the level
with open('level.json') as json_file:
    data = json.load(json_file)
    LINES = data[current_level]["level"]
SCORE = data[0]["time"]
game_update = True

BULLETS = []

#initializing the players
player = Player(400, 460)
enemy = Enemy(30, 450)
run = True
winstatus = False

pygame.display.set_caption('Selest')
background = pygame.Surface(win.get_size())
background.fill((0, 0, 0))

#start button is the coords of the start button (x,y,w,h)
startbutton = (200, 200, 100, 50)
endbutton = (176, 200, 148, 50)
def update():

    #only update if game is running
    if game_update:
        if game_started:
            enemy.update(player)
            #update player twice so more gravity and as a backup
            player.update()
            player.update()
            '''
            #if detected that game needs to end, dont update again
            print(game_update,not(winstatus))
            if game_update :
                if not(winstatus):
                    print("second updatwe")
                    player.update()
            else:
                #if game needs to end quit drawing
                return
            '''




    #bg must be blit first to see things that are on top of it
    win.blit(bg, (0, 0))

    #draw start button if game isnt running
    if not(game_started):
        pygame.draw.rect(win, (255, 0, 0),startbutton)
        btntext = comicsans.render("Start", True, (0, 0, 0))
        win.blit(btntext, (startbutton[0] + 10,startbutton[1] + 2))
    if winstatus:
        #if won display the win text
        pygame.draw.rect(win, (0, 255, 0), endbutton)
        btntext = comicsans.render("You Won!", True, (0, 0, 0))
        win.blit(btntext, (endbutton[0] + 10, endbutton[1] + 2))

    #only show game elemnts if gme is running
    if game_started:
        if game_update:
            # writing the score to the screen
            textsurface = comicsans.render("Score: " + str(SCORE), True, (0, 0, 0))
            win.blit(textsurface, (0, 0))

            #drawaing chars
            enemy.draw(win)
            player.draw(win)

            #draw each platform
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
counter = 0
game_started = False
while run:
    clock.tick(30)
    for event in pygame.event.get():

        # check if window was losed to stop the game loop
        if event.type == pygame.QUIT:
            run = False

    if game_started:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            if player.x + player.w < ( winw- 5):
                player.x += 6
        if keys[pygame.K_LEFT]:
            if player.x > 2:
                player.x -= 6
        if keys[pygame.K_UP]:
            player.jump()






    #run update after key recog
    update()
    #print(winstatus)
    mouse_cords = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0] == 1 and not(game_started):
        # print("Here")
        # check ifit is pressed on the rect
        # print(mouse_cords)
        if mouse_cords[0] > startbutton[0] and mouse_cords[0] < startbutton[0] + startbutton[2] and mouse_cords[1] > startbutton[1] and mouse_cords[1] < startbutton[1] +  startbutton[3]:
            print("btn presssed")
            game_started = True

    if winstatus:
        #print("check for end buton status")
        if pygame.mouse.get_pressed()[0] == 1 :
            # print("Here")
            # check ifit is pressed on the rect
            # print(mouse_cords)
            if mouse_cords[0] > endbutton[0] and mouse_cords[0] < endbutton[0] + endbutton[2] and mouse_cords[1] > endbutton[1] and mouse_cords[1] < endbutton[1] + endbutton[3]:
                print("end btn presssed")
                run = False




    if game_started:
        #check for collision
        collidestatus = enemy.collide(player)
        if collidestatus:
            print("Hit the monster")
            break

        counter += 1

        if counter == 30:
            SCORE -= 1
            counter = 0

        #if time runs out, quit
        if SCORE == 0:
            print("out of time")
            break


pygame.quit()
