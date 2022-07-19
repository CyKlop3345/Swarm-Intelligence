import pygame
import random
import math
import time
pygame.init()

mode = "setPoints"
points = []
ways = []
ants = []
antNum = 0
stepNum = 0
recDist = 0
recIterat = 1
recTime = 0
timeStart = 0
iteratNum = 1
recWays = []
WHITE = (255,255,255)
BLACK = (10,10,10)
GRAY = (30,30,30)
RED = (255,0,0)
YELLOW = (175,175,0)
BLUE = (0,150,220)
F1 = 4
F2 = 1
antPhero = 800
vaporize = 0.64
font = pygame.font.SysFont('arial', 16)

class Points:
    def __init__(self, pos):
        self.color = BLUE
        self.pos = pos

class Ways:
    def __init__(self, p1, p2):
        self.color = GRAY
        self.points = [p1, p2]

        self.pos = [p1.pos, p2.pos]
        dist_x = self.pos[0][0] - self.pos[1][0]
        dist_y = self.pos[0][1] - self.pos[1][1]
        self.dist = ((dist_x**2)+(dist_y**2))**0.5
        self.near = 1/self.dist

        self.phero = 3
        self.thickness = int(self.phero)
        self.wish = (self.near**F1) * (self.phero**F2)

    def vaporize(self):
        self.phero *= vaporize
        if self.phero < 0.5:
            self.phero = 0.5
        self.recountPhero()

    def getPhero(self, phero):
        self.phero += phero
        self.recountPhero()

    def recountPhero(self):
        self.thickness = int(self.phero)
        self.wish = (self.near**F1) * (self.phero**F2)


class Ants:
    def __init__(self, startPoint):
        self.color = YELLOW
        self.startPoint = startPoint
        self.curPoint = startPoint
        self.pos = startPoint.pos
        self.nextPoints = []
        self.ways = []
        self.phero = antPhero

    def oneStep(self):
        global stepNum, antNum, recDist, iteratNum, recIterat, recTime
        if stepNum == 0:
            self.ways.clear()
            self.path = [self.startPoint]
            self.nextPoints = points.copy()
            self.nextPoints.remove(self.startPoint)
            self.curPoint = self.startPoint
            self.pos = self.startPoint.pos
        if stepNum < len(points)-1:
            stepNum += 1
            nextWays = []
            for i in range(len(ways)):
                if self.curPoint in ways[i].points and (ways[i].points[0] in self.nextPoints or ways[i].points[1] in self.nextPoints):
                    nextWays.append(ways[i])
            wishes = 0
            for i in range(len(nextWays)):
                wishes += nextWays[i].wish
            chances = []
            for i in range(len(nextWays)):
                chances.append(nextWays[i].wish/wishes)
            rnd = random.random()
            i = -1
            g = 0
            while g < rnd:
                i += 1
                g += chances[i]
            self.ways.append(nextWays[i])
            if self.curPoint == nextWays[i].points[0]:
                self.nextPoints.remove(nextWays[i].points[1])
                self.curPoint = nextWays[i].points[1]
                self.path.append(nextWays[i].points[1])
                self.pos = nextWays[i].points[1].pos
            else:
                self.nextPoints.remove(nextWays[i].points[0])
                self.curPoint = nextWays[i].points[0]
                self.path.append(nextWays[i].points[0])
                self.pos = nextWays[i].points[0].pos
        elif stepNum == len(points)-1:
            stepNum += 1
            for i in range(len(ways)):
                if self.curPoint in ways[i].points and self.startPoint in ways[i].points:
                    self.ways.append(ways[i])
            self.curPoint = self.startPoint
            self.pos = self.startPoint.pos
        else:
            stepNum = 0
            curDist = 0
            for i in range(len(self.ways)):
                curDist += self.ways[i].dist
            if curDist < recDist or recDist == 0:
                recDist = curDist
                recIterat = iteratNum
                recWays.clear()
                for i in range(len(self.ways)):
                    recWays.append(self.ways[i])
                recTime = time.time() - timeStart
            if antNum < len(ants)-1:
                antNum += 1
            else:
                antNum = 0
                iteratNum += 1
                length = 0
                for i in range(len(self.ways)):
                    length += self.ways[i].dist
                for i in range(len(ways)):
                    ways[i].vaporize()
                for i in range(len(ants)):
                    phero_0 = ants[i].phero/length
                    for g in range(len(ants[i].ways)):
                        ants[i].ways[g].getPhero(phero_0)
                self.ways.clear()

def drawPoints():
    for i in range(len(points)):
        pygame.draw.circle(screen, points[i].color, points[i].pos, 10)

def drawWays():
    for i in range(len(ways)):
        pygame.draw.line(screen, ways[i].color, ways[i].pos[0], ways[i].pos[1], ways[i].thickness)

def drawRecWay():
    for i in range(len(recWays)):
        pygame.draw.line(screen, YELLOW, recWays[i].pos[0], recWays[i].pos[1], 10)

def drawCurWay():
    for i in range(len(ants[antNum].ways)):
        pygame.draw.line(screen, RED, ants[antNum].ways[i].pos[0], ants[antNum].ways[i].pos[1], 3)

def drawAnt():
    pygame.draw.circle(screen, ants[antNum].color, ants[antNum].pos, 5)

def createPoint(pos):
    pygame.draw.circle(screen, BLUE, pos, 10)
    points.append(Points(pos))

def oneStep():
    ants[antNum].oneStep()

def logic():
    global mode
    if mode == "setPoints":
        mode = "setWays"

    if mode == "setWays":
        for i in range(len(points)):
            for g in range(i+1, len(points)):
                ways.append(Ways(points[i], points[g]))
        drawWays()
        mode = "setAnts"

    if mode == "setAnts":
        for i in range(len(points)):
            ants.append(Ants(points[i]))
        mode = "Swarm"

    if mode == "Swarm":
        ants[antNum].oneStep()

    screen.fill(BLACK)
    drawWays()
    drawRecWay()
    # drawCurWay()
    drawPoints()
    # drawAnt()

    timeCur = time.time() - timeStart

    iteratNumText = font.render("Iterat number: " + str(iteratNum), True, (0,255,255))
    timeText = font.render("Time: " + str(round(timeCur)), True, (0,255,255))
    recText = font.render("Record: " + str(round(recDist)), True, (0,255,255))
    recIteratText = font.render("Record iterat: " + str(recIterat), True, (0,255,255))
    recTimeText = font.render("Record time: " + str(round(recTime)), True, (0,255,255))

    screen.blit(iteratNumText, (10, 520))
    screen.blit(timeText, (10, 535))
    screen.blit(recText, (10, 550))
    screen.blit(recIteratText, (10, 565))
    screen.blit(recTimeText, (10, 580))

def start(F1_0, F2_0, antPhero_0, vaporize_0):
    global timeStart, mode, F1, F2, antPhero, vaporize
    timeStart = time.time()

    if mode == "setPoints":
        # P1 = [[53,53],[219,27],[360,80],[520,40],[40,215],[230,195],[340,203],[555,209],[35,453],[213,396],[351,352],[512,400]]
        # P2 = [[70,50],[280,80],[480,40],[30,160],[210,190],[410,180],[560,170],[110,310],[320,300],[520,330],[30,460],[220,450],[410,470],[580,480],[120,570],[310,570],[520,560]]
        # for i in range(len(P2)):
        # points.append(Points(P2[i]))
        #
        # for i in range(24):
        #     rndPos = (random.randint(0,1000), random.randint(0,600))
        #     points.append(Points(rndPos))
        #     pygame.draw.circle(screen, WHITE, rndPos, 10)
        mode = "setWays"
    F1 = F1_0
    F2 = F2_0
    antPhero = antPhero_0
    vaporize = vaporize_0

def reset():
    global timeStart, antNum, stepNum, recDist, recIterat, iteratNum, recWays, mode
    timeStart = time.time()
    ways.clear()
    ants.clear()
    antNum = 0
    stepNum = 0
    recDist = 0
    recIterat = 0
    iteratNum = 1
    recWays = []
    mode = "setWays"

def settings(screen_0):
    global screen
    screen = screen_0
