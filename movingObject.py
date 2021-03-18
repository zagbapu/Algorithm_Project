# import pygame module in this program
# Zikora was here
import pygame

# --- constants ---
pygame.init()

# --- constants ---
winDim = 500
carDim = 14
laneDim= 30
lineThickness = 5
laneLength = (winDim - laneDim) / 2

# --- colors ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

game_font = pygame.font.SysFont("bahnschrift", 15)

class Car:

    def __init__(self, x, y):
        # to keep position and size
        self.rect = pygame.Rect(0, 0, carDim, carDim)


    def draw(self,x,y):
        self.rect.center = x, y
        pygame.draw.rect(win, RED, self.rect)


    def update(self, event):
        # if left arrow key is pressed
        if keys[pygame.K_LEFT] and x > 0:
            # decrement in x co-ordinate
            self.x -= vel

            # if left arrow key is pressed
        if keys[pygame.K_RIGHT] and x < winDim - carDim:
            # increment in x co-ordinate
            self.x += vel

            # if left arrow key is pressed
        if keys[pygame.K_UP] and y > 0:
            # decrement in y co-ordinate
            self.y -= vel

            # if left arrow key is pressed
        if keys[pygame.K_DOWN] and y < winDim - carDim:
            # increment in y co-ordinate
            y += vel


def show_xy(): #Display messages
    xdisp = game_font.render("x-pos: " + str(x), True, WHITE)
    win.blit(xdisp, [0, 5])
    ydisp = game_font.render("y-pos: " + str(y), True, WHITE)
    win.blit(ydisp, [0, laneDim])


def draw_lane():
    pygame.draw.line(win, WHITE, (laneLength, 0), (laneLength, laneLength),lineThickness)
    pygame.draw.line(win, WHITE, (laneLength+laneDim, 0), (laneLength+laneDim, laneLength),lineThickness)
    pygame.draw.line(win, WHITE, (0, laneLength), (laneLength, laneLength),lineThickness)
    pygame.draw.line(win, WHITE, (0, laneLength+laneDim), (laneLength, laneLength+laneDim),lineThickness)
    pygame.draw.line(win, WHITE, (laneLength, winDim), (laneLength, laneLength+laneDim),lineThickness)
    pygame.draw.line(win, WHITE, (laneLength+laneDim, winDim), (laneLength+laneDim, laneLength+laneDim),lineThickness)
    pygame.draw.line(win, WHITE, (winDim, laneLength), (laneLength+laneDim, laneLength),lineThickness)
    pygame.draw.line(win, WHITE, (winDim, laneLength+laneDim), (laneLength+laneDim, laneLength+laneDim),lineThickness)


def draw_car():
    pygame.draw.rect(win, RED, (x - carDim/2, y - carDim/2, carDim, carDim))


win = pygame.display.set_mode((winDim, winDim))

# set the pygame window name
pygame.display.set_caption("Crossroads")

# drawing lane lines

# object current co-ordinates
x = winDim/2
y = winDim/2

# dimensions of the object
width = 15
height = 15

# velocity / speed of movement
vel = 5

# Indicates pygame is running
run = True

# infinite loop
while run:
    # creates time delay of 10ms
    pygame.time.delay(10)

    # iterate over the list of Event objects
    # that was returned by pygame.event.get() method.
    for event in pygame.event.get():

        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
        if event.type == pygame.QUIT:
            # it will make exit the while loop
            run = False
    # stores keys pressed
    keys = pygame.key.get_pressed()

    # if left arrow key is pressed
    if keys[pygame.K_LEFT] and x > 0:
        # decrement in x co-ordinate
        x -= vel

        # if left arrow key is pressed
    if keys[pygame.K_RIGHT] and x < winDim - carDim:
        # increment in x co-ordinate
        x += vel

        # if left arrow key is pressed
    if keys[pygame.K_UP] and y > 0:
        # decrement in y co-ordinate
        y -= vel

        # if left arrow key is pressed
    if keys[pygame.K_DOWN] and y < winDim - carDim:
        # increment in y co-ordinate
        y += vel

        # completely fill the surface object
    # with black colour
    win.fill(BLACK)

    # drawing object on screen which is rectangle here

    show_xy()
    draw_lane()
    draw_car()

# it refreshes the window
    pygame.display.update()

# closes the pygame window
pygame.quit()
