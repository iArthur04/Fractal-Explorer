# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLOR_PALETTE = [(i % 256, (i * 3) % 256, (i * 7) % 256) for i in range(256)]

# Screen
WIDTH, HEIGHT = 800, 600
ZOOM_FACTOR = 0.5
PAN_SPEED = 0.1

# Add this at the bottom
def generate_color_palette(offset=0):
    return [( (i + offset) % 256, (i * 3 + offset) % 256, (i * 7 + offset) % 256 ) for i in range(256)]