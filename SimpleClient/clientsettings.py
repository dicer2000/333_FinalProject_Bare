import os

# Show Options
CLIENT_SHOW_VIEW = True
TRANSMIT = True
SHOW_CHARS = True
SHOW_STATS = True

# Window settings
RES = WIDTH, HEIGHT = 800, 800
FPS = 30
BUFFER_SIZE = WIDTH * HEIGHT + 6
PIXEL_WIDTH = 20
PIXEL_HEIGHT = 20
SCREEN_WIDTH = WIDTH // PIXEL_WIDTH
SCREEN_HEIGHT = HEIGHT // PIXEL_HEIGHT
SCREEN_SIZE = SCREEN_WIDTH * SCREEN_HEIGHT

# Client Settings
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
THETA_SPACING = 10
PHI_SPACING = 3
CHARS = ".,-~;>=!*#$@"

R1 = 10
R2 = 20
K2 = 200
K1 = SCREEN_HEIGHT * K2 * 3 / (8 * (R1 + R2))
os.environ['SDL_VIDEO_CENTERED'] = '1'


# Comms Settings
SERVER_ADDRESS = "localhost"
SERVER_PORT = 64000