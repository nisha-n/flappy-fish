from eventBasedAnimationClass import EventBasedAnimationClass
from Tkinter import *
import math
import random
import time

"""
An underwater version of Flappy Bird
"""

class Food(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.foodWidth = 15
        self.foodHeight = 15
        self.visible = True

    def draw(self, canvas):
        if self.visible == True:
            canvas.create_oval(self.x, self.y, self.x + self.foodWidth,
                               self.y + self.foodHeight, fill="goldenrod")

    def move(self):
        self.x -= 1

    def overlaps(self, leftX, leftY, rightX, rightY):
        if self.visible == True and FlappyFish.rectanglesOverlap(leftX, leftY, 
                                     rightX - leftX, 
                                     rightY - leftY, self.x, 
                                     self.y, self.foodWidth, 
                                     self.foodHeight):
            return True

    def makeInvisible(self):
        # make food disappear
        self.visible = False

class PairLines(object):

    def __init__(self, x, y, height):
        self.x = x
        self.y = y
        self.length = random.randint(40, height/2-30)
        self.lineDistance = random.randint(30, 50)
        self.lineWidth = 8

    def draw(self, canvas, foodMode):
        color = "darkGreen"
        canvas.create_line(self.x, self.y, self.x, 
                           self.y - self.length, fill=color, 
                           width = self.lineWidth)
        canvas.create_line(self.x + self.lineDistance, 0,
                           self.x + self.lineDistance, self.length,
                           fill=color, width = self.lineWidth)

    def move(self):
        self.x -= 1

    def overlaps(self, leftX, leftY, rightX, rightY):
        # overlap with bottom line
        if FlappyFish.rectanglesOverlap(leftX, leftY, rightX - leftX, 
                                     rightY - leftY, self.x - self.lineWidth/2, 
                                     self.y - self.length, self.lineWidth, 
                                     self.length):
            return True
        # top line
        if FlappyFish.rectanglesOverlap(leftX, leftY, rightX - leftX, 
                                     rightY - leftY, 
                                     self.x + self.lineDistance, 0, 
                                     self.lineWidth,
                                     self.length):
            return True

class Shark(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sharkWidth = 120
        self.sharkHeight = 15
        self.visible = True
        self.sharkImage = None

    def draw(self, canvas):
        if self.visible == True:
            # image from 
# http://ed101.bu.edu/StudentDoc/Archives/ED101fa10/lizabeth/References.html
            if self.sharkImage == None:
                self.sharkImage = PhotoImage(file="cartoonshark.gif")
                self.sharkImage = self.sharkImage.subsample(2,4)
            canvas.create_image(self.x + self.sharkWidth/2, 
                                self.y - self.sharkHeight/2, 
                                image=self.sharkImage)

    def move(self):
        self.x -= 2

    def overlaps(self, leftX, leftY, rightX, rightY):
        if self.visible == False:
            return False
        if FlappyFish.rectanglesOverlap(leftX, leftY, rightX - leftX, 
                                     rightY - leftY, self.x, 
                                     self.y - self.sharkHeight, self.sharkWidth, 
                                     self.sharkHeight):
            return True

    def makeInvisible(self):
        self.visible = False

class Tuna(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tunaWidth = 65
        self.tunaHeight = 25
        self.visible = True
        self.tunaImage = None

    def draw(self, canvas):
        if self.visible == True:
            # image from 
            # http://www.how-to-draw-funny-cartoons.com/cartoon-tuna.html
            if self.tunaImage == None:
                self.tunaImage = PhotoImage(file="tuna.gif")
                self.tunaImage = self.tunaImage.subsample(6, 6)
            canvas.create_image(self.x + self.tunaWidth/2, 
                                self.y - self.tunaHeight/2,
                                image=self.tunaImage)

    def move(self):
        self.x -= 2

    def overlaps(self, leftX, leftY, rightX, rightY):
        if self.visible == False:
            return False
        if FlappyFish.rectanglesOverlap(leftX, leftY, rightX - leftX, 
                                     rightY - leftY, self.x, 
                                     self.y - self.tunaHeight, self.tunaWidth, 
                                     self.tunaHeight):
            return True

    def makeInvisible(self):
        self.visible = False


class Bullet(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bulletWidth = 10
        self.bulletHeight = 10
        self.visible = True

    def draw(self, canvas):
        if self.visible == True:
            canvas.create_oval(self.x, self.y, self.x + self.bulletWidth,
                               self.y + self.bulletWidth, fill="brown")

    def move(self):
        self.x += 1

    def makeInvisible(self):
        self.visible = False

class Bubbles(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bubbleWidth = 15
        self.bubbleHeight = 15
        self.bubbleImage = None

    def draw(self, canvas):
        # image from http://www.pennyparker1.com/children1.html
        if self.bubbleImage == None:
            self.bubbleImage = PhotoImage(file="bubble1.gif")
            self.bubbleImage = self.bubbleImage.subsample(2, 2)
        canvas.create_image(self.x + self.bubbleWidth/2, 
                            self.y+self.bubbleHeight/2, image=self.bubbleImage)

    def moveUp(self):
        self.y -= 1

class FlappyFish(EventBasedAnimationClass):

    def __init__(self):
        width = 500
        height = 400
        super(FlappyFish, self).__init__(width, height)
        self.timerDelay = 5
        self.fishX = self.width/5
        self.fishY = self.height/4
        self.fishWidth = 25
        self.fishHeight = 25
        self.textMargin = 55
        self.buttonWidth = 80
        self.buttonHeight = 40
        self.lastLineIndex = 0
        self.minLineGap = 65
        self.up = False
        self.speed = 3
        self.image = None
        self.foodModeCounter = 0
        self.timeElapsed = 0.0
        self.highScore = 0
        self.highScore = self.readHighScore()
        self.twoPlayer = False
        self.p1Score = None
        self.firstGame = False
        self.secondGame = False
        self.onePlayerWidth = 0
        self.twoPlayerWidth = 0
        self.instructionsWidth = 0
        self.bullets = []
        self.bubbles = []
        self.bubbleWidth = 15
        self.sharks = []
        self.sharkHeight = 15
        self.sharkY = 0
        self.pairLines = []
        self.food = []
        self.tuna = []
        self.tunaHeight = 25
        self.totalPauseTime = 0
        self.numFishKilled = 0

    def onKeyPressed(self, event):
        if (event.keysym == "p"):
            self.pause = not self.pause
            if self.pause == True:
                self.startPause = time.time()
            else:
                self.endPause = time.time()
                self.totalPauseTime += self.endPause - self.startPause
        if (event.keysym == "r"):
            # restart
            self.initAnimation()
            self.twoPlayer = False
        if self.pause == True or self.gameOver == True:
            return
        if self.firstPlayerStartScreen == True:
            if (event.keysym == "s"):
                # start two player game
                self.firstGame = True
                self.startGame = True
                self.startTime = time.time()
                self.twoPlayer = True
                self.p1Score = None
                self.firstPlayerStartScreen = False
        if self.gameOver == False:
            if (event.keysym == "Up"):
                self.up = True
        if (event.keysym == "q"):
            self.gameOver = True
        if (event.keysym == "space") and (self.firstPlayerStartScreen == False):
            # shoot bullets
            bulletX = self.fishX + self.fishWidth + 1
            bulletY = self.fishY + self.fishHeight/2
            self.bullets.append(Bullet(bulletX, bulletY))
        elif (event.keysym == "h"):
            self.instructions = False

    def onKeyReleased(self, event):
        if (event.keysym == "Up"):
            self.up = False

    def onMousePressed(self, event):
        if self.startGame == False:
            if self.isOnePlayer(event.x, event.y):
                self.startGame = True
                self.startTime = time.time()
            elif self.isTwoPlayer(event.x, event.y):
                self.startGame = True
                self.firstPlayerStartScreen = True
        if self.isInstructions(event.x, event.y):
                self.instructions = True
        if self.twoPlayer == True:
            if self.gameOver == True and self.secondGame == False:
                # click to start second game
                self.foodModeCounter = 0
                self.firstGame = False
                self.secondGame = True
                self.initAnimation()
                self.startGame = True
                self.startTime = time.time()

    def onMouseMotion(self, event):
        (x, y) = (event.x, event.y)
        if self.isOnePlayer(x, y):
            self.onePlayerWidth = 3
        elif self.isTwoPlayer(x, y):
            self.twoPlayerWidth = 3
        elif self.isInstructions(x, y):
            self.instructionsWidth = 3
        else:
            self.onePlayerWidth = 0
            self.twoPlayerWidth = 0
            self.instructionsWidth = 0

    def isOnePlayer(self, ex, ey):
        if (self.width/4 < ex < self.width/4 + self.buttonWidth) and \
            (ey > self.height/3 + self.textMargin) and \
            (ey < self.height/3 + self.buttonHeight + self.textMargin):
            return True
        return False

    def isTwoPlayer(self, ex, ey):
        if (ex > self.width/4 + 2*self.buttonWidth) and \
            (ex < self.width/4 + 3*self.buttonWidth) and \
            (ey > self.height/3 + self.textMargin) and \
            (ey < self.height/3 + self.buttonHeight + self.textMargin):
            return True
        return False

    def isInstructions(self, ex, ey):
        if (ex > self.width/2 - self.buttonWidth/2) and \
            (ex < self.width/2 + self.buttonWidth/2) and \
            (ey > self.height/3 + 2*self.textMargin) and \
            (ey < self.height/3 + 2*self.textMargin + self.buttonHeight):
            return True
        return False

    def drawInstructions(self):
        textHeight = 175
        instructions = """\n
        \t\t Instructions:\n
        Use the Up arrow to direct the fish through the obstacles\n
        Avoid the lines and other fish and don't go off the screen\n
        Collecting food makes the fish invincible for five seconds\n
        In invincible mode, the fish can go through obstacles without dying\n
        Press space to shoot bullets at the other fish\n
        Press p to pause, q to quit, and r to restart the game\n
           Press h to exit this help screen"""
        self.canvas.create_rectangle(5, 5, self.width, self.height,
                                     fill="deepSkyBlue", width=5, 
                                     outline="dodgerBlue")
        self.canvas.create_text(self.width/2, textHeight, text=instructions,
                                font="EngraversMT 14", fill="black",
                                width=490)

    def moveGame(self):
        randomInt = random.randint(1, 1000)
        if randomInt <= 25:
            n = len(self.pairLines)
            if n == 0 or self.pairLines[n-1].x < self.width - \
                        (self.pairLines[n-1].lineDistance + 10):
                self.pairLines.append(PairLines(self.width, self.height, 
                                  self.height))
        elif randomInt <= 33:
            n = len(self.sharks)
            if n == 0 or self.sharks[n-1].x < self.width - \
                        (self.sharks[n-1].sharkWidth - 10):
                self.sharkY = random.randint(self.sharkHeight, 
                                             self.height-self.sharkHeight)
                self.sharks.append(Shark(self.width, self.sharkY))
        elif randomInt <= 35:
            foodY = random.randint(20, self.height - 20)
            self.food.append(Food(self.width, foodY))
        elif randomInt <= 38:
            if len(self.bubbles) < 3:
                bubbleX = random.randint(self.fishX + 10, self.width)
                self.bubbles.append(Bubbles(bubbleX, 
                                    self.height - self.bubbleWidth))
        elif randomInt <= 40:
            n = len(self.tuna)
            if n == 0 or self.tuna[n-1].x < self.width - \
                        (self.tuna[n-1].tunaWidth - 10):
                self.tunaY = random.randint(self.tunaHeight, 
                                            self.height-self.tunaHeight)
                self.tuna.append(Tuna(self.width, self.tunaY))
        for i in xrange(self.speed):
            for item in self.pairLines:
                item.move()
            for item in self.bullets:
                item.move()
            for item in self.sharks:
                item.move()
            for item in self.tuna:
                item.move()
            for item in self.food:
                item.move()
        n = len(self.bullets)
        while i < n:
            if self.bullets[i].x > self.width:
                self.bullets.pop(i)
                n = n - 1
            else:
                i = i + 1
        for item in self.bubbles:
            item.moveUp()
        n = len(self.bubbles)
        while i < n:
            if self.bubbles[i].y < 0:
                self.bubbles.pop(i)
                n = n - 1
            else:
                i = i + 1
        n = len(self.sharks)
        while i < n:
            if self.sharks[i].x < 0:
                self.sharks.pop(i)
                n = n - 1
            else:
                i = i + 1
        n = len(self.tuna)
        while i < n:
            if self.tuna[i].x < 0:
                self.tuna.pop(i)
                n = n - 1
            else:
                i = i + 1
        n = len(self.pairLines)
        while i < n:
            if (self.pairLines[i].x + self.pairLines[i].lineDistance) < 0:
                self.pairLines.pop(i)
                n = n - 1
            else:
                i = i + 1
        n = len(self.food)
        while i < n:
            if self.food[i].x < 0:
                self.food.pop(i)
                n = n - 1
            else:
                i = i + 1

    def onTimerFired(self):
        if self.pause == True:
            return
        if self.startGame == False:
            return
        if self.firstPlayerStartScreen == True:
            return
        self.setGameStatus()
        if self.gameOver == False:
            if self.up == False:
                self.fishY += 2
            else:
                self.fishY -= 2
            if self.firstPlayerStartScreen == False:
                self.moveGame()
        else:
            self.gameOver = True

    def drawFish(self):
        if self.foodMode == True:
            # image from http://www.pennyparker1.com/children1.html
            self.bubbleImage = PhotoImage(file="bubble1.gif")
            imageSize = ( (self.bubbleImage.width(), self.bubbleImage.height()) )
            self.canvas.create_image(self.fishX + self.fishWidth/2, 
                                     self.fishY + self.fishHeight/2, 
                                     image=self.bubbleImage)
        # image from http://www.clipartbest.com/animated-fish-pictures
        self.fishImage = PhotoImage(file="fish1.gif")
        self.fishImage = self.fishImage.subsample(10,10)
        self.canvas.create_image(self.fishX + self.fishWidth/2, 
                                 self.fishY + self.fishHeight/2, 
                                 image=self.fishImage)
        imageSize = ( (self.fishImage.width(), self.fishImage.height()) )

    def drawStartText(self):
        textMargin = self.textMargin
        buttonWidth = self.buttonWidth
        buttonHeight = self.buttonHeight
        text = "Welcome to Flappy Fish!\n          Click to play"
        # image from 
        # http://wallpaperswide.com/underwater_bubbles_2-wallpapers.html
        self.startImage = PhotoImage(file="startScreen.gif")
        self.startImage = self.startImage.zoom(2, 4)
        self.canvas.create_image(self.width/2, self.height/2, 
                                 image=self.startImage)
        self.canvas.create_text(self.width/2, self.height/3, 
                         text=text, font="Herculanum 26 bold")
        self.canvas.create_rectangle(self.width/4, self.height/3 + textMargin,
                                self.width/4 + buttonWidth, 
                                self.height/3 + buttonHeight + textMargin,
                                fill="lightBlue", width=self.onePlayerWidth)
        self.canvas.create_text(self.width/4 + buttonWidth/2, 
                                self.height/3 + textMargin + buttonHeight/2,
                                text="One Player")
        self.canvas.create_rectangle(self.width/4 + 2*buttonWidth, 
                                     self.height/3 + textMargin,
                                     self.width/4 + 3*buttonWidth, 
                                     self.height/3 + buttonHeight + textMargin,
                                     fill="lightBlue", 
                                     width=self.twoPlayerWidth)
        self.canvas.create_text(self.width/4 + 5*buttonWidth/2, 
                                self.height/3 + textMargin+buttonHeight/2,
                                text="Two Player")
        self.canvas.create_rectangle(self.width/2 - buttonWidth/2, 
                                     self.height/3 + 2*textMargin,
                                     self.width/2 + buttonWidth/2,
                                     self.height/3 + 2*textMargin+buttonHeight,
                                     fill="lightBlue", 
                                     width=self.instructionsWidth)
        self.canvas.create_text(self.width/2, 
                                self.height/3 + 2*textMargin + buttonHeight/2,
                                text="Instructions")

    def setGameStatus(self):
        if self.gameOver == True:
            return
        if self.fishY < 0 or self.fishY + self.fishHeight >= self.height:
            self.gameOver = True
        if self.foodMode == True:
            self.foodModeCounter -= 1
            if self.foodModeCounter == 0:
                self.foodMode = False
        for i in xrange(len(self.pairLines)):
            if self.pairLines[i].overlaps(self.fishX, self.fishY, 
                                       self.fishX + self.fishWidth,
                                       self.fishY + self.fishHeight) and \
                                       self.foodMode == False:
                self.gameOver = True
        for i in xrange(len(self.sharks)):
            if self.sharks[i].overlaps(self.fishX, self.fishY, 
                                       self.fishX + self.fishWidth,
                                       self.fishY + self.fishHeight) and \
                                       self.foodMode == False:
                self.gameOver = True
        for i in xrange(len(self.tuna)):
            if self.tuna[i].overlaps(self.fishX, self.fishY, 
                                       self.fishX + self.fishWidth,
                                       self.fishY + self.fishHeight) and \
                                       self.foodMode == False:
                self.gameOver = True
        for i in xrange(len(self.food)):
            if self.food[i].overlaps(self.fishX, self.fishY, 
                                       self.fishX + self.fishWidth,
                                       self.fishY + self.fishHeight):
                self.foodMode = True
                self.foodModeCounter += 500
                self.food[i].makeInvisible()
        for i in xrange(len(self.bullets)):
            for j in xrange(len(self.sharks)):
                bulletWidth = self.bullets[i].bulletWidth
                bulletHeight = self.bullets[i].bulletHeight
                if self.bullets[i].visible == True:
                    # checks if bullet hits shark
                    if self.sharks[j].overlaps(self.bullets[i].x, 
                                               self.bullets[i].y,
                                               self.bullets[i].x + bulletWidth,
                                               self.bullets[i].y+bulletHeight):
                        self.sharks[j].makeInvisible()
                        self.bullets[i].makeInvisible()
                        self.numFishKilled += 1
        for i in xrange(len(self.bullets)):
            for j in xrange(len(self.tuna)):
                bulletWidth = self.bullets[i].bulletWidth
                bulletHeight = self.bullets[i].bulletHeight
                if self.bullets[i].visible == True:
                    if self.tuna[j].overlaps(self.bullets[i].x, 
                                             self.bullets[i].y,
                                             self.bullets[i].x + bulletWidth,
                                             self.bullets[i].y+bulletHeight):
                        self.tuna[j].makeInvisible()
                        self.bullets[i].makeInvisible()
                        self.numFishKilled += 1

    def drawGameOverText(self):
        textMargin = 20
        self.canvas.create_text(self.width/2, self.height/2,
                                text="Game Over! Press r to restart",
                                font="Arial 16 bold")
        self.canvas.create_text(self.width/2, self.height/2 + textMargin,
                                text="Final Score: " + str(self.timeElapsed),
                                font="Arial 14")
        self.canvas.create_text(self.width/2, self.height/2 + 2 * textMargin,
                                text="High score: " + str(self.highScore),
                                font="Arial 14")

    def drawScores(self):
        foodCount = self.foodModeCounter/100.0
        if self.gameOver == False and self.pause == False:
            endTime = time.time()
            # add 5 points each time shark is killed
            self.timeElapsed = round((endTime - self.startTime) - \
                                      self.totalPauseTime, 1) + \
                                      5 * self.numFishKilled
            # speed increases every 50 points
            if self.timeElapsed > 1 and self.timeElapsed % 50 == 0:
                if self.increasedSpeed == False:
                    self.speed += 1
                    self.increasedSpeed = True
            else:
                self.increasedSpeed = False
        self.canvas.create_text(10, 15, text="Score: " + str(self.timeElapsed),
                                anchor=W, fill="white")
        self.canvas.create_text(10, 30, text="High score: " + \
                                str(self.highScore), anchor=W, fill="white")
        if foodCount > 0:
            self.canvas.create_text(10, self.height - 30, 
                                    text="Time left in invincible mode:", 
                                    anchor=W, fill="white")
            self.canvas.create_text(10, self.height - 15, text=str(foodCount), 
                                    anchor=W, fill="white")

    def readHighScore(self):
        try:
            myFile = open('tpHighScore.txt', 'r')
            self.highScore = myFile.read()
        finally:
            myFile.close()
            return self.highScore
    
    def writeHighScore(self):
        if float(self.timeElapsed) > float(self.highScore):
            myFile = open('tpHighScore.txt', 'w')
            self.highScore = float(self.timeElapsed)
            myFile.write(str(self.highScore))
            myFile.close()
        else:
            return

    def loadGame(self):
        self.up = False
        self.fishY = self.height/4
        self.readHighScore()
        self.pairLines = []
        self.bubbles = []
        self.bullets = []
        self.sharks = []
        self.tuna = []
        self.food = []

    def drawTwoPlayerStartScreen(self):
        textMargin = 15
        if self.p1Score == None:
            self.p1Score = self.timeElapsed
        text1 = "Player 1 score: " + str(self.p1Score)
        text2 = "\nPlayer 2, click to begin game"
        self.canvas.create_text(self.width/2, self.height/2,
                                text=text1, font="Arial 16 bold")
        self.canvas.create_text(self.width/2, self.height/2 + textMargin,
                                text=text2, font="Arial 16")

    def drawTwoPlayerScores(self):
        textMargin = 30
        p1Score = self.p1Score
        p2Score = self.timeElapsed
        if int(p1Score) > int(p2Score):
            winner = "Player 1 wins!"
        if int(p2Score) > int(p1Score):
            winner = "Player 2 wins!"
        else:
            winner = "It's a tie!"
        text = "Player 1 score: " + str(p1Score) + "\nPlayer 2 score: " + \
                str(p2Score)
        text2 = "Press r to restart"
        self.canvas.create_text(self.width/2, self.height/2, 
                                text=winner, font="Arial 16 bold")
        self.canvas.create_text(self.width/2, self.height/2 + textMargin, 
                                text=text, font="Arial 16")
        self.canvas.create_text(self.width/2, self.height/2 + 2*textMargin,
                                text=text2, font="Arial 16")

    def drawPairLines(self):
        for item in self.pairLines:
            item.draw(self.canvas, self.foodMode)

    def drawSharks(self):
        for item in self.sharks:
            item.draw(self.canvas)

    def drawTuna(self):
        for item in self.tuna:
            item.draw(self.canvas)

    def drawBullets(self):
        for item in self.bullets:
            item.draw(self.canvas)

    def drawBubbles(self):
        for item in self.bubbles:
            item.draw(self.canvas)

    def drawFood(self):
        for item in self.food:
            item.draw(self.canvas)

    def drawFirstPlayerStartScreen(self):
        self.canvas.create_text(self.width/2, self.height/2,
                                text="Player 1, press 's' to start game",
                                font="Arial 16 bold")

    def redrawAll(self):
        self.canvas.delete(ALL)
        if self.startGame == False and self.instructions == False:
            self.drawStartText()
        elif self.instructions == True:
            self.drawInstructions()
        elif (self.startGame):
            if self.image == None:
                # image from http://www.brunsonimages.com/wall/wallmain.htm
                self.image = PhotoImage(file="ocean1.gif")
                self.image = self.image.zoom(2, 4)
            self.canvas.create_image(self.width/2, self.height/2, 
                                     image=self.image)
            self.drawBullets()
            self.drawBubbles()
            self.drawPairLines()
            self.drawSharks()
            self.drawTuna()
            self.drawFood()
            if self.firstPlayerStartScreen == True:
                self.drawFirstPlayerStartScreen()
            else:
                self.drawScores()
                self.drawFish()
        if self.gameOver == True:
            if self.twoPlayer == False:
                self.drawGameOverText()
                self.writeHighScore()
            else:
                if self.firstGame == True:
                    self.drawTwoPlayerStartScreen()
                else:
                    self.secondGame = False
                    self.drawTwoPlayerScores()

    @staticmethod
    def rectanglesOverlap(left1, top1, width1, height1,
                          left2, top2, width2, height2):
        noOverlap = left1 > left2 + width2 or left2 > left1 + width1 or \
                    top1 > top2 + height2 or top2 > top1 + height1
        return noOverlap == False

    def initAnimation(self):
        self.canvas.bind("<Motion>", self.onMouseMotion)
        self.root.bind("<KeyPress>", self.onKeyPressed)
        self.root.bind("<KeyRelease>", self.onKeyReleased)
        self.startGame = False
        self.instructions = False
        self.gameOver = False
        self.loadGame()
        self.foodMode = False
        self.bullets = []
        self.pause = False
        self.up = False
        self.speed = 3
        self.numFishKilled = 0
        self.firstPlayerStartScreen = False
        self.totalPauseTime = 0

FlappyFish().run()
