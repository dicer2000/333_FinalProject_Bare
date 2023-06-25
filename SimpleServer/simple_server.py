#  /\_/\  Simple Server
# ( o o ) Programming Project
#  =( )=  Fall 2023
#   ~*~   (Cat by ChatGPT)

import pygame as pg
import sys
import socket
import atexit
from threading import Event, Thread, Lock
import copy
from common import SafeFrame, SafeExiting
from serversettings import *
import colorsys
import select

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
        self.new_game()

    def new_game(self):
        pass

    def update(self):
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'Simple Server - {self.clock.get_fps():.1f}')

    def draw(self):
        # Draw to the main Screen
        self.screen.fill('black')

        strData = current_frame.get()
        # Display it all if we have good data
        if strData is not None and len(strData) == (HEIGHT/PIXEL_HEIGHT) * (WIDTH/PIXEL_WIDTH):

            vert_chars = int(HEIGHT/PIXEL_HEIGHT)
            horz_chars = int(WIDTH/PIXEL_WIDTH)
            for i in range(vert_chars):
                for j in range(horz_chars):
                    self.text_display(strData[i*vert_chars+j], j*PIXEL_WIDTH, i*PIXEL_HEIGHT)

        # Drawn screen to forefront
        pg.display.update()

    def check_events(self):
        # Check for keyboard events
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                exiting.set(True)

    def run(self):
        # Called once to manage whole game
        while not exiting.get():
            self.check_events()
            self.update()
            self.draw()
        pg.quit()

    def text_display(self, char, x, y):
        text = self.font.render(str(char), True, WHITE)
        #self.hsv2rgb(self.hue, 1, 1))
        text_rect = text.get_rect(center=(x, y))
        self.screen.blit(text, text_rect)


def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()


