import pygame
import time
import objects

########################################## CONSTANTS ##################################################
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WIDTH = 20
HEIGHT = 20
MARGIN = 3
#######################################################################################################

NUM_CELL_HORZ = int(input("Input the number of Horizontal cells on the grid\n"))
NUM_CELL_VERT = int(input("Input the number of Vertical cells on the grid\n"))

grid = []
queue = [""]

pygame.init()

window_size = [NUM_CELL_HORZ * WIDTH + (NUM_CELL_HORZ + 1) * MARGIN, NUM_CELL_VERT * WIDTH + (NUM_CELL_VERT + 1) * MARGIN]
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Array Backed Grid")

clock = pygame.time.Clock()

def main():
    done = False
    initGrid()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if validGrid():
                        beginPath()
                        time.sleep(10)
                        done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                if grid[row][column].value != 3:
                    grid[row][column].value += 1
                elif grid[row][column].value == 3:
                    grid[row][column].value = 0
    
        screen.fill(BLACK)
        drawGrid()
    
        clock.tick(60)
        pygame.display.flip()

def initGrid():
    for row in range(NUM_CELL_VERT):
        grid.append([])
        for column in range(NUM_CELL_HORZ):
            grid[row].append(objects.cell(WHITE, "white"))

def drawGrid():
    for row in range(NUM_CELL_VERT):
        for column in range(NUM_CELL_HORZ):
            if grid[row][column].value == 1:
                grid[row][column].color_value = BLACK
                grid[row][column].color_name = "black"
            elif grid[row][column].value == 2:
                grid[row][column].color_value = GREEN
                grid[row][column].color_name = "green"
            elif grid[row][column].value == 3:
                grid[row][column].color_value = RED
                grid[row][column].color_name = "red"
            elif grid[row][column].value == 0:
                grid[row][column].color_value = WHITE
                grid[row][column].color_name = "white"

            pygame.draw.rect(screen, grid[row][column].color_value, ((MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT))

def validGrid():
    redCount = 0
    greenCount = 0
    for row in range(NUM_CELL_VERT):
        for column in range(NUM_CELL_HORZ):
            if grid[row][column].color_name == "red":
                redCount += 1
            elif grid[row][column].color_name == "green":
                greenCount += 1
            
    if redCount != 1 or greenCount != 1:
        return False

    return True

def beginPath():
    directions = ""
    while not endReached(directions):
        directions = dequeue()
        for k in ["L", "R", "D", "U"]:
            path = directions + k
            if validMove(path):
                enqueue(path)

def dequeue():
    if len(queue) > 0:
        output = queue[0]
        for i in range(len(queue)-1):
            queue[i] = queue[i+1]

        queue.pop(len(queue)-1)
        return output
    else:
        return ""

def enqueue(input):
    queue.append(input)

def endReached(directions):
    x = 0
    y = 0
    for row in range(NUM_CELL_VERT):
        for column in range(NUM_CELL_HORZ):
            if grid[row][column].color_name == "green":
                x = row
                y = column
    
    for dir in directions:
        if dir == "L":
            x -= 1
        elif dir == "R":
            x += 1
        elif dir == "D":
            y -= 1
        elif dir == "U":
            y += 1
        
    if grid[x][y].color_name == "red":
        print("Path found")
        printPath(directions)
        return True
    
    return False

def validMove(directions):
    x = 0
    y = 0
    for row in range(NUM_CELL_VERT):
        for column in range(NUM_CELL_HORZ):
            if grid[row][column].color_name == "green":
                x = row
                y = column
    
    for dir in directions:
        if dir == "L":
            x -= 1
        elif dir == "R":
            x += 1
        elif dir == "D":
            y -= 1
        elif dir == "U":
            y += 1
        
    if x < 0 or x >= NUM_CELL_VERT or y < 0 or y >= NUM_CELL_HORZ :
        return False
    elif grid[x][y].color_name == "black":
        return False
    
    return True


def printPath(directions):
    x = 0
    y = 0
    for row in range(NUM_CELL_VERT):
        for column in range(NUM_CELL_HORZ):
            if grid[row][column].color_name == "green":
                x = row
                y = column
    
    for dir in directions:
        if dir == "L":
            x -= 1
            grid[x][y].color_value = BLUE
            grid[x][y].color_name = "blue"
            pygame.draw.rect(screen, grid[x][y].color_value, ((MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT))
        elif dir == "R":
            x += 1
            grid[x][y].color_value = BLUE
            grid[x][y].color_name = "blue"
            pygame.draw.rect(screen, grid[x][y].color_value, ((MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT))
        elif dir == "D":
            y -= 1
            grid[x][y].color_value = BLUE
            grid[x][y].color_name = "blue"
            pygame.draw.rect(screen, grid[x][y].color_value, ((MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT))
        elif dir == "U":
            y += 1
            grid[x][y].color_value = BLUE
            grid[x][y].color_name = "blue"
            pygame.draw.rect(screen, grid[x][y].color_value, ((MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT))
        
        clock.tick(60)
        pygame.display.flip()

main()
# pygame.quit()