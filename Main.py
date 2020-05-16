import pygame
import random
from threading import Timer

pygame.init()

WIDTH = 1400
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
s = pygame.Surface((400, 680), pygame.SRCALPHA)

pygame.display.set_caption("Cards")

imgDict = {
    0: "PNG/AS.png", 4: "PNG/AH.png", 8: "PNG/AC.png", 12: "PNG/AD.png",
    1: "PNG/JS.png", 5: "PNG/JH.png", 9: "PNG/JC.png", 13: "PNG/JD.png",
    2: "PNG/QS.png", 6: "PNG/QH.png", 10: "PNG/QC.png", 14: "PNG/QD.png",
    3: "PNG/KS.png", 7: "PNG/KH.png", 11: "PNG/KC.png", 15: "PNG/KD.png"
}
imgBack = pygame.image.load("PNG/red_back1.png")
imgBack = pygame.transform.scale(imgBack, (int(691 / 6.5), int(1056 / 6.5)))
trans = pygame.image.load("PNG/trans.png")

cardList = []
flips = 0
combinations = 0
start_time = 0
time = 0
gameStart = False
m_x = 0
m_y = 0
click = (0, 0, 0)


class Card:
    def __init__(self, x, y, key):
        self.x = x
        self.y = y
        self.displace = 0
        self.key = key
        self.face = pygame.image.load(imgDict[key % 16])
        self.face = pygame.transform.scale(self.face, (int(691 / 6.5), int(1056 / 6.5)))
        self.back = imgBack
        self.zoomBack = pygame.transform.scale(self.back, (int(691 / 6.5) + 10, int(1056 / 6.5) + 10))
        self.busy = False
        self.img = self.back

    def display(self):
        screen.blit(self.img, (self.x + self.displace, self.y + self.displace))

    def canFlip(self):
        if self.busy:
            return False
        else:
            return True

    def flip(self):
        self.displace = 0
        self.img = self.face
        self.busy = True
        return self.key


def matchLogic(check1, check2, clist):
    global combinations
    if check1 - check2 == 16 or check1 - check2 == -16:
        for obj in clist:
            if check1 == obj.key:
                obj.displace = 5
                obj.img = trans
            if check2 == obj.key:
                obj.displace = 5
                obj.img = trans
                # print(imgDict[obj.key % 16])
        combinations += 1
        print("Combinations: " + str(combinations))
        # print("MATCH!!!")
        return True
    else:
        for obj in clist:
            if check1 == obj.key:
                obj.img = obj.back
                obj.busy = False
            if check2 == obj.key:
                obj.img = obj.back
                obj.busy = False
        # print("NOT MATCH!!!")
        return False


def button(text, colour, coordinates, x, y):
    sFont = pygame.font.SysFont("Verdana", 25)
    pygame.draw.rect(s, colour, (x, y, 100, 50))
    pygame.draw.rect(s, [0, 0, 0], (x, y, 100, 50), 2)
    start = sFont.render(text, True, [0, 0, 0])
    s.blit(start, coordinates)


def scoreBoard():
    global flips, combinations, start_time, time, gameStart, m_x, m_y, click
    hfont = pygame.font.SysFont("Trebuchet MS", 50, italic="True")
    cFont = pygame.font.SysFont("Trebuchet MS", 22)
    sFont = pygame.font.SysFont("Segoe UI", 40)
    breakL = cFont.render("_________________________________", True, [0, 0, 0])
    title = hfont.render("MEMORY GAME", True, [208, 32, 0])
    s.blit(title, (30, 20))
    s.blit(breakL, (0, 70))
    caption = cFont.render("Match all the cards as fast as possible", True, [50, 0, 150])
    s.blit(caption, (10, 110))
    caption1 = cFont.render("Test your memory skills here", True, [50, 0, 150])
    s.blit(caption1, (60, 140))
    s.blit(breakL, (0, 160))
    if not gameStart:
        button("START", [0, 200, 0], (60, 610), 50, 600)
        if 1040 < m_x < 1140 and 610 < m_y < 660:
            button("START", [0, 150, 0], (60, 610), 50, 600)
            if click[0]:
                button("START", [0, 200, 0], (60, 610), 50, 600)
                start_time = pygame.time.get_ticks()
                gameStart = True
        button("QUIT", [200, 0, 0], (265, 610), 250, 600)
        if 1240 < m_x < 1340 and 610 < m_y < 660:
            button("QUIT", [150, 0, 0], (265, 610), 250, 600)
            if click[0]:
                button("QUIT", [200, 0, 0], (265, 610), 250, 600)
                pygame.quit()
                quit()
    if gameStart:
        time = (pygame.time.get_ticks() - start_time) // 1000
        timet = sFont.render("Time : " + str(time) + " sec", True, [0, 0, 200])
        s.blit(timet, (20, 220))
        flip = sFont.render("Flips : " + str(flips), True, [0, 0, 200])
        s.blit(flip, (20, 300))
        comb = sFont.render("Combinations : " + str(combinations), True, [0, 0, 200])
        s.blit(comb, (20, 380))


def over():
    global flips, combinations, start_time, time, gameStart, m_x, m_y, click, cardList
    hfont = pygame.font.SysFont("Trebuchet MS", 55, bold="True")
    cFont = pygame.font.SysFont("Trebuchet MS", 22)
    sFont = pygame.font.SysFont("Segoe UI", 40)
    breakL = cFont.render("_________________________________", True, [0, 0, 0])
    title = hfont.render("GAME OVER", True, [210, 0, 0])
    s.blit(title, (30, 50))
    s.blit(breakL, (0, 130))
    timet = sFont.render("Total time : " + str(time) + " sec", True, [0, 0, 200])
    s.blit(timet, (20, 220))
    flip = sFont.render("Total flips : " + str(flips), True, [0, 0, 200])
    s.blit(flip, (20, 300))
    button("REPLAY", [0, 200, 0], (53, 610), 50, 600)
    if 1040 < m_x < 1140 and 610 < m_y < 660:
        button("REPLAY", [0, 150, 0], (53, 610), 50, 600)
        if click[0]:
            init()
            start_time = pygame.time.get_ticks()
            gameStart = True
    button("QUIT", [200, 0, 0], (265, 610), 250, 600)
    if 1240 < m_x < 1340 and 610 < m_y < 660:
        button("QUIT", [150, 0, 0], (265, 610), 250, 600)
        if click[0]:
            button("QUIT", [200, 0, 0], (265, 610), 250, 600)
            pygame.quit()
            quit()


def init():
    global cardList, flips, combinations, start_time, time
    flips = 0
    combinations = 0
    start_time = 0
    time = 0
    cardPosList = []  # coordinates
    for j in range(0, 4):
        for i in range(0, 8):
            if i == 0 and j == 0:
                cardPosList.append((20, 10))
            elif j == 0 and i != 0:
                cardPosList.append((int(((691 * i) + (i + 1) * 100) / 6.5) + 5, 10))
            elif j != 0 and i == 0:
                cardPosList.append((20, int(((1056 * j) + (j + 1) * 65) / 6.5)))
            elif j != 0 and i != 0:
                cardPosList.append((int(((691 * i) + (i + 1) * 100) / 6.5) + 5, int(((1056 * j) + (j + 1) * 65) / 6.5)))
    # print(cardPosList)

    cardList = []  # list of objects of class Card
    for i in range(32):
        # cardList.append(Card(cardPosList[i][0], cardPosList[i][1], i))
        pos = random.choice(cardPosList)
        cardList.append(Card(pos[0], pos[1], i))
        cardPosList.remove(pos)


def game_loop():
    state = True
    global flips, combinations, start_time, time, gameStart, m_x, m_y, click, cardList
    init()
    cardsToCheck = []

    while state:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                state = False

        m_x = pygame.mouse.get_pos()[0]
        m_y = pygame.mouse.get_pos()[1]
        click = pygame.mouse.get_pressed()

        screen.fill([0, 100, 0])
        for obj in cardList:
            obj.display()
        if gameStart:
            for obj in cardList:
                if obj.x < m_x < obj.x + 106 and obj.y < m_y < obj.y + 162:
                    if not obj.busy:
                        obj.img = obj.zoomBack
                        obj.displace = -5
                    if click[0]:
                        if obj.canFlip() and 0 <= len(cardsToCheck) < 2:
                            cardsToCheck.append(obj.flip())
                            flips += 1
                            print(flips)

                else:
                    if not obj.busy:
                        obj.displace = 0
                        obj.img = obj.back
            if len(cardsToCheck) == 2:
                r = Timer(0.5, matchLogic, (cardsToCheck[0], cardsToCheck[1], cardList))
                r.start()
                cardsToCheck.clear()

        screen.blit(s, (990, 10))
        s.fill((255, 255, 255, 125))
        pygame.draw.rect(s, (0, 0, 0), (0, 0, 400, 680), 10)

        if combinations == 16:
            gameStart = False
            over()
        else:
            scoreBoard()
        pygame.display.update()

    pygame.quit()
    quit()


game_loop()
