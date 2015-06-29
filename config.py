
def scale_calc(X, this, X1):  # useful function used in calculating initial values. Use it when done to convert constants
    return X1 * this / X

# constants.............................................................
FPS = 200
WIDTH, HEIGHT = 1000, 500
TOP, BOTTOM, LEFT, RIGHT = 2, HEIGHT, 0, WIDTH - 2
LINESH, LINESV = 50, 25
BOUNDARY = [(0, 0), (WIDTH - 2, 0), (WIDTH - 2, HEIGHT - 2), (0, HEIGHT - 2)]



BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
DARKGRAY = (30, 30, 30)
BRIGHTGRAY = (140, 140, 140)
# game variables............................................................

# constants for paddlespeed and initial ball speed
PADDLESPEED, BALLSPEED = 14/2, (12/2, 0)
XDAMPING, YDAMPING = 1.005, .3
WALLDAMPING=0.1
WINREQ = 5  # score at which game finishes
