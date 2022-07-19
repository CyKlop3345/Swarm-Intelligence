import pygame
import random
import math
pygame.init()

screen = pygame.display.set_mode((600,600))
points = []
ways = []
ants = []
antNum = 0
stepNum = 0
recDist = 0
recWays = []
WHITE = (255,255,255)
GREEN = (50,150,50)
RED = (255,0,0)
class Points:
    def __init__(self, pos):
        self.pos = pos
        self.color = (255,255,255)

class Ways:
    def __init__(self, p1, p2):
        self.color = GREEN
        self.points = [p1, p2]
        self.pos = [p1.pos, p2.pos]
        dist_x = self.pos[0][0] - self.pos[1][0]
        dist_y = self.pos[0][1] - self.pos[1][1]
        self.dist = ((dist_x**2)+(dist_y**2))**0.5
        self.near = 1/self.dist
        self.phero = 1
        self.thickness = round(self.phero/2)
        self.wish = (self.near**4) * (self.phero**1)

    def getPhero(self, phero):
        self.phero += phero*self.dist
        if self.phero > 15:
            self.phero = 15
        self.thickness = math.ceil(self.phero/2)
        self.wish = (self.near**4) * (self.phero**1)

    def vaporize(self):
        self.phero *= 0.8
        if self.phero < 2:
            self.phero = 2

class Ants:
    def __init__(self, startPoint):
        self.color = (0,0,0)
        self.startPoint = startPoint
        self.curPoint = startPoint
        self.pos = startPoint.pos
        self.nextPoints = []
        self.ways = []
        self.phero = 10

    def oneStep(self):
        global stepNum, antNum, recDist
        if stepNum == 0:
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
            self.ways.append(nextWays[i])
        elif stepNum < len(points):
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
                recDist = round(curDist)
                recWays.clear()
                for i in range(len(self.ways)):
                    recWays.append(self.ways[i])
            if antNum < len(ants)-1:
                antNum += 1
            else:
                antNum = 0
                length = 0
                for i in range(len(self.ways)):
                    length += self.ways[i].dist
                phero_0 = self.phero/length
                for i in range(len(ways)):
                    ways[i].vaporize()
                for i in range(len(ants)):
                    for g in range(len(self.ways)):
                        ants[i].ways[g].getPhero(phero_0)

def drawPoints():
    for i in range(len(points)):
        pygame.draw.circle(screen, points[i].color, points[i].pos, 10)

def drawWays():
    for i in range(len(ways)):
        pygame.draw.line(screen, ways[i].color, ways[i].pos[0], ways[i].pos[1], ways[i].thickness)

def drawRecWay():
    for i in range(len(recWays)):
        pygame.draw.line(screen, (255,255,255), recWays[i].pos[0], recWays[i].pos[1], 10)

def drawAnt():
    pygame.draw.circle(screen, ants[antNum].color, ants[antNum].pos, 5)

def main():
    pygame.display.set_caption("Swarm intelligence")
    clock = pygame.time.Clock()
    fps = 30
    mode = "setPoints"
    font = pygame.font.SysFont('arial', 16)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if mode == "setPoints":
                        mode = "setWays"
                    if mode == "Swarm":
                        ants[antNum].oneStep()
            if mode == "setPoints":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        points.append(Points(event.pos))
                        pygame.draw.circle(screen, WHITE, event.pos, 10)
                        pygame.display.flip()

        if mode == "setPoints":
            P1 = [[53,53],[219,27],[360,80],[520,40],[40,215],[230,195],[340,203],[555,209],[35,453],[213,396],[351,352],[512,400]]
            for i in range(24):
                rndPos = (random.randint(0,600), random.randint(0,600))
                points.append(Points(rndPos))
                pygame.draw.circle(screen, WHITE, rndPos, 10)
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

        screen.fill((0,0,0))
        drawWays()
        drawPoints()
        drawRecWay()

        if mode == "Swarm":
            recText = font.render("record: " + str(recDist), True, (255, 255, 0))
            screen.blit(recText, (10, 5))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
