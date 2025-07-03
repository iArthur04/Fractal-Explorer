import pygame
import numpy as np
from constants import *
from fractals import *

def render_fractal(screen, x_min, x_max, y_min, y_max, max_iter, fractal_type, color_palette):
    """Render the fractal to the screen using optimized numpy array operations."""
    x = np.linspace(x_min, x_max, WIDTH)
    y = np.linspace(y_min, y_max, HEIGHT)
    X, Y = np.meshgrid(x, y)
    C = X + Y * 1j

    if fractal_type == "mandelbrot":
        iter_vals = np.vectorize(mandelbrot)(C, max_iter)
    else:
        iter_vals = np.vectorize(lambda z: julia(z, max_iter))(C)

    # Clip values to palette range and create RGB array
    iter_vals = np.clip(iter_vals, 0, len(color_palette) - 1)
    rgb_array = np.array([color_palette[val] for val in iter_vals.flatten()]).reshape(HEIGHT, WIDTH, 3)
    
    # Transpose to match pygame's expected format (WIDTH, HEIGHT, 3)
    rgb_array = rgb_array.transpose(1, 0, 2)
    
    # Blit the array to screen
    pygame.surfarray.blit_array(screen, rgb_array)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fractal Explorer")
    clock = pygame.time.Clock()

    # Parameters
    x_min, x_max = -2.5, 1.5
    y_min, y_max = -2.0, 2.0
    max_iter = 100
    fractal_type = "mandelbrot"
    color_offset = 0

    running = True
    while running:
        # Color cycling - generate new palette each frame
        color_offset = (color_offset + 1) % 256
        current_palette = generate_color_palette(color_offset)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    fractal_type = "mandelbrot"
                elif event.key == pygame.K_j:
                    fractal_type = "julia"
                elif event.key == pygame.K_s:
                    pygame.image.save(screen, f"fractal_{fractal_type}.png")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if event.button == 1:  # Left click
                    if fractal_type == "julia":
                        cx = x_min + (mouse_x / WIDTH) * (x_max - x_min)
                        cy = y_min + (mouse_y / HEIGHT) * (y_max - y_min)
                        set_julia_c(complex(cx, cy))
                    else:  # Zoom for Mandelbrot
                        x_center = x_min + (mouse_x / WIDTH) * (x_max - x_min)
                        y_center = y_min + (mouse_y / HEIGHT) * (y_max - y_min)
                        x_min, x_max = x_center - (x_max - x_min) * ZOOM_FACTOR, x_center + (x_max - x_min) * ZOOM_FACTOR
                        y_min, y_max = y_center - (y_max - y_min) * ZOOM_FACTOR, y_center + (y_max - y_min) * ZOOM_FACTOR
                elif event.button == 3:  # Right click (zoom out)
                    x_min, x_max = x_min * (1 + ZOOM_FACTOR), x_max * (1 + ZOOM_FACTOR)
                    y_min, y_max = y_min * (1 + ZOOM_FACTOR), y_max * (1 + ZOOM_FACTOR)

        # Pan with arrow keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            x_min -= PAN_SPEED * (x_max - x_min)
            x_max -= PAN_SPEED * (x_max - x_min)
        elif keys[pygame.K_RIGHT]:
            x_min += PAN_SPEED * (x_max - x_min)
            x_max += PAN_SPEED * (x_max - x_min)
        elif keys[pygame.K_UP]:
            y_min -= PAN_SPEED * (y_max - y_min)
            y_max -= PAN_SPEED * (y_max - y_min)
        elif keys[pygame.K_DOWN]:
            y_min += PAN_SPEED * (y_max - y_min)
            y_max += PAN_SPEED * (y_max - y_min)

        render_fractal(screen, x_min, x_max, y_min, y_max, max_iter, fractal_type, current_palette)
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()