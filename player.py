import pygame
import os
bg = pygame.image.load("img/bg.png")
char = pygame.image.load("img/potato.png")

class Player:
    def __init__(self, x, y):
        self.g = 2
        self.x = x
        self.y = y
        self.h = 24
        self.w = 24
        self.jumph = 110
        self.isJump = False
        self.jumpcount = 10

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
        if self.y + self.h == 70:
            print("win")

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
                print(int(self.y + self.h - self.jumph*0.7 ), LINES[i-1]["xy"][1] - LINES[i]["xy"][1])
                equation =( self.x > LINES[i-1]["x2y2"][0] or self.x < LINES[i-1]["xy"][0]) or   self.y + self.h - self.jumph < LINES[i]["xy"][1] - LINES[i-1]["xy"][1]
                #print("here" + str(equation))



            #print(equation)
            if  self.y + self.h == line["xy"][1]:
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
player = Player(260, 120)
run = True
pygame.init()
winh = 500
winw = winh
win = pygame.display.set_mode((winw, winh))

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
            player.x += 6
    if keys[pygame.K_LEFT]:
        if player.x > 2:

            player.x -= 6
    for event in pygame.event.get():

        # wont throw an error if it quits.It thought player playerre quiting so it would quit.But now player arent so it works
        if event.type == pygame.QUIT:
            run = False

        if keys[pygame.K_UP]:

            player.jump()

    player.update()
    update()

pygame.quit()