import pygame
from solver import Puzzle

class GUI:
    def __init__(self):
        self.initSizes()
        self.initColors()

        self.selectedCell = (None, None)
        self.clockSpeed = 60
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", self.cellSize // 2, bold=True)
        self.puzzle = Puzzle()

        self.cellPositions = [
            [self.getCellRect(row, col) for col in range(self.cols)]
            for row in range(self.rows)
        ]

        self.conflicts = []

        self.title = "Sudoku Solver"
        self.window = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        self.updateDisplay()
        self.mainloop()

    def initSizes(self):
        self.rows = 9
        self.cols = 9
        self.cellSize = 40
        self.borderSize = 2
        self.largeBorderSize = 5
        self.windowWidth = (
            (self.cellSize * self.cols)
            + (self.borderSize * 6)
            + (self.largeBorderSize * 2)
        )
        self.windowHeight = (
            self.cellSize * self.rows
            + (self.borderSize * 6)
            + (self.largeBorderSize * 2)
        )

    def initColors(self):
        self.fontColor = (0, 0, 0)
        self.cellColor = (255, 255, 255)
        self.borderColor = (0, 0, 0)
        self.selectColor = (255, 255, 0)
        self.conflictColor = (255, 0, 0)

    def getCellRect(self, row, col):
        x = 0
        y = 0

        x += col * self.cellSize
        numBorders = col
        numLargeBorders = col // 3
        numNormalBorders = numBorders - numLargeBorders

        x += self.borderSize * numNormalBorders
        x += self.largeBorderSize * numLargeBorders

        y += row * self.cellSize
        numBorders = row
        numLargeBorders = row // 3
        numNormalBorders = numBorders - numLargeBorders

        y += self.borderSize * numNormalBorders
        y += self.largeBorderSize * numLargeBorders

        return pygame.Rect(x, y, self.cellSize, self.cellSize)

    def drawCells(self):
        for row in range(self.rows):
            for col in range(self.cols):
                cellRect = self.getCellRect(row, col)
                num = self.puzzle.getCell(row, col)

                # Hilights the selected cell by mouse
                if self.selectedCell != (row, col):
                    pygame.draw.rect(self.window, self.cellColor, cellRect)

                else:
                    pygame.draw.rect(self.window, self.selectColor, cellRect)

                # Draws the number
                if num != 0:
                    if (row, col) in self.conflicts:
                        color = self.conflictColor
                    else:
                        color = self.fontColor

                    textSurface = self.font.render(str(num), True, color)
                    textRect = textSurface.get_rect()
                    textX = self.getCellRect(row, col).centerx - textRect.centerx
                    textY = self.getCellRect(row, col).centery - textRect.centery

                    self.window.blit(textSurface, (textX, textY))

    def updateDisplay(self):
        pygame.display.set_caption(self.title)
        self.window.fill(self.borderColor)
        self.drawCells()

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
            pygame.display.set_caption(f"{self.title} - Solving...")
            pygame.display.update()
            self.puzzle.solve()
            self.selectedCell = (None, None)
            self.updateDisplay()

        elif key == pygame.K_c:
            self.puzzle.clearPuzzle()
            self.conflicts = []
            self.updateDisplay()


    def mainloop(self):
        while True:
            self.clock.tick(self.clockSpeed)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                elif (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and pygame.mouse.get_pressed()[0] # if left click
                ):  
                    self.mousePress(pygame.mouse.get_pos())
                    

                elif event.type == pygame.KEYDOWN:
                    self.keyPress(event.key)


pygame.init()
window = GUI()
