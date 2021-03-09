# import pygame module in this program
# Zikora was here
import pygame

# activate the pygame library .
# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()

# create the display surface object
# of specific dimension..e(500, 500).
winDim = 500
carDim = 15
laneDim= 30
lineThickness = 5
laneLength = (winDim - laneDim) / 2

# Initializing colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

win = pygame.display.set_mode((winDim, winDim))

# set the pygame window name
pygame.display.set_caption("Crossroads")

# drawing lane lines

# object current co-ordinates
x = 200
y = 200

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
    pygame.draw.rect(win, RED , (x, y, carDim, carDim))
    pygame.draw.line(win, WHITE, (laneLength, 0), (laneLength, laneLength),lineThickness)
    pygame.draw.line(win, WHITE, (laneLength+laneDim, 0), (laneLength+laneDim, laneLength),lineThickness)
    pygame.draw.line(win, WHITE, (0, laneLength), (laneLength, laneLength),lineThickness)
    pygame.draw.line(win, WHITE, (0, laneLength+laneDim), (laneLength, laneLength+laneDim),lineThickness)
    pygame.draw.line(win, WHITE, (laneLength, winDim), (laneLength, laneLength+laneDim),lineThickness)
    pygame.draw.line(win, WHITE, (laneLength+laneDim, winDim), (laneLength+laneDim, laneLength+laneDim),lineThickness)
    pygame.draw.line(win, WHITE, (winDim, laneLength), (laneLength+laneDim, laneLength),lineThickness)
    pygame.draw.line(win, WHITE, (winDim, laneLength+laneDim), (laneLength+laneDim, laneLength+laneDim),lineThickness)





# it refreshes the window
    pygame.display.update()

# closes the pygame window
pygame.quit()


#This is Israa