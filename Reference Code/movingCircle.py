import pygame

# --- constants ---

#grid
W = 25
H = 25
M = 2

SIZE = (550, 700)

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)

FPS = 25
# --- classes ---

class Player:

    def __init__(self):
        # to keep position and size
        self.rect = pygame.Rect(0, 0, 20, 20)

        # set start position
        self.rect.center = x, y

    def draw(self):
        pygame.draw.circle(screen, RED, self.rect.center, self.r)

    def update(self, event):
        # create copy of position
        newrect = self.rect.copy()

        # move "copy" to new position
        if event.key == pygame.K_LEFT:
            newrect.x -= 27
        elif event.key == pygame.K_RIGHT:
            newrect.x += 27
        elif event.key == pygame.K_UP:
            newrect.y -= 27
        elif event.key == pygame.K_DOWN:
            newrect.y += 27

        # check if "copy" is still in rectangles
        for rectangle in all_rectangles:
            if newrect.colliderect(rectangle):
                # now you can set new position
                self.rect = newrect
                # don't check other rectangles
                break

# --- main ---

# - init -

pygame.init()

screen = pygame.display.set_mode(SIZE)
screen_rect = screen.get_rect()

# - objects -

player1 = Player()

# create list with rectangles (but not draw them)

map = [
    "########  #######",
    "#      ####     #",
    "#      #  #     #",
    "#    ########   #",
    "######      #   #",
    "   #        #####",
    "   #          #  ",
    "   ############  ",
]

all_rectangles = []

for r, row in enumerate(map):
    for c, item in enumerate(row):
        if item == '#':
            all_rectangles.append(pygame.Rect((W + M) * c + M, ((H + M) * r + M), W, H))

# - mainloop -

clock = pygame.time.Clock()
done = False

while not done:

    # - events (without draws) -
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.KEYDOWN:
            player1.update(event)


    # - draw everything in one place -

    screen.fill(WHITE)

    for rectangle in all_rectangles:
        pygame.draw.rect(screen, BLACK, rectangle, 1)

    player1.draw()

    pygame.display.flip()

    # - FPS - keep the same speed on all computers -

    clock.tick(FPS)

# - end -
pygame.quit()