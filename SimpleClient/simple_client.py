#  /\_/\  Simple Client
# ( o o ) Programming Project
#  =( )=  Fall 2023
#   ~*~   (Cat by ChatGPT)

from math import cos, sin
import colorsys
import pygame as pg
import sys
import socket
import atexit
from threading import Event, Thread, Lock
import time
import copy
from common import SafeFrame, SafeExiting
from clientsettings import *

# Objects for Multi-thread use
current_frame = SafeFrame()
exiting = SafeExiting(False)

# Main game object
class Game:
    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.font = pg.font.SysFont('Arial', 20, bold=True)
        self.A_VAL, self.B_VAL = 0, 0
        self.hue = 0
        pg.display.set_caption(f'Simple Client')
        self.new_game()

    def new_game(self):
        # Start the listener
        if TRANSMIT:
            pass

    def update(self):
        global current_frame # global video image
        self.delta_time = self.clock.tick(FPS)

        # Calculate the donut and fill the output buffer
        self.output = [' '] * SCREEN_SIZE
        self.zbuffer = [0] * SCREEN_SIZE
        for theta in range(0, 628, THETA_SPACING):  # theta goes around the cross-sectional circle of a torus, from 0 to 2pi
            for phi in range(0, 628, PHI_SPACING):  # phi goes around the center of revolution of a torus, from 0 to 2pi

                cosA = cos(self.A_VAL)
                sinA = sin(self.A_VAL)
                cosB = cos(self.B_VAL)
                sinB = sin(self.B_VAL)

                costheta = cos(theta)
                sintheta = sin(theta)
                cosphi = cos(phi)
                sinphi = sin(phi)

                # x, y coordinates before revolving
                circlex = R2 + R1 * costheta
                circley = R1 * sintheta

                # 3D (x, y, z) coordinates after rotation
                x = circlex * (cosB * cosphi + sinA * sinB * sinphi) - circley * cosA * sinB
                y = circlex * (sinB * cosphi - sinA * cosB * sinphi) + circley * cosA * cosB
                z = K2 + cosA * circlex * sinphi + circley * sinA
                ooz = 1 / z  # one over z

                # x, y projection
                xp = int(SCREEN_WIDTH / 2 + K1 * ooz * x)
                yp = int(SCREEN_HEIGHT / 2 - K1 * ooz * y)

                position = xp + SCREEN_WIDTH * yp

                # luminance (L ranges from -sqrt(2) to sqrt(2))
                L = cosphi * costheta * sinB - cosA * costheta * sinphi - sinA * sintheta + cosB * (
                            cosA * sintheta - costheta * sinA * sinphi)

                if ooz > self.zbuffer[position]:
                    self.zbuffer[position] = ooz  # larger ooz means the pixel is closer to the viewer than what's already plotted
                    luminance_index = int(L * 8)  # we multiply by 8 to get luminance_index range 0..11 (8 * sqrt(2) = 11)
                    self.output[position] = CHARS[luminance_index if luminance_index > 0 else 0]
        self.A_VAL += 0.15
        self.B_VAL += 0.035
        self.hue += 0.005

        if TRANSMIT:
            current_frame.set(self.output)

    def draw(self):
        # Draw to the main Screen
        self.screen.fill('black')

        # Draw to the show on main screen
        if CLIENT_SHOW_VIEW:
            k = 0
            y_pixel = 0        
            for i in range(SCREEN_HEIGHT):
                y_pixel += PIXEL_HEIGHT
                x_pixel = 0
                for j in range(SCREEN_WIDTH):
                    x_pixel += PIXEL_WIDTH

                    if self.output[k] != ' ':
                        v = self.hsv2rgb(ord(self.output[k])/71, 1, 1)
                        if SHOW_CHARS:
                            self.text_display(self.output[k], x_pixel, y_pixel)
                        else:
                            pg.draw.rect(self.screen, v, (x_pixel, y_pixel,PIXEL_WIDTH, PIXEL_HEIGHT))

                    k += 1
        # Draw Stats
        if SHOW_STATS:           
            text = self.font.render(f'FPS: {self.clock.get_fps():.1f}', True, WHITE)
            text_rect = text.get_rect()
            text_rect.top += 5
            text_rect.left += 5
            self.screen.blit(text, text_rect)
            
        # Drawn screen to forefront
        pg.display.update()

    def check_events(self):
        global exiting # global exit program signal
        # Check for keyboard events
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                exiting.set(True)

    def run(self):
        global exiting # global exit program signal
        # Called once to manage whole game
        while not exiting.get():
            self.check_events()
            self.update()
            self.draw()
        # Shut down correctly
        pg.quit()

    ##### Communications #####

    def hsv2rgb(self, h, s, v):
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))

    def text_display(self, char, x, y):
        text = self.font.render(str(char), True, self.hsv2rgb(self.hue, 1, 1))
        text_rect = text.get_rect(center=(x, y))
        self.screen.blit(text, text_rect)


def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()


