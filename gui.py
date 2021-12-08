import pygame
from solver import Puzzle

class GUI:
    # Initialising
    def __init__(self):
        self.initSizes()
        self.initFormatting()
        self.initSpeed()
        self.initSudokuStuff()

        self.window = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        self.updateDisplay()
        self.mainloop()

    def initSizes(self):
        self.rows = self.cols = 9
        assert self.rows == self.cols
        
        self.cellSize = 40
        self.borderSize = 2
        self.largeBorderSize = 4

        self.gridWidth = self.gridHeight = (
            (self.cellSize * self.cols)
            + (self.borderSize * 6)
            + (self.largeBorderSize * 2)
        )

        self.windowWidth = self.gridWidth
        self.windowHeight = self.gridHeight + self.cellSize

    def initFormatting(self):
        self.gridSurf = pygame.Surface((self.gridWidth, self.gridHeight))
        self.solveSurf = pygame.Surface((self.gridWidth, self.cellSize))
        self.font = pygame.font.SysFont("Arial", self.cellSize // 2, bold=True)
        
        self.fontColor = (0, 0, 0)
        self.cellColor = (255, 255, 255)
        self.cellColor2 = (168, 168, 168)
        self.borderColor = (0, 0, 0)
        self.selectColor = (255, 255, 0)
        self.conflictColor = (255, 0, 0)
        self.solveColor = (29, 90, 196)

        self.selectedCell = (None, None)
        self.cellPositions = [
            [self.getCellRect(row, col) for col in range(self.cols)]
            for row in range(self.rows)
        ]
        self.conflicts = []

        self.title = "Sudoku Solver"
        pygame.display.set_caption(self.title)

    def initSpeed(self):
        self.clockSpeed = 60
        self.visualSolveDelay = 30
        self.clock = pygame.time.Clock()

    def initSudokuStuff(self):
        self.puzzle = Puzzle()
        self.solving = False
        self.visualSolving = False
        self.paused = False

    def getCellRect(self, row, col):
        numBorders = col
        numLargeBorders = col // 3
        numNormalBorders = numBorders - numLargeBorders
        x = (col * self.cellSize) + (self.borderSize * numNormalBorders) + (self.largeBorderSize * numLargeBorders)

        numBorders = row
        numLargeBorders = row // 3
        numNormalBorders = numBorders - numLargeBorders
        y = (row * self.cellSize) + (self.borderSize * numNormalBorders) + (self.largeBorderSize * numLargeBorders)

        return pygame.Rect(x, y, self.cellSize, self.cellSize)

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            elif (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and pygame.mouse.get_pressed()[0] # if left click
                ):  
                    self.mousePress(pygame.mouse.get_pos())
                    

            elif event.type == pygame.KEYDOWN and self.visualSolving:
                self.keyPressSolving(event.key)

            elif event.type == pygame.KEYDOWN:
                self.keyPress(event.key)

    # Visualize backtracking method
    def visualSolve(self):
        allSolvePos = self.puzzle.getEmptyCells()
        self.visualSolving = True
        self.updateDisplay()
        self.visualBacktrack([])
        self.selectedCell = (None, None)
        self.visualSolving = False
        self.updateDisplay(solvePos=allSolvePos)


    def visualBacktrack(self, solvePos):
        self.handleEvents()
        while self.paused:
            self.handleEvents()

        row, col = self.puzzle.getNextEmpty()
        if (row, col) == (None , None):
            return True

        pygame.time.delay(self.visualSolveDelay)
        self.selectedCell = (row, col)
        solvePos.append((row, col))
        self.updateDisplay(solvePos=solvePos)

        for num in self.puzzle.getCandidates(row, col):
            self.puzzle.setCell(row, col, num)
            self.selectedCell = (None, None)
            
            pygame.time.delay(self.visualSolveDelay)
            self.updateDisplay(solvePos=solvePos)

            if self.visualBacktrack(solvePos):
                self.selectedCell = (row, col)
                pygame.time.delay(self.visualSolveDelay)
                self.updateDisplay(solvePos=solvePos)
                self.selected = (None, None)

                return True
            else:
                self.puzzle.setCell(row, col, 0)
                
                self.selectedCell = (row, col)
                pygame.time.delay(self.visualSolveDelay)
                self.updateDisplay(solvePos=solvePos)

        self.selected = (None, None)

        return False

    
    def drawCells(self, solvePos=[]):
        for row in range(self.rows):
            for col in range(self.cols):
                cellRect = self.getCellRect(row, col)
                num = self.puzzle.getCell(row, col)

                # Hilights the selected cell by mouse
                if self.selectedCell != (row, col):
                    if (((0 <= row <= 2) or (6 <= row <= 8)) and (3 <= col <= 5)) or\
                    ((3 <= row <= 5) and (col < 3 or col > 5)):
                        pygame.draw.rect(self.gridSurf, self.cellColor2, cellRect)

                    else:
                        pygame.draw.rect(self.gridSurf, self.cellColor, cellRect)


                else:
                    pygame.draw.rect(self.gridSurf, self.selectColor, cellRect)

                # Draws the number
                if num != 0:
                    if (row, col) in self.conflicts:
                        color = self.conflictColor

                    elif (row, col) in solvePos:
                        color = self.solveColor
                    else:
                        color = self.fontColor

                    textSurface = self.font.render(str(num), True, color)
                    textRect = textSurface.get_rect()
                    textX = self.getCellRect(row, col).centerx - textRect.centerx
                    textY = self.getCellRect(row, col).centery - textRect.centery

                    self.gridSurf.blit(textSurface, (textX, textY))

    def updateGridSurf(self, solvePos=[]):
        self.gridSurf.fill(self.borderColor)
        self.drawCells(solvePos=solvePos)
        self.window.blit(self.gridSurf, (0, 0))

    def updateSolveSurf(self):
        self.solveSurf.fill(self.cellColor)
        pygame.draw.rect(self.solveSurf, self.borderColor, (0, 0, self.gridWidth, self.cellSize), width=self.borderSize)
        
        textSurface = None
        if self.solving:
            textSurface = self.font.render("Solving...", True, self.fontColor)

        elif self.visualSolving:
            if self.paused:
                textSurface = self.font.render(f"Paused", True, self.fontColor)
            else:
                textSurface = self.font.render(f"Solving with a time delay of {self.visualSolveDelay} ms...", True, self.fontColor)

        
        if self.solving or self.visualSolving:
            textRect = textSurface.get_rect()
            textX = (self.gridWidth // 2) - textRect.centerx
            textY = (self.cellSize // 2) - textRect.centery

            self.solveSurf.blit(textSurface, (textX, textY))

        self.window.blit(self.solveSurf, (0, self.gridHeight))

    def updateDisplay(self, solvePos=[]):
        pygame.display.set_caption(self.title)
        self.updateGridSurf(solvePos=solvePos)
        self.updateSolveSurf()

        pygame.display.update()

    def mousePress(self, pos):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cellPositions[row][col].collidepoint(pos):
                    if self.selectedCell != (row, col):
                        self.selectedCell = row, col

                    elif self.selectedCell == (row, col):
                        self.selectedCell = None, None
                    
                    
                    self.updateDisplay()
                    break

    def keyPressSolving(self, key):
        if (key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]):
            if key == pygame.K_UP or key == pygame.K_RIGHT:
                self.visualSolveDelay += 1

            elif (key == pygame.K_DOWN or key == pygame.K_LEFT) and self.visualSolveDelay > 1:
                self.visualSolveDelay -= 1

        elif key == pygame.K_p:
            self.paused = not self.paused
            self.updateDisplay()
            

    def keyPress(self, key):
        if self.selectedCell == (None, None): return

        keys = {
            pygame.K_0: 0, pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3,
            pygame.K_4: 4, pygame.K_5: 5, pygame.K_6: 6, pygame.K_7: 7,
            pygame.K_8: 8, pygame.K_9: 9, pygame.K_BACKSPACE: 0, pygame.K_DELETE: 0
        }

        r, c = self.selectedCell
        if key in keys:
            num = keys[key]
            self.puzzle.setCell(r, c, num)
            self.conflicts = self.puzzle.getConflicts()
            self.updateDisplay()

        elif key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
            if key == pygame.K_LEFT and c > 0:
                c -= 1

            elif key == pygame.K_RIGHT and c < self.cols-1:
                c += 1

            elif key == pygame.K_UP and r > 0:
                r -= 1

            elif key == pygame.K_DOWN and r < self.rows-1:
                r += 1
            
            self.selectedCell = (r, c)
            self.updateDisplay()
            
        elif key == pygame.K_SPACE and len(self.puzzle.getConflicts()) == 0:
            self.solve()

        elif key == pygame.K_v and len(self.puzzle.getConflicts()) == 0:
            self.visualSolve()

        elif key == pygame.K_c:
            self.puzzle.clearPuzzle()
            self.conflicts = []
            self.updateDisplay()

    def solve(self):
        solvePos = self.puzzle.getEmptyCells()
        self.solving = True
        self.updateDisplay()
        self.puzzle.solve()
        self.selectedCell = (None, None)
        self.solving = False
        self.updateDisplay(solvePos=solvePos)

    def mainloop(self):
        while True:
            self.clock.tick(self.clockSpeed)
            self.handleEvents()

pygame.init()
window = GUI()
