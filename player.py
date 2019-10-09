import pygame
import os
bg = pygame.image.load("img/bg.png")
LINES = [
{"xy": (100,400), "x2y2": (210,400) },
    {"xy": (100,430), "x2y2": (250,430) }

]

class Player:
    def __init__(self, x, y):
        self.g = 2
        self.x = x
        self.y = y
        self.h = 10
        self.w = 10
        self.jumph = 200
        self.isJump = False
        self.jumpcount = 10

    def draw(self, win):

        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.w, self.h))

    def update(self):
        #gravity conditions
        #print(self.y + self.h, self.x + self.w)

        allow = True
        for line in LINES:
            #print(not(self.y + self.h == line["xy"][1]  and self.x > line["xy"][0] and self.x < line["x2y2"][0] )  and self.y + self.h < 498)

            #print(not(self.y + self.h == line["xy"][1]  and self.x < line["x2y2"][0] and self.x > line["xy"][0] ) )
            if (allow):
                if not(not(self.y + self.h == line["xy"][1]  and self.x > line["xy"][0] and self.x < line["x2y2"][0] )  and self.y + self.h < 498):

                    allow =  False
                    #print("DISSALLOW")
        #print(allow)
        if allow:
            self.y += self.g

        #print("-----")

    def jump(self):
        print("jump command retrieved")
        #if above ground then jump

        allow = False
        if self.y + self.h >= 498 :
            #only jump if line not in the way
            print("jump called")
            for i in range(0,len(LINES)):
                line = LINES[i]
                if i != 0:
                    equation =  not(self.y +self.h - self.jumph < LINES[i-1]["xy"][1] and self.x < line["x2y2"][0] and self.x > line["xy"][0])

                else:
                    equation = not (self.y + self.h - self.jumph < LINES[i]["xy"][1] and self.x < line["x2y2"][ 0] and self.x > line["xy"][0])

                if equation :



                    allow = True
                else:
                    allow = False

            if allow:
                self.y -= self.jumph
                #print("pix")

        #if on a line jump if the line above is far away
        for i in range(0,len(LINES)):
            #print("line check")
            line = LINES[i]
            equation = False
            if i == 0:
                equation = True

            else:
                #debugging
                '''
                print(self.x , LINES[i-1]["x2y2"][0] )
                print(self.x , LINES[i-1]["xy"][1])
                print((self.x > LINES[i-1]["x2y2"][0] , self.x < LINES[i-1]["xy"][0]))
                print("xValues" + str((self.x > LINES[i-1]["x2y2"][0] or self.x < LINES[i-1]["xy"][0])))
                #print("Allowence" + str(self.y + self.h - self.jumph) + str(500 - LINES[i - 1]["xy"][1]))
                print("Allowence" + str( self.y + self.h - self.jumph < 500 - LINES[i-1]["xy"][1] ))
                '''
                equation =( self.x > LINES[i-1]["x2y2"][0] or self.x < LINES[i-1]["xy"][0]) or   self.y + self.h - self.jumph < 500 - LINES[i-1]["xy"][1]
                #print("here" + str(equation))



            #print(equation)
            if  self.y + self.h == line["xy"][1]:
                if equation:
                    self.y -= self.jumph





run = True
pygame.init()
winh = 500
winw = winh
win = pygame.display.set_mode((winw, winh))
player = Player(250, 50)
pygame.display.set_caption('Selest')
background = pygame.Surface(win.get_size())
background.fill((0, 0, 0))


def update():
    player.update()


    win.blit(bg, (0, 0))
    #drawing after bg blip

    player.draw(win)
    for line in LINES:

        c1 =  line["xy"]
        c2 = line["x2y2"]

        pygame.draw.line(win, (255,255,255), c1 ,c2 )
        pygame.draw.line(win, (255, 255, 255),c1, c2)

    # win.blit(bg, (0, 0))
    pygame.display.update()

clock = pygame.time.Clock()
while run:
    clock.tick(30)
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        if player.x + player.w < ( winw- 5):
            player.x += 4
    if keys[pygame.K_LEFT]:
        if player.x > 2:

            player.x -= 4
    for event in pygame.event.get():

        # wont throw an error if it quits.It thought player playerre quiting so it would quit.But now player arent so it works
        if event.type == pygame.QUIT:
            run = False

        if keys[pygame.K_UP]:

            player.jump()

    player.update()
    update()

pygame.quit()